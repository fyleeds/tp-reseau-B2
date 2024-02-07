# TP1 : Premiers pas Docker

Dans ce TP on va appréhender les bases de Docker.

Etant fondamentalement une techno Linux, **vous réaliserez le TP sur une VM Linux** (ou sur votre poste si vous êtes sur Linux).

> *Oui oui les dévs, on utilisera Docker avec vos Windows/MacOS plus tard. Là on va se concentrer sur l'essence du truc.*

![Meo](./docker_macron.jpg)

## Sommaire

- [TP1 : Premiers pas Docker](#tp1--premiers-pas-docker)
  - [Sommaire](#sommaire)
- [0. Setup](#0-setup)
- [I. Init](#i-init)
- [II. Images](#ii-images)
- [III. Docker compose](#iii-docker-compose)

# 0. Setup

➜ **Munissez-vous du [mémo Docker](../../cours/memo/docker.md)**

➜ **Une VM Rocky Linux sitoplé, une seul suffit**

- met lui une carte host-only pour pouvoir SSH dessus
- et une carte NAT pour un accès internet

➜ **Checklist habituelle :**

- [x] IP locale, statique ou dynamique
- [x] hostname défini
- [x] SSH fonctionnel
- [x] accès Internet
- [x] résolution de nom
- [x] SELinux en mode *"permissive"* vérifiez avec `sestatus`, voir [mémo install VM tout en bas](../../cours/memo/install_vm.md)

# I. Init

[Document dédié aux premiers pas Docker.](./init.md)

# II. Images

[Document dédié à la gestion/création d'images Docker.](./image.md)

# III. Docker compose

[Document dédié à l'utilisation de `docker-compose`.](./compose.md)

# I. Init

- [I. Init](#i-init)
  - [1. Installation de Docker](#1-installation-de-docker)
  - [2. Vérifier que Docker est bien là](#2-vérifier-que-docker-est-bien-là)
  - [3. sudo c pa bo](#3-sudo-c-pa-bo)
  - [4. Un premier conteneur en vif](#4-un-premier-conteneur-en-vif)
  - [5. Un deuxième conteneur en vif](#5-un-deuxième-conteneur-en-vif)

## 1. Installation de Docker

Pour installer Docker, il faut **toujours** (comme d'hab en fait) se référer à la doc officielle.

**Je vous laisse donc suivre les instructions de la doc officielle pour installer Docker dans la VM.**

> ***Il n'y a pas d'instructions spécifiques pour Rocky dans la doc officielle**, mais rocky est très proche de CentOS. Vous pouvez donc suivre les instructions pour CentOS 9.*

## 2. Vérifier que Docker est bien là

```bash
# est-ce que le service Docker existe ?
systemctl status docker

# si oui, on le démarre alors
sudo systemctl start docker

# voyons si on peut taper une commande docker
sudo docker info
sudo docker ps
```

## 3. sudo c pa bo

On va faire en sorte que vous puissiez taper des commandes `docker` sans avoir besoin des droits `root`, et donc de `sudo`.

Pour ça il suffit d'ajouter votre utilisateur au groupe `docker`.

> ***Pour que le changement de groupe prenne effet, il faut vous déconnecter/reconnecter de la session SSH** (pas besoin de reboot la machine, pitié).*

🌞 **Ajouter votre utilisateur au groupe `docker`**

- vérifier que vous pouvez taper des commandes `docker` comme `docker ps` sans avoir besoin des droits `root`

```
[fay@router1 ~]$ sudo usermod -aG docker fay

[fay@router1 ~]$ groups fay
fay : fay wheel docker

[fay@router1 ~]$ docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED      STATUS          PORTS                                       NAMES
fa9698c604db   redis     "docker-entrypoint.s…"   6 days ago   Up 32 minutes   0.0.0.0:6379->6379/tcp, :::6379->6379/tcp   reverent_chaum

[fay@router1 ~]$ ^C
```

➜ Vous pouvez même faire un `alias` pour `docker`

Genre si tu trouves que taper `docker` c'est long, et tu préférerais taper `dk` tu peux faire : `alias dk='docker'`. Si tu écris cette commande dans ton fichier `~/.bashrc` alors ce sera effectif dans n'importe quel `bash` que tu ouvriras plutar.

## 4. Un premier conteneur en vif

> *Je rappelle qu'un "conteneur" c'est juste un mot fashion pour dire qu'on lance un processus un peu isolé sur la machine.*

Bon trève de blabla, on va lancer un truc qui juste marche.

On va lancer un conteneur NGINX qui juste fonctionne, puis custom un peu sa conf. Ce serait par exemple pour tester une conf NGINX, ou faire tourner un serveur NGINX de production.

> *Hé les dévs, **jouez le jeu bordel**. NGINX c'est pas votre pote OK, mais on s'en fout, c'est une app comme toutes les autres, comme ta chatroom ou ta calculette. Ou Netflix ou LoL ou Spotify ou un malware. NGINX il est réputé et standard, c'est juste un outil d'étude pour nous là. Faut bien que je vous fasse lancer un truc. C'est du HTTP, c'est full standard, vous le connaissez, et c'est facile à tester/consommer : avec un navigateur.*

🌞 **Lancer un conteneur NGINX**

- avec la commande suivante :

```bash
docker run -d -p 9999:80 nginx
```

```
[fay@router1 ~]$ docker run -d -p 9999:80 nginx
Unable to find image 'nginx:latest' locally
latest: Pulling from library/nginx
af107e978371: Pull complete 
[...]
7b73345df136: Pull complete 
Digest: sha256:bd30b8d47b230de52431cc71c5cce149b8d5d4c87c204902acf2504435d4b4c9
Status: Downloaded newer image for nginx:latest
c1118462d62355089574339966d17b767ed364e2316291fc1a6dc555db32c8b1
```

> Si tu mets pas le `-d` tu vas perdre la main dans ton terminal, et tu auras les logs du conteneur directement dans le terminal. `-d` comme *daemon* : pour lancer en tâche de fond. Essaie pour voir !

🌞 **Visitons**

- vérifier que le conteneur est actif avec une commande qui liste les conteneurs en cours de fonctionnement

```
[fay@router1 ~]$ docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS                                       NAMES
c1118462d623   nginx     "/docker-entrypoint.…"   27 seconds ago   Up 24 seconds   0.0.0.0:9999->80/tcp, :::9999->80/tcp       wonderful_newton
```

- afficher les logs du conteneur

```
[fay@router1 ~]$ docker logs wonderful_newton
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
2023/12/21 10:33:05 [notice] 1#1: using the "epoll" event method
2023/12/21 10:33:05 [notice] 1#1: nginx/1.25.3
2023/12/21 10:33:05 [notice] 1#1: built by gcc 12.2.0 (Debian 12.2.0-14) 
2023/12/21 10:33:05 [notice] 1#1: OS: Linux 4.18.0-425.3.1.el8.x86_64
2023/12/21 10:33:05 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
2023/12/21 10:33:05 [notice] 1#1: start worker processes
2023/12/21 10:33:05 [notice] 1#1: start worker process 29
2023/12/21 10:33:05 [notice] 1#1: start worker process 30
```

- afficher toutes les informations relatives au conteneur avec une commande `docker inspect`

```
[fay@router1 ~]$ docker inspect wonderful_newton
[
    {
        "Id": "c1118462d62355089574339966d17b767ed364e2316291fc1a6dc555db32c8b1",
        "Created": "2023-12-21T10:33:02.773341427Z",
        "Path": "/docker-entrypoint.sh",
        "Args": [
            "nginx",
            "-g",
            "daemon off;"
        ],
        [...]
            "Networks": {
                "bridge": {
                    "IPAMConfig": null,
                    "Links": null,
                    "Aliases": null,
                    "NetworkID": "b63c8ea3a5e87e33f89759dd432dfe629d96f49d3f90ca3480a14f46ffcb42a2",
                    "EndpointID": "4ecd9a20917c9d1c0dca7bef1a5e1bb187a2f6f5ae0360e9bf9c67a5ac617a47",
                    "Gateway": "172.17.0.1",
                    "IPAddress": "172.17.0.3",
                    "IPPrefixLen": 16,
                    "IPv6Gateway": "",
                    "GlobalIPv6Address": "",
                    "GlobalIPv6PrefixLen": 0,
                    "MacAddress": "02:42:ac:11:00:03",
                    "DriverOpts": null
                }
            }
        }
    }
]
```
- afficher le port en écoute sur la VM avec un `sudo ss -lnpt`

```
[fay@router1 ~]$ sudo ss -lnpt
[sudo] password for fay: 
State   Recv-Q   Send-Q     Local Address:Port      Peer Address:Port  Process                                                                                                           
LISTEN  0        2048             0.0.0.0:9999           0.0.0.0:*      users:(("docker-proxy",pid=51465,fd=4))                                       
LISTEN  0        128              0.0.0.0:22             0.0.0.0:*      users:(("sshd",pid=19878,fd=3))                                                                       
LISTEN  0        2048                [::]:9999              [::]:*      users:(("docker-proxy",pid=51471,fd=4))                                       
LISTEN  0        128                 [::]:22                [::]:*      users:(("sshd",pid=19878,fd=4))
```
- ouvrir le port `9999/tcp` (vu dans le `ss` au dessus normalement) dans le firewall de la VM
```

[fay@router1 ~]$ sudo firewall-cmd --add-port=9999/tcp --permanent
success
```

- depuis le navigateur de votre PC, visiter le site web sur `http://IP_VM:9999`

```
PS C:\Users\clemc> curl 10.1.1.254:9999


StatusCode        : 200
StatusDescription : OK
Content           : <!DOCTYPE html>
                    <html>
                    <head>
                    <title>Welcome to nginx!</title>
                    <style>
                    html { color-scheme: light dark; }
                    body { width: 35em; margin: 0 auto;
                    font-family: Tahoma, Verdana, Arial, sans-serif; }
                    </style...
RawContent        : HTTP/1.1 200 OK
                    Connection: keep-alive
                    Accept-Ranges: bytes
                    Content-Length: 615
                    Content-Type: text/html
                    Date: Thu, 21 Dec 2023 10:40:15 GMT
                    ETag: "6537cac7-267"
                    Last-Modified: Tue, 24 Oct 2023 ...
Forms             : {}
Headers           : {[Connection, keep-alive], [Accept-Ranges, bytes], [Content-Length, 615], [Content-Type, text/html]...}
Images            : {}
InputFields       : {}
Links             : {@{innerHTML=nginx.org; innerText=nginx.org; outerHTML=<A href="http://nginx.org/">nginx.org</A>; outerText=nginx.org;
                    tagName=A; href=http://nginx.org/}, @{innerHTML=nginx.com; innerText=nginx.com; outerHTML=<A
                    href="http://nginx.com/">nginx.com</A>; outerText=nginx.com; tagName=A; href=http://nginx.com/}}
ParsedHtml        : mshtml.HTMLDocumentClass
RawContentLength  : 615
```


➜ On peut préciser genre mille options au lancement d'un conteneur, **go `docker run --help` pour voir !**

➜ Hop, on en profite pour voir un truc super utile avec Docker : le **partage de fichiers au moment où on `docker run`**

- en effet, il est possible de partager un fichier ou un dossier avec un conteneur, au moment où on le lance
- avec NGINX par exemple, c'est idéal pour déposer un fichier de conf différent à chaque conteneur NGINX qu'on lance
  - en plus NGINX inclut par défaut tous les fichiers dans `/etc/nginx/conf.d/*.conf`
  - donc suffit juste de drop un fichier là-bas
- ça se fait avec `-v` pour *volume* (on appelle ça "monter un volume")

> *C'est aussi idéal pour créer un conteneur qui setup un environnement de dév par exemple. On prépare une image qui contient Python + les libs Python qu'on a besoin, et au moment du `docker run` on partage notre code. Ainsi, on peut dév sur notre PC, et le code s'exécute dans le conteneur. On verra ça plus tard les dévs !*

🌞 **On va ajouter un site Web au conteneur NGINX**

- créez un dossier `nginx`
  - pas n'importe où, c'est ta conf caca, c'est dans ton homedir donc `/home/<TON_USER>/nginx/`
- dedans, deux fichiers : `index.html` (un site nul) `site_nul.conf` (la conf NGINX de notre site nul)
- exemple de `index.html` :

```html
<h1>MEOOOW</h1>
```

- config NGINX minimale pour servir un nouveau site web dans `site_nul.conf` :

```nginx
server {
    listen        8080;

    location / {
        root /var/www/html/index.html;
    }
}
```

- lancez le conteneur avec la commande en dessous, notez que :
  - on partage désormais le port 8080 du conteneur (puisqu'on l'indique dans la conf qu'il doit écouter sur le port 8080)
  - on précise les chemins des fichiers en entier
  - note la syntaxe du `-v` : à gauche le fichier à partager depuis ta machine, à droite l'endroit où le déposer dans le conteneur, séparés par le caractère `:`
  - c'est long putain comme commande

```bash
docker run -d -p 9999:8080 -v /home/fay/nginx/index.html:/var/www/html/index.html -v /home/fay/nginx/site_nul.conf:/etc/nginx/conf.d/site_nul.conf nginx
```

🌞 **Visitons**

- vérifier que le conteneur est actif
```

[fay@router1 nginx]$ docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS             PORTS                                               NAMES
a21e6aa430d7   nginx     "/docker-entrypoint.…"   6 seconds ago   Up 4 seconds       80/tcp, 0.0.0.0:9999->8080/tcp, :::9999->8080/tcp   vigorous_benz
```

- aucun port firewall à ouvrir : on écoute toujours port 9999 sur la machine hôte (la VM)
- visiter le site web depuis votre PC

```
9S C:\Users\clemc>


StatusCode        : 200
StatusDescription : OK
Content           : <h1>Hello<h1>

RawContent        : HTTP/1.1 200 OK
                    Connection:
                    keep-alive
                    Accept-Ranges:
                    bytes
                    Content-Length:
                    14
                    Content-Type:
                    text/html
                    Date: Thu, 21
                    Dec 2023
                    11:03:19 GMT
                    ETag:
                    "6584171d-e"
                    Last-Modified:
                    Thu, 21 Dec 2023
                    10:...
Forms             : {}
Headers           : {[Connection,
                    keep-alive],
                    [Accept-Ranges,
                    bytes],
                    [Content-Length,
                    14],
                    [Content-Type,
                    text/html]...}
Images            : {}
InputFields       : {}
Links             : {}
ParsedHtml        : mshtml.HTMLDocume
                    ntClass
RawContentLength  : 14
```

## 5. Un deuxième conteneur en vif

Cette fois on va lancer un conteneur Python, comme si on voulait tester une nouvelle lib Python par exemple. Mais sans installer ni Python ni la lib sur notre machine.

On va donc le lancer de façon interactive : on lance le conteneur, et on pop tout de suite un shell dedans pour faire joujou.

🌞 **Lance un conteneur Python, avec un shell**

- il faut indiquer au conteneur qu'on veut lancer un shell
- un shell c'est "interactif" : on saisit des trucs (input) et ça nous affiche des trucs (output)
  - il faut le préciser dans la commande `docker run` avec `-it`
- ça donne donc :

```bash
# on lance un conteneur "python" de manière interactive
# et on demande à ce conteneur d'exécuter la commande "bash" au démarrage
docker run -it python bash
```

> *Ce conteneur ne vit (comme tu l'as demandé) que pour exécuter ton `bash`. Autrement dit, si ce `bash` se termine, alors le conteneur s'éteindra. Autrement diiiit, si tu quittes le `bash`, le processus `bash` va se terminer, et le conteneur s'éteindra. C'est vraiment un conteneur one-shot quoi quand on utilise `docker run` comme ça.*

🌞 **Installe des libs Python**

- une fois que vous avez lancé le conteneur, et que vous êtes dedans avec `bash`
- installez deux libs, elles ont été choisies complètement au hasard (avec la commande `pip install`):
  - `aiohttp`
  - `aioconsole`

```
root@81a5c02c97de:/# pip install aiohttp aioconsole
Collecting aiohttp
  Obtaining dependency information for aiohttp from https://files.pythonhosted.org/packages/75/5f/90a2869ad3d1fb9bd984bfc1b02d8b19e381467b238bd3668a09faa69df5/aiohttp-3.9.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata
  Downloading aiohttp-3.9.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (7.4 kB)
Collecting aioconsole
  Obtaining dependency information for aioconsole from https://files.pythonhosted.org/packages/f7/39/b392dc1a8bb58342deacc1ed2b00edf88fd357e6fdf76cc6c8046825f84f/aioconsole-0.7.0-py3-none-any.whl.metadata
  Downloading aioconsole-0.7.0-py3-none-any.whl.metadata (5.3 kB)
[...]
Successfully built multidict
Installing collected packages: multidict, idna, frozenlist, attrs, aioconsole, yarl, aiosignal, aiohttp
Successfully installed aioconsole-0.7.0 aiohttp-3.9.1 aiosignal-1.3.1 attrs-23.1.0 frozenlist-1.4.1 idna-3.6 multidict-6.0.4 yarl-1.9.4
```
- tapez la commande `python` pour ouvrir un interpréteur Python
- taper la ligne `import aiohttp` pour vérifier que vous avez bien téléchargé la lib

> *Notez que la commande `pip` est déjà présente. En effet, c'est un conteneur `python`, donc les mecs qui l'ont construit ont fourni la commande `pip` avec !*

➜ **Tant que t'as un shell dans un conteneur**, tu peux en profiter pour te balader. Tu peux notamment remarquer :

- si tu fais des `ls` un peu partout, que le conteneur a sa propre arborescence de fichiers
- si t'essaies d'utiliser des commandes usuelles un poil évoluées, elles sont pas là
  - genre t'as pas `ip a` ou ce genre de trucs
  - un conteneur on essaie de le rendre le plus léger possible
  - donc on enlève tout ce qui n'est pas nécessaire par rapport à un vrai OS
  - juste une application et ses dépendances
