# csv2bufr-Vorlage für automatische Wetterstationen, die stündliche GBON-Daten melden

Die **AWS-Vorlage** verwendet ein standardisiertes CSV-Format, um Daten von automatischen Wetterstationen zur Unterstützung der GBON-Berichtsanforderungen zu erfassen. Diese Mapping-Vorlage konvertiert CSV-Daten in die BUFR-Sequenz 301150, 307096.

Das Format ist für den Einsatz mit automatischen Wetterstationen gedacht, die eine Mindestanzahl von Parametern melden, darunter Luftdruck, Lufttemperatur und Luftfeuchtigkeit, Windgeschwindigkeit und -richtung sowie Niederschlag auf stündlicher Basis.

## CSV-Spalten und Beschreibung

{{ read_csv("docs/assets/tables/aws-minimal.csv") }}

## Beispiel

Beispiel-CSV-Datei, die der AWS-Vorlage entspricht: [aws-example.csv](/sample-data/aws-example.csv).