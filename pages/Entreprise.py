import streamlit as st
from common import show_header

show_header()

# Informations sur l'entreprise
st.header("Profil de l'Entreprise - Bouygues SA")

st.markdown("---")

# Description principale
st.info("""
**Bouygues SA** est un groupe de services diversifié organisé autour de 4 pôles d'activités majeurs.
""")

# Pôles d'activités
st.header("Poles d'Activites")

col1, col2 = st.columns(2)

with col1:
    with st.expander("Construction (48,5% du CA)", expanded=True):
        st.markdown("""
        - **Colas** (57,6% du CA) : n°1 mondial de la route
          - Construction et entretien d'infrastructures de transport
          - Loisirs et amenagement urbain
        
        - **Bouygues Construction** (37,1%)
          - BTP et travaux publics de reseaux
          - Genie electrique et thermique
          - Maintenance d'installations
        
        - **Bouygues Immobilier** (5,3%)
          - Promotion immobiliere
        """)

with col2:
    with st.expander("Prestations de Services (33,6% du CA)", expanded=True):
        st.markdown("""
        - **Equans**
          - Services multitechniques
          - Maintenance et exploitation
          - Efficacité énergétique
        """)

st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    with st.expander("Telecommunications (13,7% du CA)", expanded=True):
        st.markdown("""
        - **Bouygues Telecom**
          - Telefonie mobile
          - Telefonie fixe
          - Acces a Internet
          - Services convergents
        """)

with col4:
    with st.expander("Medias (4,2% du CA)", expanded=True):
        st.markdown("""
        - **TF1**
          - Chaîne de télévision
          - Production audiovisuelle
          - Plateformes numériques
        """)

st.markdown("---")

# Répartition géographique
st.header("Repartition Geographique du CA")

# Création d'un dataframe pour afficher les données
import pandas as pd
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
    ]
})

st.dataframe(
    geo_data,
    use_container_width=True,
    column_config={
        "Zone Géographique": st.column_config.TextColumn("Zone Géographique"),
        "Part du CA": st.column_config.TextColumn("Part du CA")
    },
    hide_index=True
)

# Graphique circulaire pour visualisation
import plotly.express as px

ca_values = [48.7, 15.0, 14.8, 12.3, 5.0, 2.6, 1.1, 0.5]
ca_zones = geo_data['Zone Géographique'].tolist()

fig = px.pie(
    values=ca_values,
    names=ca_zones,
    title='Répartition Géographique du Chiffre d\'Affaires',
    color_discrete_sequence=px.colors.qualitative.Set3
)

fig.update_traces(
    textposition='inside',
    textinfo='percent+label',
    hovertemplate='%{label}<br>%{value}% du CA<extra></extra>'
)

fig.update_layout(
    showlegend=False,
    height=600
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Répartition par secteur d'activité
st.header("Repartition par Secteur d'Activite")

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
    ]
})

st.dataframe(
    secteur_data,
    use_container_width=True,
    column_config={
        "Secteur": st.column_config.TextColumn("Secteur"),
        "Part du CA": st.column_config.TextColumn("Part du CA")
    },
    hide_index=True
)

# Graphique barre pour les secteurs
secteur_values = [48.5, 33.6, 13.7, 4.2]
secteur_names = secteur_data['Secteur'].tolist()

fig_secteurs = px.bar(
    x=secteur_values,
    y=secteur_names,
    orientation='h',
    title='Répartition du CA par Secteur d\'Activité',
    labels={'x': 'Part du CA (%)', 'y': 'Secteur'},
    color=secteur_values,
    color_continuous_scale='Blues'
)

fig_secteurs.update_traces(
    text=[f'{v}%' for v in secteur_values],
    textposition='outside'
)

fig_secteurs.update_layout(
    height=400,
    showlegend=False
)

st.plotly_chart(fig_secteurs, use_container_width=True)

st.markdown("---")

# Résumé
st.success("""
**Résumé :** Bouygues est un groupe industriel français diversifié avec une présence forte 
en France (près de 50% du CA) et une expansion internationale significative, 
particulièrement en Europe et en Amérique du Nord. Le groupe repose principalement 
sur ses activités de construction et de services multitechniques, complétées par 
les télécommunications et les médias.
""")
