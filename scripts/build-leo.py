#!/usr/bin/env python3
"""Build Leo from the preserved core and small, editable Studio modules. No network."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess, tempfile
ROOT = Path(__file__).resolve().parents[1]
BASE_BLOB = 'e110a42b44dec2fb2ff46754efb2803154484856'
def blob_sha(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def build(dev_base=False):
    base = (ROOT/'leo-src/base.html').read_bytes()
    if not dev_base and blob_sha(base) != BASE_BLOB:
        raise SystemExit('Base changed. Review the new core and update BASE_BLOB intentionally.')
    html = base.decode('utf-8')
    css = (ROOT/'leo-src/theme.css').read_text(encoding='utf-8')
    js = (ROOT/'leo-src/studio.js').read_text(encoding='utf-8')
    if '</script' in js.lower() or '</style' in css.lower():
        raise SystemExit('Unsafe embedded closing tag in a module.')
    marker = '\ninit().catch('
    if html.count(marker)!=1 or html.count('</style>')!=1:
        raise SystemExit('Unexpected core structure; no output written.')
    # Preserve parent relationships when the existing backup importer allocates new IDs.
    old='for(const f of ns.folders)f.id=remap(f.id);'
    new='for(const f of ns.folders){f.id=remap(f.id);if(f.parentId)f.parentId=remap(f.parentId);}'
    if html.count(old)!=1:
        raise SystemExit('Backup migration anchor changed. Review before building.')
    html=html.replace(old,new,1).replace("['notebookId','pageId','folderId','assetId']","['notebookId','pageId','folderId','assetId','parentId']",1)
    # Focus synchronously: a delayed callback can steal focus from an already edited field.
    old_focus="requestAnimationFrame(()=>{const el=$('input:not([type=hidden]),textarea,button',$('#modalRoot'));el?.focus()})"
    new_focus="const autofocusEl=$('input:not([type=hidden]),textarea,button',$('#modalRoot'));autofocusEl?.focus({preventScroll:true})"
    if html.count(old_focus)!=1:
        raise SystemExit('Modal focus anchor changed. Review before building.')
    html=html.replace(old_focus,new_focus,1)
    html=html.replace("setTimeout(()=>$('#modalForm input:not([type=hidden]),#modalForm textarea')?.focus(),50)","$('#modalForm input:not([type=hidden]),#modalForm textarea')?.focus({preventScroll:true})",1)

    html=html.replace('</style>', '\n'+css+'\n</style>',1)
    html=html.replace(marker,'\n'+js+marker,1)
    html=html.replace('</head>','<link rel="icon" href="./leo-icon.svg" type="image/svg+xml"></head>',1)
    data=html.encode('utf-8')
    # Parse every embedded script before replacing any output file.
    for script in re.findall(r'<script[^>]*>(.*?)</script>',html,re.S):
        with tempfile.NamedTemporaryFile(suffix='.js',mode='w',encoding='utf-8') as file:
            file.write(script);file.flush()
            subprocess.run(['node','--check',file.name],check=True)
    (ROOT/'index.html').write_bytes(data)
    digest=hashlib.sha256(data).hexdigest()
    sw=(ROOT/'leo-src/service-worker.js').read_text(encoding='utf-8').replace('__BUILD__',digest[:16])
    (ROOT/'sw.js').write_text(sw,encoding='utf-8')
    print(json.dumps({'file':'index.html','bytes':len(data),'sha256':digest,'git_blob':blob_sha(data),'core_blob':blob_sha(base)},indent=2))
    return data
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--dev-base',action='store_true')
    build(parser.parse_args().dev_base)
