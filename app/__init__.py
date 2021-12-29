from flask import Flask, request, jsonify, send_from_directory
from .kenzie import create_directories, receive_file, files_directory, allowed_extensions, max_content_length
from werkzeug.exceptions import Conflict, RequestEntityTooLarge, NotFound
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = int(max_content_length)

create_directories()

@app.post("/upload")
def upload_file():
    try:
        files = request.files
        file_received = receive_file(files)
    except(Conflict):
        return{"message": "Arquivo já existente!"}
    except(RequestEntityTooLarge):
        return{"message": "Arquivo excede o tamanho permitido(1mb)!"}
    
    else:
        return jsonify(file_received), 201