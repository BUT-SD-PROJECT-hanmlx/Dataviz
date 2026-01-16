import streamlit as st
import pandas as pd
from common import show_header

show_header()

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv('BOUYGUES_historical_price.csv', sep=';')
    
    # Conversion des colonnes numériques (remplacer les virgules par des points)
    numeric_cols = ['Open', 'High', 'Low', 'Last', 'Close', 'Number of Shares', 'Number of Trades', 'Turnover', 'vwap']
    for col in numeric_cols:
        df[col] = df[col].astype(str).str.replace(',', '.').astype(float)
    
    # Conversion de la date
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    
    return df

df = load_data()

# Sidebar pour les filtres
st.sidebar.header("⚙️ Filtres")

# Sélection de la période
min_date = df['Date'].min().to_pydatetime()
max_date = df['Date'].max().to_pydatetime()

date_range = st.sidebar.date_input(
    "Période",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    df_filtered = df[(df['Date'].dt.date >= date_range[0]) & (df['Date'].dt.date <= date_range[1])]
else:
    df_filtered = df

# Statistiques détaillées
st.header("Statistiques Detaillees")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Statistiques de Prix")
    price_stats = pd.DataFrame({
        'Moyenne': df_filtered[['Open', 'High', 'Low', 'Close']].mean(),
        'Min': df_filtered[['Open', 'High', 'Low', 'Close']].min(),
        'Max': df_filtered[['Open', 'High', 'Low', 'Close']].max(),
        'Écart-type': df_filtered[['Open', 'High', 'Low', 'Close']].std()
    })
    st.dataframe(price_stats.style.format("{:.2f}€"), use_container_width=True)

with col2:
    st.subheader("Statistiques de Volume")
    volume_stats = pd.DataFrame({
        'Moyenne': df_filtered[['Number of Shares', 'Number of Trades', 'Turnover']].mean(),
        'Min': df_filtered[['Number of Shares', 'Number of Trades', 'Turnover']].min(),
        'Max': df_filtered[['Number of Shares', 'Number of Trades', 'Turnover']].max()
    })
    st.dataframe(volume_stats.style.format("{:,.0f}"), use_container_width=True)
