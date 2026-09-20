# Leo Studio 2

Weiterentwicklung der bestehenden Leo/Folio-App, kein Neubau. Dieser Branch wird nicht veröffentlicht. `main`, fremde Projektordner und bestehende Workflows bleiben unberührt.

## Neu

- Neue violette Oberfläche, klarere Startseite, echte Bestandszahlen, Mobilnavigation und Dunkelmodus.
- Aufgabenboard mit vier Statusspalten, Listen- und Baumansicht, Unteraufgaben, Suche, Fachfilter, Priorität, Fälligkeit, Notizbuch-Verknüpfungen und Rückgängig. Desktop: Drag & Drop. Touch: Statusmenü an jeder Karte.
- Verschachtelte Fächer mit Icons, Farben, eingeklappten Bereichen und anpassbarem Anzeigenamen.
- Unabhängige Größen für Stift, Marker, Strichradierer und Laser. Der Laser wird nach kurzer Zeit ausgeblendet und weder gespeichert noch exportiert.
- Sichtbarer Leo-Assistent im Editor; bestehende private Bridge und Pages-Sperre bleiben erhalten.
- PWA-App-Shell mit kontrollierter Update-Aktivierung. Der Service Worker cached ausschließlich die App-Shell, keine API-Aufrufe, Sitzungen oder Nutzerdateien.
- Backup-Merge erhält jetzt auch die Beziehungen neu zugeordneter Aufgaben- und Ordner-IDs. Verzögerte Formular-Fokuswechsel wurden entfernt.

## Dateien und Erweiterung

`leo-src/base.html` ist die unveränderte bisherige App (Git-Blob `e110a42b44dec2fb2ff46754efb2803154484856`). `leo-src/studio.js` und `leo-src/theme.css` enthalten die neuen Komponenten. `scripts/build-leo.py` validiert die Basis, ergänzt die Komponenten und erzeugt `index.html` und `sw.js` ohne Netzwerkzugriff. Die Quelldateien und der Build bleiben separat bearbeitbar.

`window.LeoStudio.registerView({id:'plugin-mein-tool',render(){...}})` registriert eine vertrauenswürdige lokale Ansicht; `LeoStudio.navigate('plugin-mein-tool')` öffnet sie. Das ist eine Erweiterungsbasis, kein Sandbox-System für fremden Code.

```sh
python3 scripts/build-leo.py
python3 -m pip install playwright==1.57.0
python3 -m playwright install --with-deps chromium
python3 tests/leo-e2e.py
```

Der erste Branch-Build stellt die über die GitHub-Integration übertragenen, SHA-256-geprüften Komponenten aus `.leo-studio-transfer/` wieder her. Sobald die echten Komponenten committed sind, erfolgt kein erneutes Entpacken. Es gibt keinen Deployment-Schritt.

## Kompatibilität und Grenzen

Bestehende IDs, `folio/1`, IndexedDB `folio-private-v1`, `.folio`-Backups und `window.Folio` bleiben erhalten. Vor einem Adress-/Gerätewechsel ein Backup anlegen: Browserdaten sind an ihren Ursprung gebunden und nicht verschlüsselt. Keine Patientendaten ablegen.

Moodle, LEVIS und OpenClaw sind weiterhin nur über die bereits vorhandene private Bridge nutzbar; diese wird nicht durch ein öffentliches Frontend ersetzt. Es wurden keine Zugangsdaten oder FH-Inhalte importiert. Nicht enthalten: autonome Research-Ausführung, Echtzeit-Mehrbenutzer-Sync, natives iOS/macOS-Paket, Handschrifterkennung, Infinity Canvas, neue 3D-Anatomiemodelle. Neue PDF-Importe benötigen beim ersten Mal weiterhin den bestehenden Decoder-Download.

Browser-Tests verwenden ausschließlich synthetische Daten. Die Berichte nennen den tatsächlich getesteten Modus. Simulierte Druckereignisse und Viewportgrößen sind kein Hardwaretest auf einem iPad. Echter Apple Pencil, Safari auf iPhone/iPad, reales Mikrofon und authentifizierte Hochschul-/OpenClaw-Zugänge bleiben separat zu prüfen.
