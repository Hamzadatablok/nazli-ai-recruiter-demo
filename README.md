# Interview the AI That Represents Me

A small recruiter-facing prototype built for the Nazli Tech School Talent Network video challenge.

## Run locally (Windows)
1. Install Python 3.11+ if needed.
2. Open PowerShell in this folder.
3. Create and activate an environment:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   streamlit run app.py
   ```
4. Open the local URL printed by Streamlit.

## What it demonstrates
- CV-grounded retrieval with visible source labels
- English/French/Arabic response modes
- A built-in unsupported-claim test (the Google five-year trap)
- A small evaluation snapshot

## Important scope note
This is an honest prototype, not a production LLM or a verified deployment. The curated facts must be checked against the latest CV before publishing. Add a real hosted demo only after testing and reviewing public exposure of personal contact details.
