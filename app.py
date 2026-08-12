import streamlit as st
import streamlit.components.v1 as components

# Define the new OmniTrust SVG logo (Enterprise Cyan/Blue Theme)
SVG_LOGO = """<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <rect width="200" height="200" rx="40" fill="#082f49"/>
  <circle cx="100" cy="100" r="70" fill="none" stroke="#0ea5e9" stroke-width="6"/>
  <circle cx="100" cy="100" r="45" fill="none" stroke="#38bdf8" stroke-width="4" stroke-dasharray="8 6"/>
  <path d="M100 30 L170 100 L100 170 L30 100 Z" fill="none" stroke="#0ea5e9" stroke-width="3"/>
  <circle cx="100" cy="100" r="15" fill="#ffffff"/>
</svg>"""

# Automatically save the SVG string to a file on startup
with open("logo.svg", "w") as f:
    f.write(SVG_LOGO)

# Configure Streamlit page layout
st.set_page_config(
    page_title="OmniTrust — Enterprise Verification Layer",
    page_icon="logo.svg",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if hasattr(st, "logo"):
    st.logo("logo.svg", icon_image="logo.svg")

# Hide default Streamlit padding, header, and footer
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        div.block-container {
            padding: 0rem !important;
            max-width: 100% !important;
        }
        iframe {
            width: 100% !important;
            height: 100vh !important;
            border: none;
        }
    </style>
""", unsafe_allow_html=True)

# Read and render dashboard.html
with open("dashboard.html", "r", encoding="utf-8") as f:
    html_code = f.read()

components.html(html_code, height=1000, scrolling=True)