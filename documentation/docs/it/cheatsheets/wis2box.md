# Foglio di riferimento per WIS2 in a box

## Panoramica

wis2box funziona come una suite di comandi Docker Compose. Il comando `wis2box-ctl.py` è un'utilità (scritta in Python) per eseguire facilmente i comandi Docker Compose.

## Comandi essenziali di wis2box

### Avvio e arresto

* Avviare wis2box:

```bash
python3 wis2box-ctl.py start
```

* Arrestare wis2box:

```bash
python3 wis2box-ctl.py stop
```

* Verificare che tutti i container wis2box siano in esecuzione:

```bash
python3 wis2box-ctl.py status
```

* Accedere a un container wis2box (*wis2box-management* per impostazione predefinita):

```bash
python3 wis2box-ctl.py login
```

* Accedere a un container wis2box specifico:

```bash
python3 wis2box-ctl.py login wis2box-api
```