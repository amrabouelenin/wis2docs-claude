# Conversione dei dati SYNOP in BUFR dalla riga di comando

!!! abstract "Risultati di apprendimento"
    Al termine di questa sessione pratica, sarai in grado di:

    - utilizzare lo strumento synop2bufr per convertire i report SYNOP FM-12 in BUFR;
    - diagnosticare e correggere semplici errori di codifica nei report SYNOP FM-12 prima della conversione di formato;

## Introduzione

I report meteorologici di superficie dalle stazioni terrestri sono stati storicamente riportati ogni ora o nelle ore 
sinottiche principali (00, 06, 12 e 18 UTC) e intermedie (03, 09, 15, 21 UTC). Prima della migrazione
a BUFR, questi report erano codificati nel formato testuale FM-12 SYNOP. Sebbene la migrazione a BUFR
fosse programmata per essere completata entro il 2012, un gran numero di report viene ancora scambiato nel formato 
FM-12 SYNOP tradizionale. Ulteriori informazioni sul formato FM-12 SYNOP si possono trovare nel Manuale WMO sui Codici, 
Volume I.1 (WMO-No. 306, Volume I.1).

[Manuale WMO sui Codici, Volume I.1](https://library.wmo.int/records/item/35713-manual-on-codes-international-codes-volume-i-1)

Per facilitare il completamento della migrazione a BUFR, sono stati sviluppati alcuni strumenti per
codificare i report FM-12 SYNOP in BUFR. In questa sessione imparerai come utilizzare questi strumenti e
la relazione tra le informazioni contenute nei report FM-12 SYNOP e i messaggi BUFR.

## Preparazione

!!! warning "Prerequisiti"

    - Assicurati che il tuo wis2box sia stato configurato e avviato.
    - Conferma lo stato visitando l'API wis2box (`http://<nome-host>/oapi`) e verificando che l'API sia in esecuzione.
    - Assicurati di leggere le sezioni **synop2bufr primer** ed **ecCodes primer** prima di iniziare gli esercizi.

## synop2bufr primer

Di seguito sono riportati i comandi e le configurazioni essenziali di `synop2bufr`:

### transform
La funzione `transform` converte un messaggio SYNOP in BUFR:

```bash
synop2bufr data transform --metadata mio_file.csv --output-dir ./mia_directory --year anno_messaggio --month mese_messaggio mio_SYNOP.txt
```

Nota che se i parametri metadata, output directory, year e month non sono specificati, assumeranno i loro valori predefiniti:

| Opzione      | Predefinito |
| ----------- | ----------- |
| --metadata | station_list.csv |
| --output-dir | La directory di lavoro corrente. |
| --year | L'anno corrente. |
| --month | Il mese corrente. |

!!! note
    Bisogna fare attenzione utilizzando l'anno e il mese predefiniti, poiché il giorno del mese specificato nel report potrebbe non corrispondere (ad esempio, giugno non ha 31 giorni).

Negli esempi, l'anno e il mese non sono forniti, quindi sentiti libero di specificare una data tu stesso o utilizzare i valori predefiniti.

## ecCodes primer

ecCodes fornisce sia strumenti da riga di comando sia la possibilità di essere integrato nelle tue applicazioni. Di seguito sono riportati alcuni utili
strumenti da riga di comando per lavorare con i dati BUFR.

### bufr_dump

Il comando `bufr_dump` è uno strumento generico per le informazioni BUFR. Ha molte opzioni, ma le seguenti saranno le più applicabili agli esercizi:

```bash
bufr_dump -p mio_bufr.bufr4
```

Questo mostrerà il contenuto BUFR sullo schermo. Se sei interessato ai valori assunti da una variabile in particolare, usa il comando `egrep`:

```bash
bufr_dump -p mio_bufr.bufr4 | egrep -i temperature
```

Questo mostrerà le variabili relative alla temperatura nei tuoi dati BUFR. Se vuoi farlo per più tipi di variabili, filtra l'output usando una pipe (`|`):

```bash
bufr_dump -p mio_bufr.bufr4 | egrep -i 'temperature|wind'
```

## Conversione di FM-12 SYNOP in BUFR utilizzando synop2bufr dalla riga di comando

La libreria eccodes e il modulo synop2bufr sono installati nel container wis2box-api. Per fare i prossimi esercizi, copieremo la directory synop2bufr-exercises nel container wis2box-api ed eseguiremo gli esercizi da lì.

```bash
docker cp ~/exercise-materials/synop2bufr-exercises wis2box-api:/root
```

Ora possiamo entrare nel container ed eseguire gli esercizi:

```bash
docker exec -it wis2box-api /bin/bash
```

### Esercizio 1
Naviga nella directory `/root/synop2bufr-exercises/ex_1` e ispeziona il file di messaggio SYNOP message.txt:

```bash
cd /root/synop2bufr-exercises/ex_1
more message.txt
```

!!! question

    Quanti report SYNOP ci sono in questo file?

??? success "Clicca per rivelare la risposta"
    
    C'è 1 report SYNOP, poiché c'è solo 1 delimitatore (=) alla fine del messaggio.

Ispeziona l'elenco delle stazioni:

```bash
more station_list.csv
```

!!! question

    Quante stazioni sono elencate nella lista delle stazioni?

??? success "Clicca per rivelare la risposta"

    C'è 1 stazione, il file station_list.csv contiene una riga di metadati della stazione.

!!! question
    Prova a convertire `message.txt` in formato BUFR.

??? success "Clicca per rivelare la risposta"

    Per convertire il messaggio SYNOP in formato BUFR, usa il seguente comando:

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

!!! tip

    Vedi la sezione [synop2bufr primer](#synop2bufr-primer).

Ispeziona i dati BUFR risultanti utilizzando `bufr_dump`.

!!! question
     Trova come confrontare i valori di latitudine e longitudine con quelli nell'elenco delle stazioni.

??? success "Clicca per rivelare la risposta"

    Per confrontare i valori di latitudine e longitudine nei dati BUFR con quelli nell'elenco delle stazioni, usa il seguente comando:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15015_20240921T120000.bufr4 | egrep -i 'latitude|longitude'
    ```

    Questo mostrerà i valori di latitudine e longitudine nei dati BUFR.

!!! tip

    Vedi la sezione [ecCodes primer](#eccodes-primer).

### Esercizio 2
Naviga nella directory `exercise-materials/synop2bufr-exercises/ex_2` e ispeziona il file di messaggio SYNOP message.txt:

```bash
cd /root/synop2bufr-exercises/ex_2
more message.txt
```

!!! question

    Quanti report SYNOP ci sono in questo file?

??? success "Clicca per rivelare la risposta"

    Ci sono 3 report SYNOP, poiché ci sono 3 delimitatori (=) alla fine del messaggio.

Ispeziona l'elenco delle stazioni:

```bash
more station_list.csv
```

!!! question

    Quante stazioni sono elencate nella lista delle stazioni?

??? success "Clicca per rivelare la risposta"

    Ci sono 3 stazioni, il file station_list.csv contiene tre righe di metadati delle stazioni.

!!! question
    Converti `message.txt` in formato BUFR.

??? success "Clicca per rivelare la risposta"

    Per convertire il messaggio SYNOP in formato BUFR, usa il seguente comando:

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

!!! question

    In base ai risultati degli esercizi in questo e nel precedente esercizio, come prevederesti il numero di
    file BUFR risultanti in base al numero di report SYNOP e stazioni elencate nel file di metadati delle stazioni?

??? success "Clicca per rivelare la risposta"

    Per vedere i file BUFR prodotti, esegui il seguente comando:

    ```bash
    ls -l *.bufr4
    ```

    Il numero di file BUFR prodotti sarà uguale al numero di report SYNOP nel file di messaggio.

Ispeziona i dati BUFR risultanti utilizzando `bufr_dump`.

!!! question
    Come puoi controllare l'ID della stazione WIGOS codificato all'interno dei dati BUFR di ciascun file prodotto?

??? success "Clicca per rivelare la risposta"

    Questo può essere fatto utilizzando i seguenti comandi:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15015_20240921T120000.bufr4 | egrep -i 'wigos'
    ```

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15020_20240921T120000.bufr4 | egrep -i 'wigos'
    ```

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15090_20240921T120000.bufr4 | egrep -i 'wigos'
    ```

    Nota che se hai una directory con solo questi 3 file BUFR, puoi usare i caratteri jolly di Linux come segue:

    ```bash
    bufr_dump -p *.bufr4 | egrep -i 'wigos'
    ```

### Esercizio 3
Naviga nella directory `exercise-materials/synop2bufr-exercises/ex_3` e ispeziona il file di messaggio SYNOP message.txt:

```bash
cd /root/synop2bufr-exercises/ex_3
more message.txt
```

Questo messaggio SYNOP contiene solo un report più lungo con più sezioni.

Ispeziona l'elenco delle stazioni:

```bash
more station_list.csv
```

!!! question

    È problematico che questo file contenga più stazioni di quanti siano i report nel messaggio SYNOP?

??? success "Clicca per rivelare la risposta"

    No, questo non è un problema a condizione che esista una riga nel file dell'elenco delle stazioni con un TSI della stazione corrispondente a quello del report SYNOP che stiamo cercando di convertire.

!!! note

    Il file dell'elenco delle stazioni è una fonte di metadati per `synop2bufr` per fornire le informazioni mancanti nel report SYNOP alfanumerico e richieste nel SYNOP BUFR.

!!! question
    Converti `message.txt` in formato BUFR.

??? success "Clicca per rivelare la risposta"

    Questo viene fatto utilizzando il comando `transform`, ad esempio:

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

Ispeziona i dati BUFR risultanti utilizzando `bufr_dump`.

!!! question

    Trova le seguenti variabili:

    - Temperatura dell'aria (K) del report
    - Copertura nuvolosa totale (%) del report
    - Periodo totale di sole (minuti) del report
    - Velocità del vento (m/s) del report

??? success "Clicca per rivelare la risposta"

    Per trovare le variabili per parola chiave nei dati BUFR, puoi utilizzare i seguenti comandi:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15260_20240921T115500.bufr4 | egrep -i 'temperature'
    ```

    Puoi utilizzare il seguente comando per cercare più parole chiave:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15260_20240921T115500.bufr4 | egrep -i 'temperature|cover|sunshine|wind'
    ```

!!! tip

    Potresti trovare utile l'ultimo comando della sezione [ecCodes primer](#eccodes-primer).


### Esercizio 4
Naviga nella directory `exercise-materials/synop2bufr-exercises/ex_4` e ispeziona il file di messaggio SYNOP message.txt:

```bash
cd /root/synop2bufr-exercises/ex_4
more message_incorrect.txt
```

!!! question

    Cosa c'è di sbagliato in questo file SYNOP?

??? success "Clicca per rivelare la risposta"

    Il report SYNOP per 15015 manca del delimitatore (`=`) che consente a `synop2bufr` di distinguere questo report dal successivo.

Prova a convertire `message_incorrect.txt` utilizzando `station_list.csv`

!!! question

    Quali problemi hai incontrato con questa conversione?

??? success "Clicca per rivelare la risposta"

    Per convertire il messaggio SYNOP in formato BUFR, usa il seguente comando:

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message_incorrect.txt
    ```

    Il tentativo di conversione dovrebbe generare i seguenti errori:
    
    - `[ERROR] Unable to decode the SYNOP message`
    - `[ERROR] Error parsing SYNOP report: AAXX 21121 15015 02999 02501 10103 21090 39765 42952 57020 60001 15020 02997 23104 10130 21075 30177 40377 58020 60001 81041. 10130 is not a valid group!`

### Esercizio 5
Naviga nella directory `exercise-materials/synop2bufr-exercises/ex_5` e ispeziona il file di messaggio SYNOP message.txt:

```bash
cd /root/synop2bufr-exercises/ex_5
more message.txt
```

Prova a convertire `message.txt` in formato BUFR utilizzando `station_list_incorrect.csv` 

!!! question

    Quali problemi hai incontrato con questa conversione?  
    Considerando l'errore presentato, giustifica il numero di file BUFR prodotti.

??? success "Clicca per rivelare la risposta"

    Per convertire il messaggio SYNOP in formato BUFR, usa il seguente comando:

    ```bash
    synop2bufr data transform --metadata station_list_incorrect.csv --output-dir ./ --year 