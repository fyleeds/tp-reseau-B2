# I. Simple bs program

Première partie pour mettre en place un environnement fonctionnel et deux programmes simples qui discutent à travers le réseau.

- [I. Simple bs program](#i-simple-bs-program)
  - [1. First steps](#1-first-steps)
  - [2. User friendly](#2-user-friendly)
  - [3. You say client I hear control](#3-you-say-client-i-hear-control)

## 1. First steps

> Référez-vous [**au cours sur les sockets**](../../../../cours/dev/socket/README.md) pour la syntaxe.

🌞 **`bs_server_I1.py`**

- écoute sur une IP spécifique et port 13337 en TCP
- répond automatiquement "Hi mate !" dès qu'un client se connecte
- affiche la réponse des clients qui se connectent
- _server : 
```
[fay@node2 python]$ python3 bs_server_I1.py
LISTEN 0      1          10.1.2.12:13337      0.0.0.0:*    users:(("python3",pid=1596,fd=3))
Connected by ('10.1.2.13', 48696)
Received message: Meooooo !
```
> Il faudra ouvrir ce port dans le *firewall* de la machine.

🌞 **`bs_client_I1.py`**

- se connecte à l'IP spécifique de la VM serveur et au port 13337
- envoie la string "Meooooo !"
- affiche une éventuelle réponse
- quitte proprement
```
[fay@node2 python]$ python3 bs_clientI1.py
Received message : b'Mes respects humble humain'
[fay@node2 python]$
```
➜ **Pour quitter proprement, on attend pas juste que l'exécution arrive en fin de fichier, mais on quitte explicitement**

- librairie `sys`
- elle contient une méthode `exit()`
- la méthode `exit()` prend un entier en paramètre : le code retour à retourner quand le programme se termine. Pour rappel :
  - `0` veut dire que le programme s'est terminé correctement
  - autre chose veut dire que le programme ne s'est pas terminé correctement

🌞 **Commandes...**

- je veux dans le compte-rendu toutes les commandes réalisées sur le client et le serveur pour que ça fonctionne
- et je veux aussi voir une exécution de votre programme

```
[fay@node2 python]$ python3 bs_server_I1.py
LISTEN 0      1          10.1.2.12:13337      0.0.0.0:*    users:(("python3",pid=1608,fd=3))
```
- oh et je veux un `ss` sur le serveur
dans code serveur : 
```
exit_status = os.system("ss -lntp | grep ':13337'")
```
  - n'affiche qu'une ligne : celle qui concerne l'écoute de notre programme
  - ajoutez les bonnes options à `ss` ainsi qu'un `| grep ...` pour n'afficher que la bonne ligne

## 2. User friendly

🌞 **`bs_client_I2.py`**

> Vous aurez besoin du [**cours sur la gestion d'erreurs**](../../../../cours/dev/error_handling/README.md) pour cette partie.

- retour visuel
  - afficher un message de succès chez le client quand il se co au serveur
  - le message doit être : `Connecté avec succès au serveur <IP_SERVER> sur le port <PORT>`
  - vous utiliserez un `try` `except` pour savoir si la connexion est correctement effectuée
- le programme doit permettre à l'utilisateur d'envoyer la string qu'il veut au serveur
  - on peut récupérer un input utilisateur avec la fonction `input()` en Python
  - au lancement du programme, un prompt doit apparaître pour indiquer à l'utilisateur qu'il peut envoyer une string au serveur :
    - `Que veux-tu envoyer au serveur : `
Server : 
```
[fay@node2 python]$ python3 bs_server_I1.py
LISTEN 0      1          10.1.2.12:13337      0.0.0.0:*    users:(("python3",pid=1608,fd=3))
Un client vient de se co et son IP c est ('10.1.2.13', 40264)
Received message: Connecte avec succes au serveur 10.1.2.12 sur le port 13337
Received message: lol
```
Client :
```
[fay@node2 python]$ python3 bs_clientI1.py
Que veux-tu envoyer au serveur : lol
Received message : b'Mes respects humble humain'
```
🌞 **`bs_server_I2.py`**

- retour visuel
  - afficher un message de succès quand un client se co
  - le message doit être : `Un client vient de se co et son IP c'est <CLIENT_IP>.`
- réponse adaptative
  - si le message du client contient "meo" quelque part, répondre : `Meo à toi confrère.`
  - si le message du client contient "waf" quelque part, répondre : `ptdr t ki`
  - si le message du client ne contient PAS "meo", ni "waf", répondre : `Mes respects humble humain.`

meo : 
server : 
```
[fay@node2 python]$ python3 bs_server_I1.py
Received message: meo
```
client : 
```
[fay@node2 python]$ python3 bs_clientI1.py
Received message :  b'Meo \xc3\xa0 toi confr\xc3\xa8re.'
```
waf : 
server : 
```
[fay@node2 python]$ python3 bs_server_I1.py
Received message: waf
```
client : 
```
[fay@node2 python]$ python3 bs_clientI1.py
Received message :  b'ptdr t ki'
```
a : 
server : 
```
[fay@node2 python]$ python3 bs_server_I1.py
Received message: a
```
client : 
```
[fay@node2 python]$ python3 bs_clientI1.py
Received message :  b'Mes respects humble humain.'
```
## 3. You say client I hear control

On va ajouter un peu de contrôle pour éviter que notre client fasse nawak à l'utilisation du programme.

🌞 **`bs_client_I3.py`**

- vérifier que...
  - le client saisit bien une string
    - utilisez la méthode native `type()` pour vérifier que c'est une string
  - que la string saisie par le client contient obligatoirement soit "waf" soit "meo"
    - utilisez [**une expression régulière**](https://www.programiz.com/python-programming/regex) (signalez-le moi s'il serait bon de faire un cours sur cette notion)
- sinon lever une erreur avec `raise`
  - choisissez avec pertinence l'erreur à lever dans les deux cas (s'il saisit autre chose qu'une string, ou si ça contient aucun des deux mots)
  - y'a une liste des exceptions natives (choisissez-en une donc) tout en bas du [cours sur la gestion d'erreur](../../../../cours/dev/error_handling/README.md)

> On poussera le contrôle plus loin plus tard.
```
[fay@node2 python]$ python3 bs_clientI3.py
Que veux-tu envoyer au serveur : 1
Traceback (most recent call last):
  File "bs_clientI3.py", line 17, in <module>
    raise ValueError("La chaîne doit contenir 'waf' ou 'meo'.")
ValueError: La chaîne doit contenir 'waf' ou 'meo'.

[fay@node2 python]$ python3 bs_clientI3.py
Error Occured: [Errno 111] Connection refused
[fay@node2 python]$ python3 bs_clientI3.py
Que veux-tu envoyer au serveur : m
Traceback (most recent call last):
  File "bs_clientI3.py", line 17, in <module>
    raise ValueError("La chaîne doit contenir 'waf' ou 'meo'.")
ValueError: La chaîne doit contenir 'waf' ou 'meo'.

[fay@node2 python]$ python3 bs_clientI3.py
Error Occured: [Errno 111] Connection refused
[fay@node2 python]$ python3 bs_clientI3.py
Que veux-tu envoyer au serveur : hbcsdhbfdmeohbhbfvsdf
Received message :  b'Mes respects humble humain'
```