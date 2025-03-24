# Einrichtung eines empfohlenen Datensatzes mit Zugriffskontrolle

!!! abstract "Lernziele"
    Am Ende dieser praktischen Sitzung werden Sie in der Lage sein:

    - einen neuen Datensatz mit der Datenrichtlinie 'empfohlen' zu erstellen
    - dem Datensatz ein Zugriffstoken hinzuzufügen
    - zu überprüfen, dass auf den Datensatz ohne Zugriffstoken nicht zugegriffen werden kann
    - das Zugriffstoken zu HTTP-Headern hinzuzufügen, um auf den Datensatz zuzugreifen

## Einführung

Datensätze, die nicht als 'Kern'-Datensätze in der WMO betrachtet werden, können optional mit einer Zugriffskontrollrichtlinie konfiguriert werden. wis2box bietet einen Mechanismus, um einem Datensatz ein Zugriffstoken hinzuzufügen, das Benutzer daran hindert, Daten herunterzuladen, es sei denn, sie geben das Zugriffstoken in den HTTP-Headern an.

## Vorbereitung

Stellen Sie sicher, dass Sie SSH-Zugriff auf Ihre Student-VM haben und dass Ihre wis2box-Instanz läuft.

Stellen Sie sicher, dass Sie mit dem MQTT-Broker Ihrer wis2box-Instanz über MQTT Explorer verbunden sind. Sie können die öffentlichen Anmeldedaten `everyone/everyone` verwenden, um eine Verbindung zum Broker herzustellen.

Stellen Sie sicher, dass Sie einen Webbrowser mit der wis2box-Webapp für Ihre Instanz geöffnet haben, indem Sie zu `http://<your-host>/wis2box-webapp` gehen.

## Übung 1: Erstellen eines neuen Datensatzes mit Datenrichtlinie 'empfohlen'

Gehen Sie zur Seite 'Dataset Editor' in der wis2box-Webapp und erstellen Sie einen neuen Datensatz. Verwenden Sie dieselbe Zentrum-ID wie in den vorherigen praktischen Sitzungen und verwenden Sie die Vorlage='surface-weather-observations/synop'.

Klicken Sie auf 'OK', um fortzufahren.

Setzen Sie im Dataset Editor die Datenrichtlinie auf 'recommended' (beachten Sie, dass die Änderung der Datenrichtlinie die 'Topic-Hierarchie' aktualisiert).
Ersetzen Sie die automatisch generierte 'Local ID' durch einen beschreibenden Namen für den Datensatz, z.B. 'recommended-data-with-access-control':

<img alt="create-dataset-recommended" src="../../assets/img/create-dataset-recommended.png" width="800">

Füllen Sie weiterhin die erforderlichen Felder für räumliche Eigenschaften und Kontaktinformationen aus und 'Validieren Sie das Formular', um auf Fehler zu prüfen.

Reichen Sie schließlich den Datensatz ein, indem Sie das zuvor erstellte Authentifizierungstoken verwenden, und überprüfen Sie, ob der neue Datensatz in der wis2box-Webapp erstellt wurde.

Überprüfen Sie MQTT-Explorer, um zu sehen, ob Sie die WIS2-Benachrichtigungsnachricht erhalten, die den neuen Discovery-Metadatensatz zum Thema `origin/a/wis2/<your-centre-id>/metadata` ankündigt.

## Übung 2: Hinzufügen eines Zugriffstokens zum Datensatz

Melden Sie sich beim wis2box-Management-Container an,

```bash
cd ~/wis2box-1.0.0rc1
python3 wis2box-ctl.py login
```

Von der Kommandozeile innerhalb des Containers können Sie einen Datensatz mit dem Befehl `wis2box auth add-token` sichern, indem Sie mit dem Flag `--metadata-id` die Metadaten-ID des Datensatzes und das Zugriffstoken als Argument angeben.

Um beispielsweise das Zugriffstoken `S3cr3tT0k3n` zum Datensatz mit der Metadaten-ID `urn:wmo:md:not-my-centre:core.surface-based-observations.synop` hinzuzufügen:

```bash
wis2box auth add-token --metadata-id urn:wmo:md:not-my-centre:reco.surface-based-observations.synop S3cr3tT0k3n
```

Verlassen Sie den wis2box-Management-Container:

```bash
exit
```

## Übung 3: Veröffentlichen von Daten im Datensatz

Kopieren Sie die Datei `exercise-materials/access-control-exercises/aws-example2.csv` in das Verzeichnis, das durch `WIS2BOX_HOST_DATADIR` in Ihrer `wis2box.env` definiert ist:

```bash
cp ~/exercise-materials/access-control-exercises/aws-example2.csv ~/wis2box-data
```

Verwenden Sie dann WinSCP oder einen Kommandozeilen-Editor, um die Datei `aws-example2.csv` zu bearbeiten und die WIGOS-Stationskennungen in den Eingabedaten zu aktualisieren, damit sie mit den Stationen in Ihrer wis2box-Instanz übereinstimmen.

Gehen Sie als Nächstes zum Station-Editor in der wis2box-Webapp. Aktualisieren Sie für jede Station, die Sie in `aws-example2.csv` verwendet haben, das Feld 'topic', damit es mit dem 'topic' des Datensatzes übereinstimmt, den Sie in der vorherigen Übung erstellt haben.

Diese Station wird nun mit 2 Themen verknüpft, einem für den 'core'-Datensatz und einem für den 'recommended'-Datensatz:

<img alt="edit-stations-add-topics" src="../../assets/img/edit-stations-add-topics.png" width="600">

Sie müssen Ihr Token für `collections/stations` verwenden, um die aktualisierten Stationsdaten zu speichern.

Melden Sie sich als Nächstes beim wis2box-Management-Container an:

```bash
cd ~/wis2box-1.0.0rc1
python3 wis2box-ctl.py login
```

Von der wis2box-Kommandozeile aus können wir die Beispieldatendatei `aws-example2.csv` wie folgt in einen bestimmten Datensatz einlesen:

```bash
wis2box data ingest -p /data/wis2box/aws-example2.csv --metadata-id urn:wmo:md:not-my-centre:reco.surface-based-observations.synop
```

Stellen Sie sicher, dass Sie die richtige Metadaten-ID für Ihren Datensatz angeben und **überprüfen Sie, dass Sie WIS2-Datenbenachrichtigungen in MQTT Explorer erhalten**, zum Thema `origin/a/wis2/<your-centre-id>/data/recommended/surface-based-observations/synop`.

Überprüfen Sie den kanonischen Link in der WIS2-Benachrichtigungsnachricht und kopieren/fügen Sie den Link in den Browser ein, um zu versuchen, die Daten herunterzuladen.

Sie sollten einen 403 Forbidden-Fehler sehen.

## Übung 4: Hinzufügen des Zugriffstokens zu HTTP-Headern für den Zugriff auf den Datensatz

Um zu demonstrieren, dass das Zugriffstoken erforderlich ist, um auf den Datensatz zuzugreifen, werden wir den Fehler, den Sie im Browser gesehen haben, mit der Kommandozeilenfunktion `wget` reproduzieren.

Verwenden Sie von der Kommandozeile in Ihrer Student-VM den Befehl `wget` mit dem kanonischen Link, den Sie aus der WIS2-Benachrichtigungsnachricht kopiert haben.

```bash
wget <canonical-link>
```

Sie sollten sehen, dass die HTTP-Anfrage mit *401 Unauthorized* zurückkommt und die Daten nicht heruntergeladen werden.

Fügen Sie nun das Zugriffstoken zu den HTTP-Headern hinzu, um auf den Datensatz zuzugreifen.

```bash
wget --header="Authorization: Bearer S3cr3tT0k3n" <canonical-link>
```

Jetzt sollten die Daten erfolgreich heruntergeladen werden.

## Fazit

!!! success "Herzlichen Glückwunsch!"
    In dieser praktischen Sitzung haben Sie gelernt, wie man:

    - einen neuen Datensatz mit der Datenrichtlinie 'empfohlen' erstellt
    - einem Datensatz ein Zugriffstoken hinzufügt
    - überprüft, dass auf den Datensatz ohne Zugriffstoken nicht zugegriffen werden kann
    - das Zugriffstoken zu HTTP-Headern hinzufügt, um auf den Datensatz zuzugreifen