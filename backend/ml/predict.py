from pathlib import Path
import pickle
from .preprocess import clean_text

BASE=Path(__file__).resolve().parent
with open(BASE/"model.pkl","rb") as f: MODEL=pickle.load(f)
with open(BASE/"vectorizer.pkl","rb") as f: VECTORIZER=pickle.load(f)

def predict_text(text: str):
    cleaned=clean_text(text)
    X=VECTORIZER.transform([cleaned])
    probabilities=MODEL.predict_proba(X)[0]
    classes=list(MODEL.classes_)
    idx=probabilities.argmax()
    label=str(classes[idx]).upper()
    confidence=float(probabilities[idx])
    return {"prediction":label,"confidence":confidence}
