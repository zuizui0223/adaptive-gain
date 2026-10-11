"""Fetch metadata for the public V-HOST example media on Figshare."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.request import Request, urlopen

ARTICLE_ID = 25961890
URL = f"https://api.figshare.com/v2/articles/{ARTICLE_ID}"


def main() -> None:
    req = Request(URL, headers={"User-Agent": "adaptive-gain-public-data-audit/1.0"})
    with urlopen(req, timeout=60) as response:
        payload = json.load(response)

    out = {
        "article_id": payload.get("id"),
        "title": payload.get("title"),
        "doi": payload.get("doi"),
        "url_private_api": URL,
        "url_public_api": payload.get("url_public_api"),
        "url_public_html": payload.get("url_public_html"),
        "license": payload.get("license"),
        "files": [
            {
                "id": f.get("id"),
                "name": f.get("name"),
                "size": f.get("size"),
                "download_url": f.get("download_url"),
                "computed_md5": f.get("computed_md5"),
                "mimetype": f.get("mimetype"),
            }
            for f in payload.get("files", [])
        ],
    }
    Path("vhost_example_metadata.json").write_text(
        json.dumps(out, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
