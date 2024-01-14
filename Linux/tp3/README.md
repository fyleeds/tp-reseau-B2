
# Monitoring_Server

Le service de monitoring de serveur surveille et analyse toutes les 24 heures l'état et les performances d'un serveur. Il vérifie divers paramètres tels que l'utilisation du CPU, de la mémoire, de l'espace disque, les performances du réseau, ainsi que la disponibilité et l'état des ports TCP ouverts par des applications et services exécutés sur le serveur. Cela aide à maintenir une performance optimale et à assurer la disponibilité des services et des applications hébergés sur le serveur.

## Installation

Avant d'installer Monitoring_Server, assurez-vous d'avoir les prérequis suivants :

- Python 3.6 ou supérieur
- Pip l'installateur de packet python

Pour installer Monitoring_Server, exécutez les commandes suivantes :

```bash
git clone https://github.com/fyleeds/monitoring_server.git
cd monitoring_server 
pip3 install -r requirements.txt
cd monitor/main
```
**IMPORTANT ETRE DANS LE "MAIN" pour executez commande**

**TOUS LES FICHIERS SUIVANTS DONNES SONT RETROUVABLES DANS LE DOSSIER SAVE_CONFIG A LA RACINE DU DOSSIER CLONE**

### Créer le script backup_monit.sh

```
nano /usr/local/bin/backup_script.sh
```

```
#!/bin/bash

# Changez pour le répertoire contenant votre script Python
cd /home/user/monitoring_server/monitor/main

# Exécutez le script Python
python3 monit.py -check

# Si vous avez besoin de passer des arguments au script Python, vous pouvez les ajouter après le nom du fichier
# python3 monit.py arg1 arg2
```
**VEUILLEZ CHANGER SVP LE CHEMIN PAR DEFAUT DANS LE SCRIPT !**
```
sudo chmod +x /usr/local/bin/backup_script.sh
```
### Créer le Service backup.service
```

sudo nano /etc/systemd/system/backup.service

```
```
[Unit]
Description=Service de sauvegarde quotidienne

[Service]
ExecStart=/usr/local/bin/backup_script.sh

[Install]
WantedBy=multi-user.target
```
### Créer le timer
```

sudo nano /etc/systemd/system/backup.timer

```
```

[Unit]
Description=Timer pour le service de sauvegarde quotidienne

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target

```
```

sudo systemctl enable backup.timer
sudo systemctl start backup.timer

```
```

sudo systemctl status backup.timer

```
**SI ACTIF ALORS OK !**

### Permission user
```

sudo chown user:user /usr/local/bin/backup_script.sh

```
```

sudo chown -R user:user /var/log/monit/

```
```

sudo chown -R user:user /var/monit/

```
```

sudo chown -R user:user /etc/monit/

```

## Usage

Pour utiliser Monitoring_Server, vous pouvez commencer par afficher l'aide :

```bash
python3 monit.py -h
```
```bash
[user@user main]$ python3 monit.py -h
usage: monit.py [-h] [-get_avg GET_AVG] [-check] [-list] [-last]

optional arguments:
  -h, --help        show this help message and exit
  -get_avg GET_AVG  Writes a report_average file saved in the folder
                    /var/reports_average based on the reports created
                    in the number hours you have given as argument (must be a
                    int), when no argument given write an average report based
                    on 1 hour
  -check            Write a report saved in the folder /var/reports/
                    recording theses values with specific units : CPU Metrics:
                    cpuTimeUser, cpuTimeSystem, cpuTimeIdle: Seconds;
                    cpuPercent: Percentage; cpuCount: Count; cpuStats -
                    ctx_switches, interrupts, soft_interrupts, syscalls:
                    Count; cpuFreq - current, min, max: MHz; loadAvg - 1min
                    5min 15min: Load Average; RAM Metrics: totalMemory,
                    availableMemory, cacheBuffers, cache: Bytes;
                    usedMemoryPercent: Percentage; Network Metrics: tcp - Port
                    numbers: Boolean status true/false; Disk Information:
                    totalSpace, usedSpace, freeSpace: Bytes; readSpeed,
                    writeSpeed: MB/s Megabytes per second or IOPS
  -list             List all reports
  -last             Send the last report

```
### Logs

Recuperable dans le fichier `/var/log/monit/monit.log` pour lire les dernières actions effectués

### Exemple d'Utilisation Simple

Voici un exemple simple de sauvegarde de rapport de Monitoring_Server :

```bash
python3 monit.py -check
```
```bash
[user@user main]$ python3 monit.py -check
Report file created at /var/monit/reports/report_monit_e7632170-b512-4120-8ff0-682346acc531_14-01-2024_23-48-40.json
```
## Configuration

*Monitoring_Server* peut être configuré en modifiant le fichier `monit_conf.json` dans le dossier `/etc/monit/monit_conf.json`. Voici un exemple de ce que vous pouvez y mettre **(ATTENTION PORTS TCP SEULEMENT)**:

```json
{
    "ports": {
                "web": 80,
                "ssh": 22
             }
}
```

- on précise la liste des ports TCP à surveiller
- si la connexion TCP fonctionne, c'est que le port est actif, on retourne True
- sinon False
