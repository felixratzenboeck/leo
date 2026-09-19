"""Local-match regression checks. This script does not certify real P2P connectivity."""
from pathlib import Path
import os
import shutil
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
with sync_playwright() as w:
    executable = os.environ.get('CHROMIUM_PATH') or shutil.which('chromium') or shutil.which('google-chrome')
    options = {'headless': True, 'args': ['--autoplay-policy=no-user-gesture-required']}
    if executable:
        options['executable_path'] = executable
    if hasattr(os, 'geteuid') and os.geteuid() == 0:
        options['args'].append('--no-sandbox')
    browser = w.chromium.launch(**options)
    page = browser.new_page(viewport={'width': 1440, 'height': 1000})
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.set_content((ROOT / 'ECHO-RIFT.html').read_text(encoding='utf-8'))
    page.wait_for_timeout(500)
    page.click('#playBtn')
    page.wait_for_timeout(3000)
    assert page.evaluate('EchoApp.mode') == 'bot'
    before = page.evaluate('EchoApp.state.players[0].y')
    page.keyboard.down('s')
    page.wait_for_timeout(350)
    page.keyboard.up('s')
    assert page.evaluate('EchoApp.state.players[0].y') > before + 20
    page.keyboard.press('q')
    page.wait_for_timeout(80)
    assert page.evaluate('EchoApp.state.players[0].echoCd') > 0
    page.keyboard.press('ShiftLeft')
    page.wait_for_timeout(40)
    assert page.evaluate('EchoApp.state.players[0].dashCd') > 0
    page.keyboard.press('Escape')
    page.wait_for_timeout(100)
    assert page.evaluate('EchoApp.paused')
    before = page.evaluate('EchoApp.state.t')
    page.wait_for_timeout(150)
    assert page.evaluate('EchoApp.state.t') == before
    page.click('#resumeBtn')
    page.wait_for_timeout(100)
    assert not page.evaluate('EchoApp.paused')
    page.evaluate('''let g=EchoApp.game;g.players[0].score=g.target-1;
        g.players[1].respawn=0;g.players[1].hp=100;g.players[1].inv=0;
        g.damage(g.players[1],100,0);''')
    page.wait_for_timeout(100)
    assert page.locator('#rematchBtn').is_visible()
    page.click('#rematchBtn')
    page.wait_for_timeout(50)
    assert not page.evaluate('EchoApp.state.done')
    page.keyboard.press('Escape')
    page.click('#quitBtn')
    page.click('[data-mode="local"]')
    page.click('#playBtn')
    page.wait_for_timeout(2700)
    before = page.evaluate('EchoApp.state.players.map(p=>p.y)')
    page.keyboard.down('s')
    page.keyboard.down('ArrowUp')
    page.wait_for_timeout(250)
    page.keyboard.up('s')
    page.keyboard.up('ArrowUp')
    after = page.evaluate('EchoApp.state.players.map(p=>p.y)')
    assert after[0] > before[0] and after[1] < before[1]
    assert not errors, errors
    print('PASS: movement, echo, dash, pause, victory, rematch and couch inputs')
    browser.close()
