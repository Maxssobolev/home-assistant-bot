python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python scripts/fetch_and_clean.py
python scripts/build_terms_map.py
python scripts/apply_replacements.py