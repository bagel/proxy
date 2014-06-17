#!/usr/bin/env python

import sys
import os
import json
import base64
import urllib2
import socket
import time
import re
import urlparse


def request(method, uri, protocol, headers):
    req = urllib2.Request(url=uri, headers=headers)
    req.get_method = lambda: method
    res = urllib2.urlopen(req)
    response_body = res.read()
    response_data = "HTTP/1.1 200 OK\r\n"
    for k, v in res.headers.items():
        response_data += "%s: %s\r\n" % (k.title(), v)
    response_data += "\r\n" + response_body
    return response_data

def request_sock(request_data):
    s = socket.socket()
    request_data = request_data.split('\r\n')
    data = request_data[0].split(' ')
    if data[0] != 'GET':
        return "HTTP/1.1 500\r\n"
    data_url = data[1].split('/')
    host = data_url[2]
    port = 80
    if ':' in host:
        port = int(host.split(':')[-1])
    data_url.pop(2)
    data_url.pop(0)
    data[1] = '/'.join(data_url)
    data = ' '.join(data)
    request_data = request_data[1:]
    request_data.insert(0, data)
    request_data = '\r\n'.join(request_data)
    print request_data
    s.connect((host, port))
    s.send(request_data)
    response_data = s.recv(10240)
    return response_data

def start_server():
    s1 = socket.socket()
    s1.bind(('0.0.0.0', 8080))
    s1.listen(1)
    while True:
        conn, addr = s1.accept()
        if addr:
            request_data = ""
            while True:
                recv_data = conn.recv(10240)
                request_data += recv_data
                if len(recv_data) < 10240:
                    break
            request_data = base64.b64decode(request_data.strip())
            print request_data
            response_data = request_sock(request_data)
            print response_data
            conn.send(base64.b64encode(response_data))
            conn.close()
            continue
        time.sleep(0.1)

if __name__ == "__main__":
    start_server()
