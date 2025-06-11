#!/bin/bash
# Script per avviare l'applicazione Streamlit con Python di sistema

echo "🚀 Avvio IRaMuTeQ Corpus Generator"
echo "Attivazione ambiente virtuale con Python di sistema..."
source venv_system/bin/activate

echo "Verifica dipendenze..."
python -c "import pandas as pd; import streamlit as st; print('✅ Tutte le dipendenze sono disponibili')"

echo "Avvio applicazione Streamlit..."
echo "📱 L'applicazione sarà disponibile su http://localhost:8507"
echo "⏹️  Premi Ctrl+C per fermare l'applicazione"
echo ""

# Avvia Streamlit sulla porta 8507
streamlit run iramuteq.py --server.port=8507 --server.address=0.0.0.0
