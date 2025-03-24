# Konvertierung von SYNOP-Daten zu BUFR mit der wis2box-Webapp

!!! abstract "Lernziele"
    Am Ende dieser praktischen Sitzung werden Sie in der Lage sein:

    - gültige FM-12 SYNOP-Bulletins über die wis2box-Webanwendung zur Konvertierung in BUFR und zum Austausch über das WIS2.0 einzureichen
    - einfache Kodierungsfehler in einem FM-12 SYNOP-Bulletin vor der Formatkonvertierung und dem Austausch zu validieren, zu diagnostizieren und zu beheben
    - sicherzustellen, dass die erforderlichen Stationsmetadaten in der wis2box verfügbar sind
    - erfolgreich konvertierte Bulletins zu bestätigen und zu inspizieren

## Einführung

Um manuellen Beobachtern die direkte Übermittlung von Daten an das WIS2.0 zu ermöglichen, bietet die wis2box-Webapp ein Formular zur Konvertierung von FM-12 SYNOP-Bulletins in BUFR. Das Formular ermöglicht es Benutzern auch, einfache Kodierungsfehler im FM-12 SYNOP-Bulletin vor der Formatkonvertierung und dem Austausch zu diagnostizieren und zu beheben sowie die resultierenden BUFR-Daten zu inspizieren.

## Vorbereitung

!!! warning "Voraussetzungen"

    - Stellen Sie sicher, dass Ihre wis2box konfiguriert und gestartet wurde.
    - Öffnen Sie ein Terminal und verbinden Sie sich über SSH mit Ihrer Student-VM.
    - Verbinden Sie sich mit dem MQTT-Broker Ihrer wis2box-Instanz über MQTT Explorer.
    - Öffnen Sie die wis2box-Webanwendung (``http://<Ihr-Host-Name>/wis2box-webapp``) und stellen Sie sicher, dass Sie angemeldet sind.

## Verwendung der wis2box-Webapp zur Konvertierung von FM-12 SYNOP zu BUFR

### Übung 1 - Verwendung der wis2box-Webapp zur Konvertierung von FM-12 SYNOP zu BUFR

Stellen Sie sicher, dass Sie das Auth-Token für "processes/wis2box" haben, das Sie in der vorherigen Übung generiert haben, und dass Sie mit Ihrem wis2box-Broker in MQTT Explorer verbunden sind.

Kopieren Sie die folgende Nachricht:
    
``` {.copy}
AAXX 27031
15015 02999 02501 10103 21090 39765 42952 57020 60001=
``` 

Öffnen Sie die wis2box-Webanwendung und navigieren Sie zur synop2bufr-Seite über die linke Navigationsleiste und fahren Sie wie folgt fort:

- Fügen Sie den kopierten Inhalt in das Texteingabefeld ein.
- Wählen Sie Monat und Jahr über den Datumsauswähler, nehmen Sie für diese Übung den aktuellen Monat an.
- Wählen Sie ein Thema aus dem Dropdown-Menü (die Optionen basieren auf den in der wis2box konfigurierten Datensätzen).
- Geben Sie das "processes/wis2box" Auth-Token ein, das Sie zuvor generiert haben
- Stellen Sie sicher, dass "Publish on WIS2" eingeschaltet ist
- Klicken Sie auf "SUBMIT"

<center><img alt="Dialog showing synop2bufr page, including toggle button" src="../../assets/img/synop2bufr-toggle.png"></center>

Klicken Sie auf Absenden. Sie erhalten eine Warnmeldung, da die Station nicht in der wis2box registriert ist. Gehen Sie zum Station-Editor und importieren Sie die folgende Station:

``` {.copy}
0-20000-0-15015
```

Stellen Sie sicher, dass die Station mit dem Thema verknüpft ist, das Sie im vorherigen Schritt ausgewählt haben, und kehren Sie dann zur synop2bufr-Seite zurück und wiederholen Sie den Vorgang mit denselben Daten wie zuvor.

!!! question
    Wie können Sie das Ergebnis der Konvertierung von FM-12 SYNOP zu BUFR sehen?

??? success "Klicken Sie, um die Antwort anzuzeigen"
    Der Ergebnisbereich der Seite zeigt Warnungen, Fehler und Output-BUFR-Dateien an.

    Klicken Sie auf "Output BUFR files", um eine Liste der generierten Dateien zu sehen. Sie sollten eine Datei aufgelistet sehen.

    Mit der Download-Schaltfläche können die BUFR-Daten direkt auf Ihren Computer heruntergeladen werden.

    Die Inspect-Schaltfläche führt einen Prozess aus, um die Daten aus BUFR zu konvertieren und zu extrahieren.

    <center><img alt="Dialog showing result of successfully submitting a message"
         src="../../assets/img/synop2bufr-ex2-success.png"></center>

!!! question
    Die FM-12 SYNOP-Eingabedaten enthielten nicht den Standort der Station, die Höhe oder die Barometerhöhe. 
    Bestätigen Sie, dass diese in den BUFR-Ausgabedaten enthalten sind. Woher stammen diese?

??? success "Klicken Sie, um die Antwort anzuzeigen"
    Wenn Sie auf die Schaltfläche "Inspect" klicken, sollte ein Dialog wie unten gezeigt erscheinen.

    <center><img alt="Results of the inspect button showing the basic station metadata, the station location and the observed properties"
         src="../../assets/img/synop2bufr-ex2.png"></center>

    Dies umfasst den auf einer Karte angezeigten Standort der Station und grundlegende Metadaten sowie die Beobachtungen in der Nachricht.
    
    Als Teil der Transformation von FM-12 SYNOP zu BUFR wurden der BUFR-Datei zusätzliche Metadaten hinzugefügt.
    
    Die BUFR-Datei kann auch durch Herunterladen der Datei und Validieren mit einem Tool wie dem ECMWF ecCodes BUFR-Validator inspiziert werden.

Gehen Sie zu MQTT Explorer und überprüfen Sie das WIS2-Benachrichtigungsthema, um die veröffentlichten WIS2-Benachrichtigungen zu sehen.

### Übung 2 - Verständnis der Stationsliste

Für diese nächste Übung werden Sie eine Datei mit mehreren Berichten konvertieren, siehe die Daten unten:

``` {.copy}
AAXX 27031
15015 02999 02501 10103 21090 39765 42952 57020 60001=
15020 02997 23104 10130 21075 30177 40377 58020 60001 81041=
15090 02997 53102 10139 21075 30271 40364 58031 60001 82046=
```

!!! question
    Basierend auf der vorherigen Übung, schauen Sie sich die FM-12 SYNOP-Nachricht an und prognostizieren Sie, wie viele BUFR-Ausgabenachrichten generiert werden. 
    
    Kopieren Sie nun diese Nachricht in das SYNOP-Formular und senden Sie die Daten ab.

    Entsprach die Anzahl der generierten Nachrichten Ihrer Erwartung und wenn nicht, warum nicht?

??? warning "Klicken Sie, um die Antwort anzuzeigen"
    
    Sie hätten erwarten können, dass drei BUFR-Nachrichten generiert werden, eine für jeden Wetterbericht. Stattdessen haben Sie jedoch 2 Warnungen und nur eine BUFR-Datei erhalten.
    
    Damit ein Wetterbericht in BUFR konvertiert werden kann, sind die in der Stationsliste enthaltenen grundlegenden Metadaten erforderlich. Obwohl das obige Beispiel drei Wetterberichte enthält, waren zwei der drei meldenden Stationen nicht in Ihrer wis2box registriert. 
    
    Infolgedessen führte nur einer der drei Wetterberichte zur Generierung einer BUFR-Datei und zur Veröffentlichung einer WIS2-Benachrichtigung. Die anderen beiden Wetterberichte wurden ignoriert und es wurden Warnungen generiert.

!!! hint
    Beachten Sie die Beziehung zwischen der WIGOS-Kennung und der traditionellen Stationskennung, die in der BUFR-Ausgabe enthalten ist. In vielen Fällen wird für Stationen, die zum Zeitpunkt der Migration zu WIGOS-Stationskennungen in WMO-Nr. 9 Band A aufgeführt sind, die WIGOS-Stationskennung durch die traditionelle Stationskennung mit vorangestelltem ``0-20000-0`` angegeben, z.B. aus ``15015`` wurde ``0-20000-0-15015``.

Importieren Sie über die Stationslistenseite die folgenden Stationen:

``` {.copy}
0-20000-0-15020
0-20000-0-15090
```

Stellen Sie sicher, dass die Stationen mit dem Thema verknüpft sind, das Sie in der vorherigen Übung ausgewählt haben, und kehren Sie dann zur synop2bufr-Seite zurück und wiederholen Sie den Vorgang.

Jetzt sollten drei BUFR-Dateien generiert werden und es sollten keine Warnungen oder Fehler in der Webanwendung aufgelistet sein.

Zusätzlich zu den grundlegenden Stationsinformationen werden weitere Metadaten wie die Stationshöhe über dem Meeresspiegel und die Barometerhöhe über dem Meeresspiegel für die Kodierung in BUFR benötigt. Die Felder sind in den Seiten der Stationsliste und des Stationseditors enthalten.
    
### Übung 3 - Debugging

In dieser letzten Übung werden Sie zwei der häufigsten Probleme identifizieren und korrigieren, die bei der Verwendung dieses Tools zur Konvertierung von FM-12 SYNOP zu BUFR auftreten.

Beispieldaten werden im Feld unten angezeigt. Untersuchen Sie die Daten und versuchen Sie, alle möglichen Probleme zu lösen, bevor Sie die Daten über die Webanwendung einreichen.

!!! hint
    Sie können die Daten im Eingabefeld auf der Webapplikationsseite bearbeiten. Wenn Sie Probleme übersehen, sollten diese erkannt und als Warnung oder Fehler hervorgehoben werden, sobald die Schaltfläche "Absenden" angeklickt wurde.

``` {.copy}
AAXX 27031
15015 02999 02501 10103 21090 39765 42952 57020 60001
15020 02997 23104 10130 21075 30177 40377 58020 60001 81041=
15090 02997 53102 10139 21075 30271 40364 58031 60001 82046=
```

!!! question
    Mit welchen Problemen haben Sie bei der Konvertierung der Daten in BUFR gerechnet und wie haben Sie diese überwunden? Gab es Probleme, mit denen Sie nicht gerechnet haben?

??? success "Klicken Sie, um die Antwort anzuzeigen"
    In diesem ersten Beispiel fehlt das "Ende des Textes"-Symbol (=) oder Datensatztrennzeichen zwischen dem ersten und zweiten Wetterbericht. Folglich werden die Zeilen 2 und 3 als ein einziger Bericht behandelt, was zu Fehlern bei der Analyse der Nachricht führt.

Das zweite Beispiel unten enthält mehrere häufige Probleme, die in FM-12 SYNOP-Berichten zu finden sind. Untersuchen Sie die Daten und versuchen Sie, die Probleme zu identifizieren, und reichen Sie dann die korrigierten Daten über die Webanwendung ein.

```{.copy}
AAXX 27031
15020 02997 23104 10/30 21075 30177 40377 580200 60001 81041=
```

!!! question
    Welche Probleme haben Sie gefunden und wie haben Sie diese gelöst?

??? success "Klicken Sie, um die Antwort anzuzeigen"
    Es gibt zwei Probleme im Wetterbericht.
    
    Das erste Problem in der Gruppe der vorzeichenbehafteten Lufttemperatur hat das Zehnerzeichen auf fehlend (/) gesetzt, was zu einer ungültigen Gruppe führt. In diesem Beispiel wissen wir, dass die Temperatur 13,0 Grad Celsius beträgt (aus den obigen Beispielen), so dass dieses Problem korrigiert werden kann. Im operativen Betrieb müsste der korrekte Wert mit dem Beobachter bestätigt werden.

    Das zweite Problem tritt in Gruppe 5 auf, wo ein zusätzliches Zeichen vorhanden ist, wobei das letzte Zeichen dupliziert ist. Dieses Problem kann durch Entfernen des zusätzlichen Zeichens behoben werden.

## Aufräumen

Während der Übungen in dieser Sitzung haben Sie mehrere Dateien in Ihre Stationsliste importiert. Navigieren Sie zur Stationslistenseite und klicken Sie auf die Papierkorbsymbole, um die Stationen zu löschen. Möglicherweise müssen Sie die Seite aktualisieren, damit die Stationen nach dem Löschen aus der Liste entfernt werden.

<center><img alt="Station metadata viewer"
         src="../../assets/img/synop2bufr-trash.png" width="600"></center>

## Fazit

!!! success "Herzlichen Glückwunsch!"

    In dieser praktischen Sitzung haben Sie gelernt:

    - wie das synop2bufr-Tool zur Konvertierung von FM-12 SYNOP-Berichten in BUFR verwendet werden kann;
    - wie man einen FM-12 SYNOP-Bericht über die Web-App einreicht;
    - wie man einfache Fehler in einem FM-12 SYNOP-Bericht diagnostiziert und korrigiert;
    - die Bedeutung der Registrierung von Stationen in der wis2box (und OSCAR/Surface);
    - und die Verwendung der Inspect-Schaltfläche zur Anzeige des Inhalts von BUFR-Daten.