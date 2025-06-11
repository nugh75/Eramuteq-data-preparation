#!/usr/bin/env python3
"""
Versione standalone dell'applicazione IRaMuTeQ per debugging
Converte file Excel in formato corpus IRaMuTeQ senza interfaccia web
"""

import pandas as pd
import sys
import os
from functools import reduce

def process_excel_files(file_paths, key_cols=None, descriptive_cols=None, metadata_cols=None, text_col=None):
    """
    Processa i file Excel e genera il corpus IRaMuTeQ
    """
    print(f"Caricamento di {len(file_paths)} file...")
    
    # Leggi tutti i DataFrame
    dfs = []
    for file_path in file_paths:
        try:
            df = pd.read_excel(file_path, dtype=str)
            dfs.append(df)
            print(f"✓ Caricato: {file_path} ({df.shape[0]} righe, {df.shape[1]} colonne)")
        except Exception as e:
            print(f"✗ Errore nel caricamento di {file_path}: {e}")
            return None
    
    if not dfs:
        print("Nessun file caricato correttamente")
        return None
    
    # Trova colonne comuni se non specificate
    if not key_cols:
        common_cols = list(set(dfs[0].columns).intersection(*[set(df.columns) for df in dfs[1:]]))
        print(f"Colonne comuni trovate: {common_cols}")
        if common_cols:
            key_cols = common_cols[:1]  # Usa la prima colonna comune
            print(f"Usando per il merge: {key_cols}")
    
    # Unisci o concatena
    if key_cols and len(dfs) > 1:
        print(f"Merge sui campi: {key_cols}")
        merged_df = reduce(lambda left, right: pd.merge(left, right, on=key_cols, how="inner"), dfs)
        print(f"Dataset unito: {merged_df.shape[0]} righe, {merged_df.shape[1]} colonne")
    else:
        print("Concatenazione semplice...")
        merged_df = pd.concat(dfs, ignore_index=True, sort=False)
        print(f"Dataset concatenato: {merged_df.shape[0]} righe, {merged_df.shape[1]} colonne")
    
    print(f"Colonne disponibili: {list(merged_df.columns)}")
    
    # Usa colonne di default se non specificate
    if not descriptive_cols:
        descriptive_cols = [col for col in merged_df.columns if any(keyword in col.lower() for keyword in ['nome', 'id', 'codice'])][:2]
    
    if not text_col:
        text_col = [col for col in merged_df.columns if any(keyword in col.lower() for keyword in ['testo', 'commento', 'descrizione', 'content'])]
        text_col = text_col[0] if text_col else merged_df.columns[-1]
    
    if not metadata_cols:
        metadata_cols = [col for col in merged_df.columns if col not in descriptive_cols and col != text_col][:3]
    
    print(f"Colonne descrittive: {descriptive_cols}")
    print(f"Colonne metadata: {metadata_cols}")
    print(f"Colonna testo: {text_col}")
    
    # Genera corpus
    lines = []
    for _, row in merged_df.iterrows():
        # Gestisci valori None/NaN
        meta_desc = " ".join(f"*{col}_{str(row[col]) if pd.notna(row[col]) else 'NA'}" for col in descriptive_cols)
        meta_data = " ".join(f"*{col}_{str(row[col]) if pd.notna(row[col]) else 'NA'}" for col in metadata_cols) if metadata_cols else ""
        text = str(row[text_col]).replace("\n", " ").strip() if pd.notna(row[text_col]) else ""
        
        # Salta righe senza testo significativo
        if not text or text.lower() in ['nan', 'none', '']:
            continue
        
        # Costruisci la riga del corpus
        if meta_data:
            lines.append(f"**** {meta_desc} {meta_data}\n{text}")
        else:
            lines.append(f"**** {meta_desc}\n{text}")
    
    corpus_text = "\n\n".join(lines)
    
    print(f"\n✓ Corpus generato con {len(lines)} documenti validi su {len(merged_df)} righe totali.")
    
    return corpus_text

def main():
    """Funzione principale"""
    print("=== IRaMuTeQ Corpus Generator (Standalone) ===\n")
    
    # Test con i file di esempio
    test_files = ['test_file1.csv', 'test_file2.csv']
    existing_files = [f for f in test_files if os.path.exists(f)]
    
    if existing_files:
        print(f"File di test trovati: {existing_files}")
        
        # Converti CSV in Excel per il test se necessario
        excel_files = []
        for csv_file in existing_files:
            excel_file = csv_file.replace('.csv', '.xlsx')
            if not os.path.exists(excel_file):
                print(f"Conversione {csv_file} -> {excel_file}")
                df = pd.read_csv(csv_file)
                df.to_excel(excel_file, index=False)
            excel_files.append(excel_file)
        
        corpus = process_excel_files(excel_files)
        
        if corpus:
            # Salva il corpus
            with open('corpus_output.txt', 'w', encoding='utf-8') as f:
                f.write(corpus)
            
            print(f"\n✓ Corpus salvato in: corpus_output.txt")
            print("\n=== ANTEPRIMA CORPUS ===")
            print(corpus[:500] + "..." if len(corpus) > 500 else corpus)
        else:
            print("✗ Errore nella generazione del corpus")
    else:
        print("⚠️ File di test non trovati. Creando file di esempio...")
        
        # Crea file di esempio
        data1 = {
            'ID': ['1', '2', '3'],
            'Nome': ['Mario Rossi', 'Luigi Verdi', 'Paolo Bianchi'],
            'Categoria': ['A', 'B', 'A'],
            'Testo': ['Questo è il primo documento di test', 'Il secondo documento contiene altre informazioni', 'Terzo documento con contenuto diverso']
        }
        
        data2 = {
            'ID': ['1', '2', '4'],
            'Cognome': ['Rossi', 'Verdi', 'Neri'],
            'Settore': ['IT', 'Marketing', 'HR'],
            'Commento': ['Ottimo lavoro', 'Buona presentazione', 'Da migliorare']
        }
        
        df1 = pd.DataFrame(data1)
        df2 = pd.DataFrame(data2)
        
        df1.to_excel('esempio1.xlsx', index=False)
        df2.to_excel('esempio2.xlsx', index=False)
        
        print("✓ File di esempio creati: esempio1.xlsx, esempio2.xlsx")
        
        corpus = process_excel_files(['esempio1.xlsx', 'esempio2.xlsx'])
        
        if corpus:
            with open('corpus_esempio.txt', 'w', encoding='utf-8') as f:
                f.write(corpus)
            
            print(f"\n✓ Corpus di esempio salvato in: corpus_esempio.txt")
            print("\n=== CORPUS GENERATO ===")
            print(corpus)

if __name__ == "__main__":
    main()
