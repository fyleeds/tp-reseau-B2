import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('10.1.2.12', 13337))

s.listen(1)
conn, addr = s.accept()

while True:

  try:
    # On lit les 4 premiers octets qui arrivent du client
    # Car dans le client, on a fixé la taille du header à 4 octets
    isEnded = 0
    # Une liste qui va contenir les données reçues
    chunks = []
    while isEnded == 0 :
      header = conn.recv(4)
      if not header:
        break

      # On lit la valeur
      msg_len = int.from_bytes(header[0:4], byteorder='big')

      print(f"Lecture des {msg_len} prochains octets")

      bytes_received = 0
      while bytes_received < msg_len:
          # Si on reçoit + que la taille annoncée, on lit 1024 par 1024 octets
          chunk = conn.recv(min(msg_len - bytes_received,
                                  1024))
          if not chunk:
              raise RuntimeError('Invalid chunk received bro')

          if chunk.decode('utf-8') == "hehe":
            isEnded = 1
          else:
            # on ajoute le morceau de 1024 ou moins à notre liste
            chunks.append(chunk)
          
          # on ajoute la quantité d'octets reçus au compteur
          bytes_received += len(chunk)

    # ptit one-liner pas combliqué à comprendre pour assembler la liste en un seul message
    message_received = b"".join(chunks).decode('utf-8')
    print(f"Received from client {message_received}")
    try:
      res = eval(message_received)
      print(f" le résultat est {res}")
      conn.send((str(res)).encode())
    except Exception as e:
      print(f" error sending {e}")
    conn.close()
    s.close()
    sys.exit(0)
  except socket.error:
    print("Error Occured.")
    break


