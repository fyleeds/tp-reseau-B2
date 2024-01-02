# III. Docker compose

Pour la fin de ce TP on va manipuler un peu `docker compose`.

🌞 **Créez un fichier `docker-compose.yml`**

- dans un nouveau dossier dédié `/home/<USER>/compose_test`
- le contenu est le suivant :

```yml
version: "3"

services:
  conteneur_nul:
    image: debian
    entrypoint: sleep 9999
  conteneur_flopesque:
    image: debian
    entrypoint: sleep 9999
```
```
[fay@router1 ~]$ mkdir compose_test
[fay@router1 ~]$ nano /compose_test/docker-compose.yml
```

Ce fichier est parfaitement équivalent à l'enchaînement de commandes suivantes (*ne les faites pas hein*, c'est juste pour expliquer) :

```bash
$ docker network create compose_test

```

```
[fay@router1 ~]$ docker network create compose_test
31557264f8dfbcac70356a3d66b2c4b3d18118c298c4c8110004bbad2804b521
```
```
$ docker run -d --name conteneur_nul --network compose_test debian sleep 9999
$ docker run -d --name conteneur_flopesque --network compose_test debian sleep 9999
```
```
[fay@router1 ~]$ docker run -d --name conteneur_flopesque --network compose_test debian sleep 9999
43f6a8d6c9961ff045fc33edf44a7d054cf2a6eb8e45f36fdf915fb2f5882664
```


🌞 **Lancez les deux conteneurs** avec `docker compose`

- déplacez-vous dans le dossier `compose_test` qui contient le fichier `docker-compose.yml`
- go exécuter `docker compose up -d`

> Si tu mets pas le `-d` tu vas perdre la main dans ton terminal, et tu auras les logs des deux conteneurs. `-d` comme *daemon* : pour lancer en tâche de fond.
```
[fay@router1 compose_test]$ [fay@router1 compose_test]$ docker compose up -d
[+] Running 3/3
 ✔ Network compose_test_default                  Created                                                                                         0.8s
 ✔ Container compose_test-conteneur_nul-1        Started                                                                                         0.1s
 ✔ Container compose_test-conteneur_flopesque-1  Started   
```
🌞 **Vérifier que les deux conteneurs tournent**

- toujours avec une commande `docker`
- tu peux aussi use des trucs comme `docker compose ps` ou `docker compose top` qui sont cools dukoo
  - `docker compose --help` pour voir les bails

```
[fay@router1 compose_test]$ docker compose ps
NAME                                 IMAGE     COMMAND        SERVICE               CREATED              STATUS              PORTS
compose_test-conteneur_flopesque-1   debian    "sleep 9999"   conteneur_flopesque   About a minute ago   Up About a minute
compose_test-conteneur_nul-1         debian    "sleep 9999"   conteneur_nul         About a minute ago   Up About a minute
```

🌞 **Pop un shell dans le conteneur `conteneur_nul`**

- référez-vous au mémo Docker

`docker exec -it conteneur_nul sh`

- effectuez un `ping conteneur_flopesque` (ouais ouais, avec ce nom là)
  - un conteneur est aussi léger que possible, aucun programme/fichier superflu : t'auras pas la commande `ping` !
  - il faudra installer un paquet qui fournit la commande `ping` pour pouvoir tester
  - juste pour te faire remarquer que les conteneurs ont pas besoin de connaître leurs IP : les noms fonctionnent

```
apt update and apt install iputils-ping
root@3ebc72ae7c8c:/# ping conteneur_flopesque
PING conteneur_flopesque (172.18.0.3) 56(84) bytes of data.
64 bytes from conteneur_flopesque.compose_test (172.18.0.3): icmp_seq=1 ttl=64 time=2.85 ms
64 bytes from conteneur_flopesque.compose_test (172.18.0.3): icmp_seq=2 ttl=64 time=0.105 ms
```


![In the future](./img/in_the_future.jpg)
