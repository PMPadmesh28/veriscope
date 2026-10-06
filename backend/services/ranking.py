def rank_items(items):
    return sorted(items,key=lambda x:(x.get("risk_score",0),x.get("confidence",0)),reverse=True)
