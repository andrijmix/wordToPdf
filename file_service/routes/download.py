from flask import Blueprint, current_app, send_file, render_template, request, flash, redirect, url_for
from flask.views import MethodView
import os
import zipfile
from threading import Thread

from multipart import file_path
from reportlab.lib.pagesizes import elevenSeventeen

download_bp = Blueprint("download", __name__)
import shutil
def cleanup_session_later(folder_path):
    try:
        progress_file = os.path.join(folder_path, "progress.txt")
        if os.path.exists(progress_file):
            os.remove(progress_file)
        shutil.rmtree(folder_path, ignore_errors=True)
        print(f"🧹 Session cleaned up: {folder_path}")
    except Exception as e:
        print(f"❌ Cleanup error: {e}")

class DownloadView(MethodView):
    def get(self, session_id):
        folder = os.path.join(current_app.config["UPLOAD_FOLDER"], session_id)
        if not os.path.exists(folder):
            flash("Session not found or expired.")
            return redirect(url_for("upload.upload"))

        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        if not files:
            flash("No files to download.")
            return redirect(url_for("upload.upload"))

        if len(files) == 1:
            # Один файл – повертаємо його напряму
            file_path = os.path.join(folder, files[0])
            response = send_file(file_path, as_attachment=True)
        else:
            # Більше одного – створюємо архів
            zip_filename = f"result_{session_id}.zip"
            zip_path = os.path.join(folder, zip_filename)
            with zipfile.ZipFile(zip_path, "w") as zipf:
                for fname in files:
                    if not fname.endswith(".zip"):
                        zipf.write(os.path.join(folder, fname), arcname=fname)
            response = send_file(zip_path, as_attachment=True)

        Thread(target=cleanup_session_later, args=(folder,)).start()
        return response

class FileListView(MethodView):
    def get(self, session_id):
        folder = os.path.join(current_app.config["UPLOAD_FOLDER"], session_id)
        if not os.path.exists(folder):
            flash("Session not found.")
            return redirect(url_for("upload.upload"))

        files = [
            f for f in os.listdir(folder)
            if os.path.isfile(os.path.join(folder, f)) and not f.endswith(".zip")
        ]
        return render_template("file_list.html", session_id=session_id, files=files)

# маршрути
download_bp.add_url_rule("/download/<session_id>", view_func=DownloadView.as_view("download"))
download_bp.add_url_rule("/file_service/<session_id>", view_func=FileListView.as_view("file_list"))
