# VeriScope — ML-Based Multimodal Fake News Detection and Risk Ranking

College Thinkathon prototype for October 9, 2026.

## What it does

VeriScope is a detection/flagging prototype. It accepts:
- Text news → preprocessing → TF-IDF → Logistic Regression → prediction → risk score → summary
- Image/screenshot → Tesseract OCR → extracted text → ML pipeline
- Video/reel → audio extraction through Whisper → transcript → ML pipeline

It also ranks up to 10 text news items from highest to lowest prototype risk.

**Important:** The included ML dataset is intentionally tiny and is for demonstrating the application pipeline only. It is NOT scientifically accurate and must not be presented as a validated misinformation detector.

The risk score is a prototype metric, not a scientifically validated probability of misinformation.

## Project structure

```text
fake-news-detector/
├── frontend/
├── backend/
├── data/
├── uploads/
├── tests/
├── requirements.txt
├── .env
├── .gitignore
├── README.md
└── run.py
```

## 1. Ubuntu prerequisites

Install Python, pip, Tesseract OCR and ffmpeg:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv tesseract-ocr ffmpeg
```

Check them:

```bash
python3 --version
tesseract --version
ffmpeg -version
```

Whisper uses ffmpeg to read audio/video.

## 2. Open the project

Extract the ZIP, then:

```bash
cd fake-news-detector
code .
```

If `code` is not available, open VS Code normally and choose **File → Open Folder**.

## 3. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

After activation your terminal should show something like `(.venv)`.

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Whisper can take time to install because it also needs PyTorch. On a Celeron laptop, use the `tiny` model for the demo.

## 4. Run

From the project root:

```bash
python run.py
```

Open:

```text
http://127.0.0.1:5000
```

The API health endpoint is:

```text
http://127.0.0.1:5000/api/health
```

Do not close the terminal while using the application.

## 5. Test text

1. Open the homepage.
2. Paste a short news claim into **News text**.
3. Click **Analyze News**.
4. Review Fake/Real, confidence, risk score, risk level and summary.

Because the training dataset is tiny, predictions are only a demonstration of the end-to-end pipeline.

## 6. Test an image

Use a clear JPG/PNG screenshot containing a few lines of English news text.

1. Select the image.
2. Click **Analyze News**.
3. Tesseract OCR extracts the text.
4. The extracted text is sent to the same ML pipeline.
5. The result displays the extracted text.

If OCR is poor, use a high-resolution image with strong contrast and large text.

## 7. Test a video/reel

Use a short local video with clear spoken English.

1. Select the video.
2. Click **Analyze News**.
3. Whisper `tiny` loads on first use and may take a while on CPU.
4. The transcript becomes the text sent to the ML model.

Keep the demo video short (for example 10–30 seconds) because the laptop is CPU-limited.

If video processing fails, first check:

```bash
ffmpeg -version
```

## 8. Rank up to 10 news items

1. Scroll to **Compare up to 10 news items**.
2. Enter one claim per box.
3. Click **+ Add news item** until you have the desired number, up to 10.
4. Click **Rank News**.
5. Results appear highest-risk first.

The ranking endpoint is:

```text
POST /api/rank
```

## 9. Firebase (optional)

Firebase is not needed for local ML processing. The application works without it.

To enable Firestore history:

1. Create a Firebase project in the Firebase Console.
2. Enable Firestore Database.
3. Create a service account with appropriate permissions.
4. Download its JSON key.
5. Put the JSON file in a local `secrets/` directory.
6. Set the path in `.env`, for example:

```text
FIREBASE_SERVICE_ACCOUNT_JSON=secrets/firebase-service-account.json
```

The `.gitignore` already ignores `secrets/` and common Firebase credential filenames.

**Never commit the service-account JSON file. Never paste private credentials into Python, HTML or JavaScript.**

The backend saves analysis results to the Firestore collection configured by `FIRESTORE_COLLECTION`.

## 10. GitHub safely

Create a repository on GitHub, then from the project root:

```bash
git init
git add .
git status
```

Before committing, check that `.env` and any Firebase JSON are NOT listed.

Then:

```bash
git commit -m "Initial VeriScope Thinkathon prototype"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Never upload:
- `.env`
- Firebase service-account JSON
- API keys
- passwords/tokens
- private certificates/keys
- personal/private datasets
- large local uploads

If a secret is accidentally committed, removing the file later is not enough: rotate/revoke the secret.

## 11. Thinkathon demo plan

A simple 5-minute demo:

1. **Problem (30 sec):** Social-media misinformation can appear as text, screenshots and reels.
2. **Architecture (45 sec):** Frontend → Flask → OCR/Whisper → TF-IDF + Logistic Regression → risk score → summary.
3. **Text demo (60 sec):** Analyze one news claim.
4. **Image demo (60 sec):** Upload a screenshot and show extracted OCR text.
5. **Video demo (60 sec):** Upload a short reel and show transcript + result.
6. **Ranking demo (45 sec):** Enter several claims and show highest-risk ordering.
7. **Limitations (30 sec):** Explain that the demo model uses a tiny dataset and the risk score is a prototype metric, not a validated probability.

## 12. Suggested presentation wording

Say:

> "This prototype does not automatically delete social-media content. It flags and ranks potentially risky news so a human can investigate further."

Avoid saying:
- "The model proves a post is fake."
- "The risk score is the probability that the news is false."
- "The demo dataset is accurate enough for real-world moderation."

## Architecture

```text
User
  ↓
HTML/CSS/JavaScript
  ↓
Flask API
  ├── Text → preprocessing
  ├── Image → Tesseract OCR → text
  └── Video → Whisper tiny → transcript
                ↓
          TF-IDF Vectorizer
                ↓
        Logistic Regression
                ↓
       Fake/Real + confidence
                ↓
       Prototype risk score
                ↓
          Short summary
                ↓
             UI
                ↓
       Optional Firestore history
```

## Troubleshooting

### `ModuleNotFoundError`
Activate the virtual environment and run:

```bash
pip install -r requirements.txt
```

### Tesseract not found
Run:

```bash
sudo apt install tesseract-ocr
tesseract --version
```

### ffmpeg not found
Run:

```bash
sudo apt install ffmpeg
ffmpeg -version
```

### Whisper is slow
Use:

```text
WHISPER_MODEL=tiny
```

and keep videos short.

### Port 5000 is busy

Stop the old Flask process, or temporarily change the port in `run.py` and use the matching URL.

## Disclaimer

This is an educational Thinkathon prototype. It is not a production misinformation-detection system. Real deployment would require a large, diverse, carefully labeled dataset; evaluation across languages and domains; calibration; bias/error analysis; adversarial testing; source verification; and human review.
