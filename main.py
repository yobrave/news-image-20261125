"""news-image-20261125 build step.

Validates entry.png against the competition gate (PNG format, 1 MiB cap,
1024x1024 cap), then reproduces it byte-for-byte into the directory named by
$MAKEFUN_OUTPUT_DIR and prints a JSON receipt. No re-encoding happens: the
grader receives the exact bytes rendered by the poster pipeline.
"""

import hashlib
import json
import os
import shutil
import struct
import sys
from pathlib import Path

BYTE_CAP = 1024 * 1024
SIDE_CAP = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

REPO_ROOT = Path(__file__).resolve().parent
ENTRY_FILE = REPO_ROOT / "entry.png"


def bail(text):
    print(json.dumps({"verdict": "fail", "why": text}))
    raise SystemExit(1)


def probe(raw):
    """Return IHDR facts for a PNG byte string, or bail out."""
    if raw[:8] != PNG_SIGNATURE:
        bail("file does not open with the PNG signature")
    declared = struct.unpack(">I", raw[8:12])[0]
    if raw[12:16] != b"IHDR" or declared != 13:
        bail("first chunk is not a 13-byte IHDR")
    width, height, depth, colour = struct.unpack(">IIBB", raw[16:26])
    if width > SIDE_CAP or height > SIDE_CAP:
        bail(f"dimensions {width}x{height} exceed the {SIDE_CAP}x{SIDE_CAP} cap")
    interlace = raw[28]
    if interlace > 1:
        bail(f"interlace byte {interlace} is neither 0 nor 1")
    return {"width": width, "height": height, "bit_depth": depth, "colour_type": colour, "interlace": interlace}


def replicate(into):
    """Copy entry.png byte-for-byte into `into`, creating it when missing."""
    into.mkdir(parents=True, exist_ok=True)
    landed = into / "entry.png"
    shutil.copyfile(ENTRY_FILE, landed)
    return landed


def verify(landed, size, digest):
    """Re-read the copy and confirm size and sha256 match the source."""
    echoed = landed.read_bytes()
    if len(echoed) != size:
        bail(f"copy holds {len(echoed)} bytes, source held {size}")
    if hashlib.sha256(echoed).hexdigest() != digest:
        bail("copy digest differs from source digest")


def main():
    if not ENTRY_FILE.is_file():
        bail("entry.png is missing beside main.py")
    raw = ENTRY_FILE.read_bytes()
    if len(raw) > BYTE_CAP:
        bail(f"entry.png weighs {len(raw)} bytes, past the {BYTE_CAP} cap")
    facts = probe(raw)
    digest = hashlib.sha256(raw).hexdigest()
    dest = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or (REPO_ROOT / "out"))
    landed = replicate(dest)
    verify(landed, len(raw), digest)
    receipt = {
        "verdict": "pass",
        "landed": str(landed),
        "bytes": len(raw),
        "sha256": digest,
    }
    receipt.update(facts)
    print(json.dumps(receipt))


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # unexpected trouble still answers in JSON
        print(json.dumps({"verdict": "fail", "why": f"unhandled: {exc}"}))
        sys.exit(1)
