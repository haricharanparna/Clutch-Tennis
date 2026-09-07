import streamlit as st
import pandas as pd
from supabase import create_client

# Page configuration MUST come right after imports
st.set_page_config(
    page_title="Clutch Tennis",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ... rest of your script
