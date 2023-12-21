import socket
import sys


command2= sys.argv[1]

ip_address = socket.gethostbyname(command2)
print(ip_address)