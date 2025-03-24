# Linux-Spickzettel

## Überblick

Die grundlegenden Konzepte der Arbeit in einem Linux-Betriebssystem sind **Dateien** und **Verzeichnisse** (Ordner), die in einer Baumstruktur innerhalb einer **Umgebung** organisiert sind.

Sobald Sie sich bei einem Linux-System anmelden, arbeiten Sie in einer **Shell**, in der Sie mit Dateien und Verzeichnissen arbeiten können, indem Sie Befehle ausführen, die auf dem System installiert sind. Die Bash-Shell ist eine gängige und beliebte Shell, die typischerweise auf Linux-Systemen zu finden ist.

## Bash

### Verzeichnisnavigation

* Eingabe eines absoluten Verzeichnispfads:

```bash
cd /dir1/dir2
```

* Eingabe eines relativen Verzeichnispfads:

```bash
cd ./somedir
```

* Ein Verzeichnis nach oben wechseln:

```bash
cd ..
```

* Zwei Verzeichnisse nach oben wechseln:

```bash
cd ../..
```

* Zum "Home"-Verzeichnis wechseln:

```bash
cd -
```

### Dateiverwaltung

* Dateien im aktuellen Verzeichnis auflisten:

```bash
ls
```

* Dateien im aktuellen Verzeichnis mit mehr Details auflisten:

```bash
ls -l
```

* Das Wurzelverzeichnis des Dateisystems auflisten:

```bash
ls -l /
```

* Eine leere Datei erstellen:

```bash
touch foo.txt
```

* Eine Datei mit dem `echo`-Befehl erstellen:

```bash
echo "hi there" > test-file.txt
```

* Den Inhalt einer Datei anzeigen:

```bash
cat test-file.txt
```

* Eine Datei kopieren:

```bash
cp file1 file2
```

* Platzhalter: Mit Dateimustern arbeiten:

```bash
ls -l fil*  # passt auf file1 und file2
```

* Zwei Dateien zu einer neuen Datei namens `newfile` zusammenfügen:

```bash
cat file1 file2 > newfile
```

* Eine weitere Datei an `newfile` anhängen:

```bash
cat file3 >> newfile
```

* Eine Datei löschen:

```bash
rm newfile
```

* Alle Dateien mit der gleichen Dateierweiterung löschen:

```bash
rm *.dat
```

* Ein Verzeichnis erstellen:

```bash
mkdir dir1
```

### Befehle mit Pipes verketten

Pipes ermöglichen es einem Benutzer, die Ausgabe eines Befehls an einen anderen zu senden, indem das Pipe-Symbol `|` verwendet wird:

```bash
echo "hi" | sed 's/hi/bye/'
```

* Befehlsausgaben mit grep filtern:

```bash
echo "id,title" > test-file.txt
echo "1,birds" >> test-file.txt
echo "2,fish" >> test-file.txt
echo "3,cats" >> test-file.txt

cat test-file.txt | grep fish
```

* Groß-/Kleinschreibung ignorieren:

```bash
grep -i FISH test-file.txt
```

* Übereinstimmende Zeilen zählen:

```bash
grep -c fish test-file.txt
```

* Ausgaben zurückgeben, die das Schlüsselwort nicht enthalten:

```bash
grep -v birds test-file.txt
```

* Die Anzahl der Zeilen in `test-file.txt` zählen:

```bash
wc -l test-file.txt
```

* Ausgabe seitenweise anzeigen:

```bash
more test-file.txt
```

...mit Steuerungsmöglichkeiten:

- Zeilenweise nach unten scrollen: *Enter*
- Zur nächsten Seite gehen: *Leertaste*
- Eine Seite zurückgehen: *b*

* Die ersten 3 Zeilen der Datei anzeigen:

```bash
head -3 test-file.txt
```

* Die letzten 2 Zeilen der Datei anzeigen:

```bash
tail -2 test-file.txt
```