#!/usr/bin/env python3
import pandas as pd

# Leggi CSV e converti in Excel
df1 = pd.read_csv('test_file1.csv')
df2 = pd.read_csv('test_file2.csv')

df1.to_excel('test_file1.xlsx', index=False)
df2.to_excel('test_file2.xlsx', index=False)

print("File Excel creati con successo!")
