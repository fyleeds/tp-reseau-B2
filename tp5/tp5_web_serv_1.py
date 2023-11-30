import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('localhost', 80))

s.listen(1)
conn, addr = s.accept()

while True:

  try:

    # Une liste qui va contenir les données reçues
    chunks = []
    
    # bytes_received = 0
    # while bytes_received < msg_len:
        # Si on reçoit + que la taille annoncée, on lit 1024 par 1024 octets
    chunk = conn.recv(
                            1024)
    if not chunk:
        raise RuntimeError('Invalid chunk received bro')

    # on ajoute le morceau de 1024 ou moins à notre liste
    chunks.append(chunk)
      
      # on ajoute la quantité d'octets reçus au compteur
      # bytes_received += len(chunk)

    # ptit one-liner pas combliqué à comprendre pour assembler la liste en un seul message
    message_received = b"".join(chunks).decode('utf-8')
    if "GET / " in message_received:
      html_content = "HTTP/1.0 200 OK\n\n<h1>Hello je suis un serveur HTTP</h1>"
      try:
        conn.sendall(html_content.encode())
      except Exception as e:
        print(f" error sending {e}")
    else :
      print(f"Error Request : Received from client {message_received}")
    
    conn.close()
    s.close()
    sys.exit(0)
  except socket.error as e:
    print(f"Error Occured : {e}")
    break


