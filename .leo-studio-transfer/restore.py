#!/usr/bin/env python3
"""Restore the exact reviewed text modules once; never overwrite existing modules."""
from pathlib import Path
import base64, gzip, hashlib, json
root=Path(__file__).resolve().parents[1]
folder=Path(__file__).resolve().parent
manifest=json.loads((folder/'manifest.json').read_text())
if (root/'leo-src/studio.js').exists():
    print('Editable modules already exist; preserving them.')
    raise SystemExit(0)
encoded=''.join((folder/p).read_text().strip() for p in manifest['parts'])
archive=base64.b64decode(encoded,validate=True)
assert hashlib.sha256(archive).hexdigest()==manifest['archive_sha256'],'Transfer checksum mismatch'
raw=gzip.decompress(archive)
assert len(raw)==manifest['uncompressed_bytes'],'Unexpected archive size'
files=json.loads(raw)
assert set(files)==set(manifest['files']),'Unexpected module paths'
for relative,text in files.items():
    target=root/relative
    assert target.resolve().is_relative_to(root.resolve()) and not target.exists(),relative
    assert hashlib.sha256(text.encode()).hexdigest()==manifest['files'][relative],relative
for relative,text in files.items():
    target=root/relative;target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(text.encode('utf-8'))
print('Restored',len(files),'verified source files; no existing files changed.')
