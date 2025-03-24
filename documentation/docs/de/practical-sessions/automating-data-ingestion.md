# Automatisierung der Datenaufnahme

!!! abstract "Lernergebnisse"

    Am Ende dieser praktischen Sitzung werden Sie in der Lage sein:
    
    - zu verstehen, wie die Daten-Plugins Ihres Datensatzes den Datenaufnahme-Workflow bestimmen
    - Daten in wis2box mit einem Skript unter Verwendung des MinIO Python-Clients aufzunehmen
    - Daten in wis2box aufzunehmen, indem Sie über SFTP auf MinIO zugreifen

## Einführung

Der **wis2box-management**-Container überwacht Ereignisse vom MinIO-Speicherdienst, um die Datenaufnahme basierend auf den für Ihren Datensatz konfigurierten Daten-Plugins auszulösen. Dies ermöglicht es Ihnen, Daten in den MinIO-Bucket hochzuladen und den wis2box-Workflow zu starten, um Daten auf dem WIS2-Broker zu veröffentlichen.

Die Daten-Plugins definieren die Python-Module, die vom **wis2box-management**-Container geladen werden und bestimmen, wie die Daten transformiert und veröffentlicht werden.

In der vorherigen Übung sollten Sie einen Datensatz mit der Vorlage `surface-based-observations/synop` erstellt haben, der die folgenden Daten-Plugins enthielt:

<img alt="data-mappings" src="../../assets/img/wis2box-data-mappings.png" width="800">

Wenn eine Datei in MinIO hochgeladen wird, ordnet wis2box die Datei einem Datensatz zu, wenn der Dateipfad die Datensatz-ID (`metadata_id`) enthält, und bestimmt die zu verwendenden Daten-Plugins anhand der Dateierweiterung und des in den Datensatz-Mappings definierten Dateimusters.

In den vorherigen Sitzungen haben wir den Datenaufnahme-Workflow durch die Verwendung der wis2box-Befehlszeilenfunktionalität ausgelöst, die Daten im korrekten Pfad in den MinIO-Speicher hochlädt.

Die gleichen Schritte können programmatisch mit jeder MinIO- oder S3-Client-Software durchgeführt werden, was Ihnen ermöglicht, Ihre Datenaufnahme als Teil Ihrer operativen Workflows zu automatisieren.

Alternativ können Sie auch über das SFTP-Protokoll auf MinIO zugreifen, um Daten hochzuladen und den Datenaufnahme-Workflow auszulösen.

## Vorbereitung

Melden Sie sich mit Ihrem SSH-Client (PuTTY oder einem anderen) an Ihrer Student-VM an.

Stellen Sie sicher, dass wis2box läuft:

```bash
cd ~/wis2box-1.0.0rc1/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

Stellen Sie sicher, dass MQTT Explorer läuft und mit Ihrer Instanz verbunden ist. Wenn Sie noch von der vorherigen Sitzung verbunden sind, löschen Sie alle vorherigen Nachrichten, die Sie möglicherweise aus der Warteschlange erhalten haben.
Dies kann entweder durch Trennen und Wiederverbinden oder durch Klicken auf das Papierkorbsymbol für das entsprechende Thema erfolgen.

Stellen Sie sicher, dass Sie einen Webbrowser mit dem Grafana-Dashboard für Ihre Instanz geöffnet haben, indem Sie zu `http://<your-host>:3000` gehen.

Und stellen Sie sicher, dass Sie einen zweiten Tab mit der MinIO-Benutzeroberfläche unter `http://<your-host>:9001` geöffnet haben. Denken Sie daran, dass Sie sich mit dem in Ihrer `wis2box.env`-Datei definierten `WIS2BOX_STORAGE_USER` und `WIS2BOX_STORAGE_PASSWORD` anmelden müssen.

## Übung 1: Einrichten eines Python-Skripts zur Datenaufnahme in MinIO

In dieser Übung verwenden wir den MinIO Python-Client, um Daten nach MinIO zu kopieren.

MinIO bietet einen Python-Client, der wie folgt installiert werden kann:

```bash
pip3 install minio
```

Auf Ihrer Student-VM ist das 'minio'-Paket für Python bereits installiert.

Gehen Sie in das Verzeichnis `exercise-materials/data-ingest-exercises`; dieses Verzeichnis enthält ein Beispielskript `copy_file_to_incoming.py`, das den MinIO Python-Client verwendet, um eine Datei nach MinIO zu kopieren.

Versuchen Sie, das Skript auszuführen, um die Beispieldatendatei `csv-aws-example.csv` in den `wis2box-incoming`-Bucket in MinIO zu kopieren:

```bash
cd ~/exercise-materials/data-ingest-exercises
python3 copy_file_to_incoming.py csv-aws-example.csv
```

!!! note

    Sie erhalten einen Fehler, da das Skript noch nicht für den Zugriff auf den MinIO-Endpunkt auf Ihrer wis2box konfiguriert ist.

Das Skript muss den korrekten Endpunkt für den Zugriff auf MinIO auf Ihrer wis2box kennen. Wenn wis2box auf Ihrem Host läuft, ist der MinIO-Endpunkt unter `http://<your-host>:9000` verfügbar. Das Skript muss auch mit Ihrem Speicherpasswort und dem Pfad im MinIO-Bucket aktualisiert werden, um die Daten zu speichern.

!!! question "Aktualisieren Sie das Skript und nehmen Sie die CSV-Daten auf"
    
    Bearbeiten Sie das Skript `copy_file_to_incoming.py`, um die Fehler zu beheben, mit einer der folgenden Methoden:
    - Von der Kommandozeile aus: Verwenden Sie den Texteditor `nano` oder `vim`, um das Skript zu bearbeiten
    - Mit WinSCP: Starten Sie eine neue Verbindung mit dem Dateiprotokoll `SCP` und denselben Anmeldeinformationen wie Ihr SSH-Client. Navigieren Sie zum Verzeichnis `exercise-materials/data-ingest-exercises` und bearbeiten Sie `copy_file_to_incoming.py` mit dem eingebauten Texteditor
    
    Stellen Sie sicher, dass Sie:

    - den korrekten MinIO-Endpunkt für Ihren Host definieren
    - das korrekte Speicherpasswort für Ihre MinIO-Instanz angeben
    - den korrekten Pfad im MinIO-Bucket zum Speichern der Daten angeben

    Führen Sie das Skript erneut aus, um die Beispieldatendatei `csv-aws-example.csv` in MinIO aufzunehmen:

    ```bash
    python3 copy_file_to_incoming.py csv-aws-example.csv
    ```

    Und stellen Sie sicher, dass die Fehler behoben sind.

Sie können überprüfen, ob die Daten korrekt hochgeladen wurden, indem Sie die MinIO-Benutzeroberfläche überprüfen und sehen, ob die Beispieldaten im richtigen Verzeichnis im `wis2box-incoming`-Bucket verfügbar sind.

Sie können das Grafana-Dashboard verwenden, um den Status des Datenaufnahme-Workflows zu überprüfen.

Schließlich können Sie MQTT Explorer verwenden, um zu überprüfen, ob Benachrichtigungen für die von Ihnen aufgenommenen Daten veröffentlicht wurden. Sie sollten sehen, dass die CSV-Daten in das BUFR-Format umgewandelt wurden und dass eine WIS2-Datenbenachrichtigung mit einer "kanonischen" URL veröffentlicht wurde, um das Herunterladen der BUFR-Daten zu ermöglichen.

## Übung 2: Aufnahme von Binärdaten

Als Nächstes versuchen wir, Binärdaten im BUFR-Format mit dem MinIO Python-Client aufzunehmen.

wis2box kann Binärdaten im BUFR-Format mit dem in wis2box enthaltenen Plugin `wis2box.data.bufr4.ObservationDataBUFR` aufnehmen.

Dieses Plugin teilt die BUFR-Datei in einzelne BUFR-Nachrichten auf und veröffentlicht jede Nachricht an den MQTT-Broker. Wenn die Station für die entsprechende BUFR-Nachricht nicht in den wis2box-Stationsmetadaten definiert ist, wird die Nachricht nicht veröffentlicht.

Da Sie in der vorherigen Sitzung die Vorlage `surface-based-observations/synop` verwendet haben, enthalten Ihre Datenmappings das Plugin `FM-12 data converted to BUFR` für die Datensatzmappings. Dieses Plugin lädt das Modul `wis2box.data.synop2bufr.ObservationDataSYNOP2BUFR`, um die Daten aufzunehmen.

!!! question "Aufnahme von Binärdaten im BUFR-Format"

    Führen Sie den folgenden Befehl aus, um die Binärdatendatei `bufr-example.bin` in den `wis2box-incoming`-Bucket in MinIO zu kopieren:

    ```bash
    python3 copy_file_to_incoming.py bufr-example.bin
    ```

Überprüfen Sie das Grafana-Dashboard und MQTT Explorer, um zu sehen, ob die Testdaten erfolgreich aufgenommen und veröffentlicht wurden, und wenn Sie Fehler sehen, versuchen Sie, diese zu beheben.

!!! question "Überprüfen Sie die Datenaufnahme"

    Wie viele Nachrichten wurden für dieses Datenbeispiel an den MQTT-Broker gesendet?

??? success "Klicken Sie, um die Antwort anzuzeigen"

    Wenn Sie das letzte Datenbeispiel erfolgreich aufgenommen und veröffentlicht haben, sollten Sie 10 neue Benachrichtigungen auf dem wis2box MQTT-Broker erhalten haben. Jede Benachrichtigung entspricht Daten für eine Station für einen Beobachtungszeitstempel.

    Das Plugin `wis2box.data.bufr4.ObservationDataBUFR` teilt die BUFR-Datei in einzelne BUFR-Nachrichten auf und veröffentlicht eine Nachricht für jede Station und jeden Beobachtungszeitstempel.

## Übung 3: Aufnahme von SYNOP-Daten im ASCII-Format

In der vorherigen Sitzung haben wir das SYNOP-Formular in der **wis2box-webapp** verwendet, um SYNOP-Daten im ASCII-Format aufzunehmen. Sie können SYNOP-Daten im ASCII-Format auch aufnehmen, indem Sie die Daten in MinIO hochladen.

In der vorherigen Sitzung sollten Sie einen Datensatz erstellt haben, der das Plugin 'FM-12 data converted to BUFR' für die Datensatzmappings enthielt:

<img alt="dataset-mappings" src="../../assets/img/wis2box-data-mappings.png" width="800">

Dieses Plugin lädt das Modul `wis2box.data.synop2bufr.ObservationDataSYNOP2BUFR`, um die Daten aufzunehmen.

Versuchen Sie, den MinIO Python-Client zu verwenden, um die Testdaten `synop-202307.txt` und `synop-202308.txt` in Ihre wis2box-Instanz aufzunehmen.

Beachten Sie, dass die 2 Dateien den gleichen Inhalt enthalten, aber der Dateiname unterschiedlich ist. Der Dateiname wird verwendet, um das Datum des Datenbeispiels zu bestimmen.

Das synop2bufr-Plugin stützt sich auf ein Dateimuster, um das Datum aus dem Dateinamen zu extrahieren. Die erste Gruppe im regulären Ausdruck wird verwendet, um das Jahr zu extrahieren, und die zweite Gruppe wird verwendet, um den Monat zu extrahieren.

!!! question "Nehmen Sie FM-12 SYNOP-Daten im ASCII-Format auf"

    Gehen Sie zurück zur MinIO-Oberfläche in Ihrem Browser und navigieren Sie zum `wis2box-incoming`-Bucket und in den Pfad, in den Sie die Testdaten in der vorherigen Übung hochgeladen haben.
    
    Laden Sie die neuen Dateien im richtigen Pfad im `wis2box-incoming`-Bucket in MinIO hoch, um den Datenaufnahme-Workflow auszulösen.

    Überprüfen Sie das Grafana-Dashboard und MQTT Explorer, um zu sehen, ob die Testdaten erfolgreich aufgenommen und veröffentlicht wurden.

    Was ist der Unterschied in `properties.datetime` zwischen den beiden an den MQTT-Broker gesendeten Nachrichten?

??? success "Klicken Sie, um die Antwort anzuzeigen"

    Überprüfen Sie die Eigenschaften der letzten 2 Benachrichtigungen in MQTT Explorer und Sie werden feststellen, dass eine Benachrichtigung hat:

    ```{.copy}
    "properties": {
        "data_id": "wis2/urn:wmo:md:nl-knmi-test:surface-based-observations.synop/WIGOS_0-20000-0-60355_20230703T090000",
        "datetime": "2023-07-03T09:00:00Z",
        ...
    ```

    und die andere Benachrichtigung hat:

    ```{.copy}
    "properties": {
        "data_id": "wis2/urn:wmo:md:nl-knmi-test:surface-based-observations.synop/WIGOS_0-20000-0-60355_20230803T090000",
        "datetime": "2023-08-03T09:00:00Z",
        ...
    ```

    Der Dateiname wurde verwendet, um das Jahr und den Monat des Datenbeispiels zu bestimmen.

## Übung 4: Datenaufnahme in MinIO über SFTP

Daten können auch über SFTP in MinIO aufgenommen werden.

Der in wis2box-stack aktivierte MinIO-Dienst hat SFTP auf Port 8022 aktiviert. Sie können über SFTP mit denselben Anmeldeinformationen wie für die MinIO-Benutzeroberfläche auf MinIO zugreifen. In dieser Übung verwenden wir die Admin-Anmeldeinformationen für den MinIO-Dienst, wie in `wis2box.env` definiert, aber Sie können auch zusätzliche Benutzer in der MinIO-Benutzeroberfläche erstellen.

Um über SFTP auf MinIO zuzugreifen, können Sie jede SFTP-Client-Software verwenden. In dieser Übung verwenden wir Win