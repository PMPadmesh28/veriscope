def extract_text_from_image(path):
    try:
        import pytesseract
        from PIL import Image
        image=Image.open(path)
        text=pytesseract.image_to_string(image)
        return text.strip()
    except ImportError:
        raise RuntimeError("OCR dependencies are missing. Install pytesseract and Pillow.")
    except Exception as exc:
        raise RuntimeError(f"OCR failed: {exc}")
