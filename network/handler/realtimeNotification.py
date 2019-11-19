# -*- coding:utf-8 -*-

import threading, socket
import json
from network.connection import Connection
# import config


class RealtimeNotification(threading.Thread):
    MAX_BUFFER_SIZE = 1024 * 1000 * 10

    def __init__(self, new_info_signal, network_connection_signal):
        super().__init__()
        self.new_info_signal = new_info_signal
        self.network_connection_signal = network_connection_signal

    def run(self):
        print('-------------------------')
        # ip, port = config.COMPUTING_ENGINE_ADDRESS, config.COMPUTING_ENGINE_PORT
        ip, port = '127.0.0.1', 10101
        network_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            network_connection.connect((ip, port))
            self.network_connection_signal.emit(1)
        except Exception as e:
            print('EXCEPTION: ', e)
            self.network_connection_signal.emit(0)
            return

        jmsg = json.dumps("{'reara'}")
        network_connection.sendall(jmsg.encode("utf-8"))
        while True:
            try:
                response = network_connection.recv(self.MAX_BUFFER_SIZE)
                if response is not None and len(response) > 1:
                    jresp = json.loads(response.decode('utf-8'))

                    self.new_info_signal.emit(jresp)
            except Exception as e:
                print('EXCEPTION: ', e)
                self.network_connection_signal.emit(0)
                return
            finally:
                pass


