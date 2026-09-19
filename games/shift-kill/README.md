# SHIFT//KILL — Crew Edition 2.0

Eigenständiger Canvas-Arena-Shooter mit Echo-Dash. Diese Demo erweitert die bestehende V1; das Spiel wurde nicht neu gebaut. Der Ordner `games/shift-kill/` ist vom übrigen Repository getrennt. Die vorhandene `index.html` im Repository-Hauptverzeichnis gehört nicht zu diesem Spiel und darf für diese Veröffentlichung nicht geändert werden.

## Starten

Die zugehörige `index.html` im Browser öffnen. Keine Installation, keine externen Grafik- oder Audio-Assets. Solo, zwei Personen an einer Tastatur oder zwei Geräte über WebRTC mit manuellem Einladung-/Antwortcode. V2 verwendet das Protokoll SK2; V1-Codes sind nicht kompatibel.

WASD bewegt, Maus/Trackpad zielt, F oder Klick feuert, Leertaste dasht und Q löst den Impuls aus. Auto-Feuer ist zunächst eingeschaltet. P2 im Couch-Modus: Pfeiltasten, L, K und J. Touch-Steuerung ist vorhanden.

## Gemeinsame Regeln

Die Crew-Lobby enthält 16 Optionen: zusätzliche Bots (0–4), Bot-Level, Rundendauer, Kill-Ziel, Lebenspunkte, Respawn-Zeit, Bewegungstempo, Schaden, Arena-Shift, Dash, Echo-Schuss, Impuls, Power-ups, Abpraller, zerstörbare Deckung und Test-Boosts. Vier Presets erleichtern den Einstieg. Regeln lassen sich als versioniertes JSON exportieren und importieren.

Im Couch-Duell bestätigen beide Personen die Regeln. Im P2P können beide Vorschläge machen. Der Host serialisiert Änderungen in eine gemeinsame Revision. Änderungen an Regeln oder Loadouts setzen beide Bestätigungen zurück. Erst wenn beide exakt dieselbe Revision und denselben vollständigen Regelvertrag bestätigen, kann der Host starten. Während einer Runde sind die Regeln gesperrt. Für einen Rematch wird erneut abgestimmt. Persönliche Steuerung, Audio und Darstellung bleiben getrennt.

## Was hier dezentral ist — und was nicht

Die Spieldaten werden über WebRTC zwischen den Geräten übertragen. Der manuelle Code-Austausch ersetzt einen zentralen Matchmaking-/Signaling-Dienst. STUN ist standardmäßig aus; optional können Google-STUN oder ein eigener TURN-Server verwendet werden. Eine Verbindung ist abhängig von Browser, Netzwerk und Firewall nicht garantiert. Verbindungscodes nur privat teilen.

Die Simulation ist **host-autoritativ**. Der Host berechnet den verbindlichen Spielzustand; der Gast sendet Eingaben. Das ist kein vertrauensloses Konsenssystem und kein Schutz vor einem manipulierten Host. Bei Verbindungsabbruch pausiert das Match. Automatische Host-Migration ist nicht implementiert.

Der vollständige Regelvertrag wird verglichen. Die kurze angezeigte Regel-ID ist nur eine FNV-Vergleichshilfe, kein kryptografischer Sicherheitsnachweis. Zustimmungen gelten nur für die jeweilige Sitzung und Revision.

## Shop- und Admin-Demo

**Es werden keine echten Zahlungen verarbeitet. Es gibt keine echte Admin-Anmeldung.** Der offen zugängliche Schalter „Admin-Test simulieren“ simuliert kostenlose Produktfreischaltungen für diese Sitzung. Er ist ausdrücklich kein Zugriffsschutz und darf nicht als Produktions-Adminfunktion verwendet werden.

| Produkt | Entwurfspreis | Wirkung |
| --- | ---: | --- |
| Prism Halo | 2,99 EUR | Nur Optik; unveränderte Hitbox und Kampfwerte |
| Solar Halo | 2,99 EUR | Nur Optik; unveränderte Hitbox und Kampfwerte |
| Phase Tuning | 1,99 EUR | Dash-Cooldown um 10 % kürzer: 2,25 auf 2,025 Sekunden |
| Overdrive Tuning | 1,99 EUR | Schussintervall um 8 % kürzer; kein Zusatzschaden |

Preise sind ausschließlich Demo-Entwürfe, keine eingerichteten Verkaufsangebote. Kaufbuttons führen keinen Checkout aus. Boosts sind standardmäßig aus und wirken nur, wenn die gemeinsame Regel für Test-Boosts aktiviert wurde. Loadout und Wirkung sind in der Lobby sichtbar. Admin-Simulation oder freigegebene Boosts markieren die Runde als Testmatch; sie zählt nicht zur lokalen Statistik. Beim Beenden des Admin-Tests werden simulierte Produkte abgelegt.

## Source of Truth

1. **Code und Katalog:** die versionierte Spiel-HTML in diesem Ordner; ein Release-Manifest kann deren SHA-256 dokumentieren. Änderungen an Preisen oder Regeln müssen versioniert werden.
2. **Laufendes Match:** bestätigter Regelvertrag plus Host-Spielzustand. Kein Zahlungsnachweis, kein manipulationssicheres Ranking.
3. **Spätere Käufe und Rollen:** benötigen eine separate, vertrauenswürdige Autorität mit authentifizierten Nutzern, geprüften Zahlungsereignissen, nachvollziehbaren Freischaltungen, Erstattungen/Widerrufen und serverseitig geprüften Adminrollen. Diese Schicht ist in dieser Demo nicht angebunden.

Eine frei editierbare Offline-HTML kann keine kostenpflichtigen Rechte gegenüber einem modifizierten Client sicher erzwingen. GitHub ist kein Zahlungsregister. Eine spätere Bezahlintegration darf keine Rechte allein aus LocalStorage, URL-Parametern oder einer Checkout-Erfolgsseite ableiten. Kaufvorteile dürfen nicht verborgen werden. Wettbewerbsfähige, bezahlte Ranglisten erfordern außerdem ein belastbares Anti-Cheat-/Verifikationsmodell.

## Tatsächlich durchgeführte Prüfung

56 lokale Browser-, Simulations- und Protokollprüfungen bestanden. Dazu gehören die Anwendung der gemeinsamen Regeln, beidseitige Zustimmung, Zurücksetzen nach Änderungen, Ablehnung veralteter Vorschläge, Verhinderung erfundener Gast-Zustimmung, Rematch, Verbindungsabbruch, mobile Darstellung und Shop-Simulation. Keine unbehandelten Browser-Ausnahmen im Testlauf.

**Testgrenzen:** Der Browser erhielt die HTML über Playwright `set_content`, da Datei- und Localhost-Navigation in der Testumgebung gesperrt waren. Protokolltests verwendeten kontrollierte In-Memory-Kanäle. Ein zusätzlicher echter WebRTC-Verbindungsversuch lieferte keine nutzbaren ICE-Kandidaten. Deshalb ist damit kein erfolgreicher Zwei-Geräte-/Internet-End-to-End-Test nachgewiesen. Safari/iOS und echte Zahlungen wurden nicht getestet. Ein GitHub-Commit allein belegt auch noch kein erfolgreiches Website-Deployment.

Technische Referenzen: https://webrtc.org/getting-started/peer-connections und https://docs.stripe.com/webhooks .
