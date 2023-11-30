import socket
import sys

try:
    request_line = "GET / HTTP/1.1\r\n"
    headers = "Host: www.google.com\r\nConnection: close\r\n\r\n"
    http_request = request_line + headers

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("www.google.com", 80))
    s.sendall(http_request.encode())

    chunks = []
    while True:
        chunk = s.recv(1024)
        if not chunk:
            break
        chunks.append(chunk)

    message_received = b"".join(chunks)
    try:
        print(message_received.decode('utf-8'))
    except UnicodeDecodeError:
        print("Received data is not in UTF-8 format.")
        
    s.close()
    sys.exit(0)

except socket.error as e:
    print(f"Error Occurred: {e}")
    sys.exit(1)
