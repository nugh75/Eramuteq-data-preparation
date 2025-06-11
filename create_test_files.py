#!/usr/bin/env python3
import pandas as pd
import os
import sys

print("Starting test file creation...")

# Creo dati di test
data1 = {
    'ID': ['1', '2', '3'],
    'Nome': ['Mario', 'Luigi', 'Peach'],
    'Categoria': ['A', 'B', 'A'],
    'Testo': ['Questo è il primo testo di esempio', 'Secondo testo molto interessante', 'Terzo testo con contenuto']
}

data2 = {
    'ID': ['1', '2', '4'],
    'Cognome': ['Rossi', 'Verdi', 'Bianchi'],
    'Settore': ['IT', 'Marketing', 'HR'],
    'Commento': ['Commento numero uno', 'Commento numero due', 'Commento numero tre']
}

data3 = {
    'Prodotto': ['A', 'B', 'C'],
    'Prezzo': ['10', '20', '30'],
    'Descrizione': ['Prodotto economico ma buono', 'Prodotto di qualità media', 'Prodotto premium eccellente']
}

# Creo i DataFrame
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)
df3 = pd.DataFrame(data3)

# Salvo come Excel
df1.to_excel('test_file1.xlsx', index=False)
df2.to_excel('test_file2.xlsx', index=False)
df3.to_excel('test_file3.xlsx', index=False)

print("File di test creati:")
print("- test_file1.xlsx (con colonna ID comune)")
print("- test_file2.xlsx (con colonna ID comune)")
print("- test_file3.xlsx (senza colonne comuni)")
