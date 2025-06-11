#!/usr/bin/env python3
"""
Test script per verificare la funzionalità di iramuteq.py
"""
import pandas as pd
import io
from functools import reduce

def test_iramuteq_logic():
    """Test della logica principale di iramuteq.py"""
    print("=== TEST IRAMUTEQ LOGIC ===")
    
    # Simula dati di input
    data1 = {
        'ID': ['1', '2', '3'],
        'Nome': ['Mario', 'Luigi', None],  # Test con None
        'Categoria': ['A', 'B', 'A'],
        'Testo': ['Primo testo', 'Secondo testo', 'Terzo testo']
    }
    
    data2 = {
        'ID': ['1', '2', '4'],
        'Cognome': ['Rossi', None, 'Bianchi'],  # Test con None
        'Settore': ['IT', 'Marketing', 'HR'],
        'Commento': ['Commento uno', 'Commento due', 'Commento tre']
    }
    
    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)
    
    print("Dataset 1:")
    print(df1)
    print("\nDataset 2:")
    print(df2)
    
    # Test merge
    print("\n=== TEST MERGE ===")
    key_cols = ['ID']
    merged_df = pd.merge(df1, df2, on=key_cols, how="inner")
    print("Merged DataFrame:")
    print(merged_df)
    
    # Test generazione corpus
    print("\n=== TEST CORPUS GENERATION ===")
    descriptive_cols = ['Nome', 'Cognome']
    metadata_cols = ['Categoria', 'Settore']
    text_col = 'Testo'
    
    lines = []
    for _, row in merged_df.iterrows():
        # Gestisci valori None/NaN come nel codice corretto
        meta_desc = " ".join(f"*{col}_{str(row[col]) if pd.notna(row[col]) else 'NA'}" for col in descriptive_cols)
        meta_data = " ".join(f"*{col}_{str(row[col]) if pd.notna(row[col]) else 'NA'}" for col in metadata_cols) if metadata_cols else ""
        text = str(row[text_col]).replace("\n", " ").strip() if pd.notna(row[text_col]) else ""
        
        # Salta righe senza testo significativo (come nel codice aggiornato)
        if not text or text.lower() in ['nan', 'none', '']:
            continue
        
        # Costruisci la riga del corpus
        if meta_data:
            lines.append(f"**** {meta_desc} {meta_data}\n{text}")
        else:
            lines.append(f"**** {meta_desc}\n{text}")
    
    corpus_text = "\n\n".join(lines)
    
    print(f"Corpus generato con {len(lines)} documenti validi su {len(merged_df)} righe totali.")
    print("Corpus generato:")
    print(corpus_text)
    
    # Test con concatenazione semplice
    print("\n=== TEST CONCATENAZIONE ===")
    data3 = {
        'Prodotto': ['A', 'B'],
        'Prezzo': ['10', '20'],
        'Descrizione': ['Prodotto economico', 'Prodotto premium']
    }
    df3 = pd.DataFrame(data3)
    
    # Simula concatenazione
    concat_df = pd.concat([df1, df3], ignore_index=True, sort=False)
    print("DataFrame concatenato:")
    print(concat_df)
    
    print("\n=== TEST COMPLETATO ===")

if __name__ == "__main__":
    test_iramuteq_logic()
