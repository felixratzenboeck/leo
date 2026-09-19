# ECHO RIFT

**Deine Vergangenheit schießt zurück.** Ein eigenständiges, deutschsprachiges 2D-Action-Duell für Tastatur und Trackpad. Bewaffnete Zeit-Echos, Portale, abprallende Schüsse und Dash-Parrys. Keine Konten, Bibliotheken, CDNs, heruntergeladenen Grafiken oder Audiodateien.

## Sofort spielen

Die mitgelieferte `ECHO-RIFT.html` in einem vollständigen Browser öffnen. **Warm-up** startet gegen einen Bot; **Couch-Duell** ist für zwei Personen an derselben Tastatur. Beide Modi benötigen keine Internetverbindung. Alternativ `public/index.html` mit allen fünf Nachbardateien öffnen oder den Ordner `public` statisch hosten. Auf Mobilgeräten können Dateivorschauen JavaScript blockieren; dort eine gehostete Version verwenden. Querformat vergrößert das Spielfeld.

## Steuerung

| Aktion | Spieler 1 / eigenes P2P-Gerät | Spieler 2 am selben Gerät |
|---|---|---|
| Bewegung | WASD | Pfeiltasten |
| Zielen | Trackpad oder Auto-Zielhilfe | Auto-Zielhilfe |
| Schießen | Autofeuer, Leertaste oder F | Autofeuer oder Enter |
| Dash / Parry | Shift links | Shift rechts oder Punkt |
| Zeit-Echo | Q | M oder physische Slash-Taste |
| Pause | Esc | Esc |

Im Couch-Modus zielen beide automatisch. Trackpad-Zielen benötigt kein Ziehen, Autofeuer erspart Klicks. Tastaturen können bei vielen gleichzeitig gedrückten Tasten Eingaben verschlucken. Auf Touch-Geräten stehen ein Bewegungsstick und Aktionstasten bereit.

## Spielregeln

Ein Zeit-Echo wiederholt bis zu zwei Sekunden Bewegung und Schüsse. Es braucht mindestens eine halbe Sekunde Aufzeichnung und hat acht Sekunden Abklingzeit. Dash reflektiert Geschosse; Wände bleiben fest. Portale transportieren Figuren und Projektile. Schüsse prallen zweimal ab. PATCH heilt, SPLIT erzeugt Dreifachschüsse und RUSH erhöht die Feuerrate. Alle 18 Sekunden startet eine angekündigte Sturmwelle, die per Dash durchquert werden kann.

Drei Arenen, drei Bot-Stufen und 3/5/7/10 Siegpunkte. Nach drei Minuten gewinnt die Führung; bei Gleichstand das nächste K.o. Respawn-Schutz, Ergebnisse und Revanche sind eingebaut.

## Peer-to-Peer

Beide öffnen dieselbe Version. Eine Person erstellt eine Einladung und sendet den Code. Die zweite fügt ihn unter „Ich trete bei“ ein und sendet den Antwortcode zurück. Die einladende Person übernimmt diese Antwort. Geöffnete WebRTC-Datenkanäle erlauben den Matchstart.

Der Host berechnet das Spiel mit 60 Schritten/Sekunde, Zustände werden bis zu 20-mal/Sekunde und Gasteingaben ungefähr 33-mal/Sekunde gesendet. Zuverlässige, geordnete Steuerungsnachrichten und ein separater ungeordneter Echtzeitkanal. Keine zentrale Matchmaking-Infrastruktur und kein Anti-Cheat gegen manipulierte Hosts. Beide Tabs im Vordergrund lassen. Unterbrechungen werden angezeigt, nicht durch einen Bot kaschiert.

Der Internetmodus verwendet Googles öffentlichen STUN-Dienst. Ohne Haken werden nur lokale Kandidaten gesammelt. Manche Router, Firewalls oder Browser verhindern direkte Verbindungen; ein eigener TURN-Relay kann nötig sein und ist nicht mitgeliefert. TURN-Zugangsdaten werden nicht dauerhaft gespeichert. Codes enthalten Netzwerk-Verbindungsdaten und gehören nur an vertraute Personen. Kamera und Mikrofon werden nicht benötigt.

## Bauen und prüfen

```sh
python build.py
node tests/engine.test.js
```

Python 3 genügt zum Erzeugen der Einzeldatei; kein npm oder Download ist erforderlich. Der aktuelle lokale Browser-Regressionslauf ist mit Python Playwright und Chromium reproduzierbar:

```sh
python tests/browser_e2e.py
```

`CHROMIUM_PATH` kann auf einen installierten Browser zeigen. Das separat ausgelieferte Projekt-ZIP enthält zusätzlich Desktop-/Touch-Smoke-Tests und einen echten Zwei-Browser-P2P-Test samt lokalem Testserver.

Prüfstand: **17 Engine-Tests bestanden**, einschließlich vollständiger gesetzter Bot-Matches auf allen Arenen. Chromium-Prüfungen für Start, Bewegung, Echo, Dash, Pause/Fortsetzen, Sieg, Revanche und gleichzeitige Couch-Eingaben bestanden. Touch-Emulation bei 390×844 einschließlich Bewegung, Echo und Einstellungen bestanden. Keine JavaScript-Laufzeitfehler in diesen geprüften Abläufen. Kein Test auf echter iPhone-/iPad-/Safari-Hardware.

**Ein echtes P2P-Duell wurde nicht erfolgreich verifiziert:** Die verwaltete Testumgebung liefert keine ICE-Kandidaten und blockiert lokale Navigations-URLs. Ein Einladungsversuch endet dort mit der vorgesehenen Fehlermeldung. Das ist kein erfolgreicher Netzwerktest. Zwei physische Geräte, verschiedene Router, TURN und Persistenz nach Browserneustart sind noch zu prüfen.

## Veröffentlichung

Quellcode: `game/echo-rift`, Ordner `websites/echo-rift/`. Die bestehende App auf `main` wurde nicht ersetzt.

Der separate Branch **`site/echo-rift`** enthält nur die veröffentlichungsfertigen Spieldateien im Wurzelordner. **GitHub Pages ist noch nicht aktiviert.** Aktivierung: Repository → Settings → Pages → Deploy from a branch → `site/echo-rift` → `/(root)` → Save. Dieser Branch ist ein vorbereiteter Stand; es gibt noch keinen automatischen Build vom Quellcode-Branch zum Veröffentlichungs-Branch.

Für ein neues Cloudflare-Pages-Direct-Upload-Projekt kann die mitgelieferte `ECHO-RIFT-Cloudflare.zip` verwendet werden: Sie enthält nur `index.html` direkt an der Wurzel. Für eine Git-Integration stattdessen ein eigenes Projekt mit dem statischen Branch einrichten. Cloudflare-Hosting wurde nicht aktiviert.

Offizielle Dokumentation:
- https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- https://developers.cloudflare.com/pages/get-started/direct-upload/
- https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Connectivity
