#!/usr/bin/env python
# -*- coding:utf-8 -*-
#

import socket
import threading
import socketserver
import json, types, string
import os, time
from network.utils import img_util


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        jdata = json.loads(data.decode('utf-8'))
        print("Receive data from '%r'" % (data))
        print("Receive jdata from '%r'" % (jdata))

        response1 = {
            "customer_id": "350991",
            "customer_name": "张安国",
            "customer_captured_time": time.time(),
            'customer_image': img_util.image2str('../asset/test_face/zhanganguo2.png')
        }
        response2 = {
            "customer_id": "342601",
            "customer_name": "chen yanxin",
            "customer_captured_time": time.time(),
            'customer_image': img_util.image2str('../asset/test_face/chenyanxin.png')
        }

        jresp1 = json.dumps(response1)
        jresp2 = json.dumps(response2)
        for i in range(3):
            self.request.sendall(jresp1.encode('utf-8'))
            time.sleep(1)
            self.request.sendall(jresp2.encode('utf-8'))
            time.sleep(1)
        # rec_cmd = "proccess "+rec_src+" -o "+rec_dst
        # print ("CMD '%r'" % (rec_cmd))
        # os.system(rec_cmd)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "127.0.0.1", 10101

    socketserver.TCPServer.allow_reuse_address = True
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)
    print(" .... waiting for connection")

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
