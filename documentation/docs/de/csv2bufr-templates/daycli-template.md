# csv2bufr-Vorlage für tägliche Klimadaten (DAYCLI)

Die **DAYCLI**-Vorlage bietet ein standardisiertes CSV-Format für die Konvertierung täglicher Klimadaten in die BUFR-Sequenz 307075.

Das Format ist für die Verwendung mit Klimadatenmanagementsystemen zur Veröffentlichung von Daten auf WIS2 vorgesehen, um die Berichtsanforderungen für tägliche Klimabeobachtungen zu unterstützen.

Diese Vorlage erfasst tägliche Beobachtungen von:

- Minimale, maximale und durchschnittliche Temperatur über einen Zeitraum von 24 Stunden
- Gesamte angesammelte Niederschlagsmenge über einen Zeitraum von 24 Stunden
- Gesamte Schneehöhe zum Zeitpunkt der Beobachtung
- Höhe des Neuschnees über einen Zeitraum von 24 Stunden

Diese Vorlage erfordert zusätzliche Metadaten im Vergleich zur vereinfachten AWS-Vorlage: Methode zur Berechnung der Durchschnittstemperatur; Sensor- und Stationshöhen; Expositions- und Messqualitätsklassifikation.

!!! Hinweis "Über die DAYCLI-Vorlage"
    Bitte beachten Sie, dass die DAYCLI-BUFR-Sequenz im Laufe des Jahres 2025 aktualisiert wird, um zusätzliche Informationen und überarbeitete QC-Flags einzuschließen. Die in der wis2box enthaltene DAYCLI-Vorlage wird aktualisiert, um diese Änderungen widerzuspiegeln. Die WMO wird mitteilen, wann die wis2box-Software aktualisiert wird, um die neue DAYCLI-Vorlage zu integrieren, damit Benutzer ihre Systeme entsprechend aktualisieren können.

## CSV-Spalten und Beschreibung

{{ read_csv("docs/assets/tables/daycli-table.csv") }}

## Mittelungsmethode

{{ read_csv("docs/assets/tables/averaging-method-table.csv") }}

## Qualitätsflag

{{ read_csv("docs/assets/tables/quality_flag.csv") }}

## Referenzen für Standortklassifikation

[Referenz für "temperature_siting_classification"](https://library.wmo.int/idviewer/35625/839).

[Referenz für "precipitation_siting_classification"](https://library.wmo.int/idviewer/35625/840).

## Beispiel

Beispiel-CSV-Datei, die der DAYCLI-Vorlage entspricht: [daycli-example.csv](/sample-data/daycli-example.csv).