def calculate_risk(prediction, confidence):
    confidence=max(0.0,min(1.0,float(confidence)))
    if prediction.upper()=="FAKE":
        score=50 + round(confidence*50)
    else:
        score=round((1-confidence)*50)
    score=max(0,min(100,score))
    if score<=39: level="LOW"
    elif score<=74: level="MEDIUM"
    else: level="HIGH"
    return {"risk_score":score,"risk_level":level}
