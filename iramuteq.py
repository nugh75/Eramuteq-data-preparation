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

    # Selezione delle colonne per IRaMuTeQ
    st.subheader("Seleziona colonne descrittive")
    descriptive_cols = st.multiselect("Colonne descrittive", options=merged_df.columns.tolist())

    st.subheader("Seleziona colonne metadata (opzionale)")
    metadata_cols = st.multiselect(
        "Colonne metadata", 
        options=[c for c in merged_df.columns.tolist() if c not in descriptive_cols]
    )

    st.subheader("Seleziona colonna di testo")
    available_text_cols = [c for c in merged_df.columns.tolist() if c not in descriptive_cols + metadata_cols]
    if available_text_cols:
        text_col = st.selectbox(
            "Colonna testo", 
            options=available_text_cols
        )
    else:
        st.error("Nessuna colonna disponibile per il testo dopo aver selezionato le colonne descrittive e metadata.")
        text_col = None

    if st.button("Genera corpus IRaMuTeQ"):
        if not descriptive_cols:
            st.error("Devi selezionare almeno una colonna descrittiva.")
        elif not text_col:
            st.error("Devi selezionare una colonna di testo.")
        else:
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