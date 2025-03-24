# Herunterladen und Dekodieren von Daten aus WIS2

!!! abstract "Lernergebnisse!"

    Am Ende dieser praktischen Sitzung werden Sie in der Lage sein:

    - den "wis2downloader" zu verwenden, um WIS2-Datenbenachrichtigungen zu abonnieren und Daten auf Ihr lokales System herunterzuladen
    - den Status der Downloads im Grafana-Dashboard anzuzeigen
    - einige heruntergeladene Daten mit dem "decode-bufr-jupyter"-Container zu dekodieren

## Einführung

In dieser Sitzung lernen Sie, wie Sie ein Abonnement bei einem WIS2-Broker einrichten und automatisch Daten mit dem in der wis2box enthaltenen "wis2downloader"-Dienst auf Ihr lokales System herunterladen können.

!!! note "Über wis2downloader"
     
     Der wis2downloader ist auch als eigenständiger Dienst verfügbar, der auf einem anderen System als dem, das die WIS2-Benachrichtigungen veröffentlicht, ausgeführt werden kann. Weitere Informationen zur Verwendung des wis2downloaders als eigenständigen Dienst finden Sie unter [wis2downloader](https://pypi.org/project/wis2downloader/).

     Wenn Sie Ihren eigenen Dienst zum Abonnieren von WIS2-Benachrichtigungen und zum Herunterladen von Daten entwickeln möchten, können Sie den [wis2downloader-Quellcode](https://github.com/wmo-im/wis2downloader) als Referenz verwenden.

!!! Andere Tools für den Zugriff auf WIS2-Daten

    Die folgenden Tools können auch verwendet werden, um Daten von WIS2 zu entdecken und darauf zuzugreifen:

    - [pywiscat](https://github.com/wmo-im/pywiscat) bietet Suchfunktionen für den WIS2 Global Discovery Catalogue zur Unterstützung der Berichterstattung und Analyse des WIS2-Katalogs und seiner zugehörigen Entdeckungsmetadaten
    - [pywis-pubsub](https://github.com/wmo-im/pywis-pubsub) bietet Abonnement- und Download-Funktionen für WMO-Daten aus WIS2-Infrastrukturdiensten

## Vorbereitung

Bitte melden Sie sich vor dem Start bei Ihrer Student-VM an und stellen Sie sicher, dass Ihre wis2box-Instanz läuft.

## Übung 1: Anzeigen des wis2download-Dashboards in Grafana

Öffnen Sie einen Webbrowser und navigieren Sie zum Grafana-Dashboard für Ihre wis2box-Instanz, indem Sie zu `http://<Ihr-Host>:3000` gehen.

Klicken Sie im linken Menü auf Dashboards und wählen Sie dann das **wis2downloader-Dashboard** aus.

Sie sollten das folgende Dashboard sehen:

![wis2downloader-Dashboard](../assets/img/wis2downloader-dashboard.png)

Dieses Dashboard basiert auf Metriken, die vom wis2downloader-Dienst veröffentlicht werden, und zeigt Ihnen den Status der Downloads an, die derzeit in Bearbeitung sind.

In der oberen linken Ecke sehen Sie die Abonnements, die derzeit aktiv sind.

Lassen Sie dieses Dashboard geöffnet, da Sie es in der nächsten Übung verwenden werden, um den Download-Fortschritt zu überwachen.

## Übung 2: Überprüfen der wis2downloader-Konfiguration

Der vom wis2box-Stack gestartete wis2downloader-Dienst kann über die in Ihrer wis2box.env-Datei definierten Umgebungsvariablen konfiguriert werden.

Die folgenden Umgebungsvariablen werden vom wis2downloader verwendet:

    - DOWNLOAD_BROKER_HOST: Der Hostname des MQTT-Brokers, zu dem eine Verbindung hergestellt werden soll. Standardmäßig globalbroker.meteo.fr
    - DOWNLOAD_BROKER_PORT: Der Port des MQTT-Brokers, zu dem eine Verbindung hergestellt werden soll. Standardmäßig 443 (HTTPS für Websockets)
    - DOWNLOAD_BROKER_USERNAME: Der Benutzername für die Verbindung zum MQTT-Broker. Standardmäßig everyone
    - DOWNLOAD_BROKER_PASSWORD: Das Passwort für die Verbindung zum MQTT-Broker. Standardmäßig everyone
    - DOWNLOAD_BROKER_TRANSPORT: websockets oder tcp, der Transportmechanismus für die Verbindung zum MQTT-Broker. Standardmäßig websockets,
    - DOWNLOAD_RETENTION_PERIOD_HOURS: Die Aufbewahrungsdauer in Stunden für die heruntergeladenen Daten. Standardmäßig 24
    - DOWNLOAD_WORKERS: Die Anzahl der zu verwendenden Download-Worker. Standardmäßig 8. Bestimmt die Anzahl der parallelen Downloads.
    - DOWNLOAD_MIN_FREE_SPACE_GB: Der minimale freie Speicherplatz in GB, der auf dem Volume, das die Downloads hostet, freigehalten werden soll. Standardmäßig 1.

Um die aktuelle Konfiguration des wis2downloaders zu überprüfen, können Sie den folgenden Befehl verwenden:

```bash
cat ~/wis2box-1.0.0rc1/wis2box.env | grep DOWNLOAD
```

!!! question "Überprüfen Sie die Konfiguration des wis2downloaders"
    
    Welcher MQTT-Broker ist standardmäßig für den wis2downloader eingestellt?

    Wie lange ist die standardmäßige Aufbewahrungsdauer für die heruntergeladenen Daten?

??? success "Klicken Sie, um die Antwort anzuzeigen"

    Der standardmäßige MQTT-Broker, mit dem sich der wis2downloader verbindet, ist `globalbroker.meteo.fr`.

    Die standardmäßige Aufbewahrungsdauer für die heruntergeladenen Daten beträgt 24 Stunden.

!!! note "Aktualisieren der Konfiguration des wis2downloaders"

    Um die Konfiguration des wis2downloaders zu aktualisieren, können Sie die wis2box.env-Datei bearbeiten. Um die Änderungen anzuwenden, können Sie den Startbefehl für den wis2box-Stack erneut ausführen:

    ```bash
    python3 wis2box-ctl.py start
    ```

    Sie werden sehen, dass der wis2downloader-Dienst mit der neuen Konfiguration neu gestartet wird.

Für diese Übung können Sie die Standardkonfiguration beibehalten.

## Übung 3: Hinzufügen von Abonnements zum wis2downloader

Im **wis2downloader**-Container können Sie die Befehlszeile verwenden, um Abonnements aufzulisten, hinzuzufügen und zu löschen.

Um sich beim **wis2downloader**-Container anzumelden, verwenden Sie den folgenden Befehl:

```bash
python3 wis2box-ctl.py login wis2downloader
```

Verwenden Sie dann den folgenden Befehl, um die Abonnements aufzulisten, die derzeit aktiv sind:

```bash
wis2downloader list-subscriptions
```

Dieser Befehl gibt eine leere Liste zurück, da derzeit keine Abonnements aktiv sind.

Für diese Übung abonnieren wir das Thema `cache/a/wis2/de-dwd-gts-to-wis2/#`, um Daten zu abonnieren, die vom DWD-gehosteten GTS-to-WIS2-Gateway veröffentlicht werden, und Benachrichtigungen vom Global Cache herunterzuladen.

Um dieses Abonnement hinzuzufügen, verwenden Sie den folgenden Befehl:

```bash
wis2downloader add-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

Verlassen Sie dann den **wis2downloader**-Container, indem Sie `exit` eingeben:

```bash
exit
```

Überprüfen Sie das wis2downloader-Dashboard in Grafana, um das neue Abonnement zu sehen. Warten Sie einige Minuten, und Sie sollten sehen, dass die ersten Downloads beginnen. Gehen Sie zur nächsten Übung, sobald Sie bestätigt haben, dass die Downloads beginnen.

## Übung 4: Anzeigen der heruntergeladenen Daten

Der wis2downloader-Dienst im wis2box-Stack lädt die Daten in das Verzeichnis 'downloads' in dem Verzeichnis herunter, das Sie als WIS2BOX_HOST_DATADIR in Ihrer wis2box.env-Datei definiert haben. Um den Inhalt des Downloads-Verzeichnisses anzuzeigen, können Sie den folgenden Befehl verwenden:

```bash
ls -R ~/wis2box-data/downloads
```

Beachten Sie, dass die heruntergeladenen Daten in Verzeichnissen gespeichert werden, die nach dem Thema benannt sind, unter dem die WIS2-Benachrichtigung veröffentlicht wurde.

## Übung 5: Entfernen von Abonnements aus dem wis2downloader

Melden Sie sich als Nächstes wieder beim wis2downloader-Container an:

```bash
python3 wis2box-ctl.py login wis2downloader
```

und entfernen Sie das von Ihnen erstellte Abonnement aus dem wis2downloader mit dem folgenden Befehl:

```bash
wis2downloader remove-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

Und verlassen Sie den wis2downloader-Container, indem Sie `exit` eingeben:
    
```bash
exit
```

Überprüfen Sie das wis2downloader-Dashboard in Grafana, um zu sehen, dass das Abonnement entfernt wurde. Sie sollten sehen, dass die Downloads stoppen.

## Übung 6: Abonnieren des wis2training-Brokers und Einrichten eines neuen Abonnements

Für die nächste Übung werden wir den wis2training-Broker abonnieren.

Dies zeigt, wie man einen Broker abonniert, der nicht der Standardbroker ist, und ermöglicht es Ihnen, einige Daten herunterzuladen, die vom WIS2 Training Broker veröffentlicht wurden.

Bearbeiten Sie die wis2box.env-Datei und ändern Sie DOWNLOAD_BROKER_HOST in `wis2training-broker.wis2dev.io`, DOWNLOAD_BROKER_PORT in `1883` und DOWNLOAD_BROKER_TRANSPORT in `tcp`:

```copy
# downloader settings
DOWNLOAD_BROKER_HOST=wis2training-broker.wis2dev.io
DOWNLOAD_BROKER_PORT=1883
DOWNLOAD_BROKER_USERNAME=everyone
DOWNLOAD_BROKER_PASSWORD=everyone
# download transport mechanism (tcp or websockets)
DOWNLOAD_BROKER_TRANSPORT=tcp
```

Starten Sie dann den wis2box-Stack neu, um die Änderungen anzuwenden:

```bash
python3 wis2box-ctl.py start
```

Überprüfen Sie die Logs des wis2downloaders, um zu sehen, ob die Verbindung zum neuen Broker erfolgreich war:

```bash
docker logs wis2downloader
```

Sie sollten die folgende Logmeldung sehen:

```copy
...
INFO - Connecting...
INFO - Host: wis2training-broker.wis2dev.io, port: 1883
INFO - Connected successfully
```

Jetzt richten wir ein neues Abonnement für das Thema ein, um Zyklon-Track-Daten vom WIS2 Training Broker herunterzuladen.

Melden Sie sich beim **wis2downloader**-Container an:

```bash
python3 wis2box-ctl.py login wis2downloader
```

Und führen Sie den folgenden Befehl aus (kopieren und einfügen, um Tippfehler zu vermeiden):

```bash
wis2downloader add-subscription --topic origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory
```

Verlassen Sie den **wis2downloader**-Container, indem Sie `exit` eingeben.

Warten Sie, bis Sie sehen, dass die Downloads im wis2downloader-Dashboard in Grafana beginnen.

!!! note "Herunterladen von Daten vom WIS2 Training Broker"

    Der WIS2 Training Broker ist ein Testbroker, der für Schulungszwecke verwendet wird und möglicherweise nicht ständig Daten veröffentlicht.

    Während der Präsenzschulungen wird der lokale Trainer sicherstellen, dass der WIS2 Training Broker Daten für Sie zum Herunterladen veröffentlicht.

    Wenn Sie diese Übung außerhalb einer Schulungssitzung durchführen, sehen Sie möglicherweise keine heruntergeladenen Daten.

Überprüfen Sie, ob die Daten heruntergeladen wurden, indem Sie die wis2downloader-Logs erneut überprüfen:

```bash
docker logs wis2downloader
```

Sie sollten eine Logmeldung ähnlich der folgenden sehen:

```copy
[...] INFO - Message received under topic origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory
[...] INFO - Downloaded A_JSXX05ECEP020000_C_ECMP_...
```

## Übung 7: Dekodieren der heruntergeladenen Daten

Um zu demonstrieren, wie Sie die heruntergeladenen Daten dekodieren können, starten wir einen neuen Container mit dem Image 'decode-bufr-jupyter'.

Dieser Container startet einen Jupyter-Notebook-Server auf Ihrer Instanz, der die "ecCodes"-Bibliothek enthält, mit der Sie BUFR-Daten dekodieren können.

Wir verwenden die Beispiel-Notebooks in `~/exercise-materials/notebook-examples`, um die heruntergeladenen Daten für die Zyklon-Tracks zu dekodieren.

Um den Container zu starten, verwenden Sie den folgenden Befehl:

```bash
docker run -d --name decode-bufr-jupyter \
    -v ~/wis2box-data/downloads:/root/downloads \
    -p 8888:8888 \
    -e JUPYTER_TOKEN=dataismagic! \
    mlimper/decode-bufr-jupyter
```

!!! note "Über den decode-bufr-jupyter-Container"

    Der `decode-bufr-jupyter`-Container ist ein benutzerdefinierter Container, der die ecCodes-Bibliothek enthält und einen Jupyter-Notebook-Server ausführt.