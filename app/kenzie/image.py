import os
import dotenv
from werkzeug.utils import secure_filename
from werkzeug.exceptions import Conflict

dotenv.load_dotenv()

files_directory = os.getenv("FILES_DIRECTORY")
allowed_extensions = os.getenv("ALLOWED_EXTENSIONS").split(',')
max_content_length = os.getenv("MAX_CONTENT_LENGTH")

os.makedirs(files_directory, exist_ok=True)

for extension in allowed_extensions:
    path = f"{files_directory}/{extension}"
    os.makedirs(path, exist_ok=True)