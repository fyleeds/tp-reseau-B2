import socket
import sys
import logging
import asyncio

# On définit la destination de la connexion
host = 'localhost'  # IP du serveur
port = 8888               # Port choisir par le serveur

# Create a custom logger
logger = logging.getLogger("chat_client")

async def set_logger():
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

async def input_msg(writer,prompt):
    while True:
        try :
            user_input = await asyncio.to_thread(input, prompt)
        except Exception as e:
            logger.info(f"error from input_msg {e}")
            break
        try :
            ## une ligne pour write le message (l'envoyer)
            writer.write(user_input.encode())
            ## une ligne qui attend que tout soit envoyé (on peut donc l'await)
            await writer.drain()
        except Exception as e:
            logger.info(f"error from encoding and sending {e}")
            break

async def receive_msg(reader, writer):
    while True:
        # les objets reader et writer permettent de lire/envoyer des données auux clients

        # on lit les 1024 prochains octets
        # notez le await pour indiquer que cette opération peut produire de l'attente
        try :
            data = await reader.read(1024)
            addr = writer.get_extra_info('peername')

            # si le client n'envoie rien, il s'est sûrement déco
            if data == b'':
                break

            # on décode et affiche le msg du client
            message = data.decode()
            logger.info(f"Received {message!r} from server : {addr!r}")
        except ConnectionResetError as e:
            logger.info(f"error from receiving message from server ConnectionResetError {e}")
            break

async def connect_server():
    try:
        reader, writer = await asyncio.open_connection(host="127.0.0.1", port=8888)
        return reader, writer
    # Assurez-vous que le socket est fermé même en cas d'erreur
    except Exception as e :
        print (f"Error Occured: {e}")
        sys.exit(1)

def main():
    set_logger()

    reader, writer = asyncio.run(connect_server())
    prompt = "Please enter your message : \n"
    first_connexion(writer)
    asyncio.run(client_chat(reader, writer, prompt))
   

async def client_chat(reader, writer, prompt):
    try:
        await asyncio.gather(input_msg(writer, prompt), receive_msg(reader, writer), return_exceptions=True)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        writer.close()
        await writer.wait_closed()

def first_connexion(writer):
    pseudo_message = input("Send pseudo please : ")
    try :
        ## une ligne pour write le message (l'envoyer)
        writer.write(pseudo_message.encode())
        ## une ligne qui attend que tout soit envoyé (on peut donc l'await)
        writer.drain()
    except Exception as e:
        logger.info(f"error from encoding and sending pseudo {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

