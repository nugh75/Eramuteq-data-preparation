#!/bin/bash
# Script per avviare Streamlit con configurazioni che bypassano i problemi di ctypes

echo "Attivazione ambiente virtuale..."
source venv/bin/activate

echo "Installazione dipendenze..."
pip install pandas openpyxl

echo "Configurazione Streamlit per bypassare il problema ctypes..."
echo "Avvio con file watcher disabilitato..."

# Avvia Streamlit con il file watcher disabilitato
STREAMLIT_SERVER_FILE_WATCHER_TYPE=none streamlit run iramuteq.py --server.port=8507 --server.address=0.0.0.0
