from flask import Blueprint, request, jsonify
from pathlib import Path
import uuid
from ml.predict import predict_text
from extraction.ocr import extract_text_from_image
from extraction.speech_to_text import transcribe_video
from services.risk_score import calculate_risk
from services.summarizer import summarize_text
from services.ranking import rank_items
from firebase_config import save_analysis

api = Blueprint("api", __name__)
ROOT = Path(__file__).resolve().parent.parent
IMAGE_DIR = ROOT / "uploads" / "images"
VIDEO_DIR = ROOT / "uploads" / "videos"
IMAGE_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

@api.get("/health")
def health():
    return jsonify({"status":"ok","service":"veriscope-api"})

@api.post("/analyze")
def analyze():
    try:
        text = (request.form.get("text") or "").strip()
        source = "text"
        extracted = ""
        if "image" in request.files and request.files["image"].filename:
            f=request.files["image"]
            ext=Path(f.filename).suffix.lower() or ".jpg"
            path=IMAGE_DIR/f"{uuid.uuid4().hex}{ext}"
            f.save(path)
            extracted=extract_text_from_image(path)
            if extracted.strip(): text=extracted
            source="image"
        elif "video" in request.files and request.files["video"].filename:
            f=request.files["video"]
            ext=Path(f.filename).suffix.lower() or ".mp4"
            path=VIDEO_DIR/f"{uuid.uuid4().hex}{ext}"
            f.save(path)
            extracted=transcribe_video(path)
            if extracted.strip(): text=extracted
            source="video"
        if not text:
            return jsonify({"error":"No usable text was provided or extracted."}),400
        pred= predict_text(text)
        risk=calculate_risk(pred["prediction"],pred["confidence"])
        summary=summarize_text(text)
        result={**pred,**risk,"summary":summary,"text":text,"source":source}
        save_analysis(result)
        return jsonify(result)
    except Exception as exc:
        return jsonify({"error":str(exc)}),500

@api.post("/rank")
def rank():
    try:
        data=request.get_json(silent=True) or {}
        items=data.get("items",[])
        if not isinstance(items,list) or not items or len(items)>10:
            return jsonify({"error":"Provide 1 to 10 news items."}),400
        cleaned=[str(x).strip() for x in items if str(x).strip()]
        if not cleaned:return jsonify({"error":"News items cannot be empty."}),400
        results=[]
        for text in cleaned:
            pred=predict_text(text); risk=calculate_risk(pred["prediction"],pred["confidence"])
            results.append({**pred,**risk,"text":text,"summary":summarize_text(text)})
        return jsonify({"ranking":rank_items(results)})
    except Exception as exc:
        return jsonify({"error":str(exc)}),500
