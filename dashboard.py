import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import show_header

show_header()

# Custom CSS for professional financial styling
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
    .kpi-container {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #cbd5e1;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .section-header {
        font-size: 1.75rem;
        font-weight: 500;
        color: #1e40af;
        padding: 1rem 0;
        margin: 1.5rem 0 1rem 0;
    }
    .metric-positive { color: #16a34a; font-weight: 600; }
    .metric-negative { color: #dc2626; font-weight: 600; }
    
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
st.sidebar.header("🔍 Filtres")

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

# KPIs
st.markdown('<h1 class="main-header">📊 Dashboard Financier - BOUYGUES SA</h1>', unsafe_allow_html=True)

st.markdown('<h2 class="section-header">💹 Indicateurs Clés de Performance</h2>', unsafe_allow_html=True)

current_close = df_filtered['Close'].iloc[-1]
prev_close = df_filtered['Close'].iloc[-2] if len(df_filtered) > 1 else current_close
change = ((current_close - prev_close) / prev_close) * 100

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Prix de Clôture",
        value=f"{current_close:.2f}€",
        delta=f"{change:+.2f}%",
        delta_color="normal"
    )
with col2:
    st.metric(
        label="Prix Max Période",
        value=f"{df_filtered['High'].max():.2f}€",
        delta=None
    )
with col3:
    st.metric(
        label="Prix Min Période",
        value=f"{df_filtered['Low'].min():.2f}€",
        delta=None
    )
with col4:
    st.metric(
        label="Volume Total",
        value=f"{df_filtered['Number of Shares'].sum():,.0f}",
        delta=None
    )

st.markdown('<br>', unsafe_allow_html=True)


# Graphique des prix
st.markdown('<h2 class="section-header">📈 Évolution des Prix</h2>', unsafe_allow_html=True)

fig_prices = make_subplots(rows=2, cols=1, 
                          shared_xaxes=True,
                          vertical_spacing=0.05,
                          row_heights=[0.7, 0.3],
                          subplot_titles=('<b>Prix de Clôture & Indicateurs</b>', '<b>Volume de Transactions</b>'))

# Graphique chandelier
fig_prices.add_trace(
    go.Candlestick(
        x=df_filtered['Date'],
        open=df_filtered['Open'],
        high=df_filtered['High'],
        low=df_filtered['Low'],
        close=df_filtered['Close'],
        name='BOUYGUES',
        increasing_line_color='#16a34a',
        decreasing_line_color='#dc2626'
    ),
    row=1, col=1
)

# Moyennes mobiles
df_filtered['MA20'] = df_filtered['Close'].rolling(window=20).mean()
df_filtered['MA50'] = df_filtered['Close'].rolling(window=50).mean()

fig_prices.add_trace(
    go.Scatter(
        x=df_filtered['Date'],
        y=df_filtered['MA20'],
        name='MA 20',
        line=dict(color='#f59e0b', width=2)
    ),
    row=1, col=1
)

fig_prices.add_trace(
    go.Scatter(
        x=df_filtered['Date'],
        y=df_filtered['MA50'],
        name='MA 50',
        line=dict(color='#3b82f6', width=2)
    ),
    row=1, col=1
)

# Volume
colors = ['#dc2626' if row['Close'] < row['Open'] else '#16a34a' for _, row in df_filtered.iterrows()]
fig_prices.add_trace(
    go.Bar(
        x=df_filtered['Date'],
        y=df_filtered['Number of Shares'],
        name='Volume',
        marker_color=colors,
        marker_line_color='#ffffff',
        marker_line_width=0.5
    ),
    row=2, col=1
)

fig_prices.update_layout(
    title='<b>Analyse Technique BOUYGUES</b>',
    xaxis_rangeslider_visible=False,
    height=800,
    showlegend=True,
    hovermode='x unified',
    plot_bgcolor='#f8fafc',
    paper_bgcolor='#ffffff',
    font=dict(family='Arial', size=11, color='#1e3a8a'),
    margin=dict(l=60, r=40, t=80, b=40)
)

fig_prices.update_xaxes(gridcolor='#e5e7eb', gridwidth=1, title_font=dict(color='#1e3a8a'), tickfont=dict(color='#1e3a8a'))
fig_prices.update_yaxes(gridcolor='#e5e7eb', gridwidth=1, title_font=dict(color='#1e3a8a'), tickfont=dict(color='#1e3a8a'))

st.plotly_chart(fig_prices, use_container_width=True)

st.markdown('<br>', unsafe_allow_html=True)


# Graphique VWAP
st.markdown('<h2 class="section-header">📊 Analyse VWAP (Volume Weighted Average Price)</h2>', unsafe_allow_html=True)

fig_vwap = go.Figure()

fig_vwap.add_trace(
    go.Scatter(
        x=df_filtered['Date'],
        y=df_filtered['Close'],
        name='Prix de Clôture',
        line=dict(color='#1e3a8a', width=2)
    )
)

fig_vwap.add_trace(
    go.Scatter(
        x=df_filtered['Date'],
        y=df_filtered['vwap'],
        name='VWAP',
        line=dict(color='#9333ea', width=2.5, dash='dash')
    )
)

fig_vwap.update_layout(
    title='<b>Prix de Clôture vs VWAP</b>',
    xaxis_title='Date',
    yaxis_title='Prix (€)',
    hovermode='x unified',
    height=500,
    plot_bgcolor='#f8fafc',
    paper_bgcolor='#ffffff',
    font=dict(family='Arial', size=11, color='#1e3a8a'),
    margin=dict(l=60, r=40, t=80, b=60),
    xaxis=dict(gridcolor='#e5e7eb', gridwidth=1, title_font=dict(color='#1e3a8a'), tickfont=dict(color='#1e3a8a')),
    yaxis=dict(gridcolor='#e5e7eb', gridwidth=1, title_font=dict(color='#1e3a8a'), tickfont=dict(color='#1e3a8a'))
)

st.plotly_chart(fig_vwap, use_container_width=True)

st.markdown('<br>', unsafe_allow_html=True)

# Tableau de données
st.markdown('<h2 class="section-header">📋 Données Brutes</h2>', unsafe_allow_html=True)
st.dataframe(
    df_filtered.sort_values('Date', ascending=False),
    use_container_width=True,
    height=400,
    column_config={
        "Date": st.column_config.DatetimeColumn("Date", format="DD/MM/YYYY"),
        "Open": st.column_config.NumberColumn("Ouverture", format="%.2f €"),
        "High": st.column_config.NumberColumn("Plus Haut", format="%.2f €"),
        "Low": st.column_config.NumberColumn("Plus Bas", format="%.2f €"),
        "Close": st.column_config.NumberColumn("Clôture", format="%.2f €"),
        "Number of Shares": st.column_config.NumberColumn("Volume", format=",.0f"),
        "vwap": st.column_config.NumberColumn("VWAP", format="%.2f €"),
    }
)

# Footer
st.markdown('<br>', unsafe_allow_html=True)
st.markdown('<hr>', unsafe_allow_html=True)
st.caption("💡 Dashboard financier Streamlit - Analyse des données BOUYGUES SA | Données en temps réel")
