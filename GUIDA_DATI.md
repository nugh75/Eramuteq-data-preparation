# 📊 Come Preparare i Dati per IRaMuTeQ

## 🗂️ **Struttura Dati Consigliata**

### **Esempio File Excel 1: `interviste.xlsx`**
| ID | Nome | Età | Genere | Categoria | Domanda1 | Domanda2 | Domanda3 |
|----|------|-----|--------|-----------|----------|----------|----------|
| 001 | Mario | 35 | M | Manager | Penso che il lavoro sia importante | La formazione è fondamentale | Il team è molto collaborativo |
| 002 | Anna | 28 | F | Impiegata | Il lavoro mi piace molto | Vorrei più corsi di aggiornamento | I colleghi sono disponibili |
| 003 | Luca | 42 | M | Manager | Il lavoro è stressante | La formazione è necessaria | Il team funziona bene |

### **Esempio File Excel 2: `questionari.xlsx`**
| ID | Settore | Esperienza | Commento_libero | Note_aggiuntive |
|----|---------|------------|-----------------|-----------------|
| 001 | IT | 10 anni | L'azienda ha buone prospettive future | Molto motivato |
| 002 | HR | 5 anni | Ambiente di lavoro sereno e stimolante | Cerca crescita professionale |
| 003 | IT | 15 anni | Necessari più investimenti in tecnologia | Leader naturale |

## ⚙️ **Come Configurare l'Applicazione**

### **1. Caricamento File**
- Carica uno o più file Excel
- L'app rileverà automaticamente le colonne comuni

### **2. Merge dei Dati** 
- **Colonne chiave**: Seleziona `ID` per unire i file
- Risultato: un dataset unificato con tutte le informazioni

### **3. Selezione Colonne**

#### **🏷️ Colonne Descrittive** (obbligatorie)
Identificano univocamente ogni testo nel corpus:
- `Nome`, `ID`, `Codice_partecipante`
- Esempio output: `*Nome_Mario *ID_001`

#### **📋 Colonne Metadata** (opzionali)
Caratteristiche dei partecipanti per l'analisi:
- `Età`, `Genere`, `Settore`, `Esperienza`, `Categoria`
- Esempio output: `*Età_35 *Genere_M *Settore_IT`

#### **📝 Colonne di Testo** (obbligatorie)
Il contenuto da analizzare con IRaMuTeQ:
- `Domanda1`, `Domanda2`, `Domanda3`, `Commento_libero`, `Note_aggiuntive`
- **NOVITÀ**: Puoi selezionare **più colonne** che verranno unite automaticamente

## 📄 **Formato Output Corpus IRaMuTeQ**

```
**** *Nome_Mario *ID_001 *Età_35 *Genere_M *Settore_IT
Penso che il lavoro sia importante La formazione è fondamentale Il team è molto collaborativo L'azienda ha buone prospettive future Molto motivato

**** *Nome_Anna *ID_002 *Età_28 *Genere_F *Settore_HR
Il lavoro mi piace molto Vorrei più corsi di aggiornamento I colleghi sono disponibili Ambiente di lavoro sereno e stimolante Cerca crescita professionale

**** *Nome_Luca *ID_003 *Età_42 *Genere_M *Settore_IT
Il lavoro è stressante La formazione è necessaria Il team funziona bene Necessari più investimenti in tecnologia Leader naturale
```

## 💡 **Consigli Pratici**

### **✅ Dati Ben Strutturati:**
- Una riga = un partecipante/documento
- Colonne chiare e consistenti
- ID univoci per il merge
- Testo pulito (evita caratteri speciali)

### **🔧 Colonne di Testo Multiple:**
- **Esempio**: Seleziona `Domanda1`, `Domanda2`, `Commento_libero`
- **Risultato**: Tutti i testi verranno uniti con spazi
- **Vantaggio**: Analisi completa di tutte le risposte insieme

### **📊 Vantaggi del Merge:**
- Combina dati demografici + risposte testuali
- Analisi IRaMuTeQ più ricca con metadata
- Possibilità di filtrare per caratteristiche dei partecipanti

### **⚠️ Cosa Evitare:**
- Righe completamente vuote
- Testi troppo corti (meno di 3 parole)
- Caratteri speciali nei nomi delle colonne
- ID duplicati tra file diversi
