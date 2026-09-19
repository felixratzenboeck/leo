"""Restore only the original BONK game; verify its bytes and JavaScript first.

The six base64 files transport XZ-compressed HTML, not an executable archive.
This script neither downloads dependencies nor accesses credentials.
"""
from pathlib import Path
import base64
import hashlib
import lzma
import re
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
EXPECTED_SIZE = 107634
EXPECTED_SHA256 = '889d1d2bedfe7843e9e77738fafca56c084dad50f457f50f6b1a2cd1fa496bcc'
EXPECTED_BLOB_SHA = '802fa24d2786d7d2cf8f629268d99139f7ad907f'
encoded = ''.join((HERE / f'part-{i:02d}.b64').read_text(encoding='ascii').strip() for i in range(6))
data = lzma.decompress(base64.b64decode(encoded, validate=True), memlimit=256 * 1024 * 1024)
if len(data) != EXPECTED_SIZE or hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
    raise SystemExit('Original HTML checksum or length mismatch; refusing publication.')
blob_hash = hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()
if blob_hash != EXPECTED_BLOB_SHA:
    raise SystemExit('Git blob checksum mismatch; refusing publication.')
html = data.decode('utf-8')
scripts = re.findall(r'<script\b[^>]*>(.*?)</script>', html, flags=re.S | re.I)
if not scripts or '<title>BONK! LEAGUE' not in html:
    raise SystemExit('Expected standalone game not found.')
for script in scripts:
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', encoding='utf-8') as handle:
        handle.write(script)
        handle.flush()
        subprocess.run(['node', '--check', handle.name], check=True)
target = HERE.parent / 'index.html'
if target.exists() and target.read_bytes() != data:
    raise SystemExit('A different game already occupies index.html; refusing to overwrite it.')
target.write_bytes(data)
print(f'PASS: original HTML and JavaScript verified; {len(data)} bytes; SHA256 {EXPECTED_SHA256}')
