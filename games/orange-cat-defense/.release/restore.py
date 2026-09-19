"""Restore the exact, locally tested standalone HTML. Standard library only."""
from pathlib import Path
import base64
import gzip
import hashlib
import json
import re
import subprocess
import tempfile

root = Path(__file__).resolve().parent
manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
parts = []
for entry in manifest["parts"]:
    name = entry["file"]
    if not re.fullmatch(r"part-\d{2}\.b64", name):
        raise ValueError("Invalid release part filename")
    raw = (root / name).read_bytes()
    if hashlib.sha256(raw).hexdigest() != entry["sha256"]:
        raise ValueError("Checksum mismatch: " + name)
    parts.append(raw.strip())
html = gzip.decompress(base64.b64decode(b"".join(parts), validate=True))
if len(html) != manifest["bytes"]:
    raise ValueError("HTML size mismatch")
sha = hashlib.sha256(html).hexdigest()
if sha != manifest["sha256"]:
    raise ValueError("HTML checksum mismatch")
text = html.decode("utf-8")
if "<!doctype html>" not in text.lower():
    raise ValueError("Expected a complete HTML document")
for code in re.findall(r"<script[^>]*>(.*?)</script>", text, re.S):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".js", encoding="utf-8") as f:
        f.write(code)
        f.flush()
        subprocess.run(["node", "--check", f.name], check=True)
output = root.parent / "index.html"
output.write_bytes(html)
print(f"Verified LEO Orange Cat Defense {manifest['version']}: {len(html)} bytes, SHA256 {sha}")
