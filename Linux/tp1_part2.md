# II. Images

- [II. Images](#ii-images)
  - [1. Images publiques](#1-images-publiques)
  - [2. Construire une image](#2-construire-une-image)

## 1. Images publiques

🌞 **Récupérez des images**

- avec la commande `docker pull`
- récupérez :
  - l'image `python` officielle en version 3.11 (`python:3.11` pour la dernière version)
  - l'image `mysql` officielle en version 5.7
  - l'image `wordpress` officielle en dernière version
    - c'est le tag `:latest` pour récupérer la dernière version
    - si aucun tag n'est précisé, `:latest` est automatiquement ajouté
  - l'image `linuxserver/wikijs` en dernière version
    - ce n'est pas une image officielle car elle est hébergée par l'utilisateur `linuxserver` contrairement aux 3 précédentes
    - on doit donc avoir un moins haut niveau de confiance en cette image

```
[fay@router1 ~]$ docker pull python
Using default tag: latest
latest: Pulling from library/python
Digest: sha256:3733015cdd1bd7d9a0b9fe21a925b608de82131aa4f3d397e465a1fcb545d36f
Status: Image is up to date for python:latest
docker.io/library/python:latest
[fay@router1 ~]$ docker pull wordpress
Using default tag: latest
latest: Pulling from library/wordpress
af107e978371: Already exists 
6480d4ad61d2: Pull complete 
[...] 
87728bbad961: Pull complete 
Digest: sha256:ffabdfe91eefc08f9675fe0e0073b2ebffa8a62264358820bcf7319b6dc09611
Status: Downloaded newer image for wordpress:latest
docker.io/library/wordpress:latest
[fay@router1 ~]$ docker pull mysql
Using default tag: latest
latest: Pulling from library/mysql
bce031bc522d: Pull complete 
[...] 
7320aa32bf42: Pull complete 
Digest: sha256:4ef30b2c11a3366d7bb9ad95c70c0782ae435df52d046553ed931621ea36ffa5
Status: Downloaded newer image for mysql:latest
docker.io/library/mysql:latest
[fay@router1 ~]$ docker pull  linuxserver/wikijs
Using default tag: latest
latest: Pulling from linuxserver/wikijs
8b16ab80b9bd: Pull complete 
[...]
20b23561c7ea: Pull complete 
Digest: sha256:131d247ab257cc3de56232b75917d6f4e24e07c461c9481b0e7072ae8eba3071
Status: Downloaded newer image for linuxserver/wikijs:latest
docker.io/linuxserver/wikijs:latest
```
- listez les images que vous avez sur la machine avec une commande `docker`

```
[fay@router1 ~]$ docker images
REPOSITORY           TAG       IMAGE ID       CREATED       SIZE
mysql                latest    73246731c4b0   3 days ago    619MB
linuxserver/wikijs   latest    869729f6d3c5   6 days ago    441MB
python               latest    fc7a60e86bae   2 weeks ago   1.02GB
wordpress            latest    fd2f5a0c6fba   2 weeks ago   739MB
redis                latest    76506809a39f   2 weeks ago   138MB
nginx                latest    d453dd892d93   8 weeks ago   187MB
```

> Quand on tape `docker pull python` par exemple, un certain nombre de choses est implicite dans la commande. Les images, sauf si on précise autre chose, sont téléchargées depuis [le Docker Hub](https://hub.docker.com/). Rendez-vous avec un navigateur sur le Docker Hub pour voir la liste des tags disponibles pour une image donnée. Sachez qu'il existe d'autres répertoires publics d'images comme le Docker Hub, et qu'on peut facilement héberger le nôtre. C'est souvent le cas en entreprise. **On appelle ça un "registre d'images"**.

🌞 **Lancez un conteneur à partir de l'image Python**

- lancez un terminal `bash` ou `sh`
- vérifiez que la commande `python` est installée dans la bonne version
```

[fay@router1 ~]$ docker run -it python bash
root@832b4378ec6b:/# python -v
[...]
Python 3.12.1 (main, Dec 19 2023, 20:14:15) [GCC 12.2.0] on linux
```

> *Sympa d'installer Python dans une version spéficique en une commande non ? Peu importe que Python soit déjà installé sur le système ou pas. Puis on détruit le conteneur si on en a plus besoin.*

## 2. Construire une image

Pour construire une image il faut :

- créer un fichier `Dockerfile`
- exécuter une commande `docker build` pour produire une image à partir du `Dockerfile`

🌞 **Ecrire un Dockerfile pour une image qui héberge une application Python**

- l'image doit contenir
  - une base debian (un `FROM`)
  - l'installation de Python (un `RUN` qui lance un `apt install`)
    - il faudra forcément `apt update` avant
    - en effet, le conteneur a été allégé au point d'enlever la liste locale des paquets dispos
    - donc nécessaire d'update avant de install quoique ce soit
  - l'installation de la librairie Python `emoji` (un `RUN` qui lance un `pip install`)
  - ajout de l'application (un `COPY`)
  - le lancement de l'application (un `ENTRYPOINT`)
- le code de l'application :

```python
import emoji

print(emoji.emojize("Cet exemple d'application est vraiment naze :thumbs_down:"))
```

- pour faire ça, créez un dossier `python_app_build`
  - pas n'importe où, c'est ton Dockerfile, ton caca, c'est dans ton homedir donc `/home/<USER>/python_app_build`
  - dedans, tu mets le code dans un fichier `app.py`
  - tu mets aussi `le Dockerfile` dedans

> *J'y tiens beaucoup à ça, comprenez que Docker c'est un truc que le user gère. Sauf si vous êtes un admin qui vous en servez pour faire des trucs d'admins, ça reste dans votre `/home`. Les dévs quand vous bosserez avec Windows, vous allez pas stocker vos machins dans `C:/Windows/System32/` si ? Mais plutôt dans `C:/Users/<TON_USER>/TonCaca/` non ? Alors pareil sous Linux please.*

🌞 **Build l'image**

- déplace-toi dans ton répertoire de build `cd build_nul`
- `docker build . -t app.py:latest`
  - le `.` indique le chemin vers le répertoire de build (`.` c'est le dossier actuel)
  - `-t python_app:version_de_ouf` permet de préciser un nom d'image (ou *tag*)
- une fois le build terminé, constater que l'image est dispo avec une commande `docker`

```
[fay@router1 build_nul]$ docker images
REPOSITORY           TAG       IMAGE ID       CREATED         SIZE
app2.py               latest    1de2716d7bdb   2 minutes ago   661MB
mysql                latest    73246731c4b0   3 days ago      619MB
linuxserver/wikijs   latest    869729f6d3c5   6 days ago      441MB
python               latest    fc7a60e86bae   2 weeks ago     1.02GB
wordpress            latest    fd2f5a0c6fba   2 weeks ago     739MB
redis                latest    76506809a39f   2 weeks ago     138MB
nginx                latest    d453dd892d93   8 weeks ago     187MB
```



🌞 **Lancer l'image**

- lance l'image avec `docker run` :-1: 
```
[fay@router1 build_nul]$ docker run app2.py
Cet exemple d'application est vraiment naze 👎
```

