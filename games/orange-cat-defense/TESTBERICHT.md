# Testbericht – Orange Cat Defense V2

Stand: 19. September 2026. Version 2.0.0.

## Lokale Tests: 50 / 50 bestanden

Python Playwright mit installiertem Chromium. HTML mit `set_content` geladen, da direkte Datei- und localhost-Navigation in dieser Umgebung gesperrt sind. Lokaler Speicher im Test emuliert; die Simulation für gezielte Prüfungen manuell weitergeschaltet. Zusätzlich `node --check` für das eingebettete JavaScript.

Geprüft wurden:

- 12 Klassen, sechs Karten und 40-Wellen-Anzeige; keine sichtbare Cheat-Schaltfläche beim Start.
- Layout ohne Seitenüberlauf in 1440×900, 1280×720, 1920×1080, 390×844, 320×568, 820×1180 und 844×390.
- Gültige Wege und ausreichend bebaubare Flächen auf allen sechs Karten; keine Platzierung auf Weg, Dekoration oder anderen Katzen.
- Kosten, Upgrade-Stufen, Kontext-Inspektor, zugängliche Katzenleiste, Wellenstart, Pause und Angriffe.
- Alle drei Fähigkeiten, neue Waffen, Giftwirkung, DJ/Koch-Kombination, Keramik-Aufspaltung und Tarnung.
- V2-Spielstandvalidierung, pausierte Wiederherstellung, abgewiesene beschädigte Imports und V1-Import.
- Versteckte Aktivierung per Tastatur und Logo-Tipps, Übungsmarkierung, Ausschluss von Rekorden, Unverwundbarkeit und Reset bei neuer Partie.
- Vollständige 40-Wellen-Kampagne mit automatisiertem regulärem Aufbau, Startgeld und Spielbelohnungen, ohne injizierte Ressourcen oder aktivierte Cheats: Sieg, 100 Leben, 4048 besiegte Gegner, 16 Katzen. Das belegt Durchspielbarkeit, nicht ausgewogene Schwierigkeit für alle Strategien.
- Endlosmodus und Touch-Kauf mit Bestätigung und korrekter Umrechnung der Hochformat-Koordinaten.
- Keine JavaScript-Laufzeitfehler in den Testfällen.

## Grenzen

Touch und Bildschirmgrößen wurden emuliert. Kein Test auf einem echten iPhone, iPad oder Safari. Keine Echtzeit-Langzeitmessung, kein umfassender Balancing-Test aller Schwierigkeitsgrade, keine automatisierte Audio-Wahrnehmungsprüfung. Die Speichertests prüfen Serialisierung und Wiederherstellung mit einem Speicher-Testadapter, nicht dauerhafte Speicherung auf jedem Browser/Dateisystem.

## Veröffentlichungsprüfung

Die separate GitHub Action `Orange Cat Defense V2 public URL check` ruft die öffentliche Spielseite ab und vergleicht HTTP-Status, Dateigröße und SHA-256 mit der getesteten Datei. Der jeweilige tatsächliche Status ist in GitHub Actions sichtbar; dieser Bericht nimmt kein Ergebnis vorweg.

Erwartete Datei: 121702 Bytes, SHA-256 `887d3494f4ec1fd4b2952ca80be74a1250e216e5b7395ca77aca80a1b87bc149`, Git-Blob `109cc29f46a1d7a94a56141a3fb3da4f8648897b`.
