# Konvertierung von SYNOP-Daten zu BUFR über die Kommandozeile

!!! abstract "Lernziele"
    Am Ende dieser praktischen Übung werden Sie in der Lage sein:

    - das synop2bufr-Tool zu verwenden, um FM-12 SYNOP-Berichte in BUFR zu konvertieren;
    - einfache Kodierungsfehler in FM-12 SYNOP-Berichten vor der Formatkonvertierung zu diagnostizieren und zu beheben;

## Einführung

Wettermeldungen von Landstationen wurden historisch stündlich oder zu den Haupt- 
(00, 06, 12 und 18 UTC) und Zwischen-Synoptikzeiten (03, 09, 15, 21 UTC) gemeldet. Vor der Migration
zu BUFR wurden diese Berichte im Klartext-Format FM-12 SYNOP kodiert. Obwohl die Migration zu BUFR
bis 2012 abgeschlossen sein sollte, wird eine große Anzahl von Berichten immer noch im älteren 
FM-12 SYNOP-Format ausgetauscht. Weitere Informationen zum FM-12 SYNOP-Format finden Sie im WMO-Handbuch für Codes, 
Band I.1 (WMO-Nr. 306, Band I.1).

[WMO-Handbuch für Codes, Band I.1](https://library.wmo.int/records/item/35713-manual-on-codes-international-codes-volume-i-1)

Um die Migration zu BUFR zu unterstützen, wurden einige Tools zur
Kodierung von FM-12 SYNOP-Berichten in BUFR entwickelt. In dieser Sitzung lernen Sie, wie Sie diese Tools verwenden können, sowie
die Beziehung zwischen den Informationen in den FM-12 SYNOP-Berichten und BUFR-Nachrichten.

## Vorbereitung

!!! warning "Voraussetzungen"

    - Stellen Sie sicher, dass Ihre wis2box konfiguriert und gestartet wurde.
    - Bestätigen Sie den Status, indem Sie die wis2box-API besuchen (`http://<Ihr-Host-Name>/oapi`) und überprüfen, dass die API läuft.
    - Lesen Sie unbedingt die Abschnitte **synop2bufr-Grundlagen** und **ecCodes-Grundlagen**, bevor Sie mit den Übungen beginnen.

## synop2bufr-Grundlagen

Hier sind wichtige `synop2bufr`-Befehle und Konfigurationen:

### transform
Die Funktion `transform` konvertiert eine SYNOP-Nachricht in BUFR:

```bash
synop2bufr data transform --metadata meine_datei.csv --output-dir ./mein_verzeichnis --year nachricht_jahr --month nachricht_monat meine_SYNOP.txt
```

Beachten Sie, dass wenn die Optionen für Metadaten, Ausgabeverzeichnis, Jahr und Monat nicht angegeben werden, diese ihre Standardwerte annehmen:

| Option      | Standard |
| ----------- | ----------- |
| --metadata | station_list.csv |
| --output-dir | Das aktuelle Arbeitsverzeichnis. |
| --year | Das aktuelle Jahr. |
| --month | Der aktuelle Monat. |

!!! note
    Bei Verwendung des Standard-Jahres und -Monats ist Vorsicht geboten, da der im Bericht angegebene Tag des Monats möglicherweise nicht übereinstimmt (z.B. hat der Juni keine 31 Tage).

In den Beispielen werden Jahr und Monat nicht angegeben, Sie können also entweder selbst ein Datum festlegen oder die Standardwerte verwenden.

## ecCodes-Grundlagen

ecCodes bietet sowohl Kommandozeilentools als auch die Möglichkeit, in Ihre eigenen Anwendungen eingebettet zu werden. Im Folgenden finden Sie einige nützliche Kommandozeilen-Dienstprogramme für die Arbeit mit BUFR-Daten.

### bufr_dump

Der Befehl `bufr_dump` ist ein allgemeines BUFR-Informationstool. Es hat viele Optionen, aber die folgenden werden für die Übungen am nützlichsten sein:

```bash
bufr_dump -p mein_bufr.bufr4
```

Dies zeigt den BUFR-Inhalt auf Ihrem Bildschirm an. Wenn Sie sich für die Werte einer bestimmten Variable interessieren, verwenden Sie den Befehl `egrep`:

```bash
bufr_dump -p mein_bufr.bufr4 | egrep -i temperature
```

Dies zeigt Variablen im Zusammenhang mit Temperatur in Ihren BUFR-Daten an. Wenn Sie dies für mehrere Arten von Variablen tun möchten, filtern Sie die Ausgabe mit einer Pipe (`|`):

```bash
bufr_dump -p mein_bufr.bufr4 | egrep -i 'temperature|wind'
```

## Konvertierung von FM-12 SYNOP zu BUFR mit synop2bufr über die Kommandozeile

Die eccodes-Bibliothek und das synop2bufr-Modul sind im wis2box-api-Container installiert. Um die nächsten Übungen durchzuführen, kopieren wir das Verzeichnis synop2bufr-exercises in den wis2box-api-Container und führen die Übungen von dort aus durch.

```bash
docker cp ~/exercise-materials/synop2bufr-exercises wis2box-api:/root
```

Jetzt können wir den Container betreten und die Übungen ausführen:

```bash
docker exec -it wis2box-api /bin/bash
```

### Übung 1
Navigieren Sie zum Verzeichnis `/root/synop2bufr-exercises/ex_1` und untersuchen Sie die SYNOP-Nachrichtendatei message.txt:

```bash
cd /root/synop2bufr-exercises/ex_1
more message.txt
```

!!! question

    Wie viele SYNOP-Berichte sind in dieser Datei enthalten?

??? success "Klicken Sie, um die Antwort anzuzeigen"
    
    Es gibt 1 SYNOP-Bericht, da es nur 1 Trennzeichen (=) am Ende der Nachricht gibt.

Untersuchen Sie die Stationsliste:

```bash
more station_list.csv
```

!!! question

    Wie viele Stationen sind in der Stationsliste aufgeführt?

??? success "Klicken Sie, um die Antwort anzuzeigen"

    Es gibt 1 Station, die station_list.csv enthält eine Zeile mit Stationsmetadaten.

!!! question
    Versuchen Sie, `message.txt` in das BUFR-Format zu konvertieren.

??? success "Klicken Sie, um die Antwort anzuzeigen"

    Um die SYNOP-Nachricht in das BUFR-Format zu konvertieren, verwenden Sie den folgenden Befehl:

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

!!! tip

    Siehe den Abschnitt [synop2bufr-Grundlagen](#synop2bufr-grundlagen).

Untersuchen Sie die resultierenden BUFR-Daten mit `bufr_dump`.

!!! question
     Finden Sie heraus, wie Sie die Breiten- und Längengradwerte mit denen in der Stationsliste vergleichen können.

??? success "Klicken Sie, um die Antwort anzuzeigen"

    Um die Breiten- und Längengradwerte in den BUFR-Daten mit denen in der Stationsliste zu vergleichen, verwenden Sie den folgenden Befehl:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15015_20240921T120000.bufr4 | egrep -i 'latitude|longitude'
    ```

    Dies zeigt die Breiten- und Längengradwerte in den BUFR-Daten an.

!!! tip

    Siehe den Abschnitt [ecCodes-Grundlagen](#eccodes-grundlagen).

### Übung 2
Navigieren Sie zum Verzeichnis `exercise-materials/synop2bufr-exercises/ex_2` und untersuchen Sie die SYNOP-Nachrichtendatei message.txt:

```bash
cd /root/synop2bufr-exercises/ex_2
more message.txt
```

!!! question

    Wie viele SYNOP-Berichte sind in dieser Datei enthalten?

??? success "Klicken Sie, um die Antwort anzuzeigen"

    Es gibt 3 SYNOP-Berichte, da es 3 Trennzeichen (=) am Ende der Nachricht gibt.

Untersuchen Sie die Stationsliste:

```bash
more station_list.csv
```

!!! question

    Wie viele Stationen sind in der Stationsliste aufgeführt?

??? success "Klicken Sie, um die Antwort anzuzeigen"

    Es gibt 3 Stationen, die station_list.csv enthält drei Zeilen mit Stationsmetadaten.

!!! question
    Konvertieren Sie `message.txt` in das BUFR-Format.

??? success "Klicken Sie, um die Antwort anzuzeigen"

    Um die SYNOP-Nachricht in das BUFR-Format zu konvertieren, verwenden Sie den folgenden Befehl:

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

!!! question

    Wie würden Sie basierend auf den Ergebnissen der Übungen in dieser und der vorherigen Übung die Anzahl der
    resultierenden BUFR-Dateien anhand der Anzahl der SYNOP-Berichte und der in der Stationsmetadatendatei aufgeführten Stationen vorhersagen?

??? success "Klicken Sie, um die Antwort anzuzeigen"

    Um die erzeugten BUFR-Dateien zu sehen, führen Sie den folgenden Befehl aus:

    ```bash
    ls -l *.bufr4
    ```

    Die Anzahl der erzeugten BUFR-Dateien entspricht der Anzahl der SYNOP-Berichte in der Nachrichtendatei.

Untersuchen Sie die resultierenden BUFR-Daten mit `bufr_dump`.

!!! question
    Wie können Sie die in den BUFR-Daten jeder erzeugten Datei kodierte WIGOS-Stations-ID überprüfen?

??? success "Klicken Sie, um die Antwort anzuzeigen"

    Dies kann mit den folgenden Befehlen erfolgen:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15015_20240921T120000.bufr4 | egrep -i 'wigos'
    ```

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15020_20240921T120000.bufr4 | egrep -i 'wigos'
    ```

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15090_20240921T120000.bufr4 | egrep -i 'wigos'
    ```

    Beachten Sie, dass Sie, wenn Sie ein Verzeichnis mit nur diesen 3 BUFR-Dateien haben, Linux-Platzhalter wie folgt verwenden können:

    ```bash
    bufr_dump -p *.bufr4 | egrep -i 'wigos'
    ```

### Übung 3
Navigieren Sie zum Verzeichnis `exercise-materials/synop2bufr-exercises/ex_3` und untersuchen Sie die SYNOP-Nachrichtendatei message.txt:

```bash
cd /root/synop2bufr-exercises/ex_3
more message.txt
```

Diese SYNOP-Nachricht enthält nur einen längeren Bericht mit mehr Abschnitten.

Untersuchen Sie die Stationsliste:

```bash
more station_list.csv
```

!!! question

    Ist es problematisch, dass diese Datei mehr Stationen enthält als Berichte in der SYNOP-Nachricht?

??? success "Klicken Sie, um die Antwort anzuzeigen"

    Nein, das ist kein Problem, solange es in der Stationslistendatei eine Zeile mit einer Stations-TSI gibt, die mit der des SYNOP-Berichts übereinstimmt, den wir konvertieren möchten.

!!! note

    Die Stationslistendatei ist eine Metadatenquelle für `synop2bufr`, um die Informationen bereitzustellen, die im alphanumerischen SYNOP-Bericht fehlen und im BUFR SYNOP erforderlich sind.

!!! question
    Konvertieren Sie `message.txt` in das BUFR-Format.

??? success "Klicken Sie, um die Antwort anzuzeigen"

    Dies erfolgt mit dem Befehl `transform`, zum Beispiel:

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

Untersuchen Sie die resultierenden BUFR-Daten mit `bufr_dump`.

!!! question

    Finden Sie die folgenden Variablen:

    - Lufttemperatur (K) des Berichts
    - Gesamtbewölkung (%) des Berichts
    - Gesamtdauer des Sonnenscheins (Minuten) des Berichts
    - Windgeschwindigkeit (m/s) des Berichts

??? success "Klicken Sie, um die Antwort anzuzeigen"

    Um die Variablen nach Schlüsselwort in den BUFR-Daten zu finden, können Sie die folgenden Befehle verwenden:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15260_20240921T115500.bufr4 | egrep -i 'temperature'
    ```

    Sie können den folgenden Befehl verwenden, um nach mehreren Schlüsselwörtern zu suchen:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15260_20240921T115500.bufr4 | egrep -i 'temperature|cover|sunshine|wind'
    ```

!!! tip

    Der letzte Befehl im Abschnitt [ecCodes-Grundlagen](#eccodes-grundlagen) könnte nützlich sein.


### Übung 4
Navigieren Sie zum Verzeichnis `exercise-materials/synop2bufr-exercises/ex_4` und untersuchen Sie die SYNOP-Nachrichtendatei message.txt:

```bash
cd /root/synop2bufr-exercises/ex_4
more message_incorrect.txt
```

!!!