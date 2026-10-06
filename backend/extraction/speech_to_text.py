from pathlib import Path
import os

_model = None

def transcribe_video(path):
    global _model
    try:
        import whisper
    except ImportError:
        raise RuntimeError("Whisper is not installed. Run: pip install openai-whisper")
    try:
        if _model is None:
            _model=whisper.load_model(os.getenv("WHISPER_MODEL","tiny"))
        result=_model.transcribe(str(Path(path)), fp16=False)
        return (result.get("text") or "").strip()
    except Exception as exc:
        raise RuntimeError(f"Video transcription failed. Check that ffmpeg is installed. Details: {exc}")
