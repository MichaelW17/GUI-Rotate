# -*- coding: UTF-8 -*-
import configparser
import os

APP_ICON = 'asset/icon.png'
APP_NAME = '智慧门店 - 会员识别系统'
APP_VERSION = 'v1.0.0'

__config = configparser.ConfigParser()
__config.read(os.path.join(os.getcwd(), 'asset', 'config', 'default_settings.ini'))

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
