# II. You say dev I say good practices

- [II. You say dev I say good practices](#ii-you-say-dev-i-say-good-practices)
  - [1. Args](#1-args)
  - [2. Logs](#2-logs)
    - [A. Logs serveur](#a-logs-serveur)
    - [B. Logs client](#b-logs-client)
    - [C. NOTE IMPORTANTE](#c-note-importante)

## 1. Args

Je veux une vraie gestion d'arguments et d'options sur le serveur ! C'est à dire que quand on lance la commande pour exécuter le serveur, j'aimerai pouvoir préciser sur la ligne de commande le port où je souhaite écouter.

C'est à dire, par exemple, si je veux lancer le serveur pour qu'il écoute sur le port 8888 TCP, j'aimerai pouvoir taper :

```bash
python bs_server.py -p 8888
```

**On utilise [la lib `argparse`](../../../../cours/dev/argparse/README.md) pour faire ça bien en Python !**

🌞 **`bs_server_II1.py`**

- gère l'option `-p` ou `--port`
  - ne tolère qu'un entier passé en argument
  - si c'est inférieur à 0 ou supérieur à 65535
    - afficher `ERROR Le port spécifié n'est pas un port possible (de 0 à 65535).` 
    - quitter avec le code retour 1
  - si c'est entre 0 et 1024 compris
    - afficher `ERROR Le port spécifié est un port privilégié. Spécifiez un port au dessus de 1024.`
    - quitter avec le code retour 2
  - si `-p` n'est pas utilisé, alors le port par défaut c'est `13337`
- gère l'option `-h` ou `--help`
  - affiche un petit help de la commande
  - le format du help doit respecter le format standard avec une ligne de `usage` et la liste des options possibles avec leur utilité
  - inspirez-vous de la sortie de `ls --help`

On devra donc pouvoir faire :

```
$ python bs_server_II1.py -p 8888
```

## 2. Logs

**Allô les dévs ? Ici it4 l'admin qui vous parle. Ils sont où les ptain de logs de votre application bowdel.**

![No logs](../img/nologs.jpg)

Ce qu'on ~~voudrait~~ veut :

➜ **des logs serveur**

- dans la console
- dans un fichier de log

➜ **des logs client**

- PAS dans la console : c'est le client, c'est un moldu, on lui montre R
- dans un fichier de log

---

Chaque ligne de log :

- **doit être *timestamped***
  - préfixée par date et heure, dans un format standard si possible
- **doit être nivelée**
  - je viens d'inventer le terme
  - c'est à dire que vous préciser un niveau de logging

Il existe des standards sur les niveaux de log en informatique. Les trois en gras sont les plus utilisés. En haut le plus critique, en bas, le moins :

- Emergency
- Alert
- Critical
- **Error** : ERROR ou ERR en rouge
- **Warning** : WARNING ou WARN en jaune
- Notice
- **Informational** : INFO en blanc
- Debug

**Toutes les lignes de log de ce TP devront être au format suivant :**

```
yyyy-mm-dd hh:mm:ss LEVEL message
```

Par exemple :

```
2023-11-03 03:43:21 INFO Un client vient de se co et son IP c'est <CLIENT_IP>.
```

### A. Logs serveur

Le serveur va log chacune des actions à la fois dans la console, et aussi dans un fichier.

Ce fichier il est pas à n'importe quel endroit si on utilise un système GNU/Linux, un dossier est dédié aux logs : `/var/log/`.  
On peut donc créer là-bas un sous-dossier pour notre application, et on stocke dedans le fichier de log de notre application.

Vous pouvez faire ça à la main, ou utiliser [**la librairie `logger`**](https://realpython.com/python-logging/), vous êtes libres pour le moment ! (`logger` c'est le feu quand même).

🌞 **`bs_server_II2A.py`**

- ce qui doit générer une ligne de log :
  - `INFO` lancement du serveur
    - `Le serveur tourne sur <IP>:<port>`
  - `INFO` connexion d'un client
    - l'IP du client doit apparaître dans la ligne de log
    - `Un client <IP_CLIENT> s'est connecté.`
  - `INFO` message reçu d'un client
    - `Le client <IP_CLIENT> a envoyé <MESSAGE>.`
  - `INFO` message envoyé par le serveur
    - `Réponse envoyée au client <IP_CLIENT> : <MESSAGE>.`
  - `WARN` aucun client connecté depuis + de 1 minute
    - le message : `Aucun client depuis plus de une minute.`
    - il doit apparaître toutes les minutes si personne ne se co
- en console
  - le mot-clé `INFO` doit apparaître en blanc
  - le mot clé `WARN` doit apparaître en jaune
- dans un fichier
  - le fichier doit être `/var/log/bs_server/bs_server.log`
  - le créer en amont si nécessaire, précisez la(les) commande(s) dans le compte-rendu

```
mkdir -p /var/log/bs_server/
cd var/log/bs_server/
nano bs_server.log
```

### B. Logs client

Les logs du client, c'est que dans un fichier. En effet, que ce soit une app console ou graphique, le client on veut lui montrer que ce qui est directement lié à SON utilisation de l'application. Et pas le reste.   
Donc on lui jette pas les logs et des vilaines erreurs au visage, ni 14000 messages informatifs.

Je vous laisse choisir l'emplacement du fichier de log de façon **pertinente**.

🌞 **`bs_client_II2B.py`**

- ce qui doit générer une ligne de log :
  - `INFO` connexion réussie à un serveur
    - `Connexion réussie à <IP>:<PORT>.`
  - `INFO` message envoyé par le client
    - `Message envoyé au serveur <IP_SERVER> : <MESSAGE>.`
  - `INFO` message reçu du serveur
    - `Réponse reçue du serveur <IP_SERVER> : <MESSAGE>.`
  - `ERROR` connexion au serveur échouée
    - pour le tester, il suffit de lancer le client alors que le serveur est éteint !
    - le message : `Impossible de se connecter au serveur <IP_SERVER> sur le port <PORT>.`
- en console
  - affiche juste `ERROR Impossible de se connecter au serveur <IP_SERVER> sur le port <PORT>.` en rouge quand ça fail (pas de timestamp là)
  - les messages de niveau INFO ne sont pas visibles dans la console du client
- dans un fichier
  - `<DOSSIER_DE_LOG>/bs_client.log`

```
mkdir -p /var/log/bs_client/
cd var/log/bs_client/
nano bs_client.log
```

### C. NOTE IMPORTANTE

**A partir de maintenant, vous savez gérer des logs à peu près proprement.**

Vous allez dév plusieurs machins en cours, vous devrez utiliser exactement la même méthode que précédemment pour générer les logs : timestamp, niveau de log, message, stocké dans un fichier précis etc.
