---
title: Docker cheatsheet
---

# Docker cheatsheet

## Panoramica

Docker consente di creare ambienti virtuali in modo isolato a supporto della virtualizzazione delle risorse di calcolo. Il concetto di base dietro Docker è la containerizzazione, dove il software può funzionare come servizi, interagendo con altri container software, per esempio.

Il tipico flusso di lavoro Docker prevede la creazione e la costruzione di **immagini**, che vengono poi eseguite come **container** attivi.

Docker viene utilizzato per eseguire la suite di servizi che compongono wis2box utilizzando immagini precostruite.

### Gestione delle immagini

* Elencare le immagini disponibili

```bash
docker image ls
```

* Aggiornare un'immagine:

```bash
docker pull my-image:latest
```

* Rimuovere un'immagine:

```bash
docker rmi my-image:local
```

### Gestione dei volumi

* Elencare tutti i volumi creati:

```bash
docker volume ls
```

* Visualizzare informazioni dettagliate su un volume:

```bash
docker volume inspect my-volume
```

* Rimuovere un volume:

```bash
docker volume rm my-volume
```

* Rimuovere tutti i volumi inutilizzati:

```bash
docker volume prune
```

### Gestione dei container

* Visualizzare un elenco dei container attualmente in esecuzione:

```bash
docker ps
```

* Elenco di tutti i container:

```bash
docker ps -a
```

* Entrare nel terminale interattivo di un container in esecuzione:


!!! suggerimento

    usa `docker ps` per utilizzare l'id del container nel comando seguente

```bash
docker exec -it my-container /bin/bash
```

* Rimuovere un container

```bash
docker rm my-container
```

* Rimuovere un container in esecuzione:

```bash
docker rm -f my-container
```