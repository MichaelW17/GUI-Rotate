# -*- coding:utf-8 -*-

import socket
# import config


class Connection:
    __connection_with_computing_engine = None

    @classmethod
    def get_connection_with_computing_engine(cls):
        if Connection.__connection_with_computing_engine is None:
            # ip, port = config.COMPUTING_ENGINE_ADDRESS, config.COMPUTING_ENGINE_PORT
            ip, port = '127.0.0.1', 10101
            Connection.__connection_with_computing_engine = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                Connection.__connection_with_computing_engine.connect((ip, port))
            except socket.error as e:
                Connection.__connection_with_computing_engine = None
                print(e)

        return Connection.__connection_with_computing_engine

