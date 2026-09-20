#!/usr/bin/env python3
"""Leo browser regression tests. All data is synthetic and isolated from user storage."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from datetime import date, timedelta
from playwright.sync_api import sync_playwright
import argparse, gzip, json, os, shutil, traceback
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'test-results';OUT.mkdir(exist_ok=True)
parser=argparse.ArgumentParser();parser.add_argument('--in-memory',action='store_true');args=parser.parse_args()
report={'mode':'DOM with explicit localStorage test adapter' if args.in_memory else 'Chromium, HTTP origin, native IndexedDB and Service Worker','checks':[],'not_tested':['physical Apple Pencil','iPhone/iPad Safari','real microphone hardware','authenticated Moodle/Levis/OpenClaw'],'errors':[]}
def check(title,condition=True):
    assert condition,title
    report['checks'].append(title)
    print('PASS:',title,flush=True)
def write_report():
    (OUT/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
class Handler(SimpleHTTPRequestHandler):
    extensions_map={**SimpleHTTPRequestHandler.extensions_map,'.webmanifest':'application/manifest+json'}
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(ROOT)))
Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/index.html'
MOCK="""Object.defineProperty(window,'localStorage',{value:(()=>{const m=new Map();return {getItem:k=>m.get(k)??null,setItem:(k,v)=>m.set(k,String(v)),removeItem:k=>m.delete(k),key:i=>[...m.keys()][i],get length(){return m.size}}})()})"""
def boot(page):
    if args.in_memory:
        page.evaluate(MOCK);page.set_content((ROOT/'index.html').read_text(encoding='utf-8'))
    else:page.goto(url)
    page.wait_for_function('!!window.LeoStudio',timeout=20000)
    page.wait_for_timeout(100)
def tasks(page):return page.evaluate('LeoStudio.getState().tasks')
def add_task(page,title,status='inbox',course='Anatomie',priority='normal'):
    page.locator('.pagehead [data-leo="new-task"]').click()
    page.locator('#leoTaskTitle').fill(title)
    page.locator('#leoTaskDescription').fill('Synthetische Testdaten — kein persönlicher Studieninhalt.')
    page.locator('#leoTaskStatus').select_option(status)
    page.locator('#leoTaskSubject').fill(course)
    page.locator('#leoTaskPriority').select_option(priority)
    page.locator('#leoTaskDue').fill(str(date.today()+timedelta(days=3)))
    page.locator('#modalForm button[type="submit"]').click()
    page.wait_for_selector('#modalRoot', state='hidden')
    return next(x['id'] for x in tasks(page) if x['title']==title)
def set_width(page,width):
    page.locator('#leoToolWidth').evaluate('(e,v)=>{e.value=String(v);e.dispatchEvent(new Event("input",{bubbles:true}));}',width)
def draw(page,x,y,kind='pen',pointer=7):
    for i,(dx,dy,pressure) in enumerate([(0,0,.2),(22,2,.5),(48,4,.8),(72,2,.6)]):
        page.dispatch_event('#live','pointerdown' if i==0 else 'pointermove',{'pointerId':pointer,'pointerType':kind,'isPrimary':True,'button':0,'buttons':1,'clientX':x+dx,'clientY':y+dy,'pressure':pressure})
    page.dispatch_event('#live','pointerup',{'pointerId':pointer,'pointerType':kind,'button':0,'buttons':0,'clientX':x+72,'clientY':y+2,'pressure':0})
with sync_playwright() as pw:
    launch={'headless':True,'args':['--no-sandbox']}
    if os.environ.get('LEO_CHROME'):launch['executable_path']=os.environ['LEO_CHROME']
    elif args.in_memory:launch['executable_path']='/usr/bin/chromium'
    browser=pw.chromium.launch(**launch)
    context=browser.new_context(viewport={'width':1440,'height':1000},accept_downloads=True)
    page=context.new_page();page.set_default_timeout(7000)
    page.on('pageerror',lambda e:report['errors'].append(str(e)))
    try:
        boot(page)
        check('App boots without uncaught JavaScript errors',not report['errors'])
        initial_book_ids=page.evaluate('LeoStudio.getState().notebooks.map(b=>b.id)')
        check('Fresh workspace contains three notebooks',len(initial_book_ids)==3)
        check('Leo branding is visible','Leo' in page.locator('.brand').inner_text())
        page.screenshot(path=str(OUT/'home-desktop.png'),full_page=True)
        page.locator('#sidebar [data-leo="go-tasks"]').click()
        root=add_task(page,'Skript strukturiert lernen','next',priority='high')
        check('Task creation writes into the existing task store',len(tasks(page))==1)
        page.locator(f'[data-leo="edit-task"][data-id="{root}"]').first.click()
        page.locator('[data-leo="subtask"]').click()
        page.locator('#leoTaskTitle').fill('Lernkarten vorbereiten')
        page.locator('#modalForm button[type="submit"]').click()
        child=next(t for t in tasks(page) if t['title']=='Lernkarten vorbereiten')
        check('Subtask inherits parent and subject',child['parentId']==root and child['course']=='Anatomie')
        page.locator(f'[data-leo="edit-task"][data-id="{root}"]').first.click()
        check('A descendant cannot become its parent',page.locator(f'#leoTaskParent option[value="{child["id"]}"]').count()==0)
        page.locator(f'[data-leo-subcheck="{child["id"]}"]').check()
        page.locator('#modalForm button[type="submit"]').click()
        check('Subtask completion is persisted and aggregated',next(t for t in tasks(page) if t['id']==child['id'])['done'])
        check('Parent card shows correct subtask progress','1/1 Unteraufgaben' in page.locator(f'[data-task-card="{root}"]').inner_text())
        page.locator(f'[data-leo="task-menu"][data-id="{root}"]').click()
        page.locator('[data-leo="set-status"][data-status="doing"]').click()
        check('Touch-compatible status menu moves the task',next(t for t in tasks(page) if t['id']==root)['status']=='doing')
        page.locator('[data-leo="task-undo"]').click()
        check('Task undo restores its previous status',next(t for t in tasks(page) if t['id']==root)['status']=='next')
        page.locator(f'[data-task-card="{root}"]').drag_to(page.locator('[data-status-drop="doing"]'))
        check('Desktop drag and drop moves a card',next(t for t in tasks(page) if t['id']==root)['status']=='doing')
        add_task(page,'Praxisnotizen ordnen','inbox','Praxis & Befund')
        add_task(page,'Physiologie wiederholen','done','Physiologie','low')
        page.locator('#leoTaskSearch').fill('Lernkarten')
        check('Search retains the parent of a matching subtask',page.locator(f'[data-task-card="{root}"]').count()==1)
        page.locator('#leoTaskSearch').fill('nichts-passendes-000')
        check('Search updates results without losing input focus',page.locator('[data-task-card]').count()==0 and page.locator('#leoTaskSearch').evaluate('(e)=>e===document.activeElement'))
        page.locator('#leoTaskSearch').fill('')
        page.locator('[data-leo="task-view"][data-value="list"]').click()
        check('List uses the same task data',page.locator('[data-task-card]').count()==4)
        page.locator('[data-leo="task-view"][data-value="tree"]').click()
        check('Tree renders nested task relationships',page.locator('.leo-task-children [data-task-card]').count()==1)
        page.locator('[data-leo="task-view"][data-value="board"]').click()
        page.screenshot(path=str(OUT/'board-synthetic-data.png'),full_page=True)
        xss=add_task(page,'<img src=x onerror="window.bad=1">','inbox')
        check('Task titles are escaped, not interpreted as HTML',page.locator(f'[data-task-card="{xss}"] img').count()==0 and not page.evaluate('!!window.bad'))
        page.locator('#sidebar [data-act="new-folder"]').click()
        page.locator('#leoFolderName').fill('Neuro — Testfach')
        page.locator('[data-leo="choose-icon"][data-value="🧬"]').click()
        parent=page.evaluate('LeoStudio.getState().folders[0].id')
        page.locator('#leoFolderParent').select_option(parent)
        page.locator('#modalForm button[type="submit"]').click()
        folder=page.evaluate('LeoStudio.getState().folders.find(f=>f.name==="Neuro — Testfach")')
        check('Nested subjects preserve parent and chosen icon',folder['parentId']==parent and folder['icon']=='🧬')
        page.locator('.profile .avatar').click()
        page.locator('#leoProfileName').fill('Testperson')
        page.locator('#modalForm button[type="submit"]').click()
        check('Profile is editable without changing app source','Testperson' in page.locator('.profile').inner_text())
        page.locator('#sidebar [data-act="nav"][data-view="home"]').click()
        page.locator('.pagehead [data-act="quick-note"]').click()
        page.wait_for_selector('#editor:not(.hidden)')
        check('Dedicated Leo assistant button exists in the editor',page.locator('#editorTop [data-act="open-leo"]').count()==1)
        set_width(page,7.5)
        box=page.locator('#paper').bounding_box();x=box['x']+65;y=box['y']+75
        start=page.evaluate('LeoStudio.getState().pages.reduce((s,p)=>s+p.items.length,0)')
        draw(page,x,y)
        all_items=page.evaluate('LeoStudio.getState().pages.flatMap(p=>p.items)')
        check('Stylus stroke stores pressure samples and selected width',len(all_items)==start+1 and all_items[-1]['width']==7.5 and len({p[2] for p in all_items[-1]['points']})>1)
        page.locator('[data-tool="eraser"]').click();set_width(page,70)
        draw(page,x+30,y+2,pointer=8)
        check('Variable-width eraser removes the targeted stroke',page.evaluate('LeoStudio.getState().pages.reduce((s,p)=>s+p.items.length,0)')==start)
        page.locator('#toolbar [data-act="undo"]').click()
        check('Ink undo recovers an erased stroke',page.evaluate('LeoStudio.getState().pages.reduce((s,p)=>s+p.items.length,0)')==start+1)
        page.locator('[data-tool="laser"]').click();draw(page,x+20,y+70,pointer=9)
        check('Laser draws a visible transient trail',page.evaluate('LeoStudio.getStatus().laserPoints')>0)
        check('Laser never enters permanent page data',page.evaluate('LeoStudio.getState().pages.reduce((s,p)=>s+p.items.length,0)')==start+1)
        page.wait_for_timeout(1550)
        check('Laser trail and animation stop after fade-out',page.evaluate('LeoStudio.getStatus().laserPoints')==0)
        page.locator('[data-tool="pen"]').click()
        check('Pen size is restored independently of the eraser',float(page.locator('#leoToolWidth').input_value())==7.5)
        draw(page,x+20,y+110,kind='touch',pointer=10)
        check('Finger input does not draw in pen-only mode',page.evaluate('LeoStudio.getState().pages.reduce((s,p)=>s+p.items.length,0)')==start+1)
        page.screenshot(path=str(OUT/'writing-desktop.png'),full_page=True)
        page.locator('#editorTop [data-act="close-editor"]').click()
        page.evaluate('LeoStudio.flush()')
        check('Existing notebook IDs survive all tested edits',set(initial_book_ids).issubset(set(page.evaluate('LeoStudio.getState().notebooks.map(b=>b.id)'))))
        if not args.in_memory:
            with page.expect_download() as dl:page.evaluate('Folio.backup()')
            backup=OUT/'synthetic-test-backup.folio';dl.value.save_as(backup)
            data=backup.read_bytes();payload=json.loads(gzip.decompress(data) if data[:2]==b'\x1f\x8b' else data)
            check('Full backup includes task and folder hierarchies',any(t.get('parentId')==root for t in payload['state']['tasks']) and any(f.get('parentId')==parent for f in payload['state']['folders']))
            old_tasks=len(tasks(page));old_folders=len(page.evaluate('LeoStudio.getState().folders'))
            page.locator('#fileInput').set_input_files(str(backup))
            page.locator('[data-act="apply-backup-merge"]').click()
            page.wait_for_selector('#modalRoot',state='hidden',timeout=15000)
            new_tasks=tasks(page)[old_tasks:]
            new_root=next(t for t in new_tasks if t['title']=='Skript strukturiert lernen')
            new_child=next(t for t in new_tasks if t['title']=='Lernkarten vorbereiten')
            check('Backup merge remaps task parents, preserving the original',new_root['id']!=root and new_child['parentId']==new_root['id'])
            new_folders=page.evaluate('LeoStudio.getState().folders')[old_folders:]
            check('Backup merge remaps nested subject parents',next(f for f in new_folders if f['name']=='Neuro — Testfach')['parentId']==next(f for f in new_folders if f['name']=='Anatomie')['id'])
            page.evaluate('LeoStudio.flush()');expected=len(tasks(page));page.reload();page.wait_for_function('!!window.LeoStudio')
            check('Native IndexedDB preserves tasks and profile through reload',len(tasks(page))==expected and page.evaluate('LeoStudio.getState().settings.displayName')=='Testperson')
            check('Native IndexedDB is active',page.evaluate('LeoStudio.getStatus().storage')=='indexeddb')
            page.wait_for_function('!!navigator.serviceWorker.controller',timeout=20000)
            context.set_offline(True);page.reload();page.wait_for_function('!!window.LeoStudio',timeout=20000)
            check('Installed app shell starts offline with the saved data',len(tasks(page))==expected)
            context.set_offline(False)
        context.close()
        for label,width,height,touch in [('ipad-layout',1024,768,True),('iphone-layout',390,844,True)]:
            ctx=browser.new_context(viewport={'width':width,'height':height},has_touch=touch,device_scale_factor=1)
            p=ctx.new_page();p.on('pageerror',lambda e:report['errors'].append(str(e)));boot(p)
            check(label+' has no page-level horizontal overflow',p.evaluate('document.documentElement.scrollWidth')<=width)
            p.screenshot(path=str(OUT/(label+'.png')),full_page=True)
            p.evaluate('LeoStudio.navigate("tasks")')
            check(label+' board stays in its own horizontal scroller',p.evaluate('document.documentElement.scrollWidth')<=width)
            ctx.close()
        check('No uncaught JavaScript errors across tested flows',not report['errors'])
        report['status']='passed'
    except Exception as e:
        report['status']='failed';report['failure']=str(e);report['traceback']=traceback.format_exc()
        try:page.screenshot(path=str(OUT/'failure.png'),full_page=True)
        except Exception:pass
        raise
    finally:
        write_report();browser.close();server.shutdown()
