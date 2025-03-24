---
title: WIS2 in a box Spickzettel
---

# WIS2 in a box Spickzettel

## Überblick

wis2box läuft als eine Reihe von Docker Compose-Befehlen. Der Befehl ``wis2box-ctl.py`` ist ein Hilfsprogramm (in Python geschrieben), um Docker Compose-Befehle einfach auszuführen.

## wis2box Befehlsgrundlagen

### Starten und Stoppen

* wis2box starten:

```bash
python3 wis2box-ctl.py start
```

* wis2box stoppen:

```bash
python3 wis2box-ctl.py stop
```

* Überprüfen, ob alle wis2box-Container laufen:

```bash
python3 wis2box-ctl.py status
```

* Bei einem wis2box-Container anmelden (*wis2box-management* standardmäßig):

```bash
python3 wis2box-ctl.py login
```

* Bei einem bestimmten wis2box-Container anmelden:

```bash
python3 wis2box-ctl.py login wis2box-api
```