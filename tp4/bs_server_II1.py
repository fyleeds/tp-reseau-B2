# On importe la lib argparse
import argparse
import sys
import socket
import os
# Création d'un objet ArgumentParser
parser = argparse.ArgumentParser()

# On ajoute la gestion de l'option -n ou --name
# "store" ça veut dire qu'on attend un argument à -n

# on va stocker l'argument dans une variable
parser.add_argument("-p", "--port", type=int, default=13337,
                    help="Usage: python bs_server.py [OPTION]..."
                    "Run a server"
                    "Mandatory arguments to long options are mandatory for short options too."
                    "-p, --port                  Specify the port for the server to run on."
                    "                            Ports are integer between 0 and 65535"
                    "                            Ports below 1025 are considered privileged."
                    "-h, --help                  Help of the command"
)

# Permet de mettre à jour notre objet ArgumentParser avec les nouvelles options
args = parser.parse_args()

print(args.port)

if (args.port < 0 or args.port> 65535):
    print("ERROR Le port spécifié n'est pas un port possible (de 0 à 65535).")
    sys.exit(1)
elif (args.port >= 0 and args.port<= 1024):
    print("ERROR Le port spécifié est un port privilégié. Spécifiez un port au dessus de 1024.")
    sys.exit(2)


# SOCK_STREAM is the socket type for TCP, the protocol that will be used.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# On choisit une IP et un port où on va écouter
host = '10.1.2.12' # string vide signifie, dans ce conetxte, toutes les IPs de la machine
port = args.port # port choisi arbitrairement
# Bind the socket to the address and port number.
s.bind((host, port))

# Listen for incoming connections (with a backlog of 1).
s.listen(1)

# Accept a connection.
conn, addr = s.accept()

# Main server loop.
while True:
    try:
        # Receive data from the client.
        data = conn.recv(1024)
        if not data:
            break  # Exit the inner loop if no data is received
        # Decode the received data to a string.
        message = data.decode('utf-8')

        # Print the received message.
        print(f"Received message: {message}")

        conn.sendall('Hi Mate!'.encode("utf-8"))

    except socket.error:
        print("Error Occured.")
        break

# Close the connection.
conn.close()


