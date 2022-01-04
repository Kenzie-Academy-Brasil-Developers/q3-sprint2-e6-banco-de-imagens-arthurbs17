import os, tempfile, shutil
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

def list_files_presents():
    list_files = []
    for extension in allowed_extensions:
        if len(os.listdir(f"./files/{extension}")) != 0:
            list_files.append(' '.join(os.listdir(f"./files/{extension}")))
    if len(list_files) == 0:
        raise FileNotFoundError
    else:
        return ' '.join(list_files).split()

def list_files_per_extension(extension):
    list_files = []
    extension = extension.lower()
    if extension == "jpeg":
        extension = "jpg"
    try:
        list_files = os.listdir(f"./files/{extension}")
        if len(list_files) == 0:
            return {"message": f"Nenhum arquivo {extension} existe no servidor!"}
    except TypeError:
        raise FileNotFoundError
    
    return list_files

def path_file(file_name):
    file_name = file_name.lower()
    return f"../files/{file_name.split('.')[-1]}"

def create_zip_directory(query_params, zip_name):
    extension = query_params['file_extension'].lower()
    if extension == "jpeg":
        extension = "jpg"
    path = f"{files_directory}/{extension}"

    if len(os.listdir(f"./files/{extension}")) == 0:
        raise FileNotFoundError

    shutil.make_archive(zip_name, 'zip', path)
    shutil.move(f"./{zip_name}.zip", "/tmp")
    
    return {}