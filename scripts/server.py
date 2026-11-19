import http.server
import socketserver
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000

class SPAHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT_DIR, **kwargs)

    def do_GET(self):
        clean_path = self.path.split('?')[0].split('#')[0]
        translated = self.translate_path(clean_path)
        # If the file does not exist or is a directory without index.html
        if not os.path.exists(translated) or (os.path.isdir(translated) and not os.path.exists(os.path.join(translated, 'index.html'))):
            _, ext = os.path.splitext(clean_path)
            if not ext:
                self.path = '/index.html'
        return super().do_GET()

if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(('', PORT), SPAHandler) as httpd:
            print(f"Serving on http://localhost:{PORT}")
            sys.stdout.flush()
            httpd.serve_forever()
    except OSError:
        PORT = 8080
        with socketserver.TCPServer(('', PORT), SPAHandler) as httpd:
            print(f"Serving on http://localhost:{PORT}")
            sys.stdout.flush()
            httpd.serve_forever()
