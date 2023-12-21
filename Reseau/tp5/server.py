import socket
import os

# On choisit une IP et un port où on va écouter
host = '10.1.2.12'  # string vide signifie, dans ce conetxte, toutes les IPs de la machine
port = 13337  # port choisi arbitrairement

# AF_INET is the Internet address family for IPv4.
# SOCK_STREAM is the socket type for TCP, the protocol that will be used.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
    data = conn.recv(2)
    if not data:
      break  # Exit the inner loop if no data is received

    number = int.from_bytes(data, 'big')

    # Print the received message.
    print(f"Received message: {number}")

  except socket.error:
    print("Error Occured.")
    break

# Close the connection.
conn.close()
