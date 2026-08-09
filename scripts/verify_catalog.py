#!/usr/bin/env python3
"""Validate the suite catalog and its pinned source commits."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"


def git_head(path: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(path), "rev-parse", "HEAD"], text=True
    ).strip()


def main() -> None:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    assert data["schema"] == 1
    products = data["products"]
    assert len(products) == 4
    ids: set[str] = set()
    names: set[str] = set()

    for product in products:
        product_id = product["id"]
        assert product_id not in ids
        ids.add(product_id)

        commit = product["commit"]
        assert len(commit) == 40 and all(c in "0123456789abcdef" for c in commit)
        path = ROOT / product["submodule"]
        actual = git_head(path)
        assert actual == commit, f"{product_id}: expected {commit}, got {actual}"

        assert product["repository"].startswith("https://github.com/")
        assert product["release"].startswith(product["repository"] + "/releases/tag/")
        for artifact in product["artifacts"]:
            name = artifact["name"]
            assert name not in names, f"duplicate artifact name: {name}"
            names.add(name)
            digest = artifact["sha256"]
            assert len(digest) == 64 and all(c in "0123456789abcdef" for c in digest)
            assert artifact["size"] > 0
            assert artifact["url"].startswith(product["repository"] + "/releases/download/")

    print(f"Verified {len(products)} products and {len(names)} release artifacts")


if __name__ == "__main__":
    main()
