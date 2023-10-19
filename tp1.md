# TP1 RESEAU 2023-2024


 # TP1 : Maîtrise réseau du poste

Pour ce TP, on va utiliser **uniquement votre poste** (pas de VM, rien, quedal, quetchi).

Le but du TP : se remettre dans le bain tranquillement en manipulant pas mal de concepts qu'on a vu l'an dernier.

C'est un premier TP *chill*, qui vous(ré)apprend à maîtriser votre poste en ce qui concerne le réseau. Faites le seul ou avec votre mate préféré bien sûr, mais jouez le jeu, faites vos propres recherches.

La "difficulté" va crescendo au fil du TP, mais la solution tombe très vite avec une ptite recherche Google si vos connaissances de l'an dernier deviennent floues.

- [TP1 : Maîtrise réseau du poste](#tp1--maîtrise-réseau-du-poste)
- [I. Basics](#i-basics)
- [II. Go further](#ii-go-further)
- [III. Le requin](#iii-le-requin)

# I. Basics

> Tout est à faire en ligne de commande, sauf si précision contraire.

☀️ **Carte réseau WiFi**

Déterminer...

- l'adresse MAC de votre carte WiFi
`ipconfig/all
Adresse Mac : 5C-3A-45-05-17-59 ; `

- l'adresse IP de votre carte WiFi
- `ipconfig/all
Adresse Ip : 192.168.43.80 ;`
 

- le masque de sous-réseau du réseau LAN auquel vous êtes connectés en WiFi
 
 - en notation CIDR, par exemple `/16`
`ipconfig/all
 Masque de sous-réseau (CIDR): /24`


 

  - ET en notation décimale, par exemple `255.255.0.0`

---


`ipconfig/all
Masque de sous-réseau 
: 255.255.255.0 `
☀️ **Déso pas déso**

Pas besoin d'un terminal là, juste une feuille, ou votre tête, ou un tool qui calcule tout hihi. Déterminer...

- l'adresse de réseau du LAN auquel vous êtes connectés en WiFi


- l'adresse de broadcast
 l'adresse de broadcast :
 `ipconfig/all
 192.168.43.255`

 

- le nombre d'adresses IP disponibles dans ce réseau
 https://www.site24x7.com/tools/ipv4-subnetcalculator.html
65536 subnet adresses

☀️ **Hostname**

- déterminer le hostname de votre PC

---
---
 Aller dans Systèmes sur Windows : 
 Hostname : 
 LAPTOP-1FMC1MG2

☀️ **Passerelle du réseau**

Déterminer...

- l'adresse IP de la passerelle du réseau
`ipconfig/all
192.168.43.1`
- l'adresse MAC de la passerelle du réseau

---
`arp -a
 b2-99-cc-6e-05-6a`

☀️ **Serveur DHCP et DNS**

Déterminer...

- l'adresse IP du serveur DHCP qui vous a filé une IP

`  ipconfig /all
Serveur DHCP . . . . . . . . . . . . . : 192.168.43.1`
- l'adresse IP du serveur DNS que vous utilisez quand vous allez sur internet

`  ipconfig /all
Serveur DHCP . . . . . . . . . . . . . : 192.168.43.1`

---

☀️ **Table de routage**

Déterminer...

- dans votre table de routage, laquelle est la route par défaut

Défini par 0.0.0.0 là où tout le trafic passe 

`route print
Destination réseau    Masque réseau  Adr. passerelle   Adr. interface Métrique
          0.0.0.0          0.0.0.0     192.168.43.1    192.168.43.80     55`

---

![Not sure](./img/notsure.png)

# II. Go further

> Toujours tout en ligne de commande.

---

☀️ **Hosts ?**

- faites en sorte que pour votre PC, le nom `b2.hello.vous` corresponde à l'IP `1.1.1.1`
Editer le fichier dans C:\Windows\System32\drivers\etc et ajouter la ligne 1.1.1.1 b2.hello.vous
- prouvez avec un `ping b2.hello.vous` que ça ping bien `1.1.1.1`

PS C:\Users\clemc> ping b2.hello.vous

```
ping b2.hello.vous
Envoi d’une requête 'ping' sur b2.hello.vous [1.1.1.1] avec 32 octets de données :
Réponse de 1.1.1.1 : octets=32 temps=50 ms TTL=56
Réponse de 1.1.1.1 : octets=32 temps=37 ms TTL=56
```

> Vous pouvez éditer en GUI, et juste me montrer le contenu du fichier depuis le terminal pour le compte-rendu.

---

☀️ **Go mater une vidéo youtube et déterminer, pendant qu'elle tourne...**

- l'adresse IP du serveur auquel vous êtes connectés pour regarder la vidéo
```
PS C:\Users\clemc> netstat -n
    142.250.75.238 
```
- le port du serveur auquel vous êtes connectés
 ```
PS C:\Users\clemc> netstat -n
    443
```
- le port que votre PC a ouvert en local pour se connecter au port du serveur distant

 ```
PS C:\Users\clemc> netstat -n
    59779
```

---

☀️ **Requêtes DNS**

Déterminer...

- à quelle adresse IP correspond le nom de domaine `www.ynov.com`

> Ca s'appelle faire un "lookup DNS".
```
PS C:\Users\clemc> nslookup www.ynov.com
Serveur :   UnKnown
Address:  192.168.43.1

Réponse ne faisant pas autorité :
Nom :    www.ynov.com
Addresses:  2606:4700:20::681a:ae9
          2606:4700:20::ac43:4ae2
          2606:4700:20::681a:be9
          104.26.11.233
          104.26.10.233
          172.67.74.226
```
- à quel nom de domaine correspond l'IP `174.43.238.89`

> Ca s'appelle faire un "reverse lookup DNS".
```
nslookup 174.43.238.89
Serveur :   UnKnown
Address:  192.168.43.1

Nom :    89.sub-174-43-238.myvzw.com
Address:  174.43.238.89
```
---

☀️ **Hop hop hop**

Déterminer...

- par combien de machines vos paquets passent quand vous essayez de joindre `www.ynov.com`

```
PS C:\Users\clemc> tracert www.ynov.com

Détermination de l’itinéraire vers www.ynov.com [172.67.74.226]
avec un maximum de 30 sauts :

  1     8 ms     2 ms     2 ms  192.168.43.1
  2    35 ms     *       77 ms  10.8.11.10
  3    90 ms    31 ms    39 ms  10.8.11.9
  4     *        *        *     Délai d’attente de la demande dépassé.
  5   100 ms    39 ms    37 ms  10.8.12.125
  6    78 ms    46 ms    34 ms  prs-b3-link.ip.twelve99.net [80.239.133.124]
  7    96 ms    47 ms    34 ms  prs-bb2-link.ip.twelve99.net [62.115.118.62]
  8    58 ms    38 ms    47 ms  prs-b1-link.ip.twelve99.net [62.115.125.167]
  9    68 ms    51 ms    50 ms  cloudflare-ic-375100.ip.twelve99-cust.net [80.239.194.103]
 10    90 ms    35 ms    47 ms  172.71.128.4
 11    41 ms    50 ms    30 ms  172.67.74.226

Itinéraire déterminé.
```

---

☀️ **IP publique**

Déterminer...

- l'adresse IP publique de la passerelle du réseau (le routeur d'YNOV donc si vous êtes dans les locaux d'YNOV quand vous faites le TP)

---

```
PS C:\Users\clemc> Get-NetRoute -DestinationPrefix 0.0.0.0/0 | Select-Object InterfaceAlias, NextHop

InterfaceAlias NextHop
-------------- -------
Wi-Fi          192.168.43.1
```

☀️ **Scan réseau**

Déterminer...

- combien il y a de machines dans le LAN auquel vous êtes connectés

> Allez-y mollo, on va vite flood le réseau sinon. :)

![Stop it](./img/stop.png)

# III. Le requin

Faites chauffer Wireshark. Pour chaque point, je veux que vous me livrez une capture Wireshark, format `.pcap` donc.

Faites *clean* 🧹, vous êtes des grands now :

- livrez moi des captures réseau avec uniquement ce que je demande et pas 40000 autres paquets autour
  - vous pouvez sélectionner seulement certains paquets quand vous enregistrez la capture dans Wireshark
- stockez les fichiers `.pcap` dans le dépôt git et côté rendu Markdown, vous me faites un lien vers le fichier, c'est cette syntaxe :

```markdown
[Lien vers capture ARP](./captures/arp.pcap)
```

---

☀️ **Capture ARP**

- 📁 fichier `arp.pcap`
- capturez un échange ARP entre votre PC et la passerelle du réseau

> Si vous utilisez un filtre Wireshark pour mieux voir ce trafic, précisez-le moi dans le compte-rendu.

---

☀️ **Capture DNS**

- 📁 fichier `dns.pcap`
- capturez une requête DNS vers le domaine de votre choix et la réponse
- vous effectuerez la requête DNS en ligne de commande

> Si vous utilisez un filtre Wireshark pour mieux voir ce trafic, précisez-le moi dans le compte-rendu.

---

☀️ **Capture TCP**

- 📁 fichier `tcp.pcap`
- effectuez une connexion qui sollicite le protocole TCP
- je veux voir dans la capture :
  - un 3-way handshake
  - un peu de trafic
  - la fin de la connexion TCP

> Si vous utilisez un filtre Wireshark pour mieux voir ce trafic, précisez-le moi dans le compte-rendu.

---

![Packet sniffer](img/wireshark.jpg)

> *Je sais que je vous l'ai déjà servi l'an dernier lui, mais j'aime trop ce meme hihi 🐈*