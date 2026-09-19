# BOX LEAGUE P2P 1.1.0 — Testbericht

Prüfdatum: 19. September 2026.

## Veröffentlichung tatsächlich geprüft

- Spiel: https://felixratzenboeck.github.io/leo/box-league/
- Direkte HTML-Adresse: https://felixratzenboeck.github.io/leo/websites/box-league/public/index.html
- GitHub-Workflow `BOX LEAGUE public URL verification`, Lauf 35468195942: erfolgreich.
- Beide URLs lieferten HTTP 200. Die Spielantwort wurde auf HTML-Inhaltstyp, exakt 132166 Bytes und SHA256 `9ef17b4635bac6c27fdf1ec9cc251caee9ac1f4766dca29cf4f6bd34963a0b91` geprüft.
- Der Kurzlink wurde auf das richtige Ziel und die Übernahme des privaten Einladungsfragments geprüft.
- Prüflauf: https://github.com/felixratzenboeck/leo/actions/runs/35468195942
- Pages-Deployment zu Commit `d501f87fa49b3b5482aae1870103358abc8bcdd0`: erfolgreich, Lauf 35468195299.

## Dateiverifikation

Die über die GitHub-Integration zurückgelesene Datei `websites/box-league/public/index.html` auf `main` hat den erwarteten Git-Blob `5916afe19267e61be1025333eb87dfe845a20562` und 132166 Bytes. Sie stimmt damit mit der getesteten lokalen HTML-Datei überein.

Die vorhandene Root-Startseite blieb unverändert: Blob `e110a42b44dec2fb2ff46754efb2803154484856`, 181988 Bytes. Die bereits bestehende Pages-Konfiguration wurde nicht ersetzt. Andere Anwendungen bleiben erhalten.

## Erfolgreiche lokale Prüfungen

Die komplette eingebettete JavaScript-Logik und der Node-Raumserver bestehen die Syntaxprüfung.

UI-Test mit der tatsächlichen HTML-Datei in Chromium: Version 1.1.0, Lobby, Couch-Match, Tastatureingabe, Pause, Rückkehr, Direkt-/Raum-Ansichten, Ablehnung ungültiger Einladungen, fehlender Server und unsicherer Serveradressen. Mobile Ansicht bei 390 × 844 Pixeln ohne horizontalen Überlauf. Keine erfassten JavaScript-Seitenfehler. Screenshots wurden visuell geprüft.

17 Protokollprüfungen mit echter Node-WebCrypto und einem echten lokalen HTTP-Raumserver: Einladungscode und URL-Parsing, Angebots-/Antwortverwechslung, Ablaufzeit, Sitzungsbindung, sichere Endpunkte, AES-GCM-Roundtrip, falsche Schlüssel und vertauschte Nachrichtentypen, Authentifizierung, Raum-Erstellung, unbekannte Berechtigungen, getrennte Host-/Gast-Leserechte, verschlüsselte Antwort, Schutz vor Überschreiben und Host-exklusive tatsächliche Raumlöschung.

GitHub-Release-Workflow 35468128239: erfolgreich. Er stellte nur die zuvor geprüften HTML-Bytes wieder her, prüfte SHA256 und JavaScript-Syntax und committete ausschließlich die Spiel-Datei.

## Nicht verifiziert / Einschränkungen

Die Browser-Administrationsrichtlinie der lokalen Testumgebung blockiert Datei-/HTTP(S)-Navigation und nutzbare WebRTC-Netzwerkkandidaten. UI-Tests wurden deshalb mit dem tatsächlichen HTML via `set_content` auf einer frischen leeren Browserseite ausgeführt. Der native WebRTC-Versuch lieferte eine verständliche Fehlermeldung und keine vorgetäuschte Verbindung.

Keine erfolgreiche Verbindung zwischen zwei physischen Geräten oder zwei Internetnetzen bestätigt. Keine Safari-/iPhone-Hardwaretests, keine gemessene WAN-Latenz, keine TURN-Relay-Livemessung. Die bestandenen Protokolltests und die bestätigte öffentliche Website ersetzen keinen solchen Mehrgerätetest.

Der optionale Raumserver wurde lokal geprüft, nicht öffentlich für den Nutzer in Betrieb genommen. Kein TURN-Zugang wird bereitgestellt. Manche Netzwerke benötigen einen TURN-Relay. Kein öffentlicher Spielerbrowser, kein Matchmaking, keine Host-Migration. Die Spielsimulation vertraut dem Gastgeber; keine Anti-Cheat- oder Echtgeld-Garantie.

Die Website wird zentral von GitHub Pages ausgeliefert. Dezentral ist der Spielbetrieb zwischen den Peers; der manuelle Verbindungsaufbau braucht keinen eigenen Signalisierungsserver. Der optionale Raumserver ist selbst hostbar und unabhängig austauschbar.
