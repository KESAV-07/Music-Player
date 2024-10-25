from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/callback'):
            # Parse the query parameters
            query = urllib.parse.urlparse(self.path).query
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Display the authorization code in the response
            self.wfile.write(bytes("Authorization code: " + query, "utf-8"))
            print("Received query: ", query)  # Print to console for debugging
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=RequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port 8000...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
