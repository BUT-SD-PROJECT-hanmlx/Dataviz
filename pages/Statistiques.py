import streamlit as st
import pandas as pd
from common import show_header

show_header()

# Custom CSS for professional statistics styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 600;
        color: #1e3a8a;
        padding: 1rem 0;
        border-bottom: 3px solid #3b82f6;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 500;
        color: #1e40af;
        padding: 0.75rem 0;
        margin: 1.5rem 0 1rem 0;
    }
    .stat-card {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #cbd5e1;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Ensure all text is dark and readable */
    .stMetric label {
        color: #1e3a8a !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #0f172a !important;
    }
    .stMetric [data-testid="stMetricDelta"] {
        color: #0f172a !important;
    }
    
    /* Plotly chart text color fix */
    .js-plotly-plot .g-gtitle text,
    .js-plotly-plot .g-xtitle text,
    .js-plotly-plot .g-ytitle text,
    .js-plotly-plot .xtick text,
    .js-plotly-plot .ytick text,
    .js-plotly-plot .legendtext text,
    .js-plotly-plot text,
    .plotly svg text,
    .plotly-graph-div text {
        fill: #1e3a8a !important;
        color: #1e3a8a !important;
    }
</style>
""", unsafe_allow_html=True)

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
    "Période d'analyse",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    df_filtered = df[(df['Date'].dt.date >= date_range[0]) & (df['Date'].dt.date <= date_range[1])]
else:
    df_filtered = df

# Statistiques détaillées
st.markdown('<h1 class="main-header">📊 Statistiques Détaillées</h1>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<h3 class="section-header">💰 Statistiques de Prix</h3>', unsafe_allow_html=True)
    price_stats = pd.DataFrame({
        'Moyenne': df_filtered[['Open', 'High', 'Low', 'Close']].mean(),
        'Min': df_filtered[['Open', 'High', 'Low', 'Close']].min(),
        'Max': df_filtered[['Open', 'High', 'Low', 'Close']].max(),
        'Écart-type': df_filtered[['Open', 'High', 'Low', 'Close']].std()
    })
    st.dataframe(
        price_stats.style.format("{:.2f}€"),
        use_container_width=True,
        height=350
    )

with col2:
    st.markdown('<h3 class="section-header">📈 Statistiques de Volume</h3>', unsafe_allow_html=True)
    volume_stats = pd.DataFrame({
        'Moyenne': df_filtered[['Number of Shares', 'Number of Trades', 'Turnover']].mean(),
        'Min': df_filtered[['Number of Shares', 'Number of Trades', 'Turnover']].min(),
        'Max': df_filtered[['Number of Shares', 'Number of Trades', 'Turnover']].max()
    })
    st.dataframe(
        volume_stats.style.format("{:,.0f}"),
        use_container_width=True,
        height=350
    )

st.markdown('<br>', unsafe_allow_html=True)
