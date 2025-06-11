#!/usr/bin/env python3
"""
Test semplificato senza dipendenze esterne
"""

def test_basic_logic():
    """Test della logica base senza pandas"""
    print("=== TEST LOGICA BASE ===")
    
    # Simula dati come dizionari semplici
    data1 = [
        {'ID': '1', 'Nome': 'Mario', 'Categoria': 'A', 'Testo': 'Primo testo'},
        {'ID': '2', 'Nome': 'Luigi', 'Categoria': 'B', 'Testo': 'Secondo testo'},
        {'ID': '3', 'Nome': None, 'Categoria': 'A', 'Testo': 'Terzo testo'}
    ]
    
    data2 = [
        {'ID': '1', 'Cognome': 'Rossi', 'Settore': 'IT'},
        {'ID': '2', 'Cognome': None, 'Settore': 'Marketing'},
        {'ID': '4', 'Cognome': 'Bianchi', 'Settore': 'HR'}
    ]
    
    print("Dataset 1:", data1)
    print("Dataset 2:", data2)
    
    # Simula merge inner join
    merged_data = []
    for row1 in data1:
        for row2 in data2:
            if row1['ID'] == row2['ID']:
                merged_row = {**row1, **row2}
                merged_data.append(merged_row)
    
    print("\nMerged data:", merged_data)
    
    # Test generazione corpus
    print("\n=== TEST CORPUS GENERATION ===")
    descriptive_cols = ['Nome', 'Cognome']
    metadata_cols = ['Categoria', 'Settore']
    text_col = 'Testo'
    
    lines = []
    for row in merged_data:
        # Gestisci valori None come nel codice originale
        meta_desc = " ".join(f"*{col}_{str(row[col]) if row[col] is not None else 'NA'}" for col in descriptive_cols)
        meta_data = " ".join(f"*{col}_{str(row[col]) if row[col] is not None else 'NA'}" for col in metadata_cols)
        text = str(row[text_col]).replace("\n", " ").strip() if row[text_col] is not None else ""
        
        # Costruisci la riga del corpus
        if meta_data:
            lines.append(f"**** {meta_desc} {meta_data}\n{text}")
        else:
            lines.append(f"**** {meta_desc}\n{text}")
    
    corpus_text = "\n\n".join(lines)
    
    print("Corpus generato:")
    print(corpus_text)
    print("\n=== TEST COMPLETATO CON SUCCESSO ===")

if __name__ == "__main__":
    test_basic_logic()
