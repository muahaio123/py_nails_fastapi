#!/usr/bin/env python3
"""Simple launcher for a static HTTP server to avoid running via -m http.server.

This avoids the RuntimeWarning that can occur when debugpy/runpy imports
the package 'http' before executing the 'http.server' module.

Usage: python run_http_server.py 8080
"""
import http.server
import socketserver
import sys


def main():
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass

    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving HTTP on port {port} (http://localhost:{port}/) ...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Shutting down server")


if __name__ == "__main__":
    main()
