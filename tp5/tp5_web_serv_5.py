import socket
import sys
import os
import logging

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('localhost', 80))

s.listen(1)
conn, addr = s.accept()

while True:

  try:
    header = conn.recv(4)
    if not header:
      print("no header")
      break
    # On lit la valeur
    msg_len = int.from_bytes(header[0:4], byteorder='big')
    # Une liste qui va contenir les données reçues
    chunks = []

    bytes_received = 0
    # On lit la valeur
    msg_len = int.from_bytes(header[0:4], byteorder='big')


    chunk = conn.recv(
                            1024)
    if not chunk:
        raise RuntimeError('Invalid chunk received bro')

    # on ajoute le morceau de 1024 ou moins à notre liste
    chunks.append(chunk)

    bytes_received += len(chunk)

    # ptit one-liner pas combliqué à comprendre pour assembler la liste en un seul message
    message_received = b"".join(chunks).decode('utf-8')

    try:
      # Create a custom logger
      logger = logging.getLogger("http_server")
      logger.setLevel(logging.DEBUG)  # This needs to be DEBUG to capture all levels of logs
      # Create handlers
      c_handler = logging.StreamHandler()
      c_handler.setLevel(logging.DEBUG)  # Set to DEBUG to ensure all levels are logged to console
      # Add handlers to the logger
      logger.addHandler(c_handler)
    except Exception as e:
      print(f"Failed to configure logging: {e}")
      sys.exit(1)
    
    if "/ HTTP/1.1\r\n" in message_received:
      try:
        folder_path = os.path.dirname(os.path.abspath(__file__))

        file = open(f'{folder_path}\htdocs\index.html')
        html_content = file.read()
        file.close()

        http_response = 'HTTP/1.0 200 OK\n\n' + html_content
        conn.sendall(http_response.encode())
        logger.info("Un client %s s'est connecté et a télécharger le fichier index.html.", addr)
      except Exception as e:
        print(f" error sending {e}")
      
    elif "/toto.html HTTP/1.1\r\n" in message_received:
      try:
        folder_path = os.path.dirname(os.path.abspath(__file__))

        file = open(f'{folder_path}/htdocs/toto.html')
        html_content = file.read()
        file.close()

        http_response = 'HTTP/1.0 200 OK\n\n' + html_content
        conn.sendall(http_response.encode())
        logger.info("Un client %s s'est connecté et a télécharger le fichier toto.html.", addr)
      except Exception as e:
        print(f" error sending {e}")
    elif ".jpg" in message_received:

        folder_path = os.path.dirname(os.path.abspath(__file__))

        file_path = folder_path + "/htdocs/yoshi.jpg"


        # Préparation de la réponse HTTP
        
        http_response = b'HTTP/1.1 200 OK\r\n'
        http_response += b'Content-Type: image/jpeg\r\n'
        http_response += b'\r\n'
        conn.sendall(http_response)

        with open(file_path, 'rb') as file:
          jpg_data_len = len(bytearray(file.read()))
          logger.info(f"Lecture des {jpg_data_len} prochains octets")
          file.close()

        with open(file_path, 'rb') as file:

          # header = file.read(2)
          # if not header:
          #   logger.info("no header")
          #   break
          # else :
          #   logger.info("this is the header of the image : %s",header)

          bytes_received = 0
          while bytes_received < jpg_data_len:
            chunk_len = min(jpg_data_len - bytes_received,
                                1024)
            logger.info(chunk_len)
            chunk = file.read(chunk_len)
            if not chunk:
                logger.info("no chunk")
                break  # End of file
            conn.sendall(chunk)
            logger.info(f"Sent a chunk of size: {len(chunk)} bytes.")
            bytes_received += len(chunk)

    else:
      print(f"Received from client {message_received}")
    
    conn.close()
    s.close()
    sys.exit(0)
  except socket.error as e:
    print(f"Error Occured : {e}")
    break


