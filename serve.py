"""Local static preview server for the AGDAM SOLUTION company site.

    python serve.py [port]

Binds dual-stack (::/0.0.0.0) so http://localhost:PORT works whether the
browser resolves localhost to ::1 or 127.0.0.1.
"""
import http.server
import os
import socket
import socketserver
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5340


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stdout.write("%s - %s\n" % (self.address_string(), fmt % args))
        sys.stdout.flush()


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    address_family = socket.AF_INET6

    def server_bind(self):
        self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        super().server_bind()


if __name__ == "__main__":
    with Server(("::", PORT), Handler) as httpd:
        print("serving %s on http://localhost:%d" % (ROOT, PORT))
        sys.stdout.flush()
        httpd.serve_forever()
