const analyzeBtn=document.getElementById("analyzeBtn");
if(analyzeBtn){
  analyzeBtn.addEventListener("click", async ()=>{
    const text=document.getElementById("newsText").value.trim();
    const image=document.getElementById("imageFile").files[0];
    const video=document.getElementById("videoFile").files[0];
    if(!text && !image && !video){window.Veriscope.showError("errorBox","Enter text or select an image/video.");return;}
    window.Veriscope.hide("errorBox"); document.getElementById("loading").classList.remove("hidden"); analyzeBtn.disabled=true;
    try{
      const fd=new FormData();
      if(text)fd.append("text",text);
      if(image)fd.append("image",image);
      if(video)fd.append("video",video);
      const r=await fetch(`${window.API_BASE||""}/api/analyze`,{method:"POST",body:fd});
      const d=await r.json();
      if(!r.ok)throw new Error(d.error||"Analysis failed.");
      window.Veriscope.renderResult(d);
    }catch(e){window.Veriscope.showError("errorBox",e.message);}
    finally{document.getElementById("loading").classList.add("hidden");analyzeBtn.disabled=false;}
  });
}
