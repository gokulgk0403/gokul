# LegalEase — AI-Powered Legal Document Generator

Generates employment contracts, NDAs, lease agreements, and other legal
documents from structured inputs (document type, parties, terms, effective
date), using Google's Gemini model. Export as .txt, .docx, or .pdf.

## Structure
```
LegalEase/
├── ai_core/
│   ├── gemini_generator.py   # Calls the Gemini API to draft the document
│   └── generator.py          # sanitize_text / format_docx / format_pdf / format_html_preview
├── legalEaseAPI/
│   ├── main.py                # FastAPI app entrypoint
│   └── routes.py              # POST /generate endpoint
├── frontend/
│   └── app.py                  # Streamlit UI
├── Image/
│   └── Logo.png                # Add your logo here (used in docx/pdf/UI)
├── config.py
├── requirements.txt
├── .env.example
└── run.sh
```

## Setup
1. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_key_here
   ```
4. Add a `Logo.png` to the `Image/` folder (optional — the app degrades
   gracefully without it).

## Run
Backend (Terminal 1):
```
uvicorn legalEaseAPI.main:app --reload
```
Frontend (Terminal 2):
```
streamlit run frontend/app.py
```
Or use the convenience script (macOS/Linux): `bash run.sh`

Then open http://localhost:8501 in your browser.

## Notes
- The Gemini SDK call happens in `ai_core/gemini_generator.py`; swap in a
  different model there if you'd rather not use Gemini.
- `format_docx` / `format_pdf` embed your logo and a footer, and turn
  semicolon-separated terms into a table / bullet list automatically.
