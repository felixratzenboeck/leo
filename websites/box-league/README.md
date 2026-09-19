# BOX LEAGUE — P2P Edition 1.1

Eigenständiges 5-gegen-5-Arcade-Fußballspiel mit blockigen Boxern. Die vorhandene BOX-LEAGUE-App wird erweitert, nicht neu gebaut. Keine offiziellen Teams, Logos oder FIFA/EA-Sports-Assets.

## Spiel starten

`public/index.html` im Browser öffnen. Solo und Couch funktionieren offline. Im Fern-Duell steuert jeder sein Team mit WASD, Leertaste, E, Q, F und linker Umschalttaste; Touch-Buttons sind enthalten.

## Direkter, dezentraler Modus

1. Beide öffnen dieselbe Version der Spielseite oder HTML-Datei.
2. Gastgeber: Fern-Duell → Direkt → Einladung erstellen. Den Einladungslink privat teilen und den ursprünglichen Tab geöffnet lassen.
3. Gast: Link öffnen → Antwort erstellen. Den Antwortcode zurückschicken.
4. Gastgeber: Antwort im ursprünglichen Tab einsetzen → Antwort verbinden → Gemeinsamer Anpfiff.

Einladungen laufen nach zehn Minuten ab. Neue Einladungen machen alte Antworten ungültig. Bei einer lokalen Datei wird ein Code statt eines unbrauchbaren file://-Links geteilt; dann muss der Freund ebenfalls die HTML-Datei besitzen. Eine tatsächlich veröffentlichte HTTPS-Spieladresse kann im Dialog hinterlegt werden.

Das Match verwendet native WebRTC-Datenkanäle. Ein Gastgeber berechnet den Spielstand; es gibt keinen zentralen Spielserver, keine Konten und keine automatische Host-Übernahme. Verlässt der Gastgeber das Spiel, muss eine neue Sitzung aufgebaut werden. Die Software ist nicht manipulationssicher gegenüber einem veränderten Host-Client und nicht für Echtgeld-Wettbewerbe ausgelegt.

## Optional: Ein-Link-Räume mit eigenem Vermittler

`server/server.mjs` ist ein optionaler Signalisierungsserver ohne npm-Abhängigkeiten für Node.js 22 oder neuer. Lokal starten:

```sh
node websites/box-league/server/server.mjs
```

Danach ist die lokale Testseite unter `http://127.0.0.1:8787/` erreichbar. Als Raumserver dieselbe Adresse eintragen. Diese Loopback-Adresse ist ausschließlich für Tests am selben Rechner geeignet, nicht zum Teilen mit Freunden.

Für andere Geräte einen eigenen HTTPS-Reverse-Proxy und eine erreichbare Domain verwenden. Der Server bindet standardmäßig nur an 127.0.0.1; `HOST`, `PORT`, `MAX_ROOMS` und `ALLOWED_ORIGINS` sind über Umgebungsvariablen konfigurierbar. Hinter einem lokalen HTTPS-Proxy kann die Loopback-Bindung bestehen bleiben. Beispiel:

```sh
ALLOWED_ORIGINS=https://deine-spielseite.example PORT=8787 node websites/box-league/server/server.mjs
```

Im Spiel: Eigener Raumserver → HTTPS-Adresse eintragen → Raum erstellen → privaten Link teilen. Der Gast prüft und bestätigt die Serveradresse und tritt bei. Die Antwort wird automatisch übermittelt. Es ist kein öffentlicher Raumserver oder TURN-Zugang voreingestellt.

Der Vermittler speichert ausschließlich AES-GCM-verschlüsselte Verbindungsnachrichten im Arbeitsspeicher, höchstens zehn Minuten. Der Schlüssel steht nur im privaten Einladungsfragment, nicht in der Serveranfrage. Host- und Gast-Berechtigungen sind getrennt; Antworten sind gegen Überschreiben geschützt. Der Server bietet keine Raumliste. Spielpakete laufen nicht über diesen Vermittler. Bei erfolgreicher Verbindung entfernt der Gastgeber den Raum. Rate- und Speicherlimits sind enthalten; öffentliches Hosting braucht zusätzlich betriebliche Absicherung und HTTPS.

## STUN, TURN, LAN und VPN

Der Direktmodus benötigt keinen Signalisierungsdienst. Standardmäßig wird Google STUN nur beim Verbindungsaufbau angefragt. Unter Netzwerkoptionen kann öffentlicher STUN deaktiviert werden, etwa für LAN oder ein gemeinsames VPN. Ein VPN garantiert nicht, dass jeder Browser passende ICE-Kandidaten bereitstellt.

Nicht jedes Mobilfunknetz oder jede Firewall erlaubt eine direkte Verbindung. Dafür kann auf beiden Geräten ein eigener TURN-Relay samt Zugang eingetragen werden. TURN-Zugangsdaten werden weder gespeichert noch in Einladungen übernommen. Ein Raumserver ersetzt keinen TURN-Relay. Der Verbindungsdialog unterscheidet einen direkten WebRTC-Pfad von einem TURN-Relay-Pfad; bei Relay läuft der verschlüsselte Transport über diesen Server.

Einladungslinks sind Zugangsdaten: nicht öffentlich posten. Direkte Codes enthalten Netzwerkadressen. Der Raumserver sieht Zugriffe und IP-Adressen, aber keine entschlüsselten Einladungen oder Matchdaten. Der Website-Host sieht die üblichen HTTP-Zugriffe; URL-Fragmente werden nicht als Bestandteil der HTTP-Anfrage übertragen. Es werden weder Kamera noch Mikrofon angefordert.

## Veröffentlichung

Dieses Verzeichnis ist unabhängig von der vorhandenen `index.html` im Repository-Stamm. Die bestehende Startseite darf nicht überschrieben oder ungefragt mit veröffentlicht werden. Ein Pages-Workflow darf ausschließlich die freigegebene BOX-LEAGUE-Seite als eigenes Artefakt veröffentlichen. Ein GitHub-Commit allein ist noch keine spielbare Website; der tatsächliche Deployment-Status ist separat zu prüfen.

## Technische Referenzen

- WebRTC-Verbindungsaufbau: https://webrtc.org/getting-started/peer-connections
- TURN: https://webrtc.org/getting-started/turn-server
- GitHub Pages-Workflows: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
