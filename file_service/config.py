import os

class Config:
    SECRET_KEY = "dev"  # для flash-повідомлень
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
