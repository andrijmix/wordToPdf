from waitress import serve
from app import app

serve(app, host="0.0.0.0", port=8080, max_request_body_size=10073741824)  # 10 GB limit
