import streamlit as st
import pandas as pd
from functools import reduce

st.title("Preparazione Corpus per IRaMuTeQ da Multipli Excel")

st.markdown("""
Carica uno o più file Excel, scegli le colonne chiave comuni su cui fare il merge (o filtri),
poi seleziona le colonne descrittive, metadata e testo per generare il corpus per IRaMuTeQ.
""")

# Upload di più file Excel
uploaded_files = st.file_uploader(
    "Carica uno o più file Excel", type=["xlsx", "xls"], accept_multiple_files=True
)

if uploaded_files:
    # Leggi tutti i DataFrame
    dfs = [pd.read_excel(f, dtype=str) for f in uploaded_files]
    st.success(f"{len(dfs)} file caricati correttamente")

    # Trova colonne comuni
    common_cols = list(set(dfs[0].columns).intersection(*[set(df.columns) for df in dfs[1:]]))
    if common_cols:
        st.subheader("Colonne comuni (per merge)")
        key_cols = st.multiselect(
            "Seleziona colonne chiave per unire i file (merge inner)",
            options=common_cols
        )
    else:
        st.warning("Nessuna colonna comune tra i file caricati")
        key_cols = []

    # Unisci o concatena
    if key_cols:
        merged_df = reduce(lambda left, right: pd.merge(left, right, on=key_cols, how="inner"), dfs)
        st.info(f"Dataset unito: {merged_df.shape[0]} righe, {merged_df.shape[1]} colonne")
    else:
        # semplice concatenazione
        merged_df = pd.concat(dfs, ignore_index=True, sort=False)
        st.info(f"Dataset concatenato: {merged_df.shape[0]} righe, {merged_df.shape[1]} colonne")

    # Mostra anteprima del dataset
    st.subheader("Anteprima Dataset")
    st.dataframe(merged_df.head(), use_container_width=True)
    
    st.subheader("📊 Informazioni Colonne")
    col_info = []
    for col in merged_df.columns:
        non_null = merged_df[col].notna().sum()
        total = len(merged_df)
        col_info.append({
            "Colonna": col,
            "Valori non nulli": f"{non_null}/{total} ({non_null/total*100:.1f}%)",
            "Esempio": str(merged_df[col].dropna().iloc[0])[:50] + "..." if non_null > 0 else "N/A"
        })
    st.dataframe(pd.DataFrame(col_info), use_container_width=True)

    # Selezione delle colonne per IRaMuTeQ
    st.subheader("Seleziona colonne descrittive")
    st.write("Spunta le colonne che identificano univocamente ogni documento:")
    descriptive_cols = []
    
    # Crea checkbox per colonne descrittive
    desc_cols = st.columns(min(3, len(merged_df.columns)))
    for i, col in enumerate(merged_df.columns.tolist()):
        col_index = i % 3
        with desc_cols[col_index]:
            if st.checkbox(col, key=f"desc_{col}"):
                descriptive_cols.append(col)

    st.subheader("Seleziona colonne metadata (opzionale)")
    available_metadata_cols = [c for c in merged_df.columns.tolist() if c not in descriptive_cols]
    if available_metadata_cols:
        st.write("Spunta le colonne con caratteristiche dei partecipanti (età, genere, categoria, ecc.):")
        metadata_cols = []
        
        # Crea checkbox per colonne metadata
        meta_cols = st.columns(min(3, len(available_metadata_cols)))
        for i, col in enumerate(available_metadata_cols):
            col_index = i % 3
            with meta_cols[col_index]:
                if st.checkbox(col, key=f"meta_{col}"):
                    metadata_cols.append(col)
    else:
        metadata_cols = []

    st.subheader("Seleziona colonne di testo")
    available_text_cols = [c for c in merged_df.columns.tolist() if c not in descriptive_cols + metadata_cols]
    if available_text_cols:
        st.write("Spunta le colonne contenenti il testo da analizzare (verranno unite con spazio):")
        text_cols = []
        
        # Crea checkbox per ogni colonna di testo disponibile
        cols = st.columns(min(3, len(available_text_cols)))  # Massimo 3 colonne
        for i, text_col in enumerate(available_text_cols):
            col_index = i % 3
            with cols[col_index]:
                if st.checkbox(text_col, key=f"text_{text_col}"):
                    text_cols.append(text_col)
    else:
        st.error("Nessuna colonna disponibile per il testo dopo aver selezionato le colonne descrittive e metadata.")
        text_cols = []

    if st.button("Genera corpus IRaMuTeQ"):
        if not descriptive_cols:
            st.error("Devi selezionare almeno una colonna descrittiva.")
        elif not text_cols:
            st.error("Devi selezionare almeno una colonna di testo.")
        else:
            lines = []
            for _, row in merged_df.iterrows():
                # Gestisci valori None/NaN
                meta_desc = " ".join(f"*{col}_{str(row[col]) if pd.notna(row[col]) else 'NA'}" for col in descriptive_cols)
                meta_data = " ".join(f"*{col}_{str(row[col]) if pd.notna(row[col]) else 'NA'}" for col in metadata_cols) if metadata_cols else ""
                
                # Unisci tutte le colonne di testo selezionate
                text_parts = []
                for text_col in text_cols:
                    if pd.notna(row[text_col]):
                        part = str(row[text_col]).replace("\n", " ").strip()
                        if part and part.lower() not in ['nan', 'none', '']:
                            text_parts.append(part)
                
                text = " ".join(text_parts)
                
                # Salta righe senza testo significativo
                if not text:
                    continue
                
                # Costruisci la riga del corpus
                if meta_data:
                    lines.append(f"**** {meta_desc} {meta_data}\n{text}")
                else:
                    lines.append(f"**** {meta_desc}\n{text}")

            corpus_text = "\n\n".join(lines)
            
            st.success(f"Corpus generato con {len(lines)} documenti validi su {len(merged_df)} righe totali.")

            # Anteprima
            st.subheader("Anteprima Corpus")
            st.text_area("Prime righe del corpus", value="\n".join(lines[:5]), height=200)

            # Download
            st.download_button(
                label="Scarica corpus.txt",
                data=corpus_text,
                file_name="corpus.txt",
                mime="text/plain"
            )