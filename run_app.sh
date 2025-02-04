#!/bin/bash

# Create a Virtual environment
python3 -m venv env
source env/Scripts/activate

# Install required libraries
pip install -r requirements.txt

# Start flask backend
cd flask_app
python app.py &

# Run streamlit frontend
cd ../streamlit_app
streamlit run app.py
