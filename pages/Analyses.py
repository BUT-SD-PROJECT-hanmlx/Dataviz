import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from common import show_header

show_header()

# Custom CSS for professional analysis styling
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
    .metric-card {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 1.25rem;
        border-radius: 12px;
        border: 1px solid #cbd5e1;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .conclusion-positive {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #22c55e;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        color: #1e3a8a;
    }
    .conclusion-warning {
        background: linear-gradient(135deg, #fef9c3 0%, #fef08a 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #eab308;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        color: #1e3a8a;
    }
    .conclusion-negative {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #ef4444;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        color: #1e3a8a;
    }
    .conclusion-info {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #3b82f6;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        color: #1e3a8a;
    }
    .conclusion-positive h3, .conclusion-warning h3, 
    .conclusion-negative h3, .conclusion-info h3 {
        color: #1e3a8a;
    }
    .conclusion-positive p, .conclusion-warning p, 
    .conclusion-negative p, .conclusion-info p {
        color: #1e3a8a;
    }
    .conclusion-positive ul, .conclusion-warning ul, 
    .conclusion-negative ul, .conclusion-info ul {
        color: #1e3a8a;
    }
    .conclusion-positive li, .conclusion-warning li, 
    .conclusion-negative li, .conclusion-info li {
        color: #1e3a8a;
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

st.markdown('<h1 class="main-header">📊 Analyses et Conclusions Opérationnelles</h1>', unsafe_allow_html=True)

# SECTION 1: Tendance de Prix
st.markdown('<h2 class="section-header">1️⃣ Analyse de la Tendance des Prix</h2>', unsafe_allow_html=True)

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

st.markdown('<br>', unsafe_allow_html=True)


# Conclusion sur la tendance
if total_return > 0:
    st.markdown('<div class="conclusion-positive">', unsafe_allow_html=True)
    st.markdown(f"""
    ### ✅ CONCLUSION POSITIVE
    
    L'action **BOUYGUES** a réalisé une performance positive de **{total_return:.2f}%** sur la période analysée.
    
    **📈 Recommandation :** Maintenir ou augmenter les positions. La tendance haussière indique une bonne performance de l'entreprise.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="conclusion-negative">', unsafe_allow_html=True)
    st.markdown(f"""
    ### ❌ CONCLUSION NÉGATIVE
    
    L'action **BOUYGUES** a perdu **{abs(total_return):.2f}%** sur la période analysée.
    
    **📉 Recommandation :** Surveiller de près les indicateurs financiers et la stratégie de l'entreprise avant de prendre des décisions d'investissement.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<br>', unsafe_allow_html=True)


# SECTION 2: Analyse de Volatilite
st.markdown('<h2 class="section-header">2️⃣ Analyse de la Volatilité et du Risque</h2>', unsafe_allow_html=True)

volatility = df['Daily_Return'].std()
avg_volatility = df['Volatility_20d'].mean()

col1, col2 = st.columns(2)
with col1:
    st.metric("Volatilité Moyenne (20 jours)", f"{volatility:.2f}%")
with col2:
    st.metric("Écart-type du Prix", f"{avg_volatility:.2f}€")

# Graphique de volatilite
fig_vol = go.Figure()
fig_vol.add_trace(go.Scatter(
    x=df['Date'],
    y=df['Daily_Return'],
    mode='lines',
    name='Rendements Journaliers',
    line=dict(color='#1e3a8a', width=1.5),
    fill='tozeroy',
    fillcolor='rgba(59, 130, 246, 0.1)'
))
fig_vol.add_hline(y=volatility, line_dash="dash", line_color="#dc2626", 
                annotation_text=f"+{volatility:.2f}%", annotation_position="top left",
                annotation_font=dict(size=11, color="#dc2626"))
fig_vol.add_hline(y=-volatility, line_dash="dash", line_color="#16a34a", 
                annotation_text=f"-{volatility:.2f}%", annotation_position="bottom left",
                annotation_font=dict(size=11, color="#16a34a"))
fig_vol.update_layout(
    title='<b>Rendements Journaliers et Bandes de Volatilité</b>',
    xaxis_title='Date',
    yaxis_title='Rendement (%)',
    height=400,
    plot_bgcolor='#f8fafc',
    paper_bgcolor='#ffffff',
    font=dict(family='Arial', size=11, color='#1e3a8a'),
    margin=dict(l=60, r=40, t=60, b=40),
    xaxis=dict(gridcolor='#e5e7eb', gridwidth=1, title_font=dict(color='#1e3a8a'), tickfont=dict(color='#1e3a8a')),
    yaxis=dict(gridcolor='#e5e7eb', gridwidth=1, title_font=dict(color='#1e3a8a'), tickfont=dict(color='#1e3a8a'))
)
st.plotly_chart(fig_vol, use_container_width=True)

st.markdown('<br>', unsafe_allow_html=True)

# Conclusion sur la volatilite
if volatility < 2:
    st.markdown('<div class="conclusion-positive">', unsafe_allow_html=True)
    st.markdown("""
    ### ✅ CONCLUSION : Faible Volatilité
    
    L'action présente un **risque modéré**.
    
    **📊 Recommandation :** Investissement adéquat pour les profils prudents. Variations prévisibles et risque limité.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
elif volatility < 4:
    st.markdown('<div class="conclusion-warning">', unsafe_allow_html=True)
    st.markdown("""
    ### ⚠️ CONCLUSION : Volatilité Moyenne
    
    Le risque est **équilibré**.
    
    **📊 Recommandation :** Diversifier le portefeuille pour mitiger le risque. Surveillance régulière recommandée.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="conclusion-negative">', unsafe_allow_html=True)
    st.markdown("""
    ### ❌ CONCLUSION : Haute Volatilité
    
    Risque **élevé**.
    
    **📊 Recommandation :** Allocation de capital prudente. Considérer des stratégies de couverture ou attendre une stabilisation.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<br>', unsafe_allow_html=True)


# SECTION 3: Analyse des Signaux de Trading
st.markdown('<h2 class="section-header">3️⃣ Signaux de Trading et Points d\'Entrée/Sortie</h2>', unsafe_allow_html=True)

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
fig_ma.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name='Prix', line=dict(color='#1e3a8a', width=2)))
fig_ma.add_trace(go.Scatter(x=df['Date'], y=df['MA20'], name='MA 20', line=dict(color='#f59e0b', width=2)))
fig_ma.add_trace(go.Scatter(x=df['Date'], y=df['MA50'], name='MA 50', line=dict(color='#3b82f6', width=2)))
fig_ma.update_layout(
    title='<b>Prix et Moyennes Mobiles - Identification des Signaux</b>',
    xaxis_title='Date',
    yaxis_title='Prix (€)',
    height=500,
    plot_bgcolor='#f8fafc',
    paper_bgcolor='#ffffff',
    font=dict(family='Arial', size=11, color='#1e3a8a'),
    margin=dict(l=60, r=40, t=60, b=40),
    xaxis=dict(gridcolor='#e5e7eb', gridwidth=1, title_font=dict(color='#1e3a8a'), tickfont=dict(color='#1e3a8a')),
    yaxis=dict(gridcolor='#e5e7eb', gridwidth=1, title_font=dict(color='#1e3a8a'), tickfont=dict(color='#1e3a8a'))
)
st.plotly_chart(fig_ma, use_container_width=True)

st.markdown('<br>', unsafe_allow_html=True)

# Signaux de trading
st.markdown('### 📡 Signaux Actuels', unsafe_allow_html=True)

if current_price > current_ma20 and current_ma20 > current_ma50:
    st.markdown('<div class="conclusion-positive">', unsafe_allow_html=True)
    st.markdown(f"""
    ### 🚀 SIGNAL HAUSSIER FORT
    
    Prix ({current_price:.2f}€) > MA20 ({current_ma20:.2f}€) > MA50 ({current_ma50:.2f}€)
    
    **📊 DÉCISION : SIGNAL D'ACHAT**
    - ✓ Tendance court terme haussière confirmée
    - ✓ Momentum positif
    - ✓ Maintenir les positions existantes
    """)
    st.markdown('</div>', unsafe_allow_html=True)
elif current_price > current_ma20:
    st.markdown('<div class="conclusion-warning">', unsafe_allow_html=True)
    st.markdown(f"""
    ### ⚠️ SIGNAL MIXTE
    
    Prix ({current_price:.2f}€) > MA20 ({current_ma20:.2f}€) mais MA20 < MA50 ({current_ma50:.2f}€)
    
    **📊 DÉCISION : ATTENTION / PATIENCE**
    - ⚡ Court terme positif mais long terme négatif
    - ⏳ Attendre le croisement des moyennes
    - 👁️ Surveiller le support actuel
    """)
    st.markdown('</div>', unsafe_allow_html=True)
elif current_price < current_ma20 and current_ma20 < current_ma50:
    st.markdown('<div class="conclusion-negative">', unsafe_allow_html=True)
    st.markdown(f"""
    ### 📉 SIGNAL BAISSIER FORT
    
    Prix ({current_price:.2f}€) < MA20 ({current_ma20:.2f}€) < MA50 ({current_ma50:.2f}€)
    
    **📊 DÉCISION : SIGNAL DE VENTE**
    - ✗ Tendance baissière confirmée
    - ⚠️ Risque de poursuite de la baisse
    - 💡 Considérer la réduction des positions
    """)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="conclusion-info">', unsafe_allow_html=True)
    st.markdown(f"""
    ### ⚖️ SIGNAL NEUTRE
    
    Prix ({current_price:.2f}€) proche des moyennes
    
    **📊 DÉCISION : MAINTENIR / OBSERVER**
    - 📊 Marché en consolidation
    - ⏳ Attendre une direction claire
    - 🚫 Ne pas prendre de nouvelles positions
    """)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<br>', unsafe_allow_html=True)


# SECTION 4: Points critiques (Support/Resistance)
st.markdown('<h2 class="section-header">4️⃣ Identification des Supports et Résistances</h2>', unsafe_allow_html=True)

# Calcul des supports et resistances sur 30 derniers jours
df_recent = df.tail(30)
support_level = df_recent['Low'].min()
resistance_level = df_recent['High'].max()

col1, col2 = st.columns(2)
with col1:
    st.metric("Support Actuel (30 jours)", f"{support_level:.2f}€")
with col2:
    st.metric("Résistance Actuelle (30 jours)", f"{resistance_level:.2f}€")

fig_sr = go.Figure()
fig_sr.add_trace(go.Scatter(x=df_recent['Date'], y=df_recent['Close'], name='Prix', line=dict(color='#1e3a8a', width=2.5)))
fig_sr.add_hline(y=support_level, line_dash="dash", line_color="#16a34a", 
                annotation_text=f"Support: {support_level:.2f}€", annotation_position="bottom right",
                annotation_font=dict(size=11, color="#16a34a"))
fig_sr.add_hline(y=resistance_level, line_dash="dash", line_color="#dc2626", 
                annotation_text=f"Résistance: {resistance_level:.2f}€", annotation_position="top right",
                annotation_font=dict(size=11, color="#dc2626"))
fig_sr.update_layout(
    title='<b>Prix avec Support et Résistance</b>',
    xaxis_title='Date',
    yaxis_title='Prix (€)',
    height=400,
    plot_bgcolor='#f8fafc',
    paper_bgcolor='#ffffff',
    font=dict(family='Arial', size=11, color='#1e3a8a'),
    margin=dict(l=60, r=40, t=60, b=40),
    xaxis=dict(gridcolor='#e5e7eb', gridwidth=1, title_font=dict(color='#1e3a8a'), tickfont=dict(color='#1e3a8a')),
    yaxis=dict(gridcolor='#e5e7eb', gridwidth=1, title_font=dict(color='#1e3a8a'), tickfont=dict(color='#1e3a8a'))
)
st.plotly_chart(fig_sr, use_container_width=True)

st.markdown('<br>', unsafe_allow_html=True)

# Conclusion sur les supports/resistances
distance_to_support = ((current_price - support_level) / current_price) * 100
distance_to_resistance = ((resistance_level - current_price) / current_price) * 100

if current_price > support_level * 1.02 and current_price < resistance_level * 0.98:
    st.markdown('<div class="conclusion-positive">', unsafe_allow_html=True)
    st.markdown(f"""
    ### ✅ POSITION SÉCURISÉE
    
    Le prix ({current_price:.2f}€) est dans la zone de sécurité.
    
    **📊 Informations :**
    - Distance au support: **{distance_to_support:.2f}%**
    - Distance à la résistance: **{distance_to_resistance:.2f}%**
    
    **📈 DÉCISION :** Maintenir les positions. Zone d'équilibre saine.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
elif current_price <= support_level * 1.02:
    st.markdown('<div class="conclusion-warning">', unsafe_allow_html=True)
    st.markdown(f"""
    ### ⚠️ PROXIMITÉ DU SUPPORT
    
    Le prix ({current_price:.2f}€) est proche du support ({support_level:.2f}€).
    
    **📊 DÉCISION : SURVEILLANCE ACTIVE**
    - Si le support casse → considérer une réduction de position
    - Si rebond → opportunité d'achat potentielle
    """)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="conclusion-warning">', unsafe_allow_html=True)
    st.markdown(f"""
    ### ⚠️ PROXIMITÉ DE LA RÉSISTANCE
    
    Le prix ({current_price:.2f}€) est proche de la résistance ({resistance_level:.2f}€).
    
    **📊 DÉCISION : PRENDRE DES BÉNÉFICES**
    - Risque de correction à court terme
    - Considérer la vente partielle pour sécuriser les gains
    """)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<br>', unsafe_allow_html=True)


# SECTION 5: Recommandations Globales
st.markdown('<h2 class="section-header">5️⃣ Synthèse et Recommandations Globales</h2>', unsafe_allow_html=True)

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

st.markdown(f'### 🎯 Score Global : <span style="font-size: 2rem; font-weight: bold; color: {"#22c55e" if score >= 4 else "#eab308" if score >= 2 else "#ef4444"}">{score}/5</span>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    if score >= 4:
        st.success("✅ Rendement: POSITIF")
    elif score >= 2:
        st.warning("⚠️ Rendement: MIXTE")
    else:
        st.error("❌ Rendement: NÉGATIF")

with col2:
    if volatility < 3:
        st.success("✅ Risque: FAIBLE")
    elif volatility < 5:
        st.warning("⚠️ Risque: MOYEN")
    else:
        st.error("❌ Risque: ÉLEVÉ")

with col3:
    if current_price > current_ma20:
        st.success("✅ Tendance: HAUSSIÈRE")
    else:
        st.error("❌ Tendance: BAISSIÈRE")

st.markdown('<br>', unsafe_allow_html=True)

if score >= 4:
    st.markdown('<div class="conclusion-positive">', unsafe_allow_html=True)
    st.markdown(f"""
    ### 🚀 RECOMMANDATION PRINCIPALE : ACHETER / AUGMENTER LES POSITIONS
    
    **Conditions favorables réunies :**
    - ✓ Performance positive
    - ✓ Tendance haussière
    - ✓ Volatilité contrôlée
    - ✓ Prix au-dessus des supports
    
    **💡 Action concrète :** Ouvrir ou augmenter les positions avec un stop-loss sous **{support_level:.2f}€**
    """)
    st.markdown('</div>', unsafe_allow_html=True)
elif score >= 2:
    st.markdown('<div class="conclusion-warning">', unsafe_allow_html=True)
    st.markdown(f"""
    ### ⚠️ RECOMMANDATION PRINCIPALE : MAINTENIR / OBSERVER
    
    **Situation mixte avec opportunités et risques :**
    - ⏳ Attendre plus de clarté sur la tendance
    - 👁️ Surveillance étroite des supports
    - 🚫 Ne pas prendre de nouvelles positions importantes
    
    **💡 Action concrète :** Maintenir les positions existantes, attendre les signaux futurs
    """)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="conclusion-negative">', unsafe_allow_html=True)
    st.markdown(f"""
    ### 📉 RECOMMANDATION PRINCIPALE : VENDRE / RÉDUIRE LES POSITIONS
    
    **Conditions défavorables :**
    - ✗ Performance négative
    - ✗ Tendance baissière
    - ✗ Risque élevé
    
    **💡 Action concrète :** Considérer la réduction des positions pour limiter les pertes potentielles
    """)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<br>', unsafe_allow_html=True)

st.markdown('<hr>', unsafe_allow_html=True)
st.caption("💡 Analyses réalisées automatiquement sur les données historiques BOUYGUES. Pour des décisions financières importantes, consultez un conseiller en investissement.")
