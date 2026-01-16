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
    
    # Conversion des colonnes numériques
    numeric_cols = ['Open', 'High', 'Low', 'Last', 'Close', 'Number of Shares', 'Number of Trades', 'Turnover', 'vwap']
    for col in numeric_cols:
        df[col] = df[col].astype(str).str.replace(',', '.').astype(float)
    
    # Conversion de la date
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    
    return df

df = load_data()

# Calculs pour l'analyse
df['Daily_Return'] = df['Close'].pct_change() * 100
df['MA20'] = df['Close'].rolling(window=20).mean()
df['MA50'] = df['Close'].rolling(window=50).mean()
df['Volatility_20d'] = df['Close'].rolling(window=20).std()
df['Cumulative_Return'] = (1 + df['Close'].pct_change()).cumprod() - 1

st.header("Analyses et Conclusions Operationnelles")
st.markdown("---")

# SECTION 1: Tendance de Prix
st.header("1. Analyse de la Tendance des Prix")

latest_price = df['Close'].iloc[-1]
first_price = df['Close'].iloc[0]
total_return = ((latest_price - first_price) / first_price) * 100

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Prix Initial", f"{first_price:.2f}€")
with col2:
    st.metric("Prix Actuel", f"{latest_price:.2f}€")
with col3:
    st.metric("Performance Totale", f"{total_return:+.2f}%")

st.markdown("---")

# Conclusion sur la tendance
if total_return > 0:
    st.success(f"""
    **CONCLUSION POSITIVE :** L'action BOUYGUES a realise une performance positive de {total_return:.2f}% 
    sur la periode analysee. 
    **Recommandation :** Maintenir ou augmenter les positions. La tendance haussiere indique 
    une bonne performance de l'entreprise.
    """)
else:
    st.error(f"""
    **CONCLUSION NEGATIVE :** L'action BOUYGUES a perdu {abs(total_return):.2f}% sur la periode analysee.
    **Recommandation :** Surveiller de pres les indicateurs financiers et la strategie de l'entreprise 
    avant de prendre des decisions d'investissement.
    """)

st.markdown("---")

# SECTION 2: Analyse de Volatilite
st.header("2. Analyse de la Volatilite et du Risque")

volatility = df['Daily_Return'].std()
avg_volatility = df['Volatility_20d'].mean()

col1, col2 = st.columns(2)
with col1:
    st.metric("Volatilite Moyenne (20 jours)", f"{volatility:.2f}%")
with col2:
    st.metric("Ecart-type du Prix", f"{avg_volatility:.2f}€")

# Graphique de volatilite
fig_vol = go.Figure()
fig_vol.add_trace(go.Scatter(
    x=df['Date'],
    y=df['Daily_Return'],
    mode='lines',
    name='Rendements Journaliers',
    line=dict(color='blue', width=1)
))
fig_vol.add_hline(y=volatility, line_dash="dash", line_color="red", 
                annotation_text=f"+{volatility:.2f}%", annotation_position="top left")
fig_vol.add_hline(y=-volatility, line_dash="dash", line_color="green", 
                annotation_text=f"-{volatility:.2f}%", annotation_position="bottom left")
fig_vol.update_layout(
    title="Rendements Journaliers et Bandes de Volatilite",
    xaxis_title='Date',
    yaxis_title='Rendement (%)',
    height=400
)
st.plotly_chart(fig_vol, use_container_width=True)

# Conclusion sur la volatilite
if volatility < 2:
    st.success("""
    **CONCLUSION :** Faible volatilite. L'action presente un risque modere.
    **Recommandation :** Investissement adequat pour les profils prudents. 
    Variations previsibles et risque limite.
    """)
elif volatility < 4:
    st.warning("""
    **CONCLUSION :** Volatilite moyenne. Le risque est equilibre.
    **Recommandation :** Diversifier le portefeuille pour mitiger le risque. 
    Surveillance reguliere recommandee.
    """)
else:
    st.error("""
    **CONCLUSION :** Haute volatilite. Risque eleve.
    **Recommandation :** Allocation de capital prudente. Considerer des 
    strategies de couverture ou attendre une stabilisation.
    """)

st.markdown("---")

# SECTION 3: Analyse des Signaux de Trading
st.header("3. Signaux de Trading et Points d'Entree/Sortie")

# Derniers signaux
current_price = df['Close'].iloc[-1]
current_ma20 = df['MA20'].iloc[-1]
current_ma50 = df['MA50'].iloc[-1]
current_vwap = df['vwap'].iloc[-1]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Prix Actuel", f"{current_price:.2f}€")
with col2:
    st.metric("MA 20 jours", f"{current_ma20:.2f}€")
with col3:
    st.metric("MA 50 jours", f"{current_ma50:.2f}€")

# Graphique avec MA
fig_ma = go.Figure()
fig_ma.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name='Prix', line=dict(color='blue', width=2)))
fig_ma.add_trace(go.Scatter(x=df['Date'], y=df['MA20'], name='MA 20', line=dict(color='orange', width=1.5)))
fig_ma.add_trace(go.Scatter(x=df['Date'], y=df['MA50'], name='MA 50', line=dict(color='green', width=1.5)))
fig_ma.update_layout(
    title='Prix et Moyennes Mobiles - Identification des Signaux',
    xaxis_title='Date',
    yaxis_title='Prix (€)',
    height=500
)
st.plotly_chart(fig_ma, use_container_width=True)

# Signaux de trading
st.subheader("Signaux Actuels")

if current_price > current_ma20 and current_ma20 > current_ma50:
    st.success(f"""
    **SIGNAL HAUSSIER FORT :** Prix ({current_price:.2f}€) > MA20 ({current_ma20:.2f}€) > MA50 ({current_ma50:.2f}€)
    
    **DECISION :** SIGNAL D'ACHAT
    - Tendance court terme haussiere confirmee
    - Momentum positif
    - Maintenir les positions existantes
    """)
elif current_price > current_ma20:
    st.warning(f"""
    **SIGNAL MIXTE :** Prix ({current_price:.2f}€) > MA20 ({current_ma20:.2f}€) mais MA20 < MA50 ({current_ma50:.2f}€)
    
    **DECISION :** ATTENTION / PATIENCE
    - Court terme positif mais long terme negatif
    - Attendre le croisement des moyennes
    - Surveiller le support actuel
    """)
elif current_price < current_ma20 and current_ma20 < current_ma50:
    st.error(f"""
    **SIGNAL BAISSIER FORT :** Prix ({current_price:.2f}€) < MA20 ({current_ma20:.2f}€) < MA50 ({current_ma50:.2f}€)
    
    **DECISION :** SIGNAL DE VENTE
    - Tendance baissiere confirmee
    - Risque de poursuite de la baisse
    - Considerer la reduction des positions
    """)
else:
    st.info(f"""
    **SIGNAL NEUTRE :** Prix ({current_price:.2f}€) proche des moyennes
    
    **DECISION :** MAINTENIR / OBSERVER
    - Marche en consolidation
    - Attendre une direction claire
    - Ne pas prendre de nouvelles positions
    """)

st.markdown("---")

# SECTION 4: Points critiques (Support/Resistance)
st.header("4. Identification des Supports et Resistances")

# Calcul des supports et resistances sur 30 derniers jours
df_recent = df.tail(30)
support_level = df_recent['Low'].min()
resistance_level = df_recent['High'].max()

col1, col2 = st.columns(2)
with col1:
    st.metric("Support Actuel (30 jours)", f"{support_level:.2f}€")
with col2:
    st.metric("Resistance Actuelle (30 jours)", f"{resistance_level:.2f}€")

fig_sr = go.Figure()
fig_sr.add_trace(go.Scatter(x=df_recent['Date'], y=df_recent['Close'], name='Prix', line=dict(color='blue', width=2)))
fig_sr.add_hline(y=support_level, line_dash="dash", line_color="green", 
                annotation_text=f"Support: {support_level:.2f}€", annotation_position="bottom right")
fig_sr.add_hline(y=resistance_level, line_dash="dash", line_color="red", 
                annotation_text=f"Resistance: {resistance_level:.2f}€", annotation_position="top right")
fig_sr.update_layout(
    title='Prix avec Support et Resistance',
    xaxis_title='Date',
    yaxis_title='Prix (€)',
    height=400
)
st.plotly_chart(fig_sr, use_container_width=True)

# Conclusion sur les supports/resistances
distance_to_support = ((current_price - support_level) / current_price) * 100
distance_to_resistance = ((resistance_level - current_price) / current_price) * 100

if current_price > support_level * 1.02 and current_price < resistance_level * 0.98:
    st.success(f"""
    **POSITION SECURE :** Le prix ({current_price:.2f}€) est dans la zone de securite.
    
    - Distance au support: {distance_to_support:.2f}%
    - Distance a la resistance: {distance_to_resistance:.2f}%
    
    **DECISION :** Maintenir les positions. Zone d'equilibre saine.
    """)
elif current_price <= support_level * 1.02:
    st.warning(f"""
    **PROXIMITE DU SUPPORT :** Le prix ({current_price:.2f}€) est proche du support ({support_level:.2f}€).
    
    **DECISION :** SURVEILLANCE ACTIVE. Si le support casse, considerer une reduction de position.
    Si rebond, opportuite d'achat potentielle.
    """)
else:
    st.warning(f"""
    **PROXIMITE DE LA RESISTANCE :** Le prix ({current_price:.2f}€) est proche de la resistance ({resistance_level:.2f}€).
    
    **DECISION :** PRENDRE DES BENEFICES. Risque de correction a court terme.
    Considerer la vente partielle pour securiser les gains.
    """)

st.markdown("---")

# SECTION 5: Recommandations Globales
st.header("5. Synthese et Recommandations Globales")

# Score global
score = 0
if total_return > 0:
    score += 2
if volatility < 4:
    score += 1
if current_price > current_ma20:
    score += 1
if current_price > support_level * 1.02:
    score += 1

st.subheader(f"Score Global : {score}/5")

col1, col2, col3 = st.columns(3)
with col1:
    if score >= 4:
        st.success("Rendement: POSITIF")
    elif score >= 2:
        st.warning("Rendement: MIXTE")
    else:
        st.error("Rendement: NEGATIF")

with col2:
    if volatility < 3:
        st.success("Risque: FAIBLE")
    elif volatility < 5:
        st.warning("Risque: MOYEN")
    else:
        st.error("Risque: ELEVE")

with col3:
    if current_price > current_ma20:
        st.success("Tendance: HAUSSIERE")
    else:
        st.error("Tendance: BAISSIERE")

if score >= 4:
    st.success(f"""
    **RECOMMANDATION PRINCIPALE :** ACHETER / AUGMENTER LES POSITIONS
    
    Conditions favorables reunies :
    - Performance positive
    - Tendance haussiere
    - Volatilite controlee
    - Prix au-dessus des supports
    
    **Action concrete :** Ouvrir ou augmenter les positions avec un stop-loss sous {support_level:.2f}€
    """)
elif score >= 2:
    st.warning(f"""
    **RECOMMANDATION PRINCIPALE :** MAINTENIR / OBSERVER
    
    Situation mixte avec opportunites et risques :
    - Attendre plus de clarte sur la tendance
    - Surveillance etroite des supports
    - Ne pas prendre de nouvelles positions importantes
    
    **Action concrete :** Maintenir les positions existantes, attendre les signaux futurs
    """)
else:
    st.error(f"""
    **RECOMMANDATION PRINCIPALE :** VENDRE / REDUIRE LES POSITIONS
    
    Conditions defavorables :
    - Performance negative
    - Tendance baissiere
    - Risque eleve
    
    **Action concrete :** Considerer la reduction des positions pour limiter les pertes potentielles
    """)

st.markdown("---")

st.caption("Analyses realisees automatiquement sur les donnees historiques BOUYGUES. Pour des decisions financieres importantes, consultez un conseiller en investissement.")
