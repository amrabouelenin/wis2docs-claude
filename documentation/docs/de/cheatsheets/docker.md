---
title: Docker-Spickzettel
---

# Docker-Spickzettel

## Überblick

Docker ermöglicht die Erstellung virtueller Umgebungen in isolierter Weise zur Unterstützung
der Virtualisierung von Rechenressourcen. Das grundlegende Konzept hinter Docker ist die Containerisierung,
bei der Software als Dienste laufen kann, die beispielsweise mit anderen Software-Containern interagieren.

Der typische Docker-Workflow umfasst das Erstellen und Bauen von **Images**, die dann als aktive **Container** ausgeführt werden.

Docker wird verwendet, um die Reihe von Diensten auszuführen, die wis2box mit vorgefertigten Images bilden.

### Image-Verwaltung

* Verfügbare Images auflisten

```bash
docker image ls
```

* Ein Image aktualisieren:

```bash
docker pull my-image:latest
```

* Ein Image entfernen:

```bash
docker rmi my-image:local
```

### Volume-Verwaltung

* Alle erstellten Volumes auflisten:

```bash
docker volume ls
```

* Detaillierte Informationen zu einem Volume anzeigen:

```bash
docker volume inspect my-volume
```

* Ein Volume entfernen:

```bash
docker volume rm my-volume
```

* Alle ungenutzten Volumes entfernen:

```bash
docker volume prune
```

### Container-Verwaltung

* Eine Liste der aktuell laufenden Container anzeigen:

```bash
docker ps
```

* Liste aller Container:

```bash
docker ps -a
```

* Das interaktive Terminal eines laufenden Containers öffnen:


!!! Tipp

    Verwenden Sie `docker ps`, um die Container-ID im folgenden Befehl zu verwenden

```bash
docker exec -it my-container /bin/bash
```

* Einen Container entfernen

```bash
docker rm my-container
```

* Einen laufenden Container entfernen:

```bash
docker rm -f my-container
```