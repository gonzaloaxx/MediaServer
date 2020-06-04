#!usr/bin/python3
#-*- coding:utf-8 -*-

from werkzeug.security import generate_password_hash

class ServerConfig:
    HOST = ""
    PORT = ""
    DEBUG = False

class AuthConfig:
    USERS = {
        "username_here" : generate_password_hash("password_here")
    }

class FileConfig:
    UPLOAD_FOLDER = r""
    ALLOWED_FILETYPES = ("*")


class AppConfig:
    HOST = ServerConfig.HOST
    PORT = ServerConfig.PORT
    DEBUG = ServerConfig.DEBUG
    USERS = AuthConfig.USERS
    UPLOAD_FOLDER = FileConfig.UPLOAD_FOLDER
    ALLOWED_FILETYPES = FileConfig.ALLOWED_FILETYPES
