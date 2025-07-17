from flask import Flask
from config import Config
from routes.download import download_bp
from routes.upload import upload_bp
import os

app = Flask(__name__)
app.config.from_object(Config)

# Створюємо папку для завантажень, якщо не існує
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Реєструємо blueprint
app.register_blueprint(upload_bp)
app.register_blueprint(download_bp)

if __name__ == "__main__":
    app.run(debug=False, port=5000)
