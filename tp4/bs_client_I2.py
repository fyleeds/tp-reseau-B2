import socket
import sys
# On définit la destination de la connexion
host = '10.1.2.12'  # IP du serveur
port = 13337               # Port choisir par le serveur


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    userMessage = input("Que veux-tu envoyer au serveur : ")
    s.sendall(userMessage.encode("utf-8"))
    s.sendall(b"Connecte avec succes au serveur %s sur le port %s" % (host.encode(), str(port).encode()))
    # s.sendall(b'meo')
    # s.sendall(b'waf')
    data = s.recv(1024)
    s.close()
    print(f"Received message :  {repr(data)}")
    sys.exit(0)
  # Assurez-vous que le socket est fermé même en cas d'erreur
except socket.error as e :
    print (f"Error Occured: {e}")
    sys.exit(1)

