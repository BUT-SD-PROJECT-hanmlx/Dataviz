import streamlit as st
import base64
from pathlib import Path

# Configuration commune pour toutes les pages
st.set_page_config(
    page_title="Dashboard BOUYGUES",
    page_icon="stock",
    layout="wide"
)

# Ajout du CSS pour le background
def set_background():
    # Lecture et encodage de l'image en base64
    img_path = Path("src/Xait-Customer-Story-Bouygues-Telecom-logo-banner-1920x1080.jpg")
    
    if img_path.exists():
        with open(img_path, "rb") as img_file:
            encoded_string = base64.b64encode(img_file.read()).decode()
        
        st.markdown(
            f"""
            <style>
            .stApp > div:first-child {{
                background-image: url("data:image/jpg;base64,{encoded_string}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            .stApp {{
                background: linear-gradient(rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.5));
            }}
            /* Transparence pour les graphiques Plotly */
            .js-plotly-plot, .plotly-graph-div {{
                background-color: rgba(255, 255, 255, 0.85) !important;
            }}
            /* Transparence pour les dataframes */
            .stDataFrame {{
                background-color: rgba(255, 255, 255, 0.85) !important;
            }}
            /* Transparence pour les containers */
            .block-container {{
                background-color: rgba(255, 255, 255, 0.85) !important;
                max-width: 95% !important;
                padding: 2rem 1.5rem !important;
            }}
            /* Transparence pour les metrics */
            .stMetric {{
                background-color: rgba(255, 255, 255, 0.85) !important;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 10px;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

# Logo et titre commun
def show_header():
    set_background()
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("src/Bouygues_Télécom.png", width=200)
    with col2:
        st.title("Dashboard Analyse BOUYGUES")
    st.markdown("---")
