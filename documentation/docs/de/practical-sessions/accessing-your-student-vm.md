# Zugriff auf Ihre Studenten-VM

!!! abstract "Lernziele"

    Am Ende dieser praktischen Sitzung werden Sie in der Lage sein:

    - auf Ihre Studenten-VM über SSH und WinSCP zuzugreifen
    - zu überprüfen, ob die erforderliche Software für die praktischen Übungen installiert ist
    - zu überprüfen, ob Sie Zugriff auf Übungsmaterialien für diese Schulung auf Ihrer lokalen Studenten-VM haben

## Einführung

Im Rahmen lokaler wis2box-Schulungssitzungen können Sie auf Ihre persönliche Studenten-VM im lokalen Schulungsnetzwerk mit dem Namen "WIS2-training" zugreifen.

Auf Ihrer Studenten-VM ist folgende Software vorinstalliert:

- Ubuntu 22.0.4.3 LTS [ubuntu-22.04.3-live-server-amd64.iso](https://releases.ubuntu.com/jammy/ubuntu-22.04.3-live-server-amd64.iso)
- Python 3.10.12
- Docker 24.0.6
- Docker Compose 2.21.0
- Texteditoren: vim, nano

!!! note

    Wenn Sie diese Schulung außerhalb einer lokalen Schulungssitzung durchführen möchten, können Sie Ihre eigene Instanz über einen beliebigen Cloud-Anbieter bereitstellen, zum Beispiel:

    - GCP (Google Cloud Platform) VM-Instanz `e2-medium`
    - AWS (Amazon Web Services) ec2-Instanz `t3a.medium` 
    - Azure (Microsoft) Azure Virtual Machine `standard_b2s`

    Wählen Sie Ubuntu Server 22.0.4 LTS als Betriebssystem.
    
    Stellen Sie nach dem Erstellen Ihrer VM sicher, dass Sie Python, Docker und Docker Compose installiert haben, wie unter [wis2box-software-dependencies](https://docs.wis2box.wis.wmo.int/en/latest/user/getting-started.html#software-dependencies) beschrieben.
    
    Das Release-Archiv für wis2box, das in dieser Schulung verwendet wird, kann wie folgt heruntergeladen werden:

    ```bash
    wget https://github.com/wmo-im/wis2box/releases/download/1.0.0rc1/wis2box-setup-1.0.0rc1.zip
    unzip wis2box-setup-1.0.0rc1.zip
    ```
    
    Das neueste 'wis2box-setup'-Archiv finden Sie immer unter [https://github.com/wmo-im/wis2box/releases](https://github.com/wmo-im/wis2box/releases).

    Das in dieser Schulung verwendete Übungsmaterial kann wie folgt heruntergeladen werden:

    ```bash
    wget https://training.wis2box.wis.wmo.int/exercise-materials.zip
    unzip exercise-materials.zip
    ```

    Die folgenden zusätzlichen Python-Pakete sind erforderlich, um die Übungsmaterialien auszuführen:

    ```bash
    pip3 install minio
    ```

    Wenn Sie die während lokaler WIS2-Schulungssitzungen bereitgestellte Studenten-VM verwenden, ist die erforderliche Software bereits installiert.

## Verbindung zu Ihrer Studenten-VM im lokalen Schulungsnetzwerk herstellen

Verbinden Sie Ihren PC mit dem lokalen WLAN, das während der WIS2-Schulung im Raum ausgestrahlt wird, gemäß den Anweisungen des Trainers.

Verwenden Sie einen SSH-Client, um eine Verbindung zu Ihrer Studenten-VM herzustellen, mit folgenden Angaben:

- **Host: (wird während der Präsenzschulung bereitgestellt)**
- **Port: 22**
- **Benutzername: (wird während der Präsenzschulung bereitgestellt)**
- **Passwort: (wird während der Präsenzschulung bereitgestellt)**

!!! tip
    Wenden Sie sich an einen Trainer, wenn Sie sich bezüglich des Hostnamens/Benutzernamens nicht sicher sind oder Probleme bei der Verbindung haben.

Sobald Sie verbunden sind, ändern Sie bitte Ihr Passwort, um sicherzustellen, dass andere nicht auf Ihre VM zugreifen können:

```bash
limper@student-vm:~$ passwd
Changing password for testuser.
Current password:
New password:
Retype new password:
passwd: password updated successfully
```

## Überprüfen der Softwareversionen

Um wis2box ausführen zu können, sollten auf der Studenten-VM Python, Docker und Docker Compose vorinstalliert sein.

Python-Version überprüfen:
```bash
python3 --version
```
gibt zurück:
```console
Python 3.10.12
```

Docker-Version überprüfen:
```bash
docker --version
```
gibt zurück:
```console
Docker version 24.0.6, build ed223bc
```

Docker Compose-Version überprüfen:
```bash
docker compose version
```
gibt zurück:
```console
Docker Compose version v2.21.0
```

Um sicherzustellen, dass Ihr Benutzer Docker-Befehle ausführen kann, wurde Ihr Benutzer zur Gruppe `docker` hinzugefügt.

Um zu testen, ob Ihr Benutzer docker hello-world ausführen kann, führen Sie den folgenden Befehl aus:
```bash
docker run hello-world
```

Dies sollte das hello-world-Image herunterladen und einen Container ausführen, der eine Nachricht ausgibt.

Überprüfen Sie, ob Sie Folgendes in der Ausgabe sehen:

```console
...
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

## Überprüfen der Übungsmaterialien

Überprüfen Sie den Inhalt Ihres Home-Verzeichnisses; dies sind die Materialien, die im Rahmen der Schulung und der praktischen Sitzungen verwendet werden.

```bash
ls ~/
```
gibt zurück:
```console
exercise-materials  wis2box-1.0.0rc1
```

Wenn Sie WinSCP auf Ihrem lokalen PC installiert haben, können Sie es verwenden, um eine Verbindung zu Ihrer Studenten-VM herzustellen und den Inhalt Ihres Home-Verzeichnisses zu überprüfen sowie Dateien zwischen Ihrer VM und Ihrem lokalen PC hoch- oder herunterzuladen.

WinSCP ist für die Schulung nicht erforderlich, kann aber nützlich sein, wenn Sie Dateien auf Ihrer VM mit einem Texteditor auf Ihrem lokalen PC bearbeiten möchten.

So können Sie eine Verbindung zu Ihrer Studenten-VM mit WinSCP herstellen:

Öffnen Sie WinSCP und klicken Sie auf "Neue Site". Sie können wie folgt eine neue SCP-Verbindung zu Ihrer VM erstellen:

<img alt="winscp-student-vm-scp.png" src="../../assets/img/winscp-student-vm-scp.png" width="400">

Klicken Sie auf 'Speichern' und dann auf 'Anmelden', um eine Verbindung zu Ihrer VM herzustellen.

Sie sollten dann den folgenden Inhalt sehen können:

<img alt="winscp-student-vm-exercise-materials.png" src="../../assets/img/winscp-student-vm-exercise-materials.png" width="600">

## Fazit

!!! success "Herzlichen Glückwunsch!"
    In dieser praktischen Sitzung haben Sie gelernt, wie Sie:

    - auf Ihre Studenten-VM über SSH und WinSCP zugreifen
    - überprüfen, ob die erforderliche Software für die praktischen Übungen installiert ist
    - überprüfen, ob Sie Zugriff auf Übungsmaterialien für diese Schulung auf Ihrer lokalen Studenten-VM haben