import textwrap
import streamlit as st
from supabase import create_client

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Coach Dashboard | Clutch Tennis",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# CONNECT TO SUPABASE
# ============================================================

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# ============================================================
# LOGIN PROTECTION
# ============================================================

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/login.py")

# ============================================================
# CURRENT USER
# ============================================================

user = st.session_state.get("user")
coach_email = ""

if user:
    coach_email = getattr(user, "email", "") or ""

# ============================================================
# FETCH PLAYERS
# ============================================================

player_options = {}

try:
    # Fetch profiles to populate player dropdown
    profiles_response = supabase.table("profiles").select("email, full_name").execute()
    players_data = profiles_response.data or []

    for player in players_data:
        email = player.get("email")
        name = player.get("full_name", "Player")
        if email:
            label = f"{name} — {email}" if name else email
            player_options[label] = email
except Exception as e:
    st.error("Could not fetch players list.")

# Fallback if no players are found in profiles table
if not player_options:
    player_options = {"Demo Player — player@example.com": "player@example.com"}

# ============================================================
# CUSTOM STYLING (FIXED LOW CONTRAST & DARK INPUTS)
# ============================================================

st.markdown(
    textwrap.dedent("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: #F7F8F5;
    color: #17201C;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 800px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

#MainMenu, footer {
    visibility: hidden;
}

/* FORM CARD CONTAINER */
[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1px solid #E4E9E4;
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 10px 30px rgba(23,32,28,0.05);
}

/* INPUT LABELS */
div[data-widget="stSelectbox"] label,
div[data-widget="stTextArea"] label,
div[class*="stSelectbox"] label,
div[class*="stTextArea"] label,
p {
    color: #0B3D2E !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
}

/* SELECT BOX FIX */
div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #17201C !important;
    border: 1px solid #D1D5DB !important;
    border-radius: 12px !important;
}

div[data-baseweb="select"] span {
    color: #17201C !important;
}

/* TEXT AREA FIX */
div[data-baseweb="textarea"] {
    background-color: #FFFFFF !important;
    border: 1px solid #D1D5DB !important;
    border-radius: 12px !important;
}

div[data-baseweb="textarea"] textarea {
    background-color: #FFFFFF !important;
    color: #17201C !important;
}

/* SUBMIT BUTTON FIX */
div[data-testid="stFormSubmitButton"] > button {
    background-color: #0B3D2E !important;
    color: #FFFFFF !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: none !important;
    padding: 12px 24px !important;
    width: 100% !important;
    margin-top: 10px !important;
}

div[data-testid="stFormSubmitButton"] > button:hover {
    background-color: #145A43 !important;
    color: #FFFFFF !important;
}

/* FORM HEADER */
.form-title {
    color: #0B3D2E;
    font-size: 1.8rem;
    font-weight: 800;
    margin-bottom: 5px;
}

.form-subtitle {
    color: #66706B;
    font-size: 0.95rem;
    margin-bottom: 25px;
}
</style>
"""),
    unsafe_allow_html=True,
)

# ============================================================
# FORM LAYOUT
# ============================================================

st.markdown('<div class="form-title">Send Coach Feedback 🎾</div>', unsafe_allow_html=True)
st.markdown('<div class="form-subtitle">Submit personalized notes to guide your player\'s next steps.</div>', unsafe_allow_html=True)

with st.form("coach_feedback_form", clear_on_submit=True):
    
    selected_player_label = st.selectbox(
        "Select Player",
        options=list(player_options.keys())
    )
    
    category = st.selectbox(
        "Category",
        options=[
            "Technique & Stroke",
            "Match Strategy",
            "Physical & Fitness",
            "Mental Game",
            "General Feedback"
        ]
    )
    
    feedback_notes = st.text_area(
        "Feedback Notes",
        placeholder="Enter detailed feedback on performance, drills, and focus areas...",
        height=150
    )
    
    submitted = st.form_submit_button("Submit Feedback →")
    
    if submitted:
        if not feedback_notes.strip():
            st.error("Please enter feedback notes before submitting.")
        else:
            player_email = player_options[selected_player_label]
            
            payload = {
                "coach_email": coach_email,
                "player_email": player_email,
                "category": category,
                "feedback": feedback_notes,
            }
            
            try:
                supabase.table("coach_feedback").insert(payload).execute()
                st.success(f"Feedback successfully sent to {selected_player_label}!")
            except Exception as e:
                st.error("Failed to submit feedback. Please check database permissions.")
                st.code(str(e))
