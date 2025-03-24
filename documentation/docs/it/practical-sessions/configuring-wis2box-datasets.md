# Configurazione dei dataset in wis2box

!!! abstract "Risultati di apprendimento"
    Alla fine di questa sessione pratica, sarai in grado di:

    - creare un nuovo dataset
    - creare metadati di scoperta per un dataset
    - configurare le mappature dei dati per un dataset
    - pubblicare una notifica WIS2 con un record WCMP2
    - aggiornare e ripubblicare il tuo dataset

## Introduzione

wis2box utilizza dataset che sono associati a metadati di scoperta e mappature di dati.

I metadati di scoperta vengono utilizzati per creare un record WCMP2 (WMO Core Metadata Profile 2) che viene condiviso utilizzando una notifica WIS2 pubblicata sul tuo wis2box-broker.

Le mappature dei dati vengono utilizzate per associare un plugin di dati ai tuoi dati di input, consentendo ai tuoi dati di essere trasformati prima di essere pubblicati utilizzando la notifica WIS2.

Questa sessione ti guiderà attraverso la creazione di un nuovo dataset, la creazione di metadati di scoperta e la configurazione delle mappature dei dati. Esaminerai il tuo dataset nel wis2box-api e rivedrai la notifica WIS2 per i tuoi metadati di scoperta.

## Preparazione

Connettiti al tuo broker utilizzando MQTT Explorer.

Invece di utilizzare le credenziali del tuo broker interno, utilizza le credenziali pubbliche `everyone/everyone`:

<img alt="MQTT Explorer: Connect to broker" src="../../assets/img/mqtt-explorer-wis2box-broker-everyone-everyone.png" width="800">

!!! Note

    Non è mai necessario condividere le credenziali del tuo broker interno con utenti esterni. L'utente 'everyone' è un utente pubblico per consentire la condivisione delle notifiche WIS2.

    Le credenziali `everyone/everyone` hanno accesso in sola lettura all'argomento 'origin/a/wis2/#'. Questo è l'argomento in cui vengono pubblicate le notifiche WIS2. Il Global Broker può sottoscriversi con queste credenziali pubbliche per ricevere le notifiche.
    
    L'utente 'everyone' non vedrà argomenti interni né potrà pubblicare messaggi.
    
Apri un browser e apri una pagina su `http://<tuo-host>/wis2box-webapp`. Assicurati di aver effettuato l'accesso e di poter accedere alla pagina 'dataset editor'.

Consulta la sezione su [Inizializzazione di wis2box](/practical-sessions/initializing-wis2box) se hai bisogno di ricordare come connetterti al broker o accedere al wis2box-webapp.

## Creare un token di autorizzazione per processes/wis2box

Avrai bisogno di un token di autorizzazione per l'endpoint 'processes/wis2box' per pubblicare il tuo dataset.

Per creare un token di autorizzazione, accedi alla tua VM di formazione tramite SSH e utilizza i seguenti comandi per accedere al container wis2box-management:

```bash
cd ~/wis2box-1.0.0rc1
python3 wis2box-ctl.py login
```

Quindi esegui il seguente comando per creare un token di autorizzazione generato casualmente per l'endpoint 'processes/wis2box':

```bash
wis2box auth add-token --path processes/wis2box
```

Puoi anche creare un token con un valore specifico fornendo il token come argomento al comando:

```bash
wis2box auth add-token --path processes/wis2box MyS3cretToken
```

Assicurati di copiare il valore del token e di conservarlo sul tuo computer locale, poiché ne avrai bisogno in seguito.

Una volta ottenuto il token, puoi uscire dal container wis2box-management:

```bash
exit
```

## Creazione di un nuovo dataset nel wis2box-webapp

Naviga alla pagina 'dataset editor' nel wis2box-webapp della tua istanza wis2box andando su `http://<tuo-host>/wis2box-webapp` e selezionando 'dataset editor' dal menu sul lato sinistro.

Nella pagina 'dataset editor', sotto la scheda 'Datasets', fai clic su "Create New ...":

<img alt="Create New Dataset" src="../../assets/img/wis2box-create-new-dataset.png" width="800">

Apparirà una finestra pop-up, che ti chiederà di fornire:

- **Centre ID**: questo è l'acronimo dell'agenzia (in minuscolo e senza spazi), come specificato dal Membro WMO, che identifica il centro dati responsabile della pubblicazione dei dati.
- **Data Type**: Il tipo di dati per cui stai creando metadati. Puoi scegliere tra l'utilizzo di un modello predefinito o selezionare 'other'. Se viene selezionato 'other', dovranno essere compilati manualmente più campi.

!!! Note "Centre ID"

    Il tuo centre-id dovrebbe iniziare con il TLD del tuo paese, seguito da un trattino (`-`) e un nome abbreviato della tua organizzazione (ad esempio `fr-meteofrance`). Il centre-id deve essere in minuscolo e utilizzare solo caratteri alfanumerici. L'elenco a discesa mostra tutti i centre-id attualmente registrati su WIS2 e qualsiasi centre-id che hai già creato in wis2box.

!!! Note "Modelli di tipo di dati"

    Il campo *Data Type* ti consente di selezionare da un elenco di modelli disponibili nell'editor di dataset wis2box-webapp. Un modello precompilerà il modulo con valori predefiniti suggeriti appropriati per il tipo di dati. Ciò include titolo e parole chiave suggeriti per i metadati e plugin di dati preconfigurati. L'argomento sarà fissato all'argomento predefinito per il tipo di dati.

    Ai fini della formazione utilizzeremo il tipo di dati *weather/surface-based-observations/synop* che include plugin di dati che garantiscono che i dati vengano trasformati in formato BUFR prima di essere pubblicati.

    Se desideri pubblicare avvisi CAP utilizzando wis2box, utilizza il modello *weather/advisories-warnings*. Questo modello include un plugin di dati che verifica che i dati di input siano un avviso CAP valido prima della pubblicazione. Per creare avvisi CAP e pubblicarli tramite wis2box puoi utilizzare [CAP Composer](https://github.com/wmo-raf/cap-composer).

Scegli un centre-id appropriato per la tua organizzazione.

Per **Data Type**, seleziona **weather/surface-based-observations/synop**:

<img alt="Create New Dataset Form: Initial information" src="../../assets/img/wis2box-create-new-dataset-form-initial.png" width="450">

Fai clic su *continue to form* per procedere, ti verrà ora presentato il **Dataset Editor Form**.

Poiché hai selezionato il tipo di dati **weather/surface-based-observations/synop**, il modulo sarà precompilato con alcuni valori iniziali relativi a questo tipo di dati.

## Creazione di metadati di scoperta

Il Dataset Editor Form ti consente di fornire i Metadati di Scoperta per il tuo dataset che il container wis2box-management utilizzerà per pubblicare un record WCMP2.

Poiché hai selezionato il tipo di dati 'weather/surface-based-observations/synop', il modulo sarà precompilato con alcuni valori predefiniti.

Assicurati di sostituire il 'Local ID' generato automaticamente con un nome descrittivo per il tuo dataset, ad esempio 'synop-dataset-wis2training':

<img alt="Metadata Editor: title, description, keywords" src="../../assets/img/wis2box-metadata-editor-part1.png" width="800">

Rivedi il titolo e le parole chiave, aggiornali se necessario e fornisci una descrizione per il tuo dataset.

Nota che ci sono opzioni per modificare la 'WMO Data Policy' da 'core' a 'recommended' o per modificare il tuo Metadata Identifier predefinito, mantieni data-policy come 'core' e utilizza il Metadata Identifier predefinito.

Successivamente, rivedi la sezione che definisce le tue 'Temporal Properties' e 'Spatial Properties'. Puoi regolare il riquadro di delimitazione aggiornando i campi 'North Latitude', 'South Latitude', 'East Longitude' e 'West Longitude':

<img alt="Metadata Editor: temporal properties, spatial properties" src="../../assets/img/wis2box-metadata-editor-part2.png" width="800">

Successivamente, compila la sezione che definisce le 'Contact Information of the Data Provider':

<img alt="Metadata Editor: contact information" src="../../assets/img/wis2box-metadata-editor-part3.png" width="800">

Infine, compila la sezione che definisce le 'Data Quality Information':

Una volta completata la compilazione di tutte le sezioni, fai clic su 'VALIDATE FORM' e controlla il modulo per eventuali errori:

<img alt="Metadata Editor: validation" src="../../assets/img/wis2box-metadata-validation-error.png" width="800">

Se ci sono errori, correggili e fai di nuovo clic su 'VALIDATE FORM'.

Assicurati di non avere errori e di ottenere un'indicazione pop-up che il tuo modulo è stato convalidato:

<img alt="Metadata Editor: validation success" src="../../assets/img/wis2box-metadata-validation-success.png" width="800">

Successivamente, prima di inviare il tuo dataset, rivedi le mappature dei dati per il tuo dataset.

## Configurazione delle mappature dei dati

Poiché hai utilizzato un modello per creare il tuo dataset, le mappature del dataset sono state precompilate con i plugin predefiniti per il tipo di dati 'weather/surface-based-observations/synop'. I plugin di dati vengono utilizzati nel wis2box per trasformare i dati prima che vengano pubblicati utilizzando la notifica WIS2.

<img alt="Data Mappings: update plugin" src="../../assets/img/wis2box-data-mappings.png" width="800">

Nota che puoi fare clic sul pulsante "update" per modificare le impostazioni del plugin come l'estensione del file e il pattern del file, puoi lasciare le impostazioni predefinite per ora. In una sessione successiva, imparerai di più su BUFR e sulla trasformazione dei dati in formato BUFR.

## Invio del tuo dataset

Infine, puoi fare clic su 'submit' per pubblicare il tuo dataset.

Dovrai fornire il token di autorizzazione per 'processes/wis2box' che hai creato in precedenza. Se non l'hai fatto, puoi creare un nuovo token seguendo le istruzioni nella sezione di preparazione.

Verifica di ricevere il seguente messaggio dopo aver inviato il tuo dataset, che indica che il dataset è stato inviato con successo:

<img alt="Submit Dataset Success" src="../../assets/img/wis2box-submit-dataset-success.png" width="400">

Dopo aver fatto clic su 'OK', verrai reindirizzato alla home page dell'Editor di Dataset. Ora, se fai clic sulla scheda 'Dataset', dovresti vedere il tuo nuovo dataset elencato:

<img alt="Dataset Editor: new dataset" src="../../assets/img/wis2box-dataset-editor-new-dataset.png" width="800">

## Revisione della notifica WIS2 per i tuoi metadati di scoperta

Vai su MQTT Explorer, se eri connesso al broker, dovresti vedere una nuova notifica WIS2 pubblicata sull'argomento `origin/a/wis2/<tuo-centre-id>/metadata`:

<img alt="MQTT Explorer: WIS2 notification" src="../../assets/img/mqtt-explorer-wis2-notification-metadata.png" width="800">

Ispeziona il contenuto della notifica WIS2 che hai pubblicato. Dovresti vedere un JSON con una struttura corrispondente al formato WIS Notification Message (WNM).

!!! question

    Su quale argomento viene pubblicata la notifica WIS2?

??? success "Clicca per rivelare la risposta"

    La notifica WIS2 viene pubblicata sull'argomento `origin/a/wis2/<tuo-centre-id>/metadata`.

!!! question
    
    Prova a trovare il titolo, la descrizione e le parole chiave che hai fornito nei metadati di scoperta nella notifica WIS2. Riesci a trovarli?

??? success "Clicca per rivelare la risposta"

    Nota che il titolo, la descrizione e le parole chiave che hai fornito nei metadati di scoperta **non** sono presenti nel payload della notifica WIS2!
    
    Invece, prova a cercare il link canonico nella sezione "links" nella notifica WIS2:

    <img alt="WIS2 notification for metadata, links sections" src="../../assets/img/wis2-notification-metadata-links.png" width="800">

    La notifica WIS2 contiene un link canonico al record WCMP2 che è stato pubblicato. Se copi e incolli questo link in un browser, scaricherai il record WCMP2 e vedrai il titolo, la descrizione e le parole chiave che hai fornito.

## Conclusione

!!! success "Congratulazioni!"
    In questa sessione pratica, hai imparato come:

    - creare un nuovo dataset
    - definire i tuoi metadati di scoperta
    - rivedere le tue mappature dei dati
    - pubblicare metadati di scoperta
    - rivedere la notifica WIS2 per i tuoi metadati di scoperta