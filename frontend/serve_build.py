#!/usr/bin/env python3
"""
Simple static server for a React build folder with SPA fallback.
Usage: python serve_build.py [port] [directory]
Defaults: port=3000, directory=build

This serves files from the build directory and returns index.html for
any requests that do not match a static file (fixes 404 for client-side routes).
"""
import http.server
import socketserver
import sys
import os
from http.server import SimpleHTTPRequestHandler

class SPARequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)

    def do_GET(self):
        # Translate the requested path to the local filesystem path
        requested_path = self.translate_path(self.path)

        # If the requested file doesn't exist, serve index.html instead
        if not os.path.exists(requested_path):
            # Force serve index.html
            self.path = '/index.html'
        return super().do_GET()


def run(port=3000, directory='build'):
    port = int(port)
    if not os.path.isdir(directory):
        print(f"Error: directory '{directory}' does not exist. Run a build first (npm run build).")
        sys.exit(1)

    handler_class = lambda *args, **kwargs: SPARequestHandler(*args, directory=directory, **kwargs)

    with socketserver.TCPServer(("", port), handler_class) as httpd:
        print(f"Serving '{directory}' at http://0.0.0.0:{port} (SPA fallback enabled)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Shutting down server")
            httpd.server_close()


if __name__ == '__main__':
    port = 3000
    directory = 'build'
    if len(sys.argv) >= 2:
        port = int(sys.argv[1])
    if len(sys.argv) >= 3:
        directory = sys.argv[2]
    run(port, directory)
