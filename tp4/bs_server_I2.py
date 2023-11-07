import socket
import os

# On choisit une IP et un port où on va écouter
host = '10.1.2.12' # string vide signifie, dans ce conetxte, toutes les IPs de la machine
port = 13337 # port choisi arbitrairement

# AF_INET is the Internet address family for IPv4.
# SOCK_STREAM is the socket type for TCP, the protocol that will be used.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port number.
s.bind((host, port))

# Listen for incoming connections (with a backlog of 1).
s.listen(1)

# Run the 'ss' command and capture the exit status.
exit_status = os.system("ss -lntp | grep ':13337'")

# Accept a connection.
conn, addr = s.accept()

# Print the address of the connected client.
print('Connected by', addr)

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

        # Respond to the client based on the received message.
        if message == "meo":
            conn.sendall('Meo à toi confrère.'.encode("utf-8"))
        elif message == "waf":
            conn.sendall('ptdr t ki'.encode("utf-8"))
        else:
            conn.sendall('Mes respects humble humain'.encode("utf-8"))
    except socket.error:
        print("Error Occured.")
        break

# Close the connection.
conn.close()


