let maxItems=10;
function updateCount(){const inputs=[...document.querySelectorAll(".rank-news")];const c=document.getElementById("itemCount");if(c)c.textContent=inputs.length;}
function addRankInput(){
  const box=document.getElementById("rankingInputs"); if(!box)return;
  const n=box.querySelectorAll(".rank-input-row").length;
  if(n>=maxItems)return;
  const row=document.createElement("div");row.className="rank-input-row";
  row.innerHTML=`<span>${String(n+1).padStart(2,"0")}</span><input class="rank-news" maxlength="2000" placeholder="News item ${n+1}">`;
  box.appendChild(row);updateCount();
}
function renderRanking(items){
  const box=document.getElementById("rankingResults");if(!box)return;
  box.innerHTML=items.map((x,i)=>`<div class="rank-card"><div class="rank-number">#${i+1}</div><p>${escapeHtml(x.text)}</p><div class="rank-score"><strong>${x.risk_score}</strong><small>${escapeHtml(x.risk_level)} • ${escapeHtml(x.prediction)}</small></div></div>`).join("");
  box.classList.remove("hidden");
}
function escapeHtml(s){return String(s).replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#039;"}[m]));}
const addBtn=document.getElementById("addNewsBtn");if(addBtn)addBtn.addEventListener("click",addRankInput);
const rankBtn=document.getElementById("rankBtn");
if(rankBtn)rankBtn.addEventListener("click",async()=>{
  const texts=[...document.querySelectorAll(".rank-news")].map(x=>x.value.trim()).filter(Boolean);
  if(!texts.length){window.Veriscope.showError("rankError","Enter at least one news item.");return;}
  window.Veriscope.hide("rankError");document.getElementById("rankLoading").classList.remove("hidden");rankBtn.disabled=true;
  try{
    const r=await fetch(`${window.API_BASE||""}/api/rank`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({items:texts})});
    const d=await r.json();if(!r.ok)throw new Error(d.error||"Ranking failed.");
    renderRanking(d.ranking);localStorage.setItem("veriscope_ranking",JSON.stringify(d.ranking));
  }catch(e){window.Veriscope.showError("rankError",e.message);}
  finally{document.getElementById("rankLoading").classList.add("hidden");rankBtn.disabled=false;}
});
window.addEventListener("DOMContentLoaded",()=>{
  updateCount();
  const box=document.getElementById("rankingResults"), raw=localStorage.getItem("veriscope_ranking");
  if(box&&raw){try{renderRanking(JSON.parse(raw));}catch(e){}}
});
