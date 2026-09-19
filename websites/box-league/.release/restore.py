"""Restore the exact, tested BOX LEAGUE HTML. Python standard library only."""
import base64
import hashlib
import json
import lzma
from pathlib import Path

root = Path(__file__).resolve().parent
manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
encoded = []
for part in manifest["parts"]:
    path = root / part["file"]
    if path.parent != root or not path.name.startswith("part-"):
        raise SystemExit("Unexpected release part path")
    data = path.read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    if len(data) != part["bytes"] or blob != part["git_blob"]:
        raise SystemExit("Release part checksum mismatch: " + path.name)
    encoded.append(data.strip())
compressed = base64.b64decode(b"".join(encoded), validate=True)
decoder = lzma.LZMADecompressor(memlimit=256 * 1024 * 1024)
html = decoder.decompress(compressed, max_length=200000)
if not decoder.eof or decoder.unused_data:
    raise SystemExit("Invalid or oversized release archive")
expected = "9ef17b4635bac6c27fdf1ec9cc251caee9ac1f4766dca29cf4f6bd34963a0b91"
if len(html) != 132166 or hashlib.sha256(html).hexdigest() != expected:
    raise SystemExit("HTML checksum mismatch")
if manifest["size"] != len(html) or manifest["sha256"] != expected:
    raise SystemExit("Manifest mismatch")
target = root.parent / "public" / "index.html"
if target.exists() and target.read_bytes() != html:
    raise SystemExit("Existing HTML differs; refusing to overwrite later edits")
target.parent.mkdir(parents=True, exist_ok=True)
target.write_bytes(html)
print(f"Verified BOX LEAGUE 1.1.0: {len(html)} bytes; SHA256 {expected}")
