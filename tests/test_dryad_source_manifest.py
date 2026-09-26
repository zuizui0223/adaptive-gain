import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "examples" / "fetch_dryad_source_manifest.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("dryad_manifest", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_resolve_manifest_paginates_and_normalizes_file_ids(monkeypatch):
    module = _load_module()
    calls = []

    dataset = {
        "_links": {"stash:version": {"href": "/api/v2/versions/123"}},
        "publicationDate": "2020-03-19",
        "versionNumber": 1,
        "storageSize": 42,
    }
    page1 = {
        "total": 2,
        "_embedded": {
            "stash:files": [
                {
                    "path": "a.RData",
                    "size": 10,
                    "mimeType": "application/octet-stream",
                    "digestType": "sha256",
                    "digest": "aaa",
                    "_links": {"self": {"href": "/api/v2/files/11"}},
                }
            ]
        },
    }
    page2 = {
        "total": 2,
        "_embedded": {
            "stash:files": [
                {
                    "path": "b.xlsx",
                    "size": 32,
                    "mimeType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    "digestType": "sha256",
                    "digest": "bbb",
                    "_links": {"self": {"href": "/api/v2/files/12"}},
                }
            ]
        },
    }

    def fake_get(url):
        calls.append(url)
        if "/datasets/" in url:
            return dataset
        if url.endswith("&page=1"):
            return page1
        if url.endswith("&page=2"):
            return page2
        raise AssertionError(url)

    monkeypatch.setattr(module, "_get_json", fake_get)
    result = module.resolve_manifest("doi:10.5061/dryad.example")

    assert result["file_count"] == 2
    assert [row["file_id"] for row in result["files"]] == ["11", "12"]
    assert result["files"][1]["download_url"].endswith("/files/12/download")
    assert result["bytes_downloaded"] is False
    assert any("doi%3A10.5061%2Fdryad.example" in url for url in calls)


def test_script_source_never_embeds_credentials_or_downloads_bytes():
    text = SCRIPT.read_text(encoding="utf-8")
    lower = text.lower()
    assert "authorization" not in lower
    assert "dryad_token" not in lower
    assert "bytes_downloaded" in text
    assert "False" in text
