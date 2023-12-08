import asyncio
import sys
import logging

global CLIENTS 
CLIENTS = {}
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
        print(f"Failed to configure logging: {e}\n")
        sys.exit(1)

async def add_client(addr, reader, writer,pseudo):
    # add subdictionary for this addr
    CLIENTS[addr] = {}
    # Add the reader and writer for this addr
    CLIENTS[addr]["r"] = reader
    CLIENTS[addr]["w"] = writer
    CLIENTS[addr]["pseudo"] = pseudo
    logger.info(f"Added reader and writer for client : {pseudo!r} with addr : {addr}\n")

async def update_client(addr, reader, writer):
    # Update the reader and writer for this addr
    CLIENTS[addr]["r"] = reader
    CLIENTS[addr]["w"] = writer
    logger.info(f"Updating reader and writer for this client : {addr!r}\n")

async def is_new_client(addr):
    # Ensure there is a sub-dictionary for this addr
    if addr not in CLIENTS:
        return True
    return False

async def broadcast(message,addr):
    # Prepare the message for sending
    header = f"{addr!r} says: "
    message = header + message

    try : 
        message_encoded = message.encode()
    except Exception as e:
        logger.info(f"error from encoding message {e}\n")
        return

    disconnected_clients = []
    for addr, tuple in CLIENTS.items():
        logger.info(f"Sending to {addr!r}\n")
        writer = tuple["w"]
     
        try:
            writer.write(message_encoded)
            await writer.drain()
            logger.info(f"Sent {message_encoded!r} to {addr!r}\n")
        except Exception as e:
            logger.info(f"error from sending message {e}\n")
            # If an error occurs, assume the client is disconnected
            disconnected_clients.append(addr)
            logger.info(f"Annonce : {addr} a quitté la chatroom")

    # Remove disconnected clients
    for addr in disconnected_clients:
        del CLIENTS[addr]
        logger.info(f"{addr} removed from dict CLIENTS\n")

# cette fonction sera appelée à chaque fois qu'on reçoit une connexion d'un client
async def handle_client_msg(reader, writer):
    while True:

        addr = writer.get_extra_info('peername')

        if await is_new_client(addr):

            data = await reader.read(1024)

            # si le client n'envoie rien, il s'est sûrement déco
            if data == b'':
                break

            # on décode et affiche le msg du client
            pseudo_msg = data.decode()
            logger.info(f"Received {pseudo_msg!r} from a new client : {addr!r}\n")
            try:
                pseudo_msg_splitted = pseudo_msg.split('|')
                
                if pseudo_msg_splitted[0] == "Hello":
                    logger.info(f"nickname recognised : {pseudo_msg_splitted[1]}\n")
                    await add_client(addr, reader, writer,pseudo_msg_splitted[1])
                    message = (f"Annonce {CLIENTS[addr]['pseudo']} a rejoint la chatroom")
                    logger.info(f"message to broadcast : {message}\n")
                    await broadcast(message,addr)
            except Exception as e:
                logger.info(f"error no pseudo message {e}\n")
                break
        else:
            await update_client(addr, reader, writer)
            # on lit les 1024 prochains octets
            # notez le await pour indiquer que cette opération peut produire de l'attente
            
            data = await reader.read(1024)

            # si le client n'envoie rien, il s'est sûrement déco
            if data == b'':
                break

            # on décode et affiche le msg du client
            message = data.decode()
            logger.info(f"Received {message!r} from an existing user : {addr!r}\n")

            await broadcast(message,addr)


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
    logger.info(f'Serving on {addrs}\n')

    # on lance le serveur
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    # lancement du main en asynchrone avec asyncio.run()
    asyncio.run(main())
