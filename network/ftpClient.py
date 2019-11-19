#!/usr/bin/env python
# -*- coding:utf-8 -*-
#

import socket
import threading
import socketserver
import json
from network.utils import img_util


def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))

    try:
        print("Send: {}".format(message))
        sock.sendall(message.encode("utf-8"))

        for i in range(5):
            response = sock.recv(1024*1000*10)
            jresp = json.loads(response.decode('utf-8'))
            image_byte = img_util.str2image(jresp[0]['image'])
            with open('testss'+str(i)+'.jpg', 'wb') as f:
                f.write(image_byte)  # 将图片存到当前文件的fileimage文件中

            print("Recv: ", jresp)

    finally:
        sock.close()


if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 20000
    # msg1 = [{'src':"zj", 'dst':"zjdst"}]
    # msg2 = [{'src':"ln", 'dst':"lndst"}]
    # msg3 = [{'src':"xj", 'dst':"xjdst"}]

    msg = [{
        "request": 1
    }]

    # jmsg1 = json.dumps(msg1)
    # jmsg2 = json.dumps(msg2)
    # jmsg3 = json.dumps(msg3)

    jmsg = json.dumps(msg)

    # client(HOST, PORT, jmsg1)
    # client(HOST, PORT, jmsg2)
    # client(HOST, PORT, jmsg3)

    client(HOST, PORT, jmsg)
