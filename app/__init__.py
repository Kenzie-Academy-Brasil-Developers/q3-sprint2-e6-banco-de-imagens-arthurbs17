from flask import Flask, request, jsonify, send_from_directory, render_template

from .kenzie import create_directories, receive_file, list_files_presents, list_files_per_extension, path_file, create_zip_directory, files_directory, allowed_extensions, max_content_length
from werkzeug.exceptions import Conflict, NotFound, RequestEntityTooLarge
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = int(max_content_length)

create_directories()

@app.get("/")
def home():
    return render_template("home.html")

@app.post("/upload")
def upload_file():
    try:
        files = request.files
        file_received = receive_file(files)
    except(Conflict):
        return{"message": "Arquivo já existente!"}, 409
    except(RequestEntityTooLarge):
        return{"message": "Arquivo excede o tamanho permitido(1mb)!"}, 413
    except(FileNotFoundError):
        return{"message": "Extensão não permitida nesse banco!"}, 415
    else:
        return jsonify(file_received), 201

@app.get("/files/")
def list_files():
    try:
        files = list_files_presents()
    except (FileNotFoundError):
        return {"message": "Ainda não existem arquivos armazenados!"}, 404
    return jsonify(files), 200

@app.get("/files/<extension>")
def extension_list_files(extension):
    try:
        files = list_files_per_extension(extension)
        return jsonify(files), 200
    except FileNotFoundError:
        return {"message": "Tipo não suportado no servidor"}, 404


@app.get("/download/<file_name>")
def download_file(file_name):
    file_path = path_file(file_name)
    correct_path = file_name.lower()
    try:
        return send_from_directory(
            directory=file_path,
            path=correct_path,
            as_attachment=True
        ), 200
    except NotFound:
        return {"message": "Arquivo não encontrado!"}, 404

@app.get("/download-zip/")
def download_directory_zip():
    query_params = request.args
    zip_file_name = "files_"+query_params["file_extension"]

    try:
        create_zip_directory(query_params, zip_file_name)
        return send_from_directory(
            directory="/tmp",
            path=f"{zip_file_name}.zip",
            as_attachment=True
        ), 200
    except FileNotFoundError:
        return {"message": "Arquivos desta extensão não encontrados!"}, 404