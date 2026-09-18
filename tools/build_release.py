#!/usr/bin/env python3
"""Build the standalone setting, DRFX package and checksum manifest."""
from __future__ import annotations

import hashlib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src/Galactic Crawl.setting"
DIST = ROOT / "dist"
SETTING = DIST / "Galactic-Crawl.setting"
PACKAGE = DIST / "Galactic-Crawl.drfx"
MEMBER = "Edit/Titles/Galactic Crawl.setting"
ASSETS = ("Galactic-Crawl.drfx", "Galactic-Crawl.setting", "Galactic-Crawl-quickstart-es.txt")


def main() -> None:
    source = SOURCE.read_bytes()
    SETTING.write_bytes(source)

    info = zipfile.ZipInfo(MEMBER, date_time=(1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    with zipfile.ZipFile(PACKAGE, "w") as archive:
        archive.writestr(info, source)

    checksums = [
        f"{hashlib.sha256((DIST / name).read_bytes()).hexdigest()}  {name}"
        for name in ASSETS
    ]
    (DIST / "SHA256SUMS.txt").write_text("\n".join(checksums) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
