import os
import uuid
from flask import request, send_file

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def save_uploaded_file(file_field_name="file") -> str:
    """
    Saves the uploaded file from request and returns the file path.
    """
    if file_field_name not in request.files:
        raise ValueError("No file field provided")

    file = request.files[file_field_name]
    if file.filename == "":
        raise ValueError("Empty filename")

    filename = f"{uuid.uuid4()}.pdf"
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)
    return path

def send_file_response(path: str, as_name: str = "output.pdf"):
    """
    Sends the specified file as Flask response.
    """
    return send_file(path, as_attachment=True, download_name=as_name)
