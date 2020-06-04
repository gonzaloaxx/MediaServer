#!usr/bin/python3
#-*- coding:utf-8 -*-

from os import listdir, remove
from os.path import isdir, isfile, join

from flask import Flask, request, jsonify, send_file
from flask_httpauth import HTTPBasicAuth

from werkzeug.security import check_password_hash
from werkzeug.exceptions import *
from werkzeug.utils import secure_filename

from config import AppConfig


app = Flask(__name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if (username in AppConfig.USERS) and \
            (check_password_hash(AppConfig.USERS.get(username), password)):
        return username


@app.route("/api/storage", methods=["GET"])
def storage():
    if isdir(AppConfig.UPLOAD_FOLDER):
        resources = listdir(AppConfig.UPLOAD_FOLDER)

        message = jsonify({"Message" : resources})
        return message

    raise InternalServerError


@app.route("/api/upload", methods=["POST"])
@auth.login_required
def upload():
    if not isdir(AppConfig.UPLOAD_FOLDER):
        raise InternalServerError

    if not request.files.get("file"):
        raise BadRequest

    file = request.files["file"]
    filename = file.filename

    if filename == "file":
        raise BadRequest

    if not is_allowed_filetype(filename):
        raise UnsupportedMediaType

    secure_name = secure_filename(filename)
    filepath = join(AppConfig.UPLOAD_FOLDER, secure_name)

    if isfile(filepath):
        raise Conflict

    file.save(filepath)
    message = jsonify({"Message": "File successfully uploaded"})
    return message


@app.route("/api/delete", methods=["DELETE"])
@auth.login_required
def delete():
    if not isdir(AppConfig.UPLOAD_FOLDER):
        raise InternalServerError

    if not request.args.get("filename"):
        raise BadRequest

    filename = request.args.get("filename")
    filepath = join(AppConfig.UPLOAD_FOLDER, filename)

    if not isfile(filepath):
        raise Conflict

    remove(filepath)
    message = jsonify({"Message" : "File successfully deleted"})
    return message


@app.route("/api/download", methods=["GET"])
@auth.login_required
def download():
    if not isdir(AppConfig.UPLOAD_FOLDER):
        raise InternalServerError

    if not request.args.get("filename"):
        raise BadRequest

    filename = request.args.get("filename")
    filepath = join(AppConfig.UPLOAD_FOLDER, filename)

    if not isfile(filepath):
        raise Conflict

    return send_file(filepath, as_attachment=True)



def is_allowed_filetype(filename):
    if "*" in AppConfig.ALLOWED_FILETYPES:
        return True
    
    elif filename.split(".")[-1] in AppConfig.ALLOWED_FILETYPES:
        return True


if __name__ == '__main__':
    app.config["SECRET_KEY"] = "SECRET_KEY_HERE"
    app.run(AppConfig.HOST, AppConfig.PORT, AppConfig.DEBUG)
