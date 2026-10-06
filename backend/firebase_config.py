import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
_initialized=False
_db=None

def _get_db():
    global _initialized,_db
    if _initialized:return _db
    _initialized=True
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore
        service_json=os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON","").strip()
        if not service_json:
            return None
        p=Path(service_json)
        if not p.is_absolute():
            p=Path(__file__).resolve().parent.parent / p
        if not p.exists():
            print(f"Firebase disabled: service account not found at {p}")
            return None
        try:
            app=firebase_admin.get_app()
        except ValueError:
            app=firebase_admin.initialize_app(credentials.Certificate(str(p)))
        _db=firestore.client(app)
        return _db
    except Exception as exc:
        print(f"Firebase disabled: {exc}")
        return None

def save_analysis(result):
    db=_get_db()
    if db is None:return False
    try:
        db.collection(os.getenv("FIRESTORE_COLLECTION","analyses")).add(result)
        return True
    except Exception as exc:
        print(f"Firebase save failed: {exc}")
        return False
