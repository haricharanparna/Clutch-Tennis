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

coach_name = "Coach"
coach_email = ""

if user:
    coach_email = getattr(user, "email", "") or ""

    if hasattr(user, "user_metadata"):
        metadata = user.user_metadata or {}
        coach_name = metadata.get("full_name", "Coach")

# ============================================================
# GET PLAYERS FROM PLAYERS TABLE
# ============================================================

# ============================================================
# GET PLAYERS FROM PLAYERS TABLE
# ============================================================

players = []

try:
    response = (
        supabase
        .table("players")
        .select("emails, full_name")
        .order("full_name")
        .execute()
    )

    for player in response.data or []:
        if player.get("emails"):
            players.append({
                "email": player["emails"],
                "name": player.get(
                    "full_name",
                    player["emails"]
                )
            })

except Exception as e:
    st.error("Unable to load players.")
    st.code(str(e))
    players = []

# ============================================================
# CUSTOM STYLING
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
    max-width: 1150px;
    padding-top: 1rem;
    padding-bottom: 4rem;
}

#MainMenu, footer {
    visibility: hidden;
}

/* ============================================================
   NAVBAR
   ============================================================ */

[data-testid="stHorizontalBlock"]:has(div.nav-logo-target) {
    background-color: #FFFFFF;
    border-radius: 40px;
    padding: 8px 16px 8px 30px;
    align-items: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    border: 1px solid #EFEFEF;
    margin-bottom: 30px;
}

.nav-logo-target {
    font-weight: 800;
    font-size: 1.3rem;
    color: #0B3D2E;
    letter-spacing: -0.5px;
    display: flex;
    align-items: center;
    white-space: nowrap;
}

.nav-logo-target span {
    color: #88C425;
    margin-left: 4px;
}

div[data-testid="stColumn"]:has(div.nav-link-btn-marker) div.stButton > button {
    background: transparent !important;
    color: #3B82F6 !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    border: none !important;
    padding: 0 !important;
    min-height: auto !important;
    box-shadow: none !important;
    text-decoration: underline !important;
}

div[data-testid="stColumn"]:has(div.nav-link-btn-marker) div.stButton > button:hover {
    color: #1D4ED8 !important;
    background: transparent !important;
}

div[data-testid="stColumn"]:has(div.nav-cta-marker) div.stButton > button {
    background-color: #0B3D2E !important;
    color: #FFFFFF !important;
    border-radius: 25px !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 8px 20px !important;
    min-height: 42px !important;
    border: none !important;
    width: 100% !important;
}

div[data-testid="stColumn"]:has(div.nav-cta-marker) div.stButton > button:hover {
    background-color: #145A43 !important;
}

/* ============================================================
   HERO
   ============================================================ */

.dashboard-hero {
    background: linear-gradient(
        135deg,
        #082D22 0%,
        #0B3D2E 55%,
        #145A43 100%
    );
    border-radius: 28px;
    padding: 45px 50px;
    color: white;
    position: relative;
    overflow: hidden;
    margin-bottom: 35px;
    box-shadow: 0 20px 50px rgba(11,61,46,0.16);
}

.dashboard-hero::after {
    content: "🎾";
    position: absolute;
    right: 50px;
    top: 15px;
    font-size: 140px;
    opacity: 0.08;
    transform: rotate(15deg);
    pointer-events: none;
}

.hero-small {
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 0.75rem;
    font-weight: 800;
    opacity: 0.7;
    margin-bottom: 12px;
}

.hero-title {
    font-size: 3rem;
    font-weight: 800;
    margin: 0;
}

.hero-title span {
    color: #C9E86A;
}

.hero-description {
    margin-top: 12px;
    font-size: 1rem;
    line-height: 1.6;
    opacity: 0.85;
    max-width: 650px;
}

/* ============================================================
   SECTION HEADERS
   ============================================================ */

.section-header {
    margin-top: 35px;
    margin-bottom: 18px;
}

.section-kicker {
    color: #0B3D2E;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 0.72rem;
    font-weight: 800;
}

.section-title {
    font-size: 1.8rem;
    font-weight: 800;
    margin-top: 4px;
    color: #17201C;
}

/* ============================================================
   CARDS
   ============================================================ */

.dashboard-card {
    background: #FFFFFF;
    border: 1px solid #E4E9E4;
    border-radius: 20px;
    padding: 25px;
    min-height: 160px;
    box-shadow: 0 8px 25px rgba(23,32,28,0.04);
}

.card-icon {
    width: 45px;
    height: 45px;
    background: #EEF5D9;
    border-radius: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    margin-bottom: 15px;
}

.card-title {
    color: #0B3D2E;
    font-size: 1.1rem;
    font-weight: 800;
    margin-bottom: 8px;
}

.card-text {
    color: #66706B;
    line-height: 1.5;
    font-size: 0.9rem;
}

/* ============================================================
   FEEDBACK
   ============================================================ */

.feedback-card {
    background: #FFFFFF;
    border: 1px solid #E4E9E4;
    border-left: 5px solid #88C425;
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 15px;
    box-shadow: 0 8px 25px rgba(23,32,28,0.04);
}

.feedback-player {
    color: #0B3D2E;
    font-weight: 800;
    font-size: 1rem;
}

.feedback-date {
    color: #8A938E;
    font-size: 0.8rem;
    margin-top: 2px;
}

.feedback-text {
    color: #59635E;
    line-height: 1.5;
    margin-top: 10px;
    font-size: 0.92rem;
}

/* ============================================================
   FORM
   ============================================================ */

div[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1px solid #E4E9E4;
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 8px 25px rgba(23,32,28,0.04);
}

/* ============================================================
   BUTTONS
   ============================================================ */

div.stButton > button {
    background: #0B3D2E;
    color: white;
    border: 0;
    border-radius: 12px;
    min-height: 48px;
    font-weight: 700;
}

</style>
"""),
    unsafe_allow_html=True,
)

# ============================================================
# NAVBAR
# ============================================================

nav_col1, nav_col2, nav_col3, nav_col4, nav_col5, nav_col6, nav_col7 = st.columns(
    [2.5, 0.8, 1.0, 1.1, 0.8, 1.0, 2.2]
)

with nav_col1:
    st.markdown(
        '<div class="nav-logo-target">🎾 CLUTCH<span>TENNIS</span></div>',
        unsafe_allow_html=True
    )

with nav_col2:
    st.markdown(
        '<div class="nav-link-btn-marker"></div>',
        unsafe_allow_html=True
    )

    if st.button("Home", key="nav_home"):
        st.switch_page("app.py")

with nav_col3:
    st.markdown(
        '<div class="nav-link-btn-marker"></div>',
        unsafe_allow_html=True
    )

    if st.button("Location", key="nav_loc"):
        st.switch_page("pages/location.py")

with nav_col4:
    st.markdown(
        '<div class="nav-link-btn-marker"></div>',
        unsafe_allow_html=True
    )

    if st.button("About Us", key="nav_about"):
        st.switch_page("pages/about.py")

with nav_col5:
    st.markdown(
        '<div class="nav-link-btn-marker"></div>',
        unsafe_allow_html=True
    )

    if st.button("FAQ", key="nav_faq"):
        st.switch_page("pages/faq.py")

with nav_col6:
    st.markdown(
        '<div class="nav-link-btn-marker"></div>',
        unsafe_allow_html=True
    )

    if st.button("Contact", key="nav_contact"):
        st.switch_page("pages/contact.py")

with nav_col7:
    st.markdown(
        '<div class="nav-cta-marker"></div>',
        unsafe_allow_html=True
    )

    if st.button(
        "Book a Free Trial",
        key="nav_cta_btn",
        use_container_width=True
    ):
        st.switch_page("pages/booking.py")

# ============================================================
# HERO
# ============================================================

st.markdown(
    textwrap.dedent(
        f"""
        <div class="dashboard-hero">

            <div class="hero-small">
                Coach Dashboard
            </div>

            <div class="hero-title">
                Welcome, <span>{coach_name}</span> 🎾
            </div>

            <div class="hero-description">
                Manage your training schedule, review active players,
                track skill development, and send detailed feedback
                to keep your athletes performing clutch.
            </div>

        </div>
        """
    ),
    unsafe_allow_html=True,
)

# ============================================================
# OVERVIEW
# ============================================================

st.markdown(
    """
    <div class="section-header">
        <div class="section-kicker">Roster & Schedule</div>
        <div class="section-title">Overview</div>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="dashboard-card">

            <div class="card-icon">👥</div>

            <div class="card-title">
                My Players
            </div>

            <div class="card-text">
                {len(players)} player(s) currently registered.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="dashboard-card">

            <div class="card-icon">📅</div>

            <div class="card-title">
                Today's Sessions
            </div>

            <div class="card-text">
                Your scheduled sessions will appear here.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="dashboard-card">

            <div class="card-icon">📈</div>

            <div class="card-title">
                Player Progress
            </div>

            <div class="card-text">
                Monitor technical and strategic growth.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        """
        <div class="dashboard-card">

            <div class="card-icon">📝</div>

            <div class="card-title">
                Feedback Sent
            </div>

            <div class="card-text">
                Track feedback submitted to players.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# FEEDBACK FORM
# ============================================================

feedback_col, recent_col = st.columns([1.2, 1])

with feedback_col:

    st.markdown(
        """
        <div class="section-header">

            <div class="section-kicker">
                Coach Communication
            </div>

            <div class="section-title">
                Give Feedback
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if not players:

        st.warning(
            "No players have been added yet."
        )

    else:

        player_options = [
            f"{player['name']} — {player['email']}"
            for player in players
        ]

        with st.form("coach_feedback_form"):

            selected_player = st.selectbox(
                "Select Player",
                player_options
            )

            feedback_category = st.selectbox(
                "Category",
                [
                    "Technique & Stroke",
                    "Match Strategy",
                    "Mental Game & Focus",
                    "Physical & Footwork"
                ]
            )

            feedback_notes = st.text_area(
                "Feedback Notes",
                placeholder=(
                    "Write notes on technique, key takeaways, "
                    "and areas to work on before the next session..."
                ),
                height=140
            )

            submitted = st.form_submit_button(
                "Submit Feedback →",
                use_container_width=True
            )

        # ====================================================
        # SAVE FEEDBACK
        # ====================================================

        if submitted:

            if not feedback_notes.strip():

                st.error(
                    "Please enter some feedback before submitting."
                )

            else:

                selected_index = player_options.index(
                    selected_player
                )

                selected_player_email = players[
                    selected_index
                ]["email"]

                try:

                    feedback_data = {
                        "coach_email": coach_email,
                        "player_email": selected_player_email,
                        "category": feedback_category,
                        "feedback": feedback_notes.strip()
                    }

                    supabase.table(
                        "coach_feedback"
                    ).insert(
                        feedback_data
                    ).execute()

                    st.success(
                        f"Feedback successfully sent to "
                        f"{players[selected_index]['name']}! 🎾"
                    )

                except Exception as e:

                    st.error(
                        "Could not save feedback."
                    )

                    st.code(str(e))

# ============================================================
# RECENT FEEDBACK
# ============================================================

with recent_col:

    st.markdown(
        """
        <div class="section-header">

            <div class="section-kicker">
                History
            </div>

            <div class="section-title">
                Recent Feedback
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    try:

        feedback_response = (
            supabase
            .table("coach_feedback")
            .select("*")
            .eq("coach_email", coach_email)
            .order("created_at", desc=True)
            .limit(10)
            .execute()
        )

        recent_feedback = feedback_response.data or []

        if not recent_feedback:

            st.info(
                "You haven't submitted any feedback yet."
            )

        else:

            for feedback in recent_feedback:

                player_email = feedback.get(
                    "player_email",
                    "Unknown player"
                )

                category = feedback.get(
                    "category",
                    "General"
                )

                feedback_text = feedback.get(
                    "feedback",
                    ""
                )

                created_at = feedback.get(
                    "created_at",
                    ""
                )

                st.markdown(
                    f"""
                    <div class="feedback-card">

                        <div class="feedback-player">
                            {player_email} — {category}
                        </div>

                        <div class="feedback-date">
                            Submitted: {created_at}
                        </div>

                        <div class="feedback-text">
                            {feedback_text}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

    except Exception as e:

        st.error(
            "Unable to load recent feedback."
        )

        st.code(str(e))

# ============================================================
# LOGOUT
# ============================================================

st.write("")

st.divider()

if st.button(
    "Log Out",
    key="logout_btn",
    use_container_width=True
):

    st.session_state["logged_in"] = False
    st.session_state["user"] = None

    st.switch_page("pages/login.py")
