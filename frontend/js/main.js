const API_BASE = window.API_BASE || "";
window.Veriscope = {
  showError(id, msg){const el=document.getElementById(id); if(el){el.textContent=msg;el.classList.remove("hidden");}},
  hide(id){document.getElementById(id)?.classList.add("hidden");},
  renderResult(data){
    document.getElementById("prediction").textContent=data.prediction || "—";
    document.getElementById("riskScore").textContent=data.risk_score ?? "—";
    document.getElementById("riskLevel").textContent=(data.risk_level || "—")+" RISK";
    document.getElementById("confidence").textContent=data.confidence!=null ? `${(data.confidence*100).toFixed(1)}%` : "—";
    document.getElementById("summary").textContent=data.summary || "—";
    document.getElementById("extractedText").textContent=data.text || "No text extracted.";
    document.getElementById("resultSection")?.classList.remove("hidden");
    localStorage.setItem("veriscope_last_result", JSON.stringify(data));
    document.getElementById("resultSection")?.scrollIntoView({behavior:"smooth",block:"start"});
  },
  renderStoredResult(){
    const raw=localStorage.getItem("veriscope_last_result");
    if(!raw)return;
    const data=JSON.parse(raw);
    this.renderResult(data);
  }
};

async function checkHealth(){
  const badge=document.getElementById("healthBadge"); if(!badge)return;
  try{const r=await fetch(`${API_BASE}/api/health`); const d=await r.json(); badge.textContent=d.status==="ok"?"API Online":"API Error";}
  catch(e){badge.textContent="API Offline";}
}
window.addEventListener("DOMContentLoaded", checkHealth);
