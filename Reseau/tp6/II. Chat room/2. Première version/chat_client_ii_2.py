import socket
import sys
import logging

# On définit la destination de la connexion
host = 'localhost'  # IP du serveur
port = 8888               # Port choisir par le serveur

# Create a custom logger
logger = logging.getLogger("chat_client")

def set_logger():
    try:
        logger.setLevel(logging.DEBUG)  # This needs to be DEBUG to capture all levels of logs
        # Create handlers
        c_handler = logging.StreamHandler()
        c_handler.setLevel(logging.DEBUG)  # Set to DEBUG to ensure all levels are logged to console
        # Add handlers to the logger
        logger.addHandler(c_handler)
    except Exception as e:
        print(f"Failed to configure logging: {e}")
        sys.exit(1)


def main():

    set_logger()
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))

        userMessage = input("Que veux-tu envoyer au serveur : ")
        s.send(userMessage.encode("utf-8"))

        data = s.recv(1024)
        s.close()
        print(f"Received message from server:  {repr(data)}")
        sys.exit(0)

    # Assurez-vous que le socket est fermé même en cas d'erreur
    except socket.error as e :
        print (f"Error Occured: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # lancement du main en asynchrone avec asyncio.run()
    main()

