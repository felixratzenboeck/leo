# BONK! LEAGUE

Raketenauto-Fußball für zwei Spieler – als eigenständige HTML-Datei, ohne Installation und ohne Konto.

## Spielen

**GitHub Pages:** https://felixratzenboeck.github.io/leo/games/bonk-league/

Alternativ `index.html` herunterladen und direkt im Browser öffnen. Der lokale Modus funktioniert ohne Internet.

## Steuerung an einer Tastatur

| Aktion | Spieler 1 | Spieler 2 |
| --- | --- | --- |
| Fahren | WASD | Pfeiltasten |
| Boost | Linke Shift-Taste | Enter oder rechte Shift-Taste |
| Bonk-Schub | Leertaste oder Q | Rücktaste oder / |
| Pause | Esc | Esc |

Im Spiel zuerst **Zu zweit** und anschließend **Anpfiff** wählen. Bot-Gegner, Training, Touch-Steuerung und weitere Einstellungen sind im Spiel erreichbar.

## Zwei Geräte per WebRTC

Beide öffnen dieselbe Spielseite und wählen **Zwei Geräte**. Der Host erstellt eine Einladung. Der Gast fügt diese ein und erstellt einen Antwort-Code, den der Host übernimmt. Nach erfolgreicher Verbindung startet der Host das Match.

Das Spiel verwendet einen öffentlichen STUN-Server zur Verbindungsfindung. Es enthält keinen TURN-Relay. In restriktiven Netzwerken kann die direkte Verbindung deshalb scheitern. Eine echte Zwei-Geräte-Verbindung wurde bei der Erstellung nicht end-to-end verifiziert.

## Veröffentlichung

Die vorhandene Datei `BONK-LEAGUE.html` wird unverändert als `index.html` veröffentlicht. Bestehende Projekte im Repository bleiben unverändert.

- Originalgröße: 107634 Bytes
- SHA-256: `889d1d2bedfe7843e9e77738fafca56c084dad50f457f50f6b1a2cd1fa496bcc`
- Git-Blob-SHA: `802fa24d2786d7d2cf8f629268d99139f7ad907f`

Es wurde keine zusätzliche Softwarelizenz vergeben.
