"""Materialize public Figshare article files with checksum receipts.

Used as an independent public-source fallback for the Villavicencio raw
flower-visitor records. The downloader relies only on the documented Figshare
v2 article metadata surface and file download URLs returned by that metadata.

This script does not transform ecological data.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
from pathlib import Path


API = "https://api.figshare.com/v2/articles/{article_id}"
USER_AGENT = "adaptive-gain-public-source-audit/1.0"


def _get_json(url: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def _download(url: str, output: Path) -> tuple[str, str, int]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    md5 = hashlib.md5()
    sha256 = hashlib.sha256()
    size = 0
    output.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(request, timeout=120) as response, output.open("wb") as handle:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            handle.write(chunk)
            md5.update(chunk)
            sha256.update(chunk)
            size += len(chunk)
    return md5.hexdigest(), sha256.hexdigest(), size


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("article_id", type=int)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()

    metadata = _get_json(API.format(article_id=args.article_id))
    args.output_dir.mkdir(parents=True, exist_ok=True)

    files = []
    for item in metadata.get("files", []):
        name = str(item.get("name") or f"figshare_file_{item.get('id')}")
        download_url = item.get("download_url")
        is_link_only = bool(item.get("is_link_only", False))
        receipt = {
            "id": item.get("id"),
            "name": name,
            "declared_size": item.get("size"),
            "declared_md5": item.get("supplied_md5") or item.get("computed_md5"),
            "is_link_only": is_link_only,
            "download_url": download_url,
            "downloaded": False,
        }
        if download_url and not is_link_only:
            path = args.output_dir / name
            md5, sha256, size = _download(str(download_url), path)
            receipt.update(
                {
                    "downloaded": True,
                    "path": str(path),
                    "observed_size": size,
                    "observed_md5": md5,
                    "observed_sha256": sha256,
                    "size_matches": (
                        item.get("size") is None or int(item["size"]) == size
                    ),
                    "md5_matches": (
                        receipt["declared_md5"] is None
                        or str(receipt["declared_md5"]).lower() == md5.lower()
                    ),
                }
            )
            if not receipt["size_matches"]:
                raise SystemExit(f"Figshare size mismatch for {name}")
            if not receipt["md5_matches"]:
                raise SystemExit(f"Figshare MD5 mismatch for {name}")
        files.append(receipt)

    manifest = {
        "schema": "adaptive-gain-figshare-public-article-manifest-v1",
        "article_id": args.article_id,
        "title": metadata.get("title"),
        "doi": metadata.get("doi"),
        "url": metadata.get("url_public_api") or metadata.get("url_private_api"),
        "version": metadata.get("version"),
        "license": metadata.get("license"),
        "file_count": len(files),
        "downloaded_count": sum(bool(item["downloaded"]) for item in files),
        "files": files,
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    if not files:
        raise SystemExit("Figshare article metadata contained no files")
    if manifest["downloaded_count"] == 0:
        raise SystemExit("Figshare article contained no downloadable files")

    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
