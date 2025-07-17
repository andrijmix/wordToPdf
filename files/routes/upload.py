import shutil
import zipfile

from flask import Blueprint, request, render_template, redirect, url_for, flash, current_app
from flask.views import MethodView
from pathlib import Path
import os
import uuid

upload_bp = Blueprint("upload", __name__)

class UploadView(MethodView):
    def __init__(self, allowed_extensions):
        self.allowed_extensions = allowed_extensions

    def get(self):
        session_id = request.args.get("session_id", "")
        return render_template("upload.html", session_id=session_id)

    def post(self):
        files = request.files.getlist("files")
        if not files or files[0].filename == "":
            flash("No files selected!")
            return redirect(url_for("upload.upload"))

        session_id = str(uuid.uuid4())
        session_folder = os.path.join(current_app.config["UPLOAD_FOLDER"], session_id)
        os.makedirs(session_folder, exist_ok=True)

        for file in files:
            filename = Path(file.filename).name
            ext = Path(filename).suffix.lower()

            if ext in self.allowed_extensions:
                file_path = os.path.join(session_folder, filename)
                file.save(file_path)

                if ext == ".zip":
                    try:
                        with zipfile.ZipFile(file_path, "r") as zip_ref:
                            zip_ref.extractall(session_folder)
                        os.remove(file_path)
                    except zipfile.BadZipFile:
                        flash(f"{filename} is not a valid ZIP file.")
                        os.remove(file_path)
            else:
                flash(f"{filename} skipped (not allowed).")

        # Delete files not in allowed extensions
        for item in os.listdir(session_folder):
            ext = Path(item).suffix.lower()
            if ext not in self.allowed_extensions and ext != ".pdf":
                file_path = os.path.join(session_folder, item)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)

        flash("Files processed.")
        return redirect(url_for("upload.upload", session_id=session_id))

# реєстрація
upload_view = UploadView.as_view("upload", allowed_extensions={".pdf", ".zip"})
upload_bp.add_url_rule("/", view_func=upload_view, methods=["GET", "POST"])
upload_bp.add_url_rule("/upload", view_func=upload_view, methods=["POST"])
