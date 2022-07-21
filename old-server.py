import network
import os
import time
try:
  import usocket as socket
except:
  import socket

server_socket = None


def handle_not_found(conn, url):
    send_response(conn, "Path not found: {}".format(url), status_code=404)

def send_header(conn, status_code=200, content_length=None ):
    conn.sendall("HTTP/1.0 {} OK\r\n".format(status_code))
    conn.sendall("Content-Type: text/html\r\n")
    if content_length is not None:
      conn.sendall("Content-Length: {}\r\n".format(content_length))
    conn.sendall("\r\n")


def send_response(conn, payload, status_code=200):
    content_length = len(payload)
    send_header(conn, status_code, content_length)
    if content_length > 0:
        conn.sendall(payload)
    conn.close()

def home_page():
  html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
  <body><h1>Hello, World!</h1></body></html>"""
  return html


def stop():
    global server_socket

    if server_socket:
        server_socket.close()
        server_socket = None
        
        
def start(port=80):
    global server_socket

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(5)

    print("Web Server Started. Waiting for connection...")

    while True:
        conn, addr = server_socket.accept()
        print('client connected from', addr)
        try:
            conn.settimeout(5.0)
            request = conn.recv(1024)
            print('Content = %s' % str(request))
            response = home_page()
            send_response(conn, response)
        finally:
            conn.close()