# Verifizierter Release — ECHO RIFT

Diese Notiz aktualisiert die früheren, eingeschränkten Prüfstände in der README.

## Erfolgreich geprüft

Am 19. September 2026 bestand Revision `c8ccdd47e7b8b94b5328d0f992cc496cd647860b` den vollständigen Workflow **ECHO RIFT checks**:

https://github.com/felixratzenboeck/leo/actions/runs/35467024456

**18 Engine-Tests und 11 Browser-Prüfungen erfolgreich, keine erfassten JavaScript-Laufzeitfehler.** Geprüft wurden Spielstart, Bewegung, Echo, Dash, Pause/Fortsetzen, Einstellungs-Persistenz über echtes Neuladen, gleichzeitige Couch-Eingaben, schmales Touch-Layout und ungültige Einladungen.

Der WebRTC-Test nutzte echte Datenkanäle zwischen zwei isolierten Chromium-Browser-Sitzungen auf einem GitHub-Runner. Einladung/Antwort, synchronisierter Spielstart, übertragene Gasteingaben und gemeinsames Pausieren/Fortsetzen bestanden. Die ersten eingeschränkten lokalen Tests ohne ICE-Kandidaten sind damit nicht mehr der letzte Netzwerk-Prüfstand.

Nicht damit belegt: zwei physische Geräte, verschiedene Internetanschlüsse/Router, ein externer TURN-Relay oder echtes Safari-/iPhone-Verhalten. Direkte Internetverbindungen sind weiterhin vom Netzwerk abhängig.

## Reproduzieren

```sh
node --test tests/engine.test.cjs
python build.py
python -m pip install playwright
python -m playwright install chromium
python tests/browser_e2e.py
```

Die Einzeldatei des erfolgreichen Builds hat SHA-256:

`a6b45a6047232315b6dc45bd4015a5d89fcf4b770067c7b7b7bbb2fc72155495`

Die ausgelieferte ZIP enthält Quellcode, Testskripte, Prüfbericht, Screenshots und die fertige Einzeldatei. Die Cloudflare-ZIP enthält nur die fertige `index.html` an der Wurzel.

## Veröffentlichung

Der Quellcode ist auf GitHub veröffentlicht. **Dieser Testlauf ist keine Aktivierung einer öffentlichen Spiel-URL.** Cloudflare Pages bzw. GitHub Pages müssen separat als Hosting aktiviert werden. Die bestehende App auf `main` wurde durch diesen Spielstand nicht ersetzt.
