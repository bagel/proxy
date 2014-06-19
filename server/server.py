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
    print data
    if data[0] == 'GET':
        data_url = data[1].split('/')
        host = data_url[2]
        port = 80
        if ':' in host:
            port = int(host.split(':')[-1])
        data_url.pop(2)
        data_url.pop(0)
        data[1] = '/'.join(data_url)
    elif data[0] == 'CONNECT':
        host = data[1].split(':')[0]
        port = 443   
    data = ' '.join(data)
    request_data = request_data[1:]
    request_data.insert(0, data)
    for i in xrange(len(request_data)):
        if re.match('Accept-Encoding', request_data[i]):
            request_data.pop(i)
            break
    request_data = '\r\n'.join(request_data)
    print request_data
    s.connect((host, port))
    s.send(request_data)
    fp = s.makefile()
    response_data = ""
    line = fp.readline()
    while line:
        print [line]
        if line == '\r\n':
            break
        if re.match('Content-Length', line):
            length = line.split(': ')[1].strip()
        response_data += line
        line = fp.readline()
    response_data += '\r\n'
    response_data += fp.read(int(length))
    #print response_data
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
            request_data = base64.b64decode(request_data)
            print request_data
            response_data = request_sock(request_data)
            #print response_data
            conn.send(base64.b64encode(response_data))
            conn.send('\r\n\r\n')
            if conn.recv(1024) == '\r\n':
                conn.close()
            continue
        time.sleep(0.1)

if __name__ == "__main__":
    start_server()
