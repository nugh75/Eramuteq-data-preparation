#!/bin/bash
# Script per avviare l'applicazione Streamlit

echo "Attivazione ambiente virtuale..."
source venv/bin/activate

echo "Verifica installazione dipendenze..."
pip install -r requirements.txt

echo "Avvio applicazione Streamlit..."
echo "L'applicazione sarà disponibile su http://localhost:8507"
streamlit run iramuteq.py --server.port=8507
