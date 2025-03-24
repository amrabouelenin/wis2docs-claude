# Traduzione in Italiano

---
title: Guida rapida Linux
---

# Guida rapida Linux

## Panoramica

I concetti base del lavoro in un sistema operativo Linux sono **file** e **directory** (cartelle) organizzati in
una struttura ad albero all'interno di un **ambiente**.

Quando accedi a un sistema Linux, stai lavorando in una **shell** in cui puoi operare su file e directory,
eseguendo comandi che sono installati sul sistema. La shell Bash è una shell comune e popolare che
si trova tipicamente sui sistemi Linux.

## Bash

### Navigazione delle Directory

* Entrare in una directory con percorso assoluto:

```bash
cd /dir1/dir2
```

* Entrare in una directory con percorso relativo:

```bash
cd ./somedir
```

* Salire di un livello nella directory:

```bash
cd ..
```

* Salire di due livelli nella directory:

```bash
cd ../..
```

* Tornare alla directory "home":

```bash
cd -
```

### Gestione dei File

* Elencare i file nella directory corrente:

```bash
ls
```

* Elencare i file nella directory corrente con maggiori dettagli:

```bash
ls -l
```

* Elencare la radice del filesystem:

```bash
ls -l /
```

* Creare un file vuoto:

```bash
touch foo.txt
```

* Creare un file da un comando `echo`:

```bash
echo "ciao" > test-file.txt
```

* Visualizzare il contenuto di un file:

```bash
cat test-file.txt
```

* Copiare un file:

```bash
cp file1 file2
```

* Caratteri jolly: operare su pattern di file:

```bash
ls -l fil*  # corrisponde a file1 e file2
```

* Concatenare due file in un nuovo file chiamato `newfile`:

```bash
cat file1 file2 > newfile
```

* Aggiungere un altro file a `newfile`:

```bash
cat file3 >> newfile
```

* Eliminare un file:

```bash
rm newfile
```

* Eliminare tutti i file con la stessa estensione:

```bash
rm *.dat
```

* Creare una directory:

```bash
mkdir dir1
```

### Concatenare comandi con le pipe

Le pipe permettono a un utente di inviare l'output di un comando a un altro usando il simbolo pipe `|`:

```bash
echo "ciao" | sed 's/ciao/arrivederci/'
```

* Filtrare gli output dei comandi usando grep:

```bash
echo "id,titolo" > test-file.txt
echo "1,uccelli" >> test-file.txt
echo "2,pesci" >> test-file.txt
echo "3,gatti" >> test-file.txt

cat test-file.txt | grep pesci
```

* Ignorare maiuscole/minuscole:

```bash
grep -i PESCI test-file.txt
```

* Contare le righe corrispondenti:

```bash
grep -c pesci test-file.txt
```

* Restituire output che non contengono la parola chiave:

```bash
grep -v uccelli test-file.txt
```

* Contare il numero di righe in `test-file.txt`:

```bash
wc -l test-file.txt
```

* Visualizzare l'output una schermata alla volta:

```bash
more test-file.txt
```

...con controlli:

- Scorrere riga per riga: *invio*
- Andare alla pagina successiva: *barra spaziatrice*
- Tornare indietro di una pagina: *b*

* Visualizzare le prime 3 righe del file:

```bash
head -3 test-file.txt
```

* Visualizzare le ultime 2 righe del file:

```bash
tail -2 test-file.txt
```