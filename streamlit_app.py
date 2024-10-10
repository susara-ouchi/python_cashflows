import os
import streamlit as st
from PIL import Image
from tools_1.run_methods import *


# Set initial theme in session state
if 'theme' not in st.session_state:
    st.session_state['theme'] = 'dark'

# Toggle theme function
def toggle_theme():
    if st.session_state['theme'] == 'dark':
        st.session_state['theme'] = 'light'
    else:
        st.session_state['theme'] = 'dark'

# Set the CSS based on the theme
if st.session_state['theme'] == 'dark':
    st.set_page_config(page_title="Milliman Interactive User Space", page_icon="graphics/Milliman_logo_Li.ico", layout="wide")
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #222b36;
        }
        .css-18e3th9, .css-1d391kg {
            background-color: #f4f4f4;
        }
        .css-1aumxhk, .css-1v3fvcr, .css-1h4f60p, h1, h2, h3, h4, h5, h6, p, label { 
            color: #FFFFFF;
        }
        .theme-button {
            background-color: #F4F4F4;
            color: #50BDFF;
            border: 1px solid #FFFFFF;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.set_page_config(page_title="Milliman Interactive User Space", page_icon="graphics/Milliman_logo_Li.ico", layout="wide")
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #F4F4F4;
        }
        .css-18e3th9, .css-1d391kg {
            background-color: #222b36;
        }
        .css-1aumxhk, .css-1v3fvcr, .css-1h4f60p, h1, h2, h3, h4, h5, h6, p, label { 
            color: #222B36;
        }
        .theme-button {
            background-color: #F4F4F4;
            color: #000000;
            border: 1px solid #000000;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Main content

if st.session_state['theme'] == 'dark':
    logo_path = r"graphics\Milliman_logo_Cloud.ico"
    logo = Image.open(logo_path)
    st.image(logo, width=60)  # Adjust the width as needed
else:
    logo_path = r"graphics\Milliman_logo_Obsidian.ico"
    logo = Image.open(logo_path)
    st.image(logo, width=60)  # Adjust the width as needed


currwd = os.path.dirname(__file__); os.chdir(currwd)
st.header("Milliman Interactive User Space")
FileExtnSupported = [".xlsx", ".csv"]

# Layout for theme toggle button
col1, col2 = st.columns([9, 1])
with col2:
    if st.session_state['theme'] == 'dark':
        theme_name = 'Theme: Dark'
    else:
        theme_name = 'Theme: Light'
    theme_toggle = st.button(theme_name, key='theme_button', on_click=toggle_theme)
    st.markdown(f'<style>.stButton button{{background-color: {"#50BDFF" if st.session_state["theme"] == "dark" else "#FFFFFF"}; color: {"#FFFFFF" if st.session_state["theme"] == "dark" else "#000000"}}}</style>', unsafe_allow_html=True)
   
   
st.write("Hello there")

