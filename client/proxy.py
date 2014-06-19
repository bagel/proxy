import sys
import os
import json
import base64
import urllib2
import socket
import time


class HTTPProxy:
    def __init__(self):
        pass

    def listen(self):
        s = socket.socket()
        s.bind(('0.0.0.0', 8080))
        s.listen(1)
        conn, addr = s.accept()
        while 1:
            print conn.recv(10240)


def start_server():
    s1 = socket.socket()
    s1.bind(('0.0.0.0', 8080))
    s1.listen(1)
    while True:
        conn, addr = s1.accept()
        if addr:
            request_data = conn.recv(10240)
            print request_data
            s2 = socket.socket()
            s2.connect(('116.251.210.147', 8080))
            s2.send(base64.b64encode(request_data))
            s2.send("\r\n\r\n")
            response_data = ""
            fp = s2.makefile()
            line = fp.readline()
            while line:
                response_data += line
                line = fp.readline()
                if line == '\r\n':
                    break
            s2.send('\r\n')
            response_data = response_data.strip()
            #print base64.b64decode(response_data)
            conn.send(base64.b64decode(response_data))
            s2.close()
            conn.close()
            continue
        time.sleep(0.1)


if __name__ == "__main__":
    start_server()

