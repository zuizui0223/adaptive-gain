"""Resolve a published Dryad DOI to a frozen anonymous file manifest.

This script intentionally downloads metadata only. Published file bytes are handled
separately because current Dryad download routes may require a bearer token.
"""

from __future__ import annotations

import argparse
import json
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://datadryad.org/api/v2"


def _get_json(url: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "adaptive-gain-source-audit/1"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def resolve_manifest(doi: str) -> dict:
    encoded = urllib.parse.quote(doi, safe="")
    dataset_url = f"{API}/datasets/{encoded}"
    dataset = _get_json(dataset_url)

    version_href = dataset["_links"]["stash:version"]["href"]
    version_url = (
        version_href
        if version_href.startswith("http")
        else "https://datadryad.org" + version_href
    )

    files = []
    page = 1
    total = None
    while total is None or len(files) < total:
        page_url = version_url.rstrip("/") + f"/files?per_page=100&page={page}"
        page_data = _get_json(page_url)
        batch = page_data.get("_embedded", {}).get("stash:files", [])
        files.extend(batch)
        total = int(page_data.get("total", len(files)))
        if not batch and len(files) < total:
            raise RuntimeError("Dryad manifest pagination stopped before total")
        page += 1

    if len(files) != total:
        raise RuntimeError(f"Dryad manifest pagination mismatch: {len(files)} != {total}")

    normalized = []
    for item in files:
        self_href = item.get("_links", {}).get("self", {}).get("href", "")
        file_id = (
            self_href.rstrip("/").rsplit("/", 1)[-1]
            if self_href
            else None
        )
        normalized.append(
            {
                "path": item.get("path"),
                "size": item.get("size"),
                "mimeType": item.get("mimeType"),
                "digestType": item.get("digestType"),
                "digest": item.get("digest"),
                "file_id": file_id,
                "download_url": (
                    None
                    if file_id is None
                    else f"{API}/files/{file_id}/download"
                ),
            }
        )

    return {
        "schema": "adaptive-gain-dryad-anonymous-manifest-v1",
        "doi": doi,
        "dataset_url": dataset_url,
        "version_url": version_url,
        "publicationDate": dataset.get("publicationDate"),
        "versionNumber": dataset.get("versionNumber"),
        "storageSize": dataset.get("storageSize"),
        "file_count": total,
        "files": normalized,
        "bytes_downloaded": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("doi")
    parser.add_argument("output", type=Path)
    parser.add_argument("--target-name")
    parser.add_argument("--target-id-output", type=Path)
    args = parser.parse_args()

    manifest = resolve_manifest(args.doi)
    args.output.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    if args.target_name is not None:
        matches = [
            item for item in manifest["files"]
            if item["path"] == args.target_name
        ]
        if len(matches) != 1:
            raise SystemExit(
                f"expected exactly one Dryad file named {args.target_name!r}; "
                f"found {len(matches)}"
            )
        file_id = matches[0]["file_id"]
        if not file_id:
            raise SystemExit(f"Dryad file {args.target_name!r} has no file id")
        if args.target_id_output is not None:
            args.target_id_output.write_text(
                str(file_id) + "\n",
                encoding="utf-8",
            )
        else:
            print(file_id)


if __name__ == "__main__":
    main()
