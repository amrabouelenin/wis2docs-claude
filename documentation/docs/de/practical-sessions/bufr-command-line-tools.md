# Arbeiten mit BUFR-Daten

!!! abstract "Lernziele"
    In dieser praktischen Übung werden Sie in einige der BUFR-Tools eingeführt, die im **wis2box-api**-Container enthalten sind und zur Umwandlung von Daten in das BUFR-Format sowie zum Lesen der in BUFR codierten Inhalte verwendet werden.
    
    Sie werden lernen:

    - wie man die Header in der BUFR-Datei mit dem Befehl `bufr_ls` untersucht
    - wie man die Daten in einer BUFR-Datei mit `bufr_dump` extrahiert und untersucht
    - die grundlegende Struktur der BUFR-Templates, die in csv2bufr verwendet werden, und wie man das Kommandozeilentool benutzt
    - und wie man grundlegende Änderungen an den BUFR-Templates vornimmt und wie man die wis2box aktualisiert, um die überarbeitete Version zu verwenden

## Einführung

Die Plugins, die Benachrichtigungen mit BUFR-Daten erzeugen, verwenden Prozesse in der wis2box-api, um mit BUFR-Daten zu arbeiten, zum Beispiel um die Daten von CSV nach BUFR oder von BUFR nach GeoJSON zu transformieren.

Der wis2box-api-Container enthält eine Reihe von Tools für die Arbeit mit BUFR-Daten.

Dazu gehören die von ECMWF entwickelten und in der ecCodes-Software enthaltenen Tools. Weitere Informationen dazu finden Sie auf der [ecCodes-Website](https://confluence.ecmwf.int/display/ECC/BUFR+tools).

In dieser Sitzung werden Sie in die Tools `bufr_ls` und `bufr_dump` aus dem ecCodes-Softwarepaket sowie in die erweiterte Konfiguration des csv2bufr-Tools eingeführt.

## Vorbereitung

Um die BUFR-Kommandozeilentools zu nutzen, müssen Sie im wis2box-api-Container angemeldet sein, und sofern nicht anders angegeben, sollten alle Befehle in diesem Container ausgeführt werden. Sie benötigen auch den MQTT Explorer, der mit Ihrem Broker verbunden ist.

Verbinden Sie sich zunächst über Ihren SSH-Client mit Ihrer Student-VM und melden Sie sich dann im wis2box-api-Container an:

```{.copy}
cd ~/wis2box-1.0.0rc1
python3 wis2box-ctl.py login wis2box-api
```

Bestätigen Sie, dass die Tools verfügbar sind, beginnend mit ecCodes:

``` {.copy}
bufr_dump -V
```
Sie sollten folgende Antwort erhalten:

```
ecCodes Version 2.28.0
```

Überprüfen Sie als Nächstes csv2bufr:

```{.copy}
csv2bufr --version
```

Sie sollten folgende Antwort erhalten:

```
csv2bufr, version 0.7.4
```

Erstellen Sie schließlich ein Arbeitsverzeichnis:

```{.copy}
cd /data/wis2box
mkdir -p working/bufr-cli
cd working/bufr-cli
```

Sie sind jetzt bereit, die BUFR-Tools zu verwenden.


## Verwendung der BUFR-Kommandozeilentools

### Übung 1 - bufr_ls
In dieser ersten Übung verwenden Sie den Befehl `bufr_ls`, um die Header einer BUFR-Datei zu untersuchen und den Inhalt der Datei zu bestimmen. Die folgenden Header sind in einer BUFR-Datei enthalten:

| Header                            | ecCodes-Schlüssel             | Beschreibung                                                                                                                                           |
|-----------------------------------|------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| originating/generating centre     | centre                       | Das Ursprungs-/Erzeugungszentrum für die Daten                                                                                                      |
| originating/generating sub-centre | bufrHeaderSubCentre          | Das Ursprungs-/Erzeugungsunterzentrum für die Daten                                                                                                  | 
| Update sequence number            | updateSequenceNumber         | Ob dies die erste Version der Daten (0) oder ein Update (>0) ist                                                                                   |               
| Data category                     | dataCategory                 | Die Art der in der BUFR-Nachricht enthaltenen Daten, z.B. Oberflächendaten. Siehe [BUFR-Tabelle A](https://github.com/wmo-im/BUFR4/blob/master/BUFR_TableA_en.csv)  |
| International data sub-category   | internationalDataSubCategory | Die Unterkategorie der in der BUFR-Nachricht enthaltenen Daten. Siehe [Common Code Table C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv) |
| Year                              | typicalYear (typicalDate)    | Typischste Zeit für den BUFR-Nachrichteninhalt                                                                                                       |
| Month                             | typicalMonth (typicalDate)   | Typischste Zeit für den BUFR-Nachrichteninhalt                                                                                                       |
| Day                               | typicalDay (typicalDate)     | Typischste Zeit für den BUFR-Nachrichteninhalt                                                                                                       |
| Hour                              | typicalHour (typicalTime)    | Typischste Zeit für den BUFR-Nachrichteninhalt                                                                                                       |
| Minute                            | typicalMinute (typicalTime)  | Typischste Zeit für den BUFR-Nachrichteninhalt                                                                                                       |
| BUFR descriptors                  | unexpandedDescriptors        | Liste von einem oder mehreren BUFR-Deskriptoren, die die in der Datei enthaltenen Daten definieren                                                                        |

Laden Sie die Beispieldatei direkt in den wis2box-management-Container mit folgendem Befehl herunter:

``` {.copy}
curl https://training.wis2box.wis.wmo.int/sample-data/bufr-cli-ex1.bufr4 --output bufr-cli-ex1.bufr4
```

Verwenden Sie nun den folgenden Befehl, um `bufr_ls` für diese Datei auszuführen:

```bash
bufr_ls bufr-cli-ex1.bufr4
```

Sie sollten folgende Ausgabe sehen:

```bash
bufr-cli-ex1.bufr4
centre                     masterTablesVersionNumber  localTablesVersionNumber   typicalDate                typicalTime                numberOfSubsets
cnmc                       29                         0                          20231002                   000000                     1
1 of 1 messages in bufr-cli-ex1.bufr4

1 of 1 total messages in 1 files
```

Für sich genommen sind diese Informationen nicht sehr aussagekräftig, da nur begrenzte Informationen zum Dateiinhalt bereitgestellt werden.

Die Standardausgabe liefert keine Informationen über den Beobachtungs- oder Datentyp und ist in einem Format, das nicht sehr leicht zu lesen ist. Es können jedoch verschiedene Optionen an `bufr_ls` übergeben werden, um sowohl das Format als auch die ausgegebenen Header-Felder zu ändern.

Verwenden Sie `bufr_ls` ohne Argumente, um die Optionen anzuzeigen:

```{.copy}
bufr_ls
```

Sie sollten folgende Ausgabe sehen:

```
NAME    bufr_ls

DESCRIPTION
        List content of BUFR files printing values of some header keys.
        Only scalar keys can be printed.
        It does not fail when a key is not found.

USAGE
        bufr_ls [options] bufr_file bufr_file ...

OPTIONS
        -p key[:{s|d|i}],key[:{s|d|i}],...
                Declaration of keys to print.
                For each key a string (key:s), a double (key:d) or an integer (key:i)
                type can be requested. Default type is string.
        -F format
                C style format for floating-point values.
        -P key[:{s|d|i}],key[:{s|d|i}],...
                As -p adding the declared keys to the default list.
        -w key[:{s|d|i}]{=|!=}value,key[:{s|d|i}]{=|!=}value,...
                Where clause.
                Messages are processed only if they match all the key/value constraints.
                A valid constraint is of type key=value or key!=value.
                For each key a string (key:s), a double (key:d) or an integer (key:i)
                type can be specified. Default type is string.
                In the value you can also use the forward-slash character '/' to specify an OR condition (i.e. a logical disjunction)
                Note: only one -w clause is allowed.
        -j      JSON output
        -s key[:{s|d|i}]=value,key[:{s|d|i}]=value,...
                Key/values to set.
                For each key a string (key:s), a double (key:d) or an integer (key:i)
                type can be defined. By default the native type is set.
        -n namespace
                All the keys belonging to the given namespace are printed.
        -m      Mars keys are printed.
        -V      Version.
        -W width
                Minimum width of each column in output. Default is 10.
        -g      Copy GTS header.
        -7      Does not fail when the message has wrong length

SEE ALSO
        Full documentation and examples at:
        <https://confluence.ecmwf.int/display/ECC/bufr_ls>
```

Führen Sie nun denselben Befehl für die Beispieldatei aus, aber geben Sie die Informationen im JSON-Format aus.

!!! question
    Welches Flag übergeben Sie an den Befehl `bufr_ls`, um die Ausgabe im JSON-Format anzuzeigen?

??? success "Klicken Sie, um die Antwort anzuzeigen"
    Sie können das Ausgabeformat mit dem Flag `-j` auf JSON ändern, d.h.
    `bufr_ls -j <input-file>`. Dies kann lesbarer sein als das Standardausgabeformat. Siehe das Beispiel unten:

    ```
    { "messages" : [
      {
        "centre": "cnmc",
        "masterTablesVersionNumber": 29,
        "localTablesVersionNumber": 0,
        "typicalDate": 20231002,
        "typicalTime": "000000",
        "numberOfSubsets": 1
      }
    ]}
    ```

Bei der Untersuchung einer BUFR-Datei möchten wir oft den Datentyp und das typische Datum/die typische Uhrzeit der Daten in der Datei bestimmen. Diese Informationen können mit dem Flag `-p` aufgelistet werden, um die auszugebenden Header auszuwählen. Mehrere Header können durch eine kommagetrennte Liste eingeschlossen werden.

Untersuchen Sie mit dem Befehl `bufr_ls` die Testdatei und identifizieren Sie den Datentyp in der Datei sowie das typische Datum und die typische Uhrzeit für diese Daten.

??? hint
    Die ecCodes-Schlüssel sind in der obigen Tabelle angegeben. Wir können Folgendes verwenden, um die dataCategory und
    internationalDataSubCategory der BUFR-Daten aufzulisten:

    ```
    bufr_ls -p dataCategory,internationalDataSubCategory bufr-cli-ex1.bufr4
    ```

    Bei Bedarf können weitere Schlüssel hinzugefügt werden.

!!! question
    Welche Art von Daten (Datenkategorie und Unterkategorie) sind in der Datei enthalten? Was ist das typische Datum und die typische Uhrzeit für die Daten?

??? success "Klicken Sie, um die Antwort anzuzeigen"
    Der Befehl, den Sie ausführen müssen, sollte ähnlich wie folgt aussehen:
    
    ```
    bufr_ls -p dataCategory,internationalDataSubCategory,typicalDate,typicalTime -j bufr-cli-ex1.bufr4
    ```

    Sie haben möglicherweise zusätzliche Schlüssel oder Jahr, Monat, Tag usw. einzeln aufgelistet. Die Ausgabe sollte
    ähnlich wie unten sein, je nachdem, ob Sie JSON oder die Standardausgabe gewählt haben.

    ```
    { "messages" : [
      {
        "dataCategory": 2,
        "internationalDataSubCategory": 4,
        "typicalDate": 20231002,
        "typicalTime": "000000"
      }
    ]}
    ```

    Daraus sehen wir:

    - Die Datenkategorie ist 2, aus [BUFR-Tabelle A](https://github.com/wmo-im/BUFR4/blob/master/BUFR_TableA_en.csv)
      können wir sehen, dass diese Datei "Vertikale Sondierungen (außer Satellit)" enthält.
    - Die internationale Unterkategorie ist 4, was auf 
      "Temperatur-/Feuchtigkeits-/Windmeldungen aus der oberen Atmosphäre von festen Landstationen (TEMP)" hinweist. Diese Information kann in
      [Common Code Table C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv) (Zeile 33) nachgeschlagen werden. Beachten Sie die Kombination
      von Kategorie und Unterkategorie.
    - Das typische Datum und die typische Uhrzeit sind 2023/10/02 und 00:00:00z.

    

### Übung 2 - bufr_dump

Der Befehl `bufr_dump` kann verwendet werden, um den Inhalt einer BUFR-Datei, einschließlich der Daten selbst, aufzulisten und zu untersuchen.

In dieser Übung verwenden wir eine BUFR-Datei, die der entspricht, die Sie während der ersten csv2bufr-Übungssitzung mit der wis2box-Webapp erstellt haben.

Laden Sie die Beispieldatei direkt mit folgendem Befehl in den wis2box-Management-Container herunter:

``` {.copy}
curl https://training.wis2box.wis.wmo.int/sample-data/bufr-cli-ex2.bufr4 --output bufr-cli-ex2.bufr4
```

Führen Sie nun den Befehl `bufr_dump` für die Datei aus und verwenden Sie das Flag `-p`, um die Daten im Klartext (key=value-Format) auszugeben:

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4
```

Sie sollten etwa 240 Schlüssel sehen, von denen viele fehlen. Dies ist typisch für reale Daten, da nicht alle eccodes-Schlüssel mit gemeldeten Daten gefüllt sind.

!!! hint
    Die fehlenden W