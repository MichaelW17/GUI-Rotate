# -*- coding: UTF-8 -*-
import configparser
import os

APP_ICON = 'asset/new_icon.png'
APP_NAME = '智慧门店 - 智能电子称'
APP_VERSION = 'v1.0.0'

__config_file = os.path.join(os.getcwd(), 'asset', 'config', 'settings.ini')
__config = configparser.ConfigParser()
__config.read(__config_file)

COMPUTING_ENGINE_ADDRESS = __config.get('network', 'computing_engine_address')
COMPUTING_ENGINE_PORT = __config.getint('network', 'computing_engine_port')

CAMERA_FRAME_WIDTH = __config.getint('camera', 'frame_width')
CAMERA_FRAME_HEIGHT = __config.getint('camera', 'frame_height')
CAMERA_FRAME_RATE = __config.getint('camera', 'frame_rate')
CAMERA_VIDEO_URL_1 = __config.get('camera', 'video_url1')
CAMERA_VIDEO_URL_2 = __config.get('camera', 'video_url2')

DATABASE_IP_ADDRESS = __config.get('database', 'ip_address')
DATABASE_IP_PORT = __config.get('database', 'ip_port')
DATABASE_USER = __config.get('database', 'user')
DATABASE_PASSWORD = __config.get('database', 'password')


def save():
    with open(__config_file, 'w+') as f:
        __config.write(f)


def add_section(section):
    __config.add_section(section)


def set_attribute(section, attribute_name, attribute_value):
    __config.set(section, attribute_name, attribute_value)
