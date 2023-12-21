import asyncio
import sys
import logging


# Create a custom logger
logger = logging.getLogger("chat_server")

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

# cette fonction sera appelée à chaque fois qu'on reçoit une connexion d'un client
async def handle_client_msg(reader, writer):
    while True:
        # les objets reader et writer permettent de lire/envoyer des données auux clients

        # on lit les 1024 prochains octets
        # notez le await pour indiquer que cette opération peut produire de l'attente
        data = await reader.read(1024)
        addr = writer.get_extra_info('peername')

        # si le client n'envoie rien, il s'est sûrement déco
        if data == b'':
            break

        # on décode et affiche le msg du client
        message = data.decode()
        logger.info(f"Received {message!r} from {addr!r}")

        # on envoie le message, ça se fait en deux lignes :
        ## une ligne pour write le message (l'envoyer)
        writer.write(f"Hello client, j'suis le serveur !".encode())
        ## une ligne qui attend que tout soit envoyé (on peut donc l'await)
        await writer.drain()

async def main():
    # on crée un objet server avec asyncio.start_server()
    ## on précise une fonction à appeler quand un paquet est reçu
    ## on précise sur quelle IP et quel port écouter

    set_logger()

    addr_server = '127.0.0.1'
    port_server = 8888
    server = await asyncio.start_server(handle_client_msg, addr_server, port_server)

    # ptit affichage côté serveur
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    logger.info(f'Serving on {addrs}')

    # on lance le serveur
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    # lancement du main en asynchrone avec asyncio.run()
    asyncio.run(main())
