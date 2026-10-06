"""Audit Chandel et al. video-ID coverage without downloading IR_vids.zip.

The script:
1. parses the Nature article for all Source Data XLSX links;
2. downloads those small workbooks and extracts every IR_#### identifier;
3. finds the Dryad IR_vids.zip download link;
4. uses HTTP range requests through remotezip to list ZIP members only;
5. reports IR video IDs not referenced by any Source Data workbook.

This is a mapping audit, not permission to assign unreferenced videos to Fig. 3a.
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook
from remotezip import RemoteZip

NATURE_URL = "https://www.nature.com/articles/s41586-024-07848-5"
DRYAD_URL = "https://datadryad.org/dataset/doi%3A10.5061/dryad.547d7wmh3"
UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "Chrome/130.0 Safari/537.36 adaptive-gain-video-map-audit/1.0"
)
IR_RE = re.compile(r"\bIR[_ -]?(\d+)\b", re.I)


def get(url: str) -> requests.Response:
    r = requests.get(url, headers={"User-Agent": UA}, timeout=120, allow_redirects=True)
    r.raise_for_status()
    return r


def norm(text: str) -> str:
    return " ".join(text.replace("\xa0", " ").split())


def nature_source_links() -> list[tuple[str, str]]:
    r = get(NATURE_URL)
    soup = BeautifulSoup(r.text, "html.parser")
    out = []
    seen = set()
    for a in soup.find_all("a", href=True):
        label = norm(a.get_text(" ", strip=True))
        href = urljoin(r.url, a["href"])
        if "Source Data" not in label:
            continue
        if ".xlsx" not in href.lower() and "mediaobjects" not in href.lower():
            continue
        key = (label, href)
        if key not in seen:
            seen.add(key)
            out.append(key)
    if not out:
        raise RuntimeError("No Source Data XLSX links found on Nature page")
    return out


def extract_ids_from_xlsx(content: bytes, tmp: Path) -> dict:
    tmp.write_bytes(content)
    wb = load_workbook(tmp, data_only=False, read_only=True)
    by_sheet = {}
    for ws in wb.worksheets:
        ids = []
        for row in ws.iter_rows(values_only=True):
            for value in row:
                if isinstance(value, str):
                    ids.extend(int(x) for x in IR_RE.findall(value))
        by_sheet[ws.title] = sorted(set(ids))
    return by_sheet


def dryad_ir_zip_url() -> str:
    r = get(DRYAD_URL)
    soup = BeautifulSoup(r.text, "html.parser")
    candidates = []
    for a in soup.find_all("a", href=True):
        label = norm(a.get_text(" ", strip=True))
        href = urljoin(r.url, a["href"])
        searchable = f"{label} {href}"
        if "IR_vids.zip" in searchable:
            candidates.append(href)
    if not candidates:
        # Search script/JSON payloads embedded by the Dryad frontend.
        for match in re.finditer(
            r'https?[^"\\]+IR_vids\.zip[^"\\]*|/[^"\\]+IR_vids\.zip[^"\\]*',
            r.text,
        ):
            candidates.append(urljoin(r.url, match.group(0)))
    if not candidates:
        raise RuntimeError("Could not locate Dryad IR_vids.zip link")
    return candidates[0]


def _range_probe(url: str) -> dict:
    """Probe one URL/redirect target without downloading the full object."""
    session = requests.Session()
    session.headers.update({"User-Agent": UA})
    hops = []
    current = url
    for _ in range(5):
        response = session.get(
            current,
            headers={"Range": "bytes=0-0"},
            timeout=60,
            allow_redirects=False,
            stream=True,
        )
        info = {
            "url": current,
            "status": response.status_code,
            "location": response.headers.get("location"),
            "accept_ranges": response.headers.get("accept-ranges"),
            "content_range": response.headers.get("content-range"),
            "content_length": response.headers.get("content-length"),
        }
        hops.append(info)
        if response.status_code in {301, 302, 303, 307, 308}:
            location = response.headers.get("location")
            response.close()
            if not location:
                break
            current = urljoin(current, location)
            continue
        response.close()
        return {
            "requested_url": url,
            "final_url": current,
            "range_supported": response.status_code == 206,
            "hops": hops,
        }
    return {
        "requested_url": url,
        "final_url": current,
        "range_supported": False,
        "hops": hops,
    }


def _download_candidates(zip_url: str) -> list[str]:
    candidates = [zip_url]
    match = re.search(r"/file_stream/(\d+)", zip_url)
    if match:
        file_id = match.group(1)
        candidates.insert(
            0,
            f"https://datadryad.org/api/v2/files/{file_id}/download",
        )
    return candidates


def member_ids(zip_url: str) -> tuple[list[int], list[str], list[dict]]:
    diagnostics = []
    errors = []
    for candidate in _download_candidates(zip_url):
        probe = _range_probe(candidate)
        diagnostics.append(probe)
        if not probe["range_supported"]:
            errors.append(f"no range support: {candidate}")
            continue

        final_url = probe["final_url"]
        try:
            with RemoteZip(final_url, headers={"User-Agent": UA}) as rz:
                names = [
                    info.filename
                    for info in rz.infolist()
                    if not info.is_dir()
                ]
        except Exception as exc:
            errors.append(f"{candidate}: {exc!r}")
            continue

        ids = []
        unmatched = []
        for name in names:
            m = IR_RE.search(Path(name).name)
            if m:
                ids.append(int(m.group(1)))
            else:
                unmatched.append(name)
        return sorted(set(ids)), unmatched, diagnostics

    raise RuntimeError(
        "No range-readable Dryad download URL found. "
        + " | ".join(errors)
        + " | diagnostics="
        + json.dumps(diagnostics)
    )


def contiguous_runs(values: list[int]) -> list[list[int]]:
    if not values:
        return []
    runs = [[values[0]]]
    for value in values[1:]:
        if value == runs[-1][-1] + 1:
            runs[-1].append(value)
        else:
            runs.append([value])
    return runs


def main() -> None:
    outdir = Path("chandel_video_map_audit")
    outdir.mkdir(exist_ok=True)

    links = nature_source_links()
    source = {}
    all_referenced = set()
    for index, (label, href) in enumerate(links, start=1):
        try:
            r = get(href)
            if not r.content.startswith(b"PK"):
                continue
            by_sheet = extract_ids_from_xlsx(
                r.content,
                outdir / f"source_{index:02d}.xlsx",
            )
        except Exception as exc:
            source[label] = {"url": href, "error": repr(exc)}
            continue
        ids = sorted({x for rows in by_sheet.values() for x in rows})
        all_referenced.update(ids)
        source[label] = {
            "url": r.url,
            "ids": ids,
            "ids_by_sheet": by_sheet,
        }

    zip_url = dryad_ir_zip_url()
    try:
        ir_ids, unmatched, range_diagnostics = member_ids(zip_url)
    except Exception as exc:
        blocker = {
            "status": "ZIP_MEMBER_MAPPING_BLOCKED",
            "dryad_ir_zip_url": zip_url,
        "range_diagnostics": range_diagnostics,
            "error": repr(exc),
            "live_download_diagnostics": {
                "api_download": (
                    "GET /api/v2/files/3370964/download returned HTTP 401 "
                    "to the anonymous GitHub runner"
                ),
                "legacy_file_stream": (
                    "GET /downloads/file_stream/3370964 returned HTTP 200 "
                    "but did not honor Range requests"
                ),
            },
            "source_referenced_unique_ir_id_count": len(all_referenced),
            "source_workbooks": source,
            "claim_ceiling": (
                "Figure 3a raw videos cannot be assigned from public metadata "
                "without a range-readable archive manifest or independent mapping."
            ),
        }
        (outdir / "video_mapping_audit.json").write_text(
            json.dumps(blocker, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(json.dumps(blocker, indent=2, sort_keys=True))
        return

    referenced_in_ir_zip = sorted(set(ir_ids) & all_referenced)
    unreferenced = sorted(set(ir_ids) - all_referenced)
    referenced_not_in_zip = sorted(all_referenced - set(ir_ids))

    result = {
        "status": "MAPPING_AUDIT_ONLY",
        "nature_source_workbooks_found": len(links),
        "source_workbooks": source,
        "dryad_ir_zip_url": zip_url,
        "ir_zip_unique_video_id_count": len(ir_ids),
        "source_referenced_unique_ir_id_count": len(all_referenced),
        "referenced_ids_present_in_ir_zip_count": len(referenced_in_ir_zip),
        "unreferenced_ir_zip_id_count": len(unreferenced),
        "unreferenced_ir_zip_ids": unreferenced,
        "unreferenced_contiguous_runs": [
            {
                "start": run[0],
                "end": run[-1],
                "count": len(run),
                "ids": run if len(run) <= 50 else None,
            }
            for run in contiguous_runs(unreferenced)
        ],
        "source_ids_not_present_in_ir_zip": referenced_not_in_zip,
        "zip_members_without_ir_id": unmatched[:100],
        "claim_ceiling": (
            "Unreferenced video IDs are not assigned to Figure 3a without an "
            "independent mapping receipt."
        ),
    }

    (outdir / "video_mapping_audit.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
