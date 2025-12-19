#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python demo_setup.py
uvicorn webapp:app --port 8000 &
streamlit run streamlit_app.py
