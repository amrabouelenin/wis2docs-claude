# Lavorare con i dati BUFR

!!! abstract "Risultati di apprendimento"
    In questa sessione pratica verrai introdotto ad alcuni degli strumenti BUFR inclusi nel container **wis2box-api** che vengono utilizzati per trasformare i dati in formato BUFR e per leggere il contenuto codificato in BUFR.
    
    Imparerai:

    - come ispezionare le intestazioni nel file BUFR utilizzando il comando `bufr_ls`
    - come estrarre e ispezionare i dati all'interno di un file bufr utilizzando `bufr_dump`
    - la struttura di base dei modelli bufr utilizzati in csv2bufr e come utilizzare lo strumento da riga di comando
    - e come apportare modifiche di base ai modelli bufr e come aggiornare il wis2box per utilizzare la versione rivista

## Introduzione

I plugin che producono notifiche con dati BUFR utilizzano processi nel wis2box-api per lavorare con i dati BUFR, ad esempio per trasformare i dati da CSV a BUFR o da BUFR a geojson.

Il container wis2box-api include numerosi strumenti per lavorare con i dati BUFR.

Questi includono gli strumenti sviluppati da ECMWF e inclusi nel software ecCodes, maggiori informazioni su questi possono essere 
trovate sul [sito web ecCodes](https://confluence.ecmwf.int/display/ECC/BUFR+tools).

In questa sessione verrai introdotto a `bufr_ls` e `bufr_dump` dal pacchetto software ecCodes e alla configurazione avanzata dello strumento csv2bufr.

## Preparazione

Per utilizzare gli strumenti da riga di comando BUFR dovrai essere connesso al container wis2box-api
e, salvo diversa indicazione, tutti i comandi dovrebbero essere eseguiti su questo container. Avrai anche bisogno di avere
MQTT Explorer aperto e connesso al tuo broker.

Prima connettiti alla tua VM studente tramite il tuo client ssh e poi accedi al container wis2box-api:

```{.copy}
cd ~/wis2box-1.0.0rc1
python3 wis2box-ctl.py login wis2box-api
```

Conferma che gli strumenti siano disponibili, iniziando con ecCodes:

``` {.copy}
bufr_dump -V
```
Dovresti ottenere la seguente risposta:

```
ecCodes Version 2.28.0
```

Poi controlla csv2bufr:

```{.copy}
csv2bufr --version
```

Dovresti ottenere la seguente risposta:

```
csv2bufr, version 0.7.4
```

Infine, crea una directory di lavoro in cui operare:

```{.copy}
cd /data/wis2box
mkdir -p working/bufr-cli
cd working/bufr-cli
```

Ora sei pronto per iniziare a utilizzare gli strumenti BUFR.


## Utilizzo degli strumenti da riga di comando BUFR

### Esercizio 1 - bufr_ls
In questo primo esercizio utilizzerai il comando `bufr_ls` per ispezionare le intestazioni di un file BUFR e determinare il 
contenuto del file. Le seguenti intestazioni sono incluse in un file BUFR:

| intestazione                     | chiave ecCodes               | descrizione                                                                                                                                           |
|----------------------------------|------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| centro di origine/generazione    | centre                       | Il centro di origine/generazione dei dati                                                                                                             |
| sotto-centro di origine/generazione | bufrHeaderSubCentre       | Il sotto-centro di origine/generazione dei dati                                                                                                       | 
| Numero di sequenza di aggiornamento | updateSequenceNumber      | Se questa è la prima versione dei dati (0) o un aggiornamento (>0)                                                                                    |               
| Categoria di dati               | dataCategory                  | Il tipo di dati contenuti nel messaggio BUFR, es. dati di superficie. Vedi [BUFR Table A](https://github.com/wmo-im/BUFR4/blob/master/BUFR_TableA_en.csv) |
| Sottocategoria internazionale di dati | internationalDataSubCategory | Il sottotipo di dati contenuti nel messaggio BUFR, es. dati di superficie. Vedi [Common Code Table C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv) |
| Anno                            | typicalYear (typicalDate)     | Tempo più tipico per i contenuti del messaggio BUFR                                                                                                   |
| Mese                            | typicalMonth (typicalDate)    | Tempo più tipico per i contenuti del messaggio BUFR                                                                                                   |
| Giorno                          | typicalDay (typicalDate)      | Tempo più tipico per i contenuti del messaggio BUFR                                                                                                   |
| Ora                             | typicalHour (typicalTime)     | Tempo più tipico per i contenuti del messaggio BUFR                                                                                                   |
| Minuto                          | typicalMinute (typicalTime)   | Tempo più tipico per i contenuti del messaggio BUFR                                                                                                   |
| Descrittori BUFR                | unexpandedDescriptors         | Elenco di uno o più descrittori BUFR che definiscono i dati contenuti nel file                                                                        |

Scarica il file di esempio direttamente nel container wis2box-management utilizzando il seguente comando:

``` {.copy}
curl https://training.wis2box.wis.wmo.int/sample-data/bufr-cli-ex1.bufr4 --output bufr-cli-ex1.bufr4
```

Ora usa il seguente comando per eseguire `bufr_ls` su questo file:

```bash
bufr_ls bufr-cli-ex1.bufr4
```

Dovresti vedere il seguente output:

```bash
bufr-cli-ex1.bufr4
centre                     masterTablesVersionNumber  localTablesVersionNumber   typicalDate                typicalTime                numberOfSubsets
cnmc                       29                         0                          20231002                   000000                     1
1 of 1 messages in bufr-cli-ex1.bufr4

1 of 1 total messages in 1 files
```

Da solo, questo output non è molto informativo, con solo informazioni limitate sul contenuto del file.

L'output predefinito non fornisce informazioni sul tipo di osservazione o dati ed è in un formato che non è
molto facile da leggere. Tuttavia, varie opzioni possono essere passate a `bufr_ls` per modificare sia il formato che i campi di intestazione 
stampati.

Usa `bufr_ls` senza argomenti per visualizzare le opzioni:

```{.copy}
bufr_ls
```

Dovresti vedere il seguente output:

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

Ora esegui lo stesso comando sul file di esempio ma visualizza le informazioni in JSON.

!!! question
    Quale flag passi al comando `bufr_ls` per visualizzare l'output in formato JSON?

??? success "Clicca per rivelare la risposta"
    Puoi cambiare il formato di output in json usando il flag `-j`, cioè
    `bufr_ls -j <input-file>`. Questo può essere più leggibile del formato di output predefinito. Vedi l'esempio di output qui sotto:

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

Quando si esamina un file BUFR, spesso vogliamo determinare il tipo di dati contenuti nel file e la data/ora tipica
dei dati nel file. Queste informazioni possono essere elencate utilizzando il flag `-p` per selezionare le intestazioni da visualizzare. È possibile
includere più intestazioni utilizzando un elenco separato da virgole.

Utilizzando il comando `bufr_ls`, ispeziona il file di test e identifica il tipo di dati contenuti nel file e la data e l'ora tipiche per quei dati.

??? hint
    Le chiavi ecCodes sono fornite nella tabella sopra. Possiamo usare quanto segue per elencare dataCategory e
    internationalDataSubCategory dei dati BUFR:

    ```
    bufr_ls -p dataCategory,internationalDataSubCategory bufr-cli-ex1.bufr4
    ```

    È possibile aggiungere ulteriori chiavi secondo necessità.

!!! question
    Che tipo di dati (categoria di dati e sottocategoria) sono contenuti nel file? Qual è la data e l'ora tipica
    per i dati?

??? success "Clicca per rivelare la risposta"
    Il comando che devi eseguire dovrebbe essere simile a:
    
    ```
    bufr_ls -p dataCategory,internationalDataSubCategory,typicalDate,typicalTime -j bufr-cli-ex1.bufr4
    ```

    Potresti avere chiavi aggiuntive, o aver elencato anno, mese, giorno ecc. individualmente. L'output dovrebbe
    essere simile a quello sotto, a seconda che tu abbia selezionato JSON o output predefinito.

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

    Da questo vediamo che:

    - La categoria di dati è 2, dalla [BUFR Table A](https://github.com/wmo-im/BUFR4/blob/master/BUFR_TableA_en.csv)
      possiamo vedere che questo file contiene dati di "Sondaggi verticali (diversi da satellite)".
    - La sottocategoria internazionale è 4, che indica 
      "Rapporti di temperatura/umidità/vento in quota da stazioni terrestri fisse (TEMP)". Questa informazione può essere cercata
      nella [Common Code Table C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv) (riga 33). Nota la combinazione
      di categoria e sottocategoria.
    - La data e l'ora tipiche sono rispettivamente 2023/10/02 e 00:00:00z.

    

### Esercizio 2 - bufr_dump

Il comando `bufr_dump` può essere utilizzato per elencare ed esaminare il contenuto di un file BUFR, inclusi i dati stessi.

In questo esercizio utilizzeremo un file BUFR che è lo stesso che hai creato durante la sessione pratica iniziale di csv2bufr utilizzando wis2box-webapp.

Scarica il file di esempio nel container wis2box management direttamente con il seguente comando:

``` {.copy}
curl https://training.wis2box.wis.wmo.int/sample-data/bufr-cli-ex2.bufr4 --output bufr-cli-ex2.bufr4
```

Ora esegui il comando `bufr_dump` sul file, utilizzando il flag `-p` per visualizzare i dati in testo semplice (formato chiave=valore):

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4
```

Dovresti vedere circa 240 chiavi in output, molte delle quali mancanti. Questo è tipico con dati del mondo reale poiché non tutte le chiavi eccodes sono popolate con dati riportati.

!!! hint
    I valori mancanti possono essere filtrati utilizzando strumenti come `grep`:
    ```{.copy}
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -v MISSING
    ```

Il file BUFR di esempio per questo esercizio proviene dalla sessione pratica csv2bufr. Scarica il file CSV originale nella tua posizione corrente come segue:

```{.copy}
curl https://training.wis2box.wis.wmo.int/sample-data/csv2bufr-ex1.csv --output csv2bufr-ex1.csv
```

E visualizza il contenuto del file con:

```{.copy}
more csv2bufr-ex1.csv
```

!!! question
    Usa il seguente comando per visualizzare la colonna 18 nel file CSV e troverai la pressione a livello del mare riportata (msl_pressure):

    ```{.copy}
    more csv2bufr-ex1.csv | cut -d ',' -f 18
    ```
    
    Quale chiave nell'output BUFR corrisponde alla pressione a livello del mare?

??? hint
    Strumenti come `grep` possono essere utilizzati in combinazione con `bufr_dump`. Per esempio:
    
    ```{.copy}
    bufr_dump -p bufr-cli-ex2.bufr4 