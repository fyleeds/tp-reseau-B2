# TP2 : Environnement virtuel

Dans ce TP, on remanipule toujours les mêmes concepts qu'au TP1, mais en environnement virtuel avec une posture un peu plus orientée administrateur qu'au TP1.

- [TP2 : Environnement virtuel](#tp2--environnement-virtuel)
- [0. Prérequis](#0-prérequis)
- [I. Topologie réseau](#i-topologie-réseau)
  - [Topologie](#topologie)
  - [Tableau d'adressage](#tableau-dadressage)
  - [Hints](#hints)
  - [Marche à suivre recommandée](#marche-à-suivre-recommandée)
  - [Compte-rendu](#compte-rendu)
- [II. Interlude accès internet](#ii-interlude-accès-internet)
- [III. Services réseau](#iii-services-réseau)
  - [1. DHCP](#1-dhcp)
  - [2. Web web web](#2-web-web-web)

# 0. Prérequis

![One IP 2 VM](./img/oneip.jpg)

La même musique que l'an dernier :

- VirtualBox
- Rocky Linux
  - préparez une VM patron, prête à être clonée
  - système à jour (`dnf update`)
  - SELinux désactivé
  - préinstallez quelques paquets, je pense à notamment à :
    - `vim`
    - `bind-utils` pour la commande `dig`
    - `traceroute`
    - `tcpdump` pour faire des captures réseau

La ptite **checklist** que vous respecterez pour chaque VM :

- [ ] carte réseau host-only avec IP statique
- [ ] pas de carte NAT, sauf si demandée
- [ ] adresse IP statique sur la carte host-only
- [ ] connexion SSH fonctionnelle
- [ ] firewall actif
- [ ] SELinux désactivé
- [ ] hostname défini

# I. Topologie réseau

## Topologie

![Topologie](./img/topo.png)

## Tableau d'adressage

| Node             | LAN1 `10.1.1.0/24` | LAN2 `10.1.2.0/24` |
| ---------------- | ------------------ | ------------------ |
| `node1.lan1.tp1` | `10.1.1.11`        | x                  |
| `node2.lan1.tp1` | `10.1.1.12`        | x                  |
| `node1.lan2.tp1` | x                  | `10.1.2.11`        |
| `node2.lan2.tp1` | x                  | `10.1.2.12`        |
| `router.tp1`     | `10.1.1.254`       | `10.1.2.254`       |


**6.** ajouter les routes statiques

- sur les deux machines du LAN1, il faut ajouter une route vers le LAN2

Sur node1.lan1.tp1 : 

> sudo nano /etc/sysconfig/network-scripts/route-enp0s3

On édite le fichier pour ajouter seulement une route de facon permanente

> 10.1.2.0/24 via 10.1.1.254 dev enp0s3

Sur node2.lan1.tp1 : 

> sudo nano /etc/sysconfig/network-scripts/route-enp0s3

On édite le fichier pour ajouter seulement une route de facon permanente

> 10.1.2.0/24 via 10.1.1.254 dev enp0s3

Les connexions depuis ces machines vers le réseau 10.1.2.0/24 passent par l'adresse du routeur sur le réseau que la machine connait soit 10.1.1.254. Enfin, Le routeur redirige vers le réseau 10.1.2.0/24 pour établir la connexion avec les machines de ce réseau.

- sur les deux machines du LAN2, il faut ajouter une route vers le LAN1

Sur node1.lan2.tp1 : 

> sudo nano /etc/sysconfig/network-scripts/route-enp0s3

On édite le fichier pour ajouter seulement une route de facon permanente

> 10.1.1.0/24 via 10.1.2.254 dev enp0s3

Sur node2.lan2.tp1 : 

> sudo nano /etc/sysconfig/network-scripts/route-enp0s3

On édite le fichier pour ajouter seulement une route de facon permanente

> 10.1.1.0/24 via 10.1.2.254 dev enp0s3

Les connexions depuis ces machines vers le réseau 10.1.1.0/24 passent par l'adresse du routeur sur le réseau que la machine connait soit 10.1.2.254. Enfin, Le routeur redirige vers le réseau 10.1.1.0/24 pour établir la connexion avec les machines de ce réseau.

## Compte-rendu

☀️ Sur **`node1.lan1.tp1`**

- afficher ses cartes réseau

```
[fay@node1 ~]$ nmcli con show

NAME           UUID                                  TYPE      DEVICE
System enp0s3  3c36b8c2-334b-57c7-91b6-4401f3489c69  ethernet  enp0s3
```
- afficher sa table de routage
```
[fay@node1 ~]$ ip route show
10.1.1.0/24 dev enp0s3 proto kernel scope link src 10.1.1.11 metric 100
10.1.2.0/24 via 10.1.1.254 dev enp0s3 proto static metric 100
```

- prouvez qu'il peut joindre 
```
[fay@node1 ~]$ ping node21
PING node21 (10.1.2.11) 56(84) bytes of data.
64 bytes from node21 (10.1.2.11): icmp_seq=1 ttl=63 time=3.43 ms
64 bytes from node21 (10.1.2.11): icmp_seq=2 ttl=63 time=1.60 ms
```

- prouvez avec un `traceroute` que le paquet passe bien par `router.tp1`

```
[fay@node1 ~]$ traceroute -m 10 10.1.2.12
traceroute to 10.1.2.12 (10.1.2.12), 10 hops max, 60 byte packets
 1  10.1.1.254 (10.1.1.254)  0.914 ms  0.895 ms  0.882 ms
 2  10.1.2.12 (10.1.2.12)  0.869 ms !X  1.989 ms !X  1.971 ms !X
```

# II. Interlude accès internet

![No internet](./img/no%20internet.jpg)


☀️ **Sur `router.tp1`**

- prouvez que vous avez un accès internet (ping d'une IP publique)

```
[fay@router1 ~]$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=115 time=16.6 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=115 time=16.2 ms
```

- prouvez que vous pouvez résoudre des noms publics (ping d'un nom de domaine public)

```
[fay@router1 ~]$ ping www.google.com
PING www.google.com (142.250.179.68) 56(84) bytes of data.
64 bytes from par21s19-in-f4.1e100.net (142.250.179.68): icmp_seq=1 ttl=115 time=16.2 ms
64 bytes from par21s19-in-f4.1e100.net (142.250.179.68): icmp_seq=2 ttl=115 time=14.9 ms
64 bytes from par21s19-in-f4.1e100.net (142.250.179.68): icmp_seq=3 ttl=115 time=14.10 ms
```

☀️ **Accès internet LAN1 et LAN2**

- ajoutez une route par défaut sur les deux machines du LAN1
```
[fay@node2 ~]$ sudo cat /etc/sysconfig/network-scripts/ifcfg-enp0s3
[fay@node2 ~]$ 
BOOTPROTO=static
DEVICE=enp0s3
ONBOOT=yes
GATEWAY=10.1.1.254

IPADDR=10.1.1.12
NETMASK=255.255.255.0
DNS1=8.8.8.8
DNS2=8.8.4.4

```

```
cat /etc/resolv.conf
#
nameserver 8.8.8.8
nameserver 8.8.4.4
```

- ajoutez une route par défaut sur les deux machines du LAN2
- configurez l'adresse d'un serveur DNS que vos machines peuvent utiliser pour résoudre des nom
- dans le compte-rendu, mettez-moi que la conf des points précédents sur `node2.lan1.tp1`
- prouvez que `node2.lan1.tp1` a un accès internet :
  - il peut ping une IP publique

```
[fay@node2 ~]$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=114 time=22.1 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=114 time=23.3 ms
```

  - il peut ping un nom de domaine public



# III. Services réseau

**Adresses IP et routage OK, maintenant, il s'agirait d'en faire quelque chose nan ?**

Dans cette partie, on va **monter quelques services orientés réseau** au sein de la topologie, afin de la rendre un peu utile que diable. Des machines qui se `ping` c'est rigolo mais ça sert à rien, des machines qui font des trucs c'est mieux.

## 1. DHCP

![Dora](./img/dora.jpg)

Petite **install d'un serveur DHCP** dans cette partie. Par soucis d'économie de ressources, on recycle une des machines précédentes : `node2.lan1.tp1` devient `dhcp.lan1.tp1`.

**Pour rappel**, un serveur DHCP, on en trouve un dans la plupart des LANs auxquels vous vous êtes connectés. Si quand tu te connectes dans un réseau, tu n'es pas **obligé** de saisir une IP statique à la mano, et que t'as un accès internet wala, alors il y a **forcément** un serveur DHCP dans le réseau qui t'a proposé une IP disponible.

> Le serveur DHCP a aussi pour rôle de donner, en plus d'une IP disponible, deux informations primordiales pour l'accès internet : l'adresse IP de la passerelle du réseau, et l'adresse d'un serveur DNS joignable depuis ce réseau.

**Dans notre TP, son rôle sera de proposer une IP libre à toute machine qui le demande dans le LAN1.**

> Vous pouvez vous référer à [ce lien](https://www.server-world.info/en/note?os=Rocky_Linux_8&p=dhcp&f=1) ou n'importe quel autre truc sur internet (je sais c'est du Rocky 8, m'enfin, la conf de ce serveur DHCP ça bouge pas trop).

---

Pour ce qui est de la configuration du serveur DHCP, quelques précisions :

- vous ferez en sorte qu'il propose des adresses IPs entre `10.1.1.100` et `10.1.1.200`
- vous utiliserez aussi une option DHCP pour indiquer aux clients que la passerelle du réseau est `10.1.1.254` : le routeur
- vous utiliserez aussi une option DHCP pour indiquer aux clients qu'un serveur DNS joignable depuis le réseau c'est `1.1.1.1`

---

☀️ **Sur `dhcp.lan1.tp1`**

- n'oubliez pas de renommer la machine (`node2.lan1.tp1` devient `dhcp.lan1.tp1`)
```
[fay@dhcp ~]$ hostname
dhcp.lan1.tp1
```
- changez son adresse IP en `10.1.1.253`
```[fay@dhcp ~]$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:a1:60:d6 brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.253/24 brd 10.1.1.255 scope global noprefixroute enp0s3
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fea1:60d6/64 scope link
       valid_lft forever preferred_lft forever
```
- setup du serveur DHCP
  - commande d'installation du paquet

`sudo dnf -y install dhcp-server `

  - fichier de conf
 
```
  [fay@node2 ~]$ sudo cat /etc/dhcp/dhcpd.conf
# specify domain name
option domain-name "srv.world";
# specify DNS server's hostname or IP address
option domain-name-servers dlp.srv.world;

# default lease time
default-lease-time 600;
# max lease time
max-lease-time 7200;

# this DHCP server to be declared valid
authoritative;

# specify network address and subnetmask
subnet 10.1.1.0 netmask 255.255.255.0 {
    # specify the range of lease IP addresses
    range 10.1.1.100 10.1.1.200;

    # specify gateway (router)
    option routers 10.1.1.254;  # Gateway IP address

    # specify DNS server
    option domain-name-servers 1.1.1.1;  # DNS server IP address
    option broadcast-address 10.1.1.255;
}
```
![Chat mignon](./gif/cat.jpg)
  - service actif
```
[fay@node2 ~]$ sudo firewall-cmd --add-service=dhcp
success
```
```
[fay@node2 ~]$ sudo firewall-cmd --runtime-to-permanent
[sudo] password for fay:
success
```
```
[fay@node2 ~]$ sudo systemctl enable --now dhcpd
[sudo] password for fay:
Created symlink /etc/systemd/system/multi-user.target.wants/dhcpd.service → /usr/lib/systemd/system/dhcpd.service.
```
```
[fay@dhcp ~]$ sudo systemctl status dhcpd
[sudo] password for fay:
● dhcpd.service - DHCPv4 Server Daemon
   Loaded: loaded (/usr/lib/systemd/system/dhcpd.service; enabled; vendor preset: disabled)
   Active: active (running) since Tue 2023-10-24 10:06:03 CEST; 9min ago
...
```
☀️ **Sur `node1.lan1.tp1`**

- demandez une IP au serveur DHCP

`sudo nmcli connection modify 3c36b8c2-334b-57c7-91b6-4401f3489c69`
- prouvez que vous avez bien récupéré une IP *via* le DHCP
```
ip a

inet 10.1.1.100/24 brd 10.1.1.255 scope global dynamic nopref ixroute enp0s3
valid_lft forever preferred_lft forever
```


- prouvez que vous avez bien récupéré l'IP de la passerelle

```
ip route show
default via 10.1.1.1 dev enp0s3 proto dhcp src 10.1.1.100 metric 100
```

- prouvez que vous pouvez `ping node1.lan2.tp1`

```
[fay@dhcp]$ ping 10.1.1.100
4 bytes from 10.1.1.100(10.1.1.100) 56(84) bytes of data
4 bytes from 10.1.1.100: icmp_seq=1 ttl=63 times=8.49ms 
```

## 2. Web web web

Un petit serveur web ? Pour la route ?

On recycle ici, toujours dans un soucis d'économie de ressources, la machine `node2.lan2.tp1` qui devient `web.lan2.tp1`. On va y monter un serveur Web qui mettra à disposition un site web tout nul.

---

La conf du serveur web :

- ce sera notre vieil ami NGINX
- il écoutera sur le port 80, port standard pour du trafic HTTP
- la racine web doit se trouver dans `/var/www/toto/`
  - vous y créerez un fichier `/var/www/toto/index.html` avec le contenu de votre choix
- vous ajouterez dans la conf NGINX **un fichier dédié** pour servir le site web nul qui se trouve dans `/var/www/toto/`
  - écoute sur le port 80
  - répond au nom `toto`
  - sert le dossier `/var/www/toto/`
- n'oubliez pas d'ouvrir le port dans le firewall 🌼

---

☀️ **Sur `web.lan2.tp1`**

Dernière partie !!!

![Chat mignon](https://i.gifer.com/Ao.gif)

- n'oubliez pas de renommer la machine (`node2.lan2.tp1` devient `web.lan2.tp1`)

```
[fay@web ~]$ sudo hostname
web.lan2.tp1
```
- setup du service Web
  - installation de NGINX

`sudo dnf install httpd`

  - gestion de la racine web `/var/www/toto/`

```
sudo mkdir -p /var/www/html/toto
sudo chown -R apache:apache /var/www/html/toto
```

  - configuration NGINX

```
<VirtualHost *:80>
    ServerName toto.com
    DocumentRoot /var/www/html/toto
</VirtualHost>
```

  - service actif
```
[fay@web ~]$ sudo systemctl status httpd

● httpd.service - The Apache HTTP Server
   Loaded: loaded (/usr/lib/systemd/system/httpd.service; enabled; vendor preset: disabled)   Active: active (running) since Tue 
   [...]
Oct 24 11:44:38 web.lan2.tp1 httpd[12674]: Server configured, listening on: port 80
```


  - ouverture du port firewall

```
sudo firewall-cmd --zone=public --add-port=80/tcp --permanent
sudo firewall-cmd --reload
```

- prouvez qu'il y a un programme NGINX qui tourne derrière le port 80 de la machine (commande `ss`)

```
[fay@web ~]$ sudo ss -ltnp | grep :80
[sudo] password for fay:
LISTEN 0      128                *:80               *:*    users:(("httpd",pid=824,fd=4),("httpd",pid=823,fd=4),("httpd",pid=822,fd=4),("httpd",pid=797,fd=4))
```
- prouvez que le firewall est bien configuré

```
[fay@web ~]$ sudo firewall-cmd --list-all
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: enp0s3
  sources:
  services: cockpit dhcpv6-client http ssh
  ports: 22/tcp 12359/tcp 8888/tcp 16360/tcp 80/tcp
  protocols:
  forward: no
  masquerade: no
  forward-ports:
  source-ports:
  icmp-blocks:
  rich rules:
```

☀️ **Sur `node1.lan1.tp1`**

- éditez le fichier `hosts` pour que `toto` pointe vers l'IP de `web.lan2.tp1`

```
[fay@node2 ~]$ sudo cat /etc/hosts
[sudo] password for fay:
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
10.1.2.11   toto
```
![Chat mignon](./gif/MondayLeftMeBroken.gif)

- visitez le site nul avec une commande `curl` et en utilisant le nom `toto`

```
[fay@web ~]$ curl toto
Bienvenue sur toto !
```

![That's all folks](./img/thatsall.jpg)