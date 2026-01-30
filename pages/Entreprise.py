import streamlit as st
import pandas as pd
import plotly.express as px
from common import show_header

show_header()

# Custom CSS for professional styling
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
    .info-box {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #3b82f6;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        color: #1e3a8a;
    }
    .summary-box {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #22c55e;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        color: #1e3a8a;
    }
    .info-box h3, .summary-box h3 {
        color: #1e3a8a;
    }
    .info-box p, .summary-box p {
        color: #1e3a8a;
    }
    .info-box ul, .summary-box ul {
        color: #1e3a8a;
    }
    .info-box li, .summary-box li {
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

# Informations sur l'entreprise
st.markdown('<h1 class="main-header">🏢 Profil de l\'Entreprise - Bouygues SA</h1>', unsafe_allow_html=True)

st.markdown('<div class="info-box">', unsafe_allow_html=True)
st.markdown("""
**Bouygues SA** est un groupe de services diversifié organisé autour de **4 pôles d'activités majeurs**, leader dans ses secteurs d'activité en France et à l'international.
""")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<br>', unsafe_allow_html=True)

# Pôles d'activités
st.markdown('<h2 class="section-header">📊 Pôles d\'Activités</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    with st.expander("🏗️ Construction (48,5% du CA)", expanded=True):
        st.markdown("""
        **Colas** (57,6% du CA) - *N°1 mondial de la route*
          - Construction et entretien d'infrastructures de transport
          - Aménagement urbain et loisirs
        
        **Bouygues Construction** (37,1%)
          - BTP et travaux publics de réseaux
          - Génie électrique et thermique
          - Maintenance d'installations
        
        **Bouygues Immobilier** (5,3%)
          - Promotion immobilière
        """)

with col2:
    with st.expander("🔧 Prestations de Services (33,6% du CA)", expanded=True):
        st.markdown("""
        **Equans**
          - Services multitechniques
          - Maintenance et exploitation
          - Efficacité énergétique et transition écologique
        """)

st.markdown('<br>', unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    with st.expander("📡 Télécommunications (13,7% du CA)", expanded=True):
        st.markdown("""
        **Bouygues Telecom**
          - Téléphonie mobile
          - Téléphonie fixe
          - Accès Internet (Fibre, 5G)
          - Services convergents B2B/B2C
        """)

with col4:
    with st.expander("📺 Médias (4,2% du CA)", expanded=True):
        st.markdown("""
        **TF1**
          - Chaîne de télévision généraliste
          - Production audiovisuelle
          - Plateformes numériques (MYTF1)
        """)


st.markdown('<br>', unsafe_allow_html=True)

# Répartition géographique
st.markdown('<h2 class="section-header">🌍 Répartition Géographique du Chiffre d\'Affaires</h2>', unsafe_allow_html=True)

# Création d'un dataframe pour afficher les données
geo_data = pd.DataFrame({
    'Zone Géographique': [
        'France',
        'Union européenne (hors France)',
        'Europe (hors UE)',
        'Amérique du Nord',
        'Asie-Pacifique',
        'Afrique',
        'Amérique Centrale et du Sud',
        'Moyen-Orient'
    ],
    'Part du CA': [
        '48,7%',
        '15,0%',
        '14,8%',
        '12,3%',
        '5,0%',
        '2,6%',
        '1,1%',
        '0,5%'
    ],
    'Valeur': [48.7, 15.0, 14.8, 12.3, 5.0, 2.6, 1.1, 0.5]
})

st.dataframe(
    geo_data[['Zone Géographique', 'Part du CA']],
    use_container_width=True,
    column_config={
        "Zone Géographique": st.column_config.TextColumn("Zone Géographique", width="large"),
        "Part du CA": st.column_config.TextColumn("Part du CA", width="medium")
    },
    hide_index=True,
    height=350
)

# Graphique circulaire pour visualisation
ca_values = geo_data['Valeur'].tolist()
ca_zones = geo_data['Zone Géographique'].tolist()

fig = px.pie(
    values=ca_values,
    names=ca_zones,
    title='<b>Répartition Géographique du Chiffre d\'Affaires</b>',
    color_discrete_sequence=['#1e3a8a', '#2563eb', '#3b82f6', '#60a5fa', '#93c5fd', '#bfdbfe', '#dbeafe', '#eff6ff'],
    hole=0.4
)

fig.update_traces(
    textposition='outside',
    textinfo='percent+label',
    textfont_size=11,
    hovertemplate='%{label}<br>%{value}% du CA<extra></extra>',
    marker=dict(line=dict(color='#ffffff', width=2))
)

fig.update_layout(
    showlegend=True,
    legend=dict(
        orientation="v",
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.02,
        font=dict(size=10, color='#1e3a8a')
    ),
    height=600,
    margin=dict(r=200, l=20, t=60, b=20),
    title_font=dict(size=18, family="Arial", color='#1e3a8a'),
    font=dict(family='Arial', size=11, color='#1e3a8a')
)

st.plotly_chart(fig, use_container_width=True)

st.markdown('<br>', unsafe_allow_html=True)

# Répartition par secteur d'activité
st.markdown('<h2 class="section-header">📈 Répartition par Secteur d\'Activité</h2>', unsafe_allow_html=True)

secteur_data = pd.DataFrame({
    'Secteur': [
        'Construction',
        'Services multitechniques',
        'Télécommunications',
        'Médias'
    ],
    'Part du CA': [
        '48,5%',
        '33,6%',
        '13,7%',
        '4,2%'
    ],
    'Valeur': [48.5, 33.6, 13.7, 4.2]
})

st.dataframe(
    secteur_data[['Secteur', 'Part du CA']],
    use_container_width=True,
    column_config={
        "Secteur": st.column_config.TextColumn("Secteur", width="large"),
        "Part du CA": st.column_config.TextColumn("Part du CA", width="medium")
    },
    hide_index=True,
    height=250
)

# Graphique barre pour les secteurs
secteur_values = secteur_data['Valeur'].tolist()
secteur_names = secteur_data['Secteur'].tolist()

fig_secteurs = px.bar(
    x=secteur_values,
    y=secteur_names,
    orientation='h',
    title='<b>Répartition du CA par Secteur d\'Activité</b>',
    labels={'x': 'Part du CA (%)', 'y': 'Secteur'},
    color=secteur_values,
    color_continuous_scale=['#1e3a8a', '#3b82f6', '#60a5fa', '#93c5fd'],
    text=[f'{v}%' for v in secteur_values]
)

fig_secteurs.update_traces(
    textposition='outside',
    textfont=dict(size=13, color='#1e3a8a'),
    marker=dict(line=dict(color='#ffffff', width=2))
)

fig_secteurs.update_layout(
    height=400,
    showlegend=False,
    xaxis=dict(gridcolor='#e5e7eb', gridwidth=1, title_font=dict(color='#1e3a8a'), tickfont=dict(color='#1e3a8a')),
    yaxis=dict(gridcolor='#e5e7eb', gridwidth=1, title_font=dict(color='#1e3a8a'), tickfont=dict(color='#1e3a8a')),
    plot_bgcolor='#f8fafc',
    margin=dict(l=20, r=20, t=60, b=40),
    title_font=dict(size=18, family="Arial", color='#1e3a8a'),
    font=dict(family='Arial', size=11, color='#1e3a8a')
)

st.plotly_chart(fig_secteurs, use_container_width=True)

st.markdown('<br>', unsafe_allow_html=True)

# Résumé
st.markdown('<div class="summary-box">', unsafe_allow_html=True)
st.markdown("""
### 📌 Résumé Exécutif

**Bouygues** est un groupe industriel français diversifié avec une **présence forte en France** (48,7% du CA) et une **expansion internationale significative**, particulièrement en Europe et en Amérique du Nord.

**Points clés :**
- ✓ Leader dans la construction et les services multitechniques
- ✓ Portefeuille équilibré avec 4 pôles d'activités complémentaires
- ✓ Présence mondiale dans plus de 80 pays
- ✓ Position stratégique dans les secteurs de croissance (télécoms, médias)
""")
st.markdown('</div>', unsafe_allow_html=True)
