# Haukia AC Cooling Calculator — Streamlit

Arabic-friendly cooling calculator. Enter room dimensions, heat level, people, and appliance watts; it computes recommended **BTU** and **tons of cooling**.

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy to Streamlit Community Cloud
1. Push to GitHub (public repo).
2. Go to https://share.streamlit.io → **New app**.
3. Choose your repo/branch and set main file path to `streamlit_app.py`.
4. Deploy.
