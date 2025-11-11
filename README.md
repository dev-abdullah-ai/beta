# Haukia AC Cooling Calculator — Streamlit (v2)

## Features
- Three pages: **Welcome**, **Calculator**, **Support**.
- **Light/Dark toggle** at top (CSS-based).
- Dimension fields are **empty by default**. Validation on calculate.
- Appliances **Add** clears the input without reruns.

## Run
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy
Push to GitHub and deploy on Streamlit Community Cloud with main file `streamlit_app.py`.
