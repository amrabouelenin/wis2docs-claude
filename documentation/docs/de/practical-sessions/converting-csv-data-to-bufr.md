# Konvertierung von CSV-Daten zu BUFR

!!! abstract "Lernziele"
    Am Ende dieser praktischen Sitzung werden Sie in der Lage sein:

    - die **MinIO UI** zu nutzen, um CSV-Eingabedateien hochzuladen und das Ergebnis zu überwachen
    - das Format für CSV-Daten für die Verwendung mit der Standard-BUFR-Vorlage für automatische Wetterstationen zu kennen
    - den Dataset-Editor in der **wis2box webapp** zu verwenden, um einen Datensatz für die Veröffentlichung von DAYCLI-Nachrichten zu erstellen
    - das Format für CSV-Daten für die Verwendung mit der DAYCLI-BUFR-Vorlage zu kennen
    - **wis2box webapp** zu verwenden, um Beispieldaten für AWS-Stationen zu validieren und in BUFR zu konvertieren (optional)

## Einführung

Durch Kommas getrennte Werte (CSV) werden häufig verwendet, um Beobachtungs- und andere Daten in einem tabellarischen Format aufzuzeichnen. 
Die meisten Datenlogger, die zur Aufzeichnung von Sensorausgaben verwendet werden, können die Beobachtungen in abgegrenzten Dateien exportieren, einschließlich im CSV-Format.
Ebenso ist es einfach, die erforderlichen Daten in CSV-formatierten Dateien zu exportieren, wenn Daten in eine Datenbank aufgenommen werden. 
Um den Austausch von Daten zu erleichtern, die ursprünglich in tabellarischen Datenformaten gespeichert wurden, wurde in der wis2box ein CSV-zu-BUFR-Konverter implementiert, der die gleiche Software wie für SYNOP zu BUFR verwendet.

In dieser Sitzung lernen Sie die Verwendung des csv2bufr-Konverters in der wis2box für die folgenden integrierten Vorlagen kennen:

- **AWS** (aws-template.json): Mapping-Vorlage für die Konvertierung von CSV-Daten aus einer vereinfachten automatischen Wetterstationsdatei in die BUFR-Sequenz 301150, 307096"
- **DayCLI** (daycli-template.json): Mapping-Vorlage für die Konvertierung von täglichen Klimadaten im CSV-Format in die BUFR-Sequenz 307075

## Vorbereitung

Stellen Sie sicher, dass der wis2box-Stack mit `python3 wis2box.py start` gestartet wurde

Stellen Sie sicher, dass Sie einen Webbrowser mit der MinIO-Benutzeroberfläche für Ihre Instanz geöffnet haben, indem Sie zu `http://<your-host>:9000` gehen.
Wenn Sie Ihre MinIO-Anmeldedaten nicht mehr wissen, können Sie diese in der Datei `wis2box.env` im Verzeichnis `wis2box-1.0.0rc1` auf Ihrer Student-VM finden.

Stellen Sie sicher, dass Sie MQTT Explorer geöffnet haben und mit Ihrem Broker verbunden sind, indem Sie die Anmeldedaten `everyone/everyone` verwenden.

## Übung 1: Verwendung von csv2bufr mit der 'AWS'-Vorlage

Die 'AWS'-Vorlage bietet eine vordefinierte Mapping-Vorlage zur Konvertierung von CSV-Daten von AWS-Stationen zur Unterstützung der GBON-Berichtsanforderungen. 

Die Beschreibung der AWS-Vorlage finden Sie [hier](/csv2bufr-templates/aws-template).

### Überprüfen Sie die aws-example Eingabedaten

Laden Sie das Beispiel für diese Übung über den folgenden Link herunter:

[aws-example.csv](/sample-data/aws-example.csv)

Öffnen Sie die heruntergeladene Datei in einem Editor und untersuchen Sie den Inhalt:

!!! question
    Was fällt Ihnen bei der Untersuchung der Datums-, Zeit- und Identifikationsfelder (WIGOS und traditionelle Kennungen) auf? Wie würde das heutige Datum dargestellt werden?

??? success "Klicken Sie, um die Antwort zu sehen"
    Jede Spalte enthält ein einzelnes Informationsstück. Zum Beispiel ist das Datum in Jahr, Monat und Tag aufgeteilt, was widerspiegelt, wie die Daten in BUFR gespeichert werden. Das heutige Datum würde auf die Spalten "year", "month" und "day" aufgeteilt werden. Ebenso muss die Zeit in "hour" und "minute" und die WIGOS-Stationskennung in ihre jeweiligen Komponenten aufgeteilt werden.

!!! question
    Wie werden fehlende Daten in der Datendatei kodiert?
    
??? success "Klicken Sie, um die Antwort zu sehen"
    Fehlende Daten innerhalb der Datei werden durch leere Zellen dargestellt. In einer CSV-Datei würde dies durch ``,,`` kodiert werden. Beachten Sie, dass dies eine leere Zelle ist und nicht als Zeichenkette mit Länge Null kodiert wird, z.B. ``,"",``.

!!! hint "Fehlende Daten"
    Es ist bekannt, dass Daten aus verschiedenen Gründen fehlen können, sei es aufgrund eines Sensorausfalls oder weil der Parameter nicht beobachtet wird. In diesen Fällen können fehlende Daten wie in der obigen Antwort kodiert werden, die anderen Daten im Bericht bleiben gültig.

!!! question
    Welche WIGOS-Stationskennungen haben die Stationen, die Daten in der Beispieldatei melden? Wie wird sie in der Eingabedatei definiert?

??? success "Klicken Sie, um die Antwort zu sehen"

    Die WIGOS-Stationskennung wird durch 4 separate Spalten in der Datei definiert:

    - **wsi_series**: WIGOS-Identifikationsreihe
    - **wsi_issuer**: WIGOS-Aussteller der Kennung
    - **wsi_issue_number**: WIGOS-Ausgabenummer
    - **wsi_local**: WIGOS lokale Kennung

    Die in der Beispieldatei verwendeten WIGOS-Stationskennungen sind `0-20000-0-60351`, `0-20000-0-60355` und `0-20000-0-60360`.	

### Aktualisieren Sie die Beispieldatei

Aktualisieren Sie die heruntergeladene Beispieldatei, um das heutige Datum und die aktuelle Uhrzeit zu verwenden, und ändern Sie die WIGOS-Stationskennungen, um Stationen zu verwenden, die Sie in der wis2box-Webapp registriert haben.

### Laden Sie die Daten in MinIO hoch und überprüfen Sie das Ergebnis

Navigieren Sie zur MinIO-Benutzeroberfläche und melden Sie sich mit den Anmeldedaten aus der Datei `wis2box.env` an.

Navigieren Sie zu **wis2box-incoming** und klicken Sie auf die Schaltfläche "Create new path":

<img alt="Bild, das die MinIO-Benutzeroberfläche mit hervorgehobener Schaltfläche zum Erstellen eines Ordners zeigt" src="../../assets/img/minio-create-new-path.png"/>

Erstellen Sie einen neuen Ordner im MinIO-Bucket, der der dataset-id für den Datensatz entspricht, den Sie mit der Vorlage='weather/surface-weather-observations/synop' erstellt haben:

<img alt="Bild, das die MinIO-Benutzeroberfläche mit hervorgehobener Schaltfläche zum Erstellen eines Ordners zeigt" src="../../assets/img/minio-create-new-path-metadata_id.png"/>

Laden Sie die heruntergeladene Beispieldatei in den von Ihnen erstellten Ordner im MinIO-Bucket hoch:

<img alt="Bild, das die MinIO-Benutzeroberfläche mit hochgeladenem aws-example zeigt" src="../../assets/img/minio-upload-aws-example.png"/></center>

Überprüfen Sie das Grafana-Dashboard unter `http://<your-host>:3000`, um zu sehen, ob es WARNUNGEN oder FEHLER gibt. Wenn Sie welche sehen, versuchen Sie, sie zu beheben und wiederholen Sie die Übung.

Überprüfen Sie den MQTT Explorer, um zu sehen, ob Sie WIS2-Datenbenachrichtigungen erhalten.

Wenn Sie die Daten erfolgreich aufgenommen haben, sollten Sie 3 Benachrichtigungen im MQTT Explorer zum Thema `origin/a/wis2/<centre-id>/data/weather/surface-weather-observations/synop` für die 3 Stationen sehen, für die Sie Daten gemeldet haben:

<img width="450" alt="Bild, das den MQTT Explorer nach dem Hochladen von AWS zeigt" src="../../assets/img/mqtt-explorer-aws-upload.png"/>

## Übung 2 - Verwendung der 'DayCLI'-Vorlage

In der vorherigen Übung haben wir den Datensatz verwendet, den Sie mit Data-type='weather/surface-weather-observations/synop' erstellt haben, der die CSV-zu-BUFR-Konvertierungsvorlage auf die AWS-Vorlage vorkonfiguriert hat.

In der nächsten Übung werden wir die 'DayCLI'-Vorlage verwenden, um tägliche Klimadaten in BUFR zu konvertieren.

Die Beschreibung der DAYCLI-Vorlage finden Sie [hier](/csv2bufr-templates/daycli-template).

!!! Note "Über die DAYCLI-Vorlage"
    Bitte beachten Sie, dass die DAYCLI-BUFR-Sequenz im Laufe des Jahres 2025 aktualisiert wird, um zusätzliche Informationen und überarbeitete QC-Flags aufzunehmen. Die in der wis2box enthaltene DAYCLI-Vorlage wird entsprechend aktualisiert. Die WMO wird mitteilen, wann die wis2box-Software aktualisiert wird, um die neue DAYCLI-Vorlage zu integrieren, damit Benutzer ihre Systeme entsprechend aktualisieren können.

### Erstellen eines wis2box-Datensatzes zur Veröffentlichung von DAYCLI-Nachrichten

Gehen Sie zum Dataset-Editor in der wis2box-Webapp und erstellen Sie einen neuen Datensatz. Verwenden Sie dieselbe centre-id wie in den vorherigen praktischen Sitzungen und wählen Sie **Data Type='climate/surface-based-observations/daily'**:

<img alt="Erstellen Sie einen neuen Datensatz in der wis2box-Webapp für DAYCLI" src="../../assets/img/wis2box-webapp-create-dataset-daycli.png"/>

Klicken Sie auf "CONTINUE TO FORM" und fügen Sie eine Beschreibung für Ihren Datensatz hinzu, legen Sie die Bounding Box fest und geben Sie die Kontaktinformationen für den Datensatz an. Sobald Sie alle Abschnitte ausgefüllt haben, klicken Sie auf 'VALIDATE FORM' und überprüfen Sie das Formular.

Überprüfen Sie die Daten-Plugins für die Datensätze. Klicken Sie auf "UPDATE" neben dem Plugin mit dem Namen "CSV data converted to BUFR" und Sie werden sehen, dass die Vorlage auf **DayCLI** eingestellt ist:

<img alt="Aktualisieren Sie das Daten-Plugin für den Datensatz, um die DAYCLI-Vorlage zu verwenden" src="../../assets/img/wis2box-webapp-update-data-plugin-daycli.png"/>

Schließen Sie die Plugin-Konfiguration und senden Sie das Formular mit dem Authentifizierungstoken, das Sie in der vorherigen praktischen Sitzung erstellt haben.

Sie sollten jetzt einen zweiten Datensatz in der wis2box-Webapp haben, der so konfiguriert ist, dass er die DAYCLI-Vorlage für die Konvertierung von CSV-Daten in BUFR verwendet.

### Überprüfen Sie die daycli-example Eingabedaten

Laden Sie das Beispiel für diese Übung über den folgenden Link herunter:

[daycli-example.csv](/sample-data/daycli-example.csv)

Öffnen Sie die heruntergeladene Datei in einem Editor und untersuchen Sie den Inhalt:

!!! question
    Welche zusätzlichen Variablen sind in der daycli-Vorlage enthalten?

??? success "Klicken Sie, um die Antwort zu sehen"
    Die daycli-Vorlage enthält wichtige Metadaten zur Instrumentenaufstellung und Messqualitätsklassifikationen für Temperatur und Feuchtigkeit, Qualitätskontrollflags und Informationen darüber, wie die tägliche Durchschnittstemperatur berechnet wurde.

### Aktualisieren Sie die Beispieldatei

Die Beispieldatei enthält eine Zeile mit Daten für jeden Tag in einem Monat und meldet Daten für eine Station. Aktualisieren Sie die heruntergeladene Beispieldatei, um das heutige Datum und die aktuelle Uhrzeit zu verwenden, und ändern Sie die WIGOS-Stationskennungen, um eine Station zu verwenden, die Sie in der wis2box-Webapp registriert haben.

### Laden Sie die Daten in MinIO hoch und überprüfen Sie das Ergebnis

Wie zuvor müssen Sie die Daten in den 'wis2box-incoming'-Bucket in MinIO hochladen, damit sie vom csv2bufr-Konverter verarbeitet werden können. Diesmal müssen Sie einen neuen Ordner im MinIO-Bucket erstellen, der der dataset-id für den Datensatz entspricht, den Sie mit der Vorlage='climate/surface-based-observations/daily' erstellt haben, die sich von der dataset-id unterscheidet, die Sie in der vorherigen Übung verwendet haben:

<img alt="Bild, das die MinIO-Benutzeroberfläche mit hochgeladenem DAYCLI-Beispiel zeigt" src="../../assets/img/minio-upload-daycli-example.png"/></center>

Überprüfen Sie nach dem Hochladen der Daten, ob es keine WARNUNGEN oder FEHLER im Grafana-Dashboard gibt, und überprüfen Sie den MQTT Explorer, um zu sehen, ob Sie WIS2-Datenbenachrichtigungen erhalten.

Wenn Sie die Daten erfolgreich aufgenommen haben, sollten Sie 30 Benachrichtigungen im MQTT Explorer zum Thema `origin/a/wis2/<centre-id>/data/climate/surface-base