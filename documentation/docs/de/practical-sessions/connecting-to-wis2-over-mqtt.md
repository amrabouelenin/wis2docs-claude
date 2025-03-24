# Verbindung zu WIS2 über MQTT

!!! abstract "Lernziele"

    Am Ende dieser praktischen Sitzung werden Sie in der Lage sein:

    - sich mit dem WIS2 Global Broker über MQTT Explorer zu verbinden
    - die WIS2-Themenstruktur zu überprüfen
    - die Struktur der WIS2-Benachrichtigungsnachrichten zu überprüfen

## Einführung

WIS2 verwendet das MQTT-Protokoll, um die Verfügbarkeit von Wetter-/Klima-/Wasserdaten bekannt zu geben. Der WIS2 Global Broker abonniert alle WIS2-Knoten im Netzwerk und veröffentlicht die empfangenen Nachrichten erneut. Der Global Cache abonniert den Global Broker, lädt die Daten in der Nachricht herunter und veröffentlicht die Nachricht dann erneut im `cache`-Thema mit einer neuen URL. Der Global Discovery Catalogue veröffentlicht Erkennungsmetadaten vom Broker und bietet eine Such-API.

Dies ist ein Beispiel für die Struktur einer WIS2-Benachrichtigungsnachricht, die zum Thema `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop` empfangen wurde:

```json
{
  "id": "59f9b013-c4b3-410a-a52d-fff18f3f1b47",
  "type": "Feature",
  "version": "v04",
  "geometry": {
    "coordinates": [
      -38.69389,
      -17.96472,
      60
    ],
    "type": "Point"
  },
  "properties": {
    "data_id": "br-inmet/data/core/weather/surface-based-observations/synop/WIGOS_0-76-2-2900801000W83499_20240815T060000",
    "datetime": "2024-08-15T06:00:00Z",
    "pubtime": "2024-08-15T09:52:02Z",
    "integrity": {
      "method": "sha512",
      "value": "TBuWycx/G0lIiTo47eFPBViGutxcIyk7eikppAKPc4aHgOmTIS5Wb9+0v3awMOyCgwpFhTruRRCVReMQMp5kYw=="
    },
    "content": {
      "encoding": "base64",
      "value": "QlVGUgAA+gQAABYAACsAAAAAAAIAHAAH6AgPBgAAAAALAAABgMGWx1AAAM0ABOIAAAODM0OTkAAAAAAAAAAAAAAKb5oKEpJ6YkJ6mAAAAAAAAAAAAAAAAv0QeYA29WQa87ZhH4CQP//z+P//BD////+ASznXuUb///8MgAS3/////8X///e+AP////AB/+R/yf////////////////////6/1/79H/3///gEt////////4BLP6QAf/+/pAB//4H0YJ/YeAh/f2///7TH/////9+j//f///////////////////v0f//////////////////////wNzc3Nw==",
      "size": 250
    },
    "wigos_station_identifier": "0-76-2-2900801000W83499"
  },
  "links": [
    {
      "rel": "canonical",
      "type": "application/bufr",
      "href": "http://wis2bra.inmet.gov.br/data/2024-08-15/wis/br-inmet/data/core/weather/surface-based-observations/synop/WIGOS_0-76-2-2900801000W83499_20240815T060000.bufr4",
      "length": 250
    }
  ]
}
```

In dieser praktischen Sitzung lernen Sie, wie Sie das MQTT Explorer-Tool verwenden, um eine MQTT-Client-Verbindung zu einem WIS2 Global Broker einzurichten und WIS2-Benachrichtigungsnachrichten anzuzeigen.

MQTT Explorer ist ein nützliches Tool, um die Themenstruktur für einen bestimmten MQTT-Broker zu durchsuchen und zu überprüfen, welche Daten veröffentlicht werden.

Beachten Sie, dass MQTT hauptsächlich für die "Maschine-zu-Maschine"-Kommunikation verwendet wird; das bedeutet, dass normalerweise ein Client die empfangenen Nachrichten automatisch analysieren würde. Um programmatisch mit MQTT zu arbeiten (zum Beispiel in Python), können Sie MQTT-Client-Bibliotheken wie [paho-mqtt](https://pypi.org/project/paho-mqtt) verwenden, um eine Verbindung zu einem MQTT-Broker herzustellen und eingehende Nachrichten zu verarbeiten. Es gibt zahlreiche MQTT-Client- und Server-Software, je nach Ihren Anforderungen und Ihrer technischen Umgebung.

## Verwendung von MQTT Explorer zur Verbindung mit dem Global Broker

Um Nachrichten anzuzeigen, die von einem WIS2 Global Broker veröffentlicht wurden, können Sie "MQTT Explorer" verwenden, der von der [MQTT Explorer-Website](https://mqtt-explorer.com) heruntergeladen werden kann.

Öffnen Sie MQTT Explorer und fügen Sie eine neue Verbindung zum Global Broker hinzu, der von MeteoFrance mit den folgenden Details gehostet wird:

- Host: globalbroker.meteo.fr
- Port: 8883
- Benutzername: everyone
- Passwort: everyone

<img alt="mqtt-explorer-global-broker-connection" src="../../assets/img/mqtt-explorer-global-broker-connection.png" width="800">

Klicken Sie auf die Schaltfläche 'ADVANCED', entfernen Sie die vorkonfigurierten Themen und fügen Sie die folgenden Themen zum Abonnieren hinzu:

- `origin/a/wis2/#`

<img alt="mqtt-explorer-global-broker-advanced" src="../../assets/img/mqtt-explorer-global-broker-sub-origin.png" width="800">

!!! note
    Bei der Einrichtung von MQTT-Abonnements können Sie die folgenden Platzhalter verwenden:

    - **Einstufiger Platzhalter (+)**: Ein einstufiger Platzhalter ersetzt eine Themenebene
    - **Mehrstufiger Platzhalter (#)**: Ein mehrstufiger Platzhalter ersetzt mehrere Themenebenen

    In diesem Fall abonniert `origin/a/wis2/#` alle Themen unter dem Thema `origin/a/wis2`.

Klicken Sie auf 'BACK', dann auf 'SAVE', um Ihre Verbindungs- und Abonnementdetails zu speichern. Klicken Sie dann auf 'CONNECT':

Nachrichten sollten in Ihrer MQTT Explorer-Sitzung wie folgt erscheinen:

<img alt="mqtt-explorer-global-broker-topics" src="../../assets/img/mqtt-explorer-global-broker-msg-origin.png" width="800">

Sie sind jetzt bereit, die WIS2-Themen und die Nachrichtenstruktur zu erkunden.

## Übung 1: Überprüfung der WIS2-Themenstruktur

Verwenden Sie MQTT, um die Themenstruktur unter den `origin`-Themen zu durchsuchen.

!!! question
    
    Wie können wir das WIS-Zentrum unterscheiden, das die Daten veröffentlicht hat?

??? success "Klicken Sie, um die Antwort anzuzeigen"

    Sie können auf der linken Seite im MQTT Explorer klicken, um die Themenstruktur zu erweitern.
    
    Wir können das WIS-Zentrum, das die Daten veröffentlicht hat, anhand der vierten Ebene der Themenstruktur unterscheiden. Zum Beispiel sagt uns das folgende Thema:

    `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`

    dass die Daten von einem WIS-Zentrum mit der Zentren-ID `br-inmet` veröffentlicht wurden, was die Zentren-ID für das Instituto Nacional de Meteorologia - INMET, Brasilien, ist.

!!! question

    Wie können wir zwischen Nachrichten unterscheiden, die von WIS-Zentren mit einem GTS-zu-WIS2-Gateway und Nachrichten, die von WIS-Zentren mit einem WIS2-Knoten veröffentlicht wurden?

??? success "Klicken Sie, um die Antwort anzuzeigen"

    Wir können Nachrichten von einem GTS-zu-WIS2-Gateway anhand der Zentren-ID in der Themenstruktur unterscheiden. Zum Beispiel sagt uns das folgende Thema:

    `origin/a/wis2/de-dwd-gts-to-wis2/data/core/I/S/A/I/01/sbbr`

    dass die Daten vom GTS-zu-WIS2-Gateway veröffentlicht wurden, das vom Deutschen Wetterdienst (DWD), Deutschland, gehostet wird. Das GTS-zu-WIS2-Gateway ist ein spezieller Typ von Datenveröffentlicher, der Daten aus dem Global Telecommunication System (GTS) an WIS2 veröffentlicht. Die Themenstruktur besteht aus den TTAAii CCCC-Headern für die GTS-Nachrichten.

## Übung 2: Überprüfung der WIS2-Nachrichtenstruktur

Trennen Sie die Verbindung zu MQTT Explorer und aktualisieren Sie die 'Advanced'-Abschnitte, um das Abonnement wie folgt zu ändern:

* `origin/a/wis2/+/data/core/weather/surface-based-observations/synop`
* `cache/a/wis2/+/data/core/weather/surface-based-observations/synop`

<img alt="mqtt-explorer-global-broker-topics-exercise2" src="../../assets/img/mqtt-explorer-global-broker-sub-origin-cache-synop.png" width="800">

!!! note
    Der `+`-Platzhalter wird verwendet, um alle WIS-Zentren zu abonnieren.

Stellen Sie die Verbindung zum Global Broker wieder her und warten Sie, bis Nachrichten erscheinen.

Sie können den Inhalt der WIS2-Nachricht im Abschnitt "Value" auf der rechten Seite anzeigen. Versuchen Sie, die Themenstruktur zu erweitern, um die verschiedenen Ebenen der Nachricht zu sehen, bis Sie die letzte Ebene erreichen, und überprüfen Sie den Nachrichteninhalt einer der Nachrichten.

!!! question

    Wie können wir den Zeitstempel identifizieren, zu dem die Daten veröffentlicht wurden? Und wie können wir den Zeitstempel identifizieren, zu dem die Daten gesammelt wurden?

??? success "Klicken Sie, um die Antwort anzuzeigen"

    Der Zeitstempel, zu dem die Daten veröffentlicht wurden, ist im Abschnitt `properties` der Nachricht mit einem Schlüssel von `pubtime` enthalten.

    Der Zeitstempel, zu dem die Daten gesammelt wurden, ist im Abschnitt `properties` der Nachricht mit einem Schlüssel von `datetime` enthalten.

    <img alt="mqtt-explorer-global-broker-msg-properties" src="../../assets/img/mqtt-explorer-global-broker-msg-properties.png" width="800">

!!! question

    Wie können wir die Daten von der in der Nachricht angegebenen URL herunterladen?

??? success "Klicken Sie, um die Antwort anzuzeigen"

    Die URL ist im Abschnitt `links` mit `rel="canonical"` enthalten und wird durch den Schlüssel `href` definiert.

    Sie können die URL kopieren und in einen Webbrowser einfügen, um die Daten herunterzuladen.

## Übung 3: Überprüfung des Unterschieds zwischen 'origin'- und 'cache'-Themen

Stellen Sie sicher, dass Sie noch mit dem Global Broker verbunden sind und die Themenabonnements `origin/a/wis2/+/data/core/weather/surface-based-observations/synop` und `cache/a/wis2/+/data/core/weather/surface-based-observations/synop` wie in Übung 2 beschrieben verwenden.

Versuchen Sie, eine Nachricht für dieselbe Zentren-ID zu identifizieren, die sowohl auf den Themen `origin` als auch `cache` veröffentlicht wurde.

!!! question

    Was ist der Unterschied zwischen den Nachrichten, die auf den Themen `origin` und `cache` veröffentlicht wurden?

??? success "Klicken Sie, um die Antwort anzuzeigen"

    Die auf den `origin`-Themen veröffentlichten Nachrichten sind die ursprünglichen Nachrichten, die der Global Broker von den WIS2-Knoten im Netzwerk erneut veröffentlicht.

    Die auf den `cache`-Themen veröffentlichten Nachrichten sind die Nachrichten für Daten, die vom Global Cache heruntergeladen wurden. Wenn Sie den Inhalt der Nachricht aus dem Thema überprüfen, das mit `cache` beginnt, werden Sie sehen, dass der 'canonical'-Link zu einer neuen URL aktualisiert wurde.
    
    Es gibt mehrere Global Caches im WIS2-Netzwerk, sodass Sie eine Nachricht von jedem Global Cache erhalten, der die Nachricht heruntergeladen hat.

    Der Global Cache lädt nur Nachrichten herunter und veröffentlicht sie erneut, die in der Themenhierarchie `../data/core/...` veröffentlicht wurden.

## Fazit

!!! success "Herzlichen Glückwunsch!"
    In dieser praktischen Sitzung haben Sie gelernt:

    - wie man WIS2 Global Broker-Dienste mit MQTT Explorer abonniert
    - die WIS2-Themenstruktur
    - die Struktur der WIS2-Benachrichtigungsnachrichten
    - den Unterschied zwischen Kern- und empfohlenen Daten
    - die Themenstruktur, die vom GTS-zu-WIS2-Gateway verwendet wird
    - den Unterschied zwischen Global Broker-Nachrichten, die auf den Themen `origin` und `cache` veröffentlicht wurden