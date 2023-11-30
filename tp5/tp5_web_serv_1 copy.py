from http.server import BaseHTTPRequestHandler, HTTPServer
import os

# Define the handler for the HTTP server
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Serve index.html for any GET request
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Check if index.html exists
            if os.path.exists('index.html'):
                # Read and serve the content of index.html
                with open('index.html', 'r') as file:
                    html_content = file.read()
                    self.wfile.write(html_content.encode('utf-8'))
            else:
                # Send a simple response if index.html is not found
                self.wfile.write(b"<html><head><title>Server</title></head><body><h1>Index.html not found</h1></body></html>")
        else:
            # Handle any other GET requests
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"<html><head><title>404</title></head><body><h1>404 Not Found</h1></body></html>")

# Set up and start the server
port = 8000
server_address = ('', port)
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
print(f"Server started at http://localhost:{port}")
httpd.serve_forever()
