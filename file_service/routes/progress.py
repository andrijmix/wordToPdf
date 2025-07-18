from flask import Blueprint, jsonify, current_app
import os

progress_bp = Blueprint("progress", __name__)

@progress_bp.route("/progress_meta/<session_id>")
def progress_meta(session_id):
    session_folder = os.path.join(current_app.config["UPLOAD_FOLDER"], session_id)
    progress_file = os.path.join(session_folder, "progress.txt")

    if os.path.exists(progress_file):
        last_modified = os.path.getmtime(progress_file)
    else:
        last_modified = 0

    return jsonify({"last_modified": last_modified})


@progress_bp.route("/progress/<session_id>")
def get_progress(session_id):
    session_folder = os.path.join(current_app.config["UPLOAD_FOLDER"], session_id)
    progress_file = os.path.join(session_folder, "progress.txt")

    try:
        with open(progress_file, "r") as f:
            percent = int(f.read().strip())
    except Exception:
        percent = 0

    return jsonify({"progress": percent})


@progress_bp.route("/cancel/<session_id>", methods=["POST"])
def cancel_ocr(session_id):
    session_folder = os.path.join(current_app.config["UPLOAD_FOLDER"], session_id)
    cancel_file = os.path.join(session_folder, "cancel.txt")
    with open(cancel_file, "w") as f:
        f.write("1")
    return jsonify({"status": "canceled"})
