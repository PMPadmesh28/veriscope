from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent / "backend"))
from app import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
