import streamlit as st

st.set_page_config(
    page_title="Clutch Tennis | About",
    page_icon="🎾",
    layout="wide"
)

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/login.py")

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
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
    padding-top: 2rem;
    padding-bottom: 4rem;
}

#MainMenu, footer {
    visibility: hidden;
}

.page-hero {
    background: linear-gradient(
        135deg,
        #082D22,
        #0B3D2E
    );
    border-radius: 26px;
    padding: 50px;
    color: white;
    margin-bottom: 45px;
}

.kicker {
    color: #C9E86A;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 0.75rem;
    font-weight: 800;
}

.page-title {
    font-size: 3rem;
    font-weight: 800;
    margin-top: 10px;
}

.page-subtitle {
    font-size: 1.05rem;
    opacity: 0.82;
    max-width: 650px;
    line-height: 1.7;
}

.section-title {
    color: #0B3D2E;
    font-size: 1.8rem;
    font-weight: 800;
    margin: 35px 0 15px;
}

.info-card {
    background: white;
    border: 1px solid #E4E9E4;
    border-radius: 20px;
    padding: 30px;
    height: 100%;
    box-shadow: 0 8px 25px rgba(23,32,28,0.04);
}

.info-card h3 {
    color: #0B3D2E;
    margin-bottom: 10px;
}

.info-card p {
    color: #66706B;
    line-height: 1.7;
}

.coach-card {
    background: white;
    border: 1px solid #E4E9E4;
    border-radius: 20px;
    padding: 25px;
    min-height: 310px;
    box-shadow: 0 8px 25px rgba(23,32,28,0.04);
}

.coach-number {
    font-size: 2.2rem;
    font-weight: 800;
    color: #C9E86A;
}

.coach-name {
    color: #0B3D2E;
    font-size: 1.2rem;
    font-weight: 800;
    margin-top: 12px;
}

.coach-role {
    color: #7A837F;
    font-size: 0.85rem;
    margin: 5px 0 20px;
}

.coach-list {
    color: #59635E;
    line-height: 1.9;
    padding-left: 20px;
}

div.stButton > button {
    background: #0B3D2E;
    color: white;
    border: 0;
    border-radius: 12px;
    min-height: 48px;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HERO
# -----------------------------
st.markdown("""
<div class="page-hero">
    <div class="kicker">About Clutch Tennis</div>
    <div class="page-title">
        More than tennis.
    </div>
    <div class="page-subtitle">
        We help players develop the skills, confidence, and mindset
        needed to compete at their best.
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# STORY
# -----------------------------
st.markdown(
    '<div class="section-title">Our Approach</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
<div class="info-card">
    <h3>🎾 Skill</h3>
    <p>
        Build strong fundamentals and develop the technical
        skills needed to become a better tennis player.
    </p>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div class="info-card">
    <h3>🧠 Mindset</h3>
    <p>
        Develop confidence, focus, and mental toughness for
        challenging moments on the court.
    </p>
</div>
""", unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
<div class="info-card">
    <h3>🏆 Competition</h3>
    <p>
        Practice strategies and match situations that prepare
        players for competitive tennis.
    </p>
</div>
""", unsafe_allow_html=True)

with col4:
    st.markdown("""
<div class="info-card">
    <h3>💪 Confidence</h3>
    <p>
        Learn to trust your preparation and your abilities
        when matches become challenging.
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# COACHES
# -----------------------------
st.markdown(
    '<div class="section-title">Meet the Coaches</div>',
    unsafe_allow_html=True
)

coaches = [
    (
        "01",
        "Coach 1",
        "Head Coach",
        ["Tennis coaching experience", "Competitive tennis experience",
         "Player development", "Match strategy"]
    ),
    (
        "02",
        "Coach 2",
        "Assistant Coach",
        ["Tennis coaching experience", "Competitive tennis experience",
         "Technical development", "Footwork training"]
    ),
    (
        "03",
        "Coach 3",
        "Performance Coach",
        ["Athletic performance", "Movement training",
         "Speed and agility", "Player conditioning"]
    ),
    (
        "04",
        "Coach 4",
        "Mental Toughness Coach",
        ["Mental game development", "Match preparation",
         "Confidence building", "Competitive mindset"]
    ),
    (
        "05",
        "Coach 5",
        "Match Strategy Coach",
        ["Match strategy", "Tactical development",
         "Competitive experience", "Game planning"]
    )
]

coach_columns = st.columns(5)

for column, coach in zip(coach_columns, coaches):

    number, name, role, qualifications = coach

    with column:

        qualifications_html = ""

        for item in qualifications:
            qualifications_html += f"<li>{item}</li>"

        st.markdown(
            f"""
<div class="coach-card">
    <div class="coach-number">
        {number}
    </div>
    <div class="coach-name">
        {name}
    </div>
    <div class="coach-role">
        {role}
    </div>
    <ul class="coach-list">
        {qualifications_html}
    </ul>
</div>
""",
            unsafe_allow_html=True
        )

# -----------------------------
# WHY CLUTCH
# -----------------------------
st.markdown(
    '<div class="section-title">Why Clutch Tennis?</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="info-card">
<p>🎯 <strong>Personalized Training</strong><br>
Training is built around each player's individual goals.</p>
<p>💪 <strong>Confidence</strong><br>
Develop the confidence to trust your skills during matches.</p>
<p>🧠 <strong>Mental Toughness</strong><br>
Stay focused and composed in competitive situations.</p>
<p>🏆 <strong>Match Preparation</strong><br>
Practice strategies that translate directly to competitive tennis.</p>
</div>
""", unsafe_allow_html=True)

st.write("")

if st.button("Book a Lesson →", use_container_width=True):
    st.switch_page("pages/booking.py")
