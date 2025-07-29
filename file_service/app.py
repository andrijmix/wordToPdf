from flask import Flask, current_app
from file_service.routes.download import download_bp
from file_service.routes.upload import upload_bp, UploadView
from file_service.routes.progress import progress_bp
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"  # для flash-повідомлень
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "uploads")

# Створюємо папку для завантажень, якщо не існує
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# 🧩 Обгортка для виклику OCR з session_id
def after_upload_action(session_id):

    session_folder = os.path.join(app.config["UPLOAD_FOLDER"], session_id)
    print(f"📦 Post-processing for session {session_id}")

# реєстрація UploadView з передачею callback'у
upload_view = UploadView.as_view(
    "upload",
    allowed_extensions={".xlsx"},
    on_upload_done=after_upload_action
)

upload_bp.add_url_rule("/", view_func=upload_view, methods=["GET", "POST"])
upload_bp.add_url_rule("/upload", view_func=upload_view, methods=["POST"])

# Реєструємо blueprint
app.register_blueprint(upload_bp)
app.register_blueprint(download_bp)
app.register_blueprint(progress_bp)


if __name__ == "__main__":
    app.run("0.0.0.0", debug=False, port=5000)
