Hier ist die deutsche Übersetzung des Markdown-Inhalts:

---
title: Startseite
---

<img alt="WMO Logo" src="assets/img/wmo-logo.png" width="200">
# WIS2 in a box Training

WIS2 in a box ([wis2box](https://docs.wis2box.wis.wmo.int)) ist eine freie und quelloffene (FOSS) Referenzimplementierung eines WMO WIS2-Knotens. Das Projekt bietet ein Plug-and-Play-Toolset zum Erfassen, Verarbeiten und Veröffentlichen von Wetter-/Klima-/Wasserdaten unter Verwendung standardbasierter Ansätze in Übereinstimmung mit den WIS2-Prinzipien. wis2box bietet auch Zugang zu allen Daten im WIS2-Netzwerk. wis2box ist so konzipiert, dass es für Datenanbieter eine niedrige Einstiegshürde darstellt und ermöglicht Infrastruktur und Dienste für Datensuche, -zugriff und -visualisierung.

Dieses Training bietet schrittweise Erklärungen zu verschiedenen Aspekten des wis2box-Projekts sowie eine Reihe von Übungen, die Ihnen helfen, Daten in WIS2 zu veröffentlichen und herunterzuladen. Das Training wird in Form von Überblickspräsentationen sowie praktischen Übungen angeboten.

Die Teilnehmer können mit Beispieldaten und -metadaten arbeiten sowie ihre eigenen Daten und Metadaten integrieren.

Dieses Training deckt ein breites Spektrum an Themen ab (Installation/Einrichtung/Konfiguration, Veröffentlichung/Herunterladen von Daten usw.).

## Ziele und Lernergebnisse

Die Ziele dieses Trainings sind, sich mit Folgendem vertraut zu machen:

- Kernkonzepte und Komponenten der WIS2-Architektur
- Daten- und Metadatenformate, die in WIS2 für Suche und Zugriff verwendet werden
- wis2box-Architektur und -Umgebung
- wis2box-Kernfunktionen:
    - Metadatenverwaltung
    - Datenerfassung und Umwandlung in das BUFR-Format
    - MQTT-Broker für die Veröffentlichung von WIS2-Nachrichten
    - HTTP-Endpunkt für den Datendownload
    - API-Endpunkt für programmatischen Zugriff auf Daten

## Navigation

Die linke Navigation bietet ein Inhaltsverzeichnis für das gesamte Training.

Die rechte Navigation bietet ein Inhaltsverzeichnis für eine bestimmte Seite.

## Voraussetzungen

### Wissen

- Grundlegende Linux-Befehle (siehe [Spickzettel](cheatsheets/linux.md))
- Grundkenntnisse in Netzwerken und Internetprotokollen

### Software

Für dieses Training werden folgende Tools benötigt:

- Eine Instanz mit Ubuntu-Betriebssystem (wird von WMO-Trainern während lokaler Trainingseinheiten bereitgestellt), siehe [Zugriff auf Ihre Studenten-VM](practical-sessions/accessing-your-student-vm.md#introduction)
- SSH-Client für den Zugriff auf Ihre Instanz
- MQTT Explorer auf Ihrem lokalen Computer
- SCP- und FTP-Client zum Kopieren von Dateien von Ihrem lokalen Computer

## Konventionen

!!! question

    Ein so markierter Abschnitt fordert Sie auf, eine Frage zu beantworten.

Außerdem werden Sie im Text Tipps und Hinweise finden:

!!! tip

    Tipps helfen Ihnen dabei, Aufgaben am besten zu erledigen.

!!! note

    Hinweise bieten zusätzliche Informationen zum Thema der praktischen Sitzung sowie dazu, wie Aufgaben am besten erledigt werden können.

Beispiele werden wie folgt dargestellt:

Konfiguration
``` {.yaml linenums="1"}
my-collection-defined-in-yaml:
    type: collection
    title: my title defined as a yaml attribute named title
    description: my description as a yaml attribute named description
```

Snippets, die in einem Terminal/einer Konsole eingegeben werden müssen, werden wie folgt dargestellt:

```bash
echo 'Hello world'
```

Container-Namen (laufende Images) werden in **Fettdruck** dargestellt.

## Trainingsort und -materialien

Die Trainingsinhalte, das Wiki und der Issue-Tracker werden auf GitHub unter [https://github.com/wmo-im/wis2box-training](https://github.com/wmo-im/wis2box-training) verwaltet.

## Drucken des Materials

Dieses Training kann als PDF exportiert werden. Um dieses Trainingsmaterial zu speichern oder zu drucken, gehen Sie zur [Druckseite](print_page) und wählen Sie Datei > Drucken > Als PDF speichern.

## Übungsmaterialien

Übungsmaterialien können aus der [exercise-materials.zip](/exercise-materials.zip) Zip-Datei heruntergeladen werden.

## Unterstützung

Für Probleme/Fehler/Vorschläge oder Verbesserungen/Beiträge zu diesem Training nutzen Sie bitte den [GitHub Issue Tracker](https://github.com/wmo-im/wis2box-training/issues).

Alle wis2box-Fehler, Verbesserungen und Probleme können auf [GitHub](https://github.com/wmo-im/wis2box/issues) gemeldet werden.

Für zusätzliche Unterstützung oder Fragen kontaktieren Sie bitte wis2-support@wmo.int.

Wie immer ist die wis2box-Kerndokumentation unter [https://docs.wis2box.wis.wmo.int](https://docs.wis2box.wis.wmo.int) zu finden.

Beiträge sind immer willkommen und werden gefördert!