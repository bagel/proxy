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
            s2.send("\r\n")
            response_data = ""
            while True:
                recv_data = s2.recv(10240)
                response_data += recv_data
                if len(recv_data) < 10240:
                    break
            print base64.b64decode(response_data)
            conn.send(base64.b64decode(response_data))
            s2.close()
            conn.close()
            continue
        time.sleep(0.1)


if __name__ == "__main__":
    start_server()

