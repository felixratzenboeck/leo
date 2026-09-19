# BONK! LEAGUE

Raketenauto-Fußball für zwei Spieler – als eigenständige HTML-Datei, ohne Installation und ohne Konto.

## Spielen

**Öffentliche Spielseite:** https://felixratzenboeck.github.io/leo/games/bonk-league/

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

Standardmäßig werden nur direkte lokale Verbindungskandidaten verwendet. Der öffentliche Google-STUN-Dienst ist **optional und zunächst ausgeschaltet**; aktivierbar über „Auch über Internet versuchen“. Es ist kein TURN-Relay eingebaut. In restriktiven Netzwerken kann die direkte Verbindung deshalb scheitern. Eine echte Zwei-Geräte-Verbindung wurde bei der Erstellung nicht end-to-end verifiziert; die öffentliche Bereitstellung ändert diese Einschränkung nicht.

## Veröffentlichung und Dateiintegrität

Die ursprüngliche Datei `BONK-LEAGUE.html` ist unverändert als `index.html` im öffentlichen Repository veröffentlicht. Die Leo-Startseite und andere Projekte werden durch diese Veröffentlichung nicht verändert.

- Originalgröße: 107634 Bytes
- SHA-256: `889d1d2bedfe7843e9e77738fafca56c084dad50f457f50f6b1a2cd1fa496bcc`
- Git-Blob-SHA: `802fa24d2786d7d2cf8f629268d99139f7ad907f`

Die Dateien unter `.release/` sind ein verlustfrei komprimiertes Transportformat für das Original. `restore.py` prüft die Größe, beide Prüfsummen und die eingebettete JavaScript-Syntax, bevor ausschließlich die Spieldatei geschrieben wird. Eine abweichende vorhandene Spieldatei wird nicht überschrieben.

Der GitHub-Actions-Workflow **BONK LEAGUE public URL verification** prüft zusätzlich den öffentlichen HTTPS-Aufruf, HTTP-Status, Inhaltstyp und die exakte SHA-256-Prüfsumme. Der aktuelle Prüflauf ist unter „Actions“ im Repository einsehbar.

Es wurde keine zusätzliche Softwarelizenz vergeben. Eigenständiges Spiel; keine offizielle Verbindung zu Rocket League.
