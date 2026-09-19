"""Real browser checks served over localhost; networking failures are failures, not skips."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
import json
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'test-results'
OUT.mkdir(exist_ok=True)
server = ThreadingHTTPServer(('127.0.0.1', 0), partial(SimpleHTTPRequestHandler, directory=str(ROOT / 'public')))
Thread(target=server.serve_forever, daemon=True).start()
URL = f'http://127.0.0.1:{server.server_port}/'
checks, errors = [], []

def ok(label):
    checks.append(label)
    print('PASS:', label, flush=True)

def setup(page):
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(URL, wait_until='networkidle')
    page.wait_for_function('!!window.EchoApp')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    try:
        ctx = browser.new_context(viewport={'width': 1440, 'height': 960})
        page = ctx.new_page()
        setup(page)
        page.screenshot(path=str(OUT / 'lobby-desktop.png'), full_page=True)
        page.click('#playBtn')
        page.wait_for_timeout(2900)
        assert page.locator('#hud').is_visible()
        before = page.evaluate('EchoApp.state.players[0].y')
        page.keyboard.down('KeyS')
        page.wait_for_timeout(300)
        page.keyboard.up('KeyS')
        assert page.evaluate('EchoApp.state.players[0].y') > before + 20
        ok('bot start, countdown and keyboard movement')
        page.keyboard.press('KeyQ')
        page.wait_for_timeout(100)
        assert page.evaluate('EchoApp.state.players[0].echoCd') > 0
        page.keyboard.press('ShiftLeft')
        page.wait_for_timeout(100)
        assert page.evaluate('EchoApp.state.players[0].dashCd') > 0
        ok('echo and dash controls')
        page.keyboard.press('Escape')
        page.wait_for_function('EchoApp.paused')
        t = page.evaluate('EchoApp.state.t')
        page.wait_for_timeout(200)
        assert page.evaluate('EchoApp.state.t') == t
        page.click('#resumeBtn')
        page.wait_for_function('!EchoApp.paused')
        ok('pause and resume freeze/restart simulation')
        page.keyboard.press('Escape')
        page.click('#quitBtn')
        page.click('#settingsBtn')
        page.fill('#name0', 'FELIX')
        page.locator('#name0').press('Tab')
        page.select_option('#aimSelect', 'keyboard')
        page.locator('#settingsDialog [data-close]').first.click()
        page.reload(wait_until='networkidle')
        page.click('#settingsBtn')
        assert page.locator('#name0').input_value() == 'FELIX'
        assert page.locator('#aimSelect').input_value() == 'keyboard'
        page.locator('#settingsDialog [data-close]').first.click()
        ok('preferences persist across a real reload')
        page.click('[data-mode="local"]')
        page.click('#playBtn')
        page.wait_for_timeout(2850)
        before = page.evaluate('EchoApp.state.players.map(p=>p.y)')
        page.keyboard.down('KeyS')
        page.keyboard.down('ArrowUp')
        page.wait_for_timeout(300)
        page.keyboard.up('KeyS')
        page.keyboard.up('ArrowUp')
        after = page.evaluate('EchoApp.state.players.map(p=>p.y)')
        assert after[0] > before[0] + 20 and after[1] < before[1] - 20
        ok('simultaneous local multiplayer controls')
        page.screenshot(path=str(OUT / 'game-desktop.png'), full_page=True)
        ctx.close()

        mobile_context = browser.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
        mobile = mobile_context.new_page()
        setup(mobile)
        assert mobile.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')
        mobile.screenshot(path=str(OUT / 'lobby-mobile.png'), full_page=True)
        mobile.click('#playBtn')
        mobile.wait_for_timeout(2800)
        assert mobile.locator('#touchControls').is_visible()
        mobile.screenshot(path=str(OUT / 'game-mobile.png'), full_page=True)
        ok('responsive mobile layout and visible touch controls')
        mobile_context.close()

        host_context, guest_context = browser.new_context(), browser.new_context()
        host, guest = host_context.new_page(), guest_context.new_page()
        for page in (host, guest):
            setup(page)
            page.select_option('#targetSelect', '3')
            page.click('[data-mode="online"]')
            page.click('#playBtn')
            page.uncheck('#internetCheck')
        guest.click('#joinTab')
        guest.fill('#offerIn', 'ER1.invalid')
        guest.click('#createAnswer')
        guest.wait_for_timeout(100)
        assert not guest.locator('#answerOut').input_value()
        assert guest.locator('#networkStatus').inner_text()
        ok('invalid invitation is rejected')
        host.click('#createOffer')
        host.wait_for_function('document.getElementById("offerOut").value.startsWith("ER1.")', timeout=20000)
        offer = host.locator('#offerOut').input_value()
        guest.fill('#offerIn', offer)
        guest.click('#createAnswer')
        guest.wait_for_function('document.getElementById("answerOut").value.startsWith("ER1.")', timeout=20000)
        host.fill('#answerIn', guest.locator('#answerOut').input_value())
        host.click('#acceptAnswer')
        for page in (host, guest):
            page.wait_for_function('EchoApp.peerStatus === "connected" && !!EchoApp.state', timeout=20000)
            page.wait_for_function('EchoApp.state.countdown <= 0', timeout=10000)
            page.uncheck('#autoFire')
        ok('real WebRTC handshake and synchronized match start')
        before = host.evaluate('EchoApp.state.players[1].y')
        # A checkbox retains keyboard focus; return focus just as a player does.
        guest.locator('#arena').focus()
        guest.keyboard.down('KeyW')
        guest.wait_for_timeout(450)
        guest.keyboard.up('KeyW')
        host.wait_for_timeout(150)
        assert host.evaluate('EchoApp.state.players[1].y') < before - 25
        ok('guest input crosses actual datachannel and moves authoritative player')
        guest.keyboard.press('Escape')
        host.wait_for_function('EchoApp.paused')
        guest.wait_for_function('EchoApp.paused')
        guest.click('#resumeBtn')
        host.wait_for_function('!EchoApp.paused')
        ok('guest pause/resume synchronizes both peers')
        assert not errors, errors
        host.screenshot(path=str(OUT / 'p2p-host.png'), full_page=True)
        guest.screenshot(path=str(OUT / 'p2p-guest.png'), full_page=True)
        ok('no JavaScript runtime exceptions')
        (OUT / 'browser.json').write_text(json.dumps({'passed': checks, 'errors': errors, 'scope': 'Chromium, two isolated browser contexts on one runner; not two physical networks'}, indent=2))
    except Exception as exc:
        (OUT / 'browser.json').write_text(json.dumps({'passed': checks, 'errors': errors, 'failure': str(exc)}, indent=2))
        raise
    finally:
        browser.close()
        server.shutdown()
