#!/usr/bin/env python3
"""Meme Sprint 3 entry: copy the pre-rendered meme image to the output dir.

Stdlib only. The grader runs `python3 -P -s /bot/main.py` in a stdlib-only
container with the repo mounted read-only; the only writable locations are
MAKEFUN_OUTPUT_DIR and /tmp, so this program only reads entry.png next to
itself and writes the copy to MAKEFUN_OUTPUT_DIR.
"""

import os
import sys

MAX_BYTES = 1 << 20
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    try:
        with open(src, "rb") as f:
            data = f.read()
    except OSError as exc:
        print(f"cannot read entry.png: {exc}", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print(f"entry.png too large: {len(data)} bytes", file=sys.stderr)
        return 1
    if not data.startswith(PNG_MAGIC):
        print("entry.png is not a PNG", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "entry.png")
        with open(out_path, "wb") as f:
            f.write(data)
        # Read back and verify the written copy is byte-identical to the
        # source, so a truncated or failed write is caught here, not later.
        with open(out_path, "rb") as f:
            written = f.read()
        if written != data:
            print(
                f"output mismatch: wrote {len(written)} bytes, "
                f"expected {len(data)}",
                file=sys.stderr,
            )
            return 1
    except OSError as exc:
        print(f"cannot write output: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {out_path} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
