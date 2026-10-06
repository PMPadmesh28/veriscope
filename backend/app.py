from flask import Flask, send_file
from flask_cors import CORS
from pathlib import Path
from routes import api

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024

CORS(app)

app.register_blueprint(api, url_prefix="/api")

FRONTEND_DIR = BASE_DIR.parent / "frontend"


@app.get("/")
def home():
    return send_file(FRONTEND_DIR / "index.html")


@app.get("/<path:path>")
def frontend(path):
    target = FRONTEND_DIR / path

    if target.is_file():
        return send_file(target)

    return send_file(FRONTEND_DIR / "index.html")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )