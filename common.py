import streamlit as st
import base64
from pathlib import Path

# Configuration commune pour toutes les pages
st.set_page_config(
    page_title="Dashboard BOUYGUES",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ajout du CSS pour le background et le style professionnel
def set_background():
    # Lecture et encodage de l'image en base64
    img_path = Path("src/Xait-Customer-Story-Bouygues-Telecom-logo-banner-1920x1080.jpg")
    
    if img_path.exists():
        with open(img_path, "rb") as img_file:
            encoded_string = base64.b64encode(img_file.read()).decode()
        
        st.markdown(
            f"""
            <style>
            /* Global styles */
            .stApp {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }}
            
            /* Background image with overlay */
            .stApp > div:first-child {{
                background-image: url("data:image/jpg;base64,{encoded_string}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            
            /* Semi-transparent overlay */
            .stApp > div:first-child::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(135deg, rgba(30, 58, 138, 0.85) 0%, rgba(59, 130, 246, 0.85) 100%);
                z-index: -1;
            }}
            
            /* Transparence pour les graphiques Plotly */
            .js-plotly-plot, .plotly-graph-div {{
                background-color: rgba(255, 255, 255, 0.95) !important;
                border-radius: 12px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }}
            
            /* Transparence pour les dataframes */
            .stDataFrame {{
                background-color: rgba(255, 255, 255, 0.95) !important;
                border-radius: 8px;
            }}
            
            /* Container principal */
            .block-container {{
                background-color: rgba(255, 255, 255, 0.95) !important;
                border-radius: 16px;
                max-width: 95% !important;
                padding: 2.5rem 2rem !important;
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
                margin-top: 1rem !important;
            }}
            
            /* Metrics styling */
            .stMetric {{
                background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
                border: 1px solid #cbd5e1;
                border-radius: 12px;
                padding: 1.25rem;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }}
            
            /* Metrics label and value colors */
            .stMetric label {{
                color: #1e3a8a !important;
                font-weight: 600;
            }}
            .stMetric [data-testid="stMetricValue"] {{
                color: #0f172a !important;
                font-weight: 700;
                font-size: 1.5rem;
            }}
            .stMetric [data-testid="stMetricDelta"] {{
                color: #0f172a !important;
                font-weight: 600;
            }}
            
            /* Sidebar styling */
            [data-testid="stSidebar"] {{
                background: linear-gradient(180deg, #1e3a8a 0%, #3b82f6 100%) !important;
            }}
            
            [data-testid="stSidebar"] > div:first-child {{
                background: transparent;
            }}
            
            /* Headers in sidebar */
            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3 {{
                color: #ffffff !important;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            }}
            
            /* Labels in sidebar */
            [data-testid="stSidebar"] label {{
                color: #ffffff !important;
                font-weight: 500;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
            }}
            
            /* Sidebar inputs */
            [data-testid="stSidebar"] input,
            [data-testid="stSidebar"] select {{
                background: rgba(255, 255, 255, 0.95) !important;
                color: #1e3a8a !important;
            }}
            
            /* Headers styling */
            h1 {{
                font-size: 2.5rem;
                font-weight: 700;
                color: #1e3a8a;
                margin-bottom: 1.5rem;
            }}
            
            h2 {{
                font-size: 1.75rem;
                font-weight: 600;
                color: #1e40af;
                margin-top: 2rem;
            }}
            
            h3 {{
                font-size: 1.25rem;
                font-weight: 600;
                color: #1e40af;
            }}
            
            /* Paragraph text */
            p {{
                color: #1e3a8a;
                line-height: 1.6;
            }}
            
            /* List items */
            li {{
                color: #1e3a8a;
            }}
            
            /* Divider styling */
            hr {{
                border: none;
                border-top: 2px solid #e5e7eb;
                margin: 2rem 0;
            }}
            
            /* Button styling */
            .stButton > button {{
                background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0.5rem 1.5rem;
                font-weight: 600;
                transition: all 0.3s ease;
            }}
            
            .stButton > button:hover {{
                background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
            }}
            
            /* Input fields */
            .stTextInput > div > div > input,
            .stSelectbox > div > div > select,
            .stDateInput > div > div > input {{
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                background: #f8fafc;
                color: #1e3a8a;
            }}
            
            /* Expander styling */
            .streamlit-expanderHeader {{
                background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
                border-radius: 8px;
                border: 1px solid #cbd5e1;
            }}
            
            /* Text color for all content */
            div[data-testid="stVerticalBlock"] > div > div > div > div,
            div[data-testid="stVerticalBlock"] > div > div > div > p,
            div[data-testid="stVerticalBlock"] > div > div > div > div > p,
            div[data-testid="stVerticalBlock"] > div > div > div > div > span {{
                color: #1e3a8a !important;
            }}
            
            /* Fix for Plotly chart titles and labels */
            .js-plotly-plot h1,
            .js-plotly-plot h2,
            .js-plotly-plot h3,
            .js-plotly-plot .g-gtitle,
            .js-plotly-plot .g-xtitle,
            .js-plotly-plot .g-ytitle,
            .js-plotly-plot .xtick text,
            .js-plotly-plot .ytick text,
            .js-plotly-plot .legendtext {{
                color: #1e3a8a !important;
            }}
            
            /* Fix for all text in Plotly */
            .plotly-graph-div text {{
                fill: #1e3a8a !important;
                color: #1e3a8a !important;
            }}
            
            /* Global text color fix */
            text {{
                fill: #1e3a8a !important;
            }}
            tspan {{
                fill: #1e3a8a !important;
            }}
            
            /* Chart specific fixes */
            [data-testid="stPlotlyChart"] text,
            .plotly svg text {{
                fill: #1e3a8a !important;
                color: #1e3a8a !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

# Logo et titre commun
def show_header():
    set_background()
    
    # Header avec logo et titre
    header_col1, header_col2 = st.columns([1, 3])
    
    with header_col1:
        if Path("src/Bouygues_Télécom.png").exists():
            st.image("src/Bouygues_Télécom.png", width=180)
    
    with header_col2:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h1 style="font-size: 2.2rem; font-weight: 700; color: #1e3a8a; margin: 0;">
                📊 Dashboard Analyse Financière
            </h1>
            <p style="font-size: 1.1rem; color: #64748b; margin: 0.5rem 0 0 0;">
                BOUYGUES SA - Analyse Complète des Marchés
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<hr style="border-top: 3px solid #3b82f6; margin: 1.5rem 0;">', unsafe_allow_html=True)
