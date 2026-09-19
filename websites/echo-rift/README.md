# ECHO RIFT

**Deine Vergangenheit schießt zurück.** Ein eigenständiges, deutschsprachiges 2D-Action-Duell für Tastatur und Trackpad. Keine Accounts, Bibliotheken, CDNs, heruntergeladenen Grafiken oder Audiodateien.

## Sofort spielen

Die mitgelieferte `ECHO-RIFT.html` in einem vollständigen Browser öffnen. **Warm-up** startet gegen einen Bot; **Couch-Duell** ist für zwei Personen an derselben Tastatur. Alternativ `public/index.html` mit allen fünf Nachbardateien öffnen oder den Ordner `public` statisch hosten.

## Steuerung

| Aktion | Spieler 1 / eigenes P2P-Gerät | Spieler 2 am selben Gerät |
|---|---|---|
| Bewegung | WASD | Pfeiltasten |
| Zielen | Trackpad oder Auto-Zielhilfe | Auto-Zielhilfe |
| Schießen | Autofeuer, Leertaste oder F | Autofeuer oder Enter |
| Dash / Parry | Shift links | Shift rechts oder N |
| Zeit-Echo | Q | M oder Komma |
| Pause | Esc | Esc |

Autofeuer lässt sich abschalten. Im Couch-Modus zielen beide automatisch. Tastaturen können bei vielen gleichzeitig gedrückten Tasten Eingaben verschlucken; Autofeuer reduziert das Problem. Touch-Steuerung ist eine zusätzliche Option, keine Voraussetzung für das Spiel.

## Spielregeln

Ein Zeit-Echo wiederholt bis zu zwei Sekunden Bewegung und Schüsse. Dash reflektiert Geschosse. Zwei Portale transportieren Figuren und Projektile. Schüsse prallen zweimal ab. PATCH heilt, SPLIT erzeugt Dreifachschüsse und RUSH erhöht die Feuerrate. Alle 18 Sekunden startet eine angekündigte Sturmwelle.

Drei Arenen, drei Bot-Stufen und 3/5/7/10 Siegpunkte stehen zur Auswahl. Nach drei Minuten entscheidet die Führung; bei Gleichstand das nächste K.o. Es gibt Respawn-Schutz, Ergebnisse und Revanche.

## Peer-to-Peer

Auf beiden Geräten dieselbe Version in einem vollständigen Browser öffnen. Eine Person erstellt eine Einladung und sendet den Code. Die zweite fügt ihn unter „Ich trete bei“ ein und sendet den Antwortcode zurück. Die einladende Person übernimmt diese Antwort. Erst nach geöffnetem WebRTC-Datenkanal und Startbestätigung läuft das Duell.

Die einladende Person berechnet das Spiel mit 60 Simulationsschritten pro Sekunde; Zustände werden mit bis zu 20 Hz und Gasteingaben mit bis zu 30 Hz übertragen. Keine zentrale Matchmaking-Infrastruktur. Kein Anti-Cheat gegen einen manipulierten Host. Beide Tabs im Vordergrund lassen; ein Hintergrundwechsel pausiert die Partie.

Der Internetmodus verwendet Googles öffentlichen STUN-Dienst. Ohne Internet-Haken werden nur lokale Kandidaten gesammelt. Einige Router, Firewalls oder Browser blockieren direkte Verbindungen. Ein optionaler eigener TURN-Relay kann nötig sein; es ist keiner mitgeliefert. TURN-Zugangsdaten werden nicht dauerhaft gespeichert. Einladungscodes enthalten Verbindungsdaten und sollten nur mit vertrauten Personen geteilt werden.

## Offline-Datei selbst bauen

Python 3 genügt:

```sh
python build.py
```

Der Build erzeugt `ECHO-RIFT.html` und bettet alle lokalen Spielressourcen ein. Kein npm und keine Downloads erforderlich.

## Veröffentlichung

Der Quellcode liegt isoliert auf `game/echo-rift` unter `websites/echo-rift/`. Die bestehende Anwendung in der Repository-Wurzel wurde nicht ersetzt. Eine GitHub-Codeveröffentlichung ist noch keine aktivierte GitHub-Pages-Spielseite.

Für Cloudflare Pages Git-Integration: Branch `game/echo-rift`, Build-Ausgabe `websites/echo-rift/public`, kein Build erforderlich. Alternativ ein **neues Direct-Upload-Projekt** mit dem mitgelieferten `ECHO-RIFT-Cloudflare.zip` anlegen. Die ZIP enthält `index.html` direkt an der Wurzel. Direct Upload und Git-Integration sind unterschiedliche Projektarten.

Offizielle Dokumentation:
- https://developers.cloudflare.com/pages/get-started/direct-upload/
- https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

## Prüfstand und Grenzen

18 automatisierte Engine-Tests bestanden, einschließlich Kollisionen, Echo, Schaden, Respawn, Parry, Portalen, Power-ups, Sturm, Zeitlimit und deterministischer Bot-Simulation. Ausführen: `node --test tests/engine.test.cjs` (Node 22 getestet).

Browserprüfungen der eingebetteten HTML in Chromium: Spielstart, Bewegung, Dash, Echo, Pause/Fortsetzen, gleichzeitige Couch-Eingaben, Einstellungsänderung und Fehlerbehandlung für ungültige Einladungscodes erfolgreich; keine JavaScript-Laufzeitfehler in diesen Abläufen. Desktop- und schmale Layouts wurden visuell geprüft. Nicht auf echter iPhone-/iPad-/Safari-Hardware getestet.

**Ein vollständiges P2P-Duell über zwei Geräte wurde nicht erfolgreich verifiziert:** Die verwaltete Testumgebung liefert keine ICE-Netzwerkadressen. Einladungsversuche ohne erreichbare Kandidaten werden deshalb mit einer klaren Fehlermeldung beendet. Das ist kein erfolgreicher Netzwerktest. Tests über verschiedene Router, TURN sowie Speicherpersistenz nach Browserneustart stehen aus.
