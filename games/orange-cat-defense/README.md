# LEO – Orange Cat Defense V2

Ein eigenständiges Tower-Defense-Spiel mit orangefarbenen Katzensoldaten. Version 2.0.0.

**Spielen:** https://felixratzenboeck.github.io/leo/games/orange-cat-defense/

Alternativ `index.html` herunterladen und im Browser öffnen. Die einzelne HTML-Datei enthält Grafik, Logik und synthetisierte Soundeffekte; keine externen Bibliotheken, Konten oder Spielserver.

## Neu in V2

- Schlanke Statuszeile, großes Spielfeld und kompakte Katzenleiste. Upgrades erscheinen erst bei Auswahl einer gesetzten Katze.
- 12 Klassen: Rekrut, Ninja, Scharfschütze, Bomber, Frostmagier, Blitzkatze, Fischkoch, Commander Leo, Pyro, Giftpfote, Laser und DJ Miau. Je zwei Upgrade-Pfade mit drei Stufen.
- Sechs Karten, drei Schwierigkeitsstufen, 40 Wellen, acht Bosswellen und anschließender Endlosmodus.
- Keramik-, Kometen- und Prisma-Gegner; Feuerkegel, Giftschaden, durchdringende Laser und stapelbare Unterstützung durch Koch plus DJ.
- Drei Fähigkeiten: Super-Miau, Zeitlupe und Katzenrausch. Geschwindigkeit bis 6-fach.
- Touch-Platzierung mit Bestätigung; automatische Hochformat-Karte auf passenden Handy-Ansichten.
- Einstellbare Effekte und Berücksichtigung reduzierter Bewegung.

## Bedienung

Katze unten auswählen, einen freien Platz neben dem Weg wählen, Welle starten. Gesetzte Katzen anklicken für Upgrades, Zielwahl und Verkauf. Auf Touch-Geräten den Bauplatz zusätzlich bestätigen. Karte, Schwierigkeit, Sound, Spielstand-Export und Import sind im Spiel erreichbar.

M: Super-Miau. F: Zeitlupe. R: Katzenrausch. Weitere Tastenkürzel stehen in der Spielhilfe.

## Spielstände

V2 verwendet einen eigenen lokalen Speicherschlüssel und überschreibt keinen V1-Spielstand. V1-Exporte können importiert werden. Eine laufende importierte Partie wird pausiert fortgesetzt. Spielstände sind lokal pro Browser und Herkunft gespeichert; zwischen Offline-Datei, Geräten und Website ist Export/Import erforderlich.

Eingriffe im versteckten Übungsmenü markieren die Partie als Übungsrunde; solche Runden schreiben keine regulären Rekorde. Das Menü ist ein lokales Easter Egg, keine geschützte Admin-Funktion.

## Veröffentlichung und Prüfung

50 automatisierte Chromium-Prüfungen bestanden; Details und Grenzen stehen in `TESTBERICHT.md`. `.release/` enthält die verlustfrei komprimierte Transportkopie mit SHA-256-Prüfsummen. Der Release-Workflow stellt die exakt geprüfte HTML-Datei wieder her und prüft die JavaScript-Syntax.

HTML: 121702 Bytes. SHA-256: `887d3494f4ec1fd4b2952ca80be74a1250e216e5b7395ca77aca80a1b87bc149`.

Andere Projekte und die Repository-Startseite werden nicht verändert. Es wurde keine zusätzliche Softwarelizenz vergeben. Kein offizielles Bloons-Produkt und keine übernommenen Bloons-Assets.
