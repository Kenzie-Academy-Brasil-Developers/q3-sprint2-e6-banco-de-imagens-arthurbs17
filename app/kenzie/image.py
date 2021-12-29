import os
import dotenv
from werkzeug.utils import secure_filename
from werkzeug.exceptions import Conflict

dotenv.load_dotenv()

files_directory = os.getenv("FILES_DIRECTORY")
allowed_extensions = os.getenv("ALLOWED_EXTENSIONS").split(',')
max_content_length = os.getenv("MAX_CONTENT_LENGTH")

def create_directories():

    os.makedirs(files_directory, exist_ok=True)

    for extension in allowed_extensions:
        path = f"{files_directory}/{extension}"
        os.makedirs(path, exist_ok=True)

def receive_file(files):
    file_received = dict()
    for key, value in enumerate(files.values(), 1):
        filename = secure_filename(value.filename).lower()
        extension = filename.split(".")[-1]

        if extension == "jpeg":
            extension = "jpg"
            split_filename = filename.split(".")
            split_filename[-1] = "jpg"
            filename = ".".join(split_filename)

        if os.path.exists(f"{files_directory}/{extension}/{filename}"):
            raise Conflict
        
        value.save(os.path.join(f"{files_directory}/{extension}", filename))
        file_received[f"file_{key}"] = filename
    
    return file_received