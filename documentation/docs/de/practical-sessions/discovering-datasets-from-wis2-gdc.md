# Entdeckung von Datensätzen aus dem WIS2 Global Discovery Catalogue

!!! abstract "Lernziele!"

    Am Ende dieser praktischen Sitzung werden Sie in der Lage sein:

    - pywiscat zu verwenden, um Datensätze aus dem Global Discovery Catalogue (GDC) zu entdecken

## Einführung

In dieser Sitzung lernen Sie, wie Sie Daten aus dem WIS2 Global Discovery Catalogue (GDC) entdecken können.

Derzeit sind folgende GDCs verfügbar:

- Environment and Climate Change Canada, Meteorological Service of Canada: <https://wis2-gdc.weather.gc.ca>
- China Meteorological Administration: <https://gdc.wis.cma.cn/api>
- Deutscher Wetterdienst: <https://wis2.dwd.de/gdc>


Während lokaler Schulungen wird ein lokaler GDC eingerichtet, damit die Teilnehmer den GDC nach den Metadaten abfragen können, die sie von ihren wis2box-Instanzen veröffentlicht haben. In diesem Fall stellen die Trainer die URL zum lokalen GDC bereit.

## Vorbereitung

!!! note
    Bitte melden Sie sich vor dem Start an Ihrer Studenten-VM an.

## Installation von pywiscat

Verwenden Sie den Python-Paketinstaller `pip3`, um pywiscat auf Ihrer VM zu installieren:
```bash
pip3 install pywiscat
```

!!! note

    Wenn Sie den folgenden Fehler erhalten:

    ```
    WARNING: The script pywiscat is installed in '/home/username/.local/bin' which is not on PATH.
    Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
    ```

    Führen Sie dann den folgenden Befehl aus:

    ```bash
    export PATH=$PATH:/home/$USER/.local/bin
    ```

    ...wobei `$USER` Ihr Benutzername auf Ihrer VM ist.

Überprüfen Sie, ob die Installation erfolgreich war:

```bash
pywiscat --version
```

## Daten mit pywiscat finden

Standardmäßig verbindet sich pywiscat mit dem Global Discovery Catalogue von Kanada. Konfigurieren wir pywiscat so, dass es den Trainings-GDC abfragt, indem wir die Umgebungsvariable `PYWISCAT_GDC_URL` setzen:

```bash
export PYWISCAT_GDC_URL=http://<lokaler-gdc-host-oder-ip>
```

Verwenden wir [pywiscat](https://github.com/wmo-im/pywiscat), um den GDC abzufragen, der im Rahmen des Trainings eingerichtet wurde.

```bash
pywiscat search --help
```

Suchen Sie nun im GDC nach allen Datensätzen:

```bash
pywiscat search
```

!!! question

    Wie viele Datensätze werden bei der Suche zurückgegeben?

??? success "Klicken Sie, um die Antwort anzuzeigen"
    Die Anzahl der Datensätze hängt vom GDC ab, den Sie abfragen. Bei Verwendung des lokalen Trainings-GDC sollten Sie sehen, dass die Anzahl der Datensätze gleich der Anzahl der Datensätze ist, die während der anderen praktischen Sitzungen in den GDC aufgenommen wurden.

Versuchen wir, den GDC mit einem Schlüsselwort abzufragen:

```bash
pywiscat search -q observations
```

!!! question

    Was ist die Datenpolitik der Ergebnisse?

??? success "Klicken Sie, um die Antwort anzuzeigen"
    Alle zurückgegebenen Daten sollten "core"-Daten angeben

Probieren Sie weitere Abfragen mit `-q` aus

!!! tip

    Das Flag `-q` erlaubt die folgende Syntax:

    - `-q synop`: Suche nach allen Datensätzen mit dem Wort "synop"
    - `-q temp`: Suche nach allen Datensätzen mit dem Wort "temp"
    - `-q "observations AND fiji"`: Suche nach allen Datensätzen mit den Wörtern "observations" und "fiji"
    - `-q "observations NOT fiji"`: Suche nach allen Datensätzen, die das Wort "observations", aber nicht das Wort "fiji" enthalten
    - `-q "synop OR temp"`: Suche nach allen Datensätzen mit "synop" oder "temp"
    - `-q "obs~"`: Unscharfe Suche

    Bei der Suche nach Begriffen mit Leerzeichen diese in doppelte Anführungszeichen setzen.

Lassen Sie uns mehr Details zu einem bestimmten Suchergebnis erhalten, an dem wir interessiert sind:

```bash
pywiscat get <id>
```

!!! tip

    Verwenden Sie den `id`-Wert aus der vorherigen Suche.


## Fazit

!!! success "Herzlichen Glückwunsch!"

    In dieser praktischen Sitzung haben Sie gelernt, wie man:

    - pywiscat verwendet, um Datensätze aus dem WIS2 Global Discovery Catalogue zu entdecken