import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
st.sidebar.header("Filtres")

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

# KPIs
st.header("Indicateurs Clés")
col1, col2, col3, col4 = st.columns(4)

current_close = df_filtered['Close'].iloc[-1]
prev_close = df_filtered['Close'].iloc[-2] if len(df_filtered) > 1 else current_close
change = ((current_close - prev_close) / prev_close) * 100

col1.metric("Prix de Clôture", f"{current_close:.2f}€", f"{change:+.2f}%")
col2.metric("Prix Max Période", f"{df_filtered['High'].max():.2f}€")
col3.metric("Prix Min Période", f"{df_filtered['Low'].min():.2f}€")
col4.metric("Volume Total", f"{df_filtered['Number of Shares'].sum():,.0f}")

st.markdown("---")

# Graphique des prix
st.header("Evolution des Prix")

fig_prices = make_subplots(rows=2, cols=1, 
                          shared_xaxes=True,
                          vertical_spacing=0.05,
                          row_heights=[0.7, 0.3],
                          subplot_titles=('Prix de Clôture', 'Volume'))

# Graphique chandelier
fig_prices.add_trace(
    go.Candlestick(
        x=df_filtered['Date'],
        open=df_filtered['Open'],
        high=df_filtered['High'],
        low=df_filtered['Low'],
        close=df_filtered['Close'],
        name='BOUYGUES'
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
        line=dict(color='orange', width=1)
    ),
    row=1, col=1
)

fig_prices.add_trace(
    go.Scatter(
        x=df_filtered['Date'],
        y=df_filtered['MA50'],
        name='MA 50',
        line=dict(color='blue', width=1)
    ),
    row=1, col=1
)

# Volume
colors = ['red' if row['Close'] < row['Open'] else 'green' for _, row in df_filtered.iterrows()]
fig_prices.add_trace(
    go.Bar(
        x=df_filtered['Date'],
        y=df_filtered['Number of Shares'],
        name='Volume',
        marker_color=colors
    ),
    row=2, col=1
)

fig_prices.update_layout(
    title='Graphique OHLC et Volume',
    xaxis_rangeslider_visible=False,
    height=800,
    showlegend=True,
    hovermode='x unified'
)

st.plotly_chart(fig_prices, use_container_width=True)

st.markdown("---")

# Graphique VWAP
st.header("Analyse VWAP")

fig_vwap = go.Figure()

fig_vwap.add_trace(
    go.Scatter(
        x=df_filtered['Date'],
        y=df_filtered['Close'],
        name='Prix de Clôture',
        line=dict(color='blue', width=2)
    )
)

fig_vwap.add_trace(
    go.Scatter(
        x=df_filtered['Date'],
        y=df_filtered['vwap'],
        name='VWAP',
        line=dict(color='purple', width=2, dash='dash')
    )
)

fig_vwap.update_layout(
    title='Prix de Clôture vs VWAP',
    xaxis_title='Date',
    yaxis_title='Prix (€)',
    hovermode='x unified'
)

st.plotly_chart(fig_vwap, use_container_width=True)

st.markdown("---")

# Tableau de données
st.header("Donnees Brutes")
st.dataframe(
    df_filtered.sort_values('Date', ascending=False),
    use_container_width=True,
    height=400
)

# Footer
st.markdown("---")
st.caption("Dashboard Streamlit - Analyse des données BOUYGUES")
