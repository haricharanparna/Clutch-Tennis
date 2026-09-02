import streamlit as st

st.set_page_config(
    page_title="Clutch Tennis | About",
    page_icon="🎾",
    layout="wide"
)

# -----------------------------
# LOGIN PROTECTION
# -----------------------------
if not st.session_state.get("logged_in", False):
    st.switch_page("pages/login.py")


# -----------------------------
# PAGE
# -----------------------------
st.title("About Clutch Tennis 🎾")

st.write(
    "Learn more about Clutch Tennis, our coaching philosophy, "
    "and the coaches behind the program."
)


# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>

    [data-testid="stAppViewContainer"] {
        background-color: #F7F8F5;
        color: #17201C;
    }

    .section-title {
        color: #0B3D2E;
        font-size: 2rem;
        font-weight: bold;
        margin-top: 30px;
        margin-bottom: 10px;
    }

    .about-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 30px;
        margin-top: 15px;
        margin-bottom: 25px;
    }

    .coach-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        min-height: 550px;
        margin-top: 15px;
    }

    .coach-name {
        color: #0B3D2E;
        font-size: 1.25rem;
        font-weight: bold;
        margin-top: 10px;
    }

    .coach-role {
        color: #666666;
        font-size: 0.9rem;
        margin-top: 5px;
        margin-bottom: 15px;
    }

    .qualifications {
        text-align: left;
        color: #17201C;
        font-size: 0.9rem;
        line-height: 1.6;
    }

    .qualifications-title {
        color: #0B3D2E;
        font-weight: bold;
        font-size: 1rem;
        margin-bottom: 5px;
    }

    div.stButton > button {
        background-color: #0B3D2E;
        color: #FFFFFF;
        border: none;
    }

</style>
""", unsafe_allow_html=True)


# -----------------------------
# ABOUT ME
# -----------------------------
st.markdown(
    '<div class="section-title">About Me</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="about-card">

<h3>Welcome to Clutch Tennis!</h3>

<p>
Clutch Tennis was created with one goal:
<strong>Train Hard. Play Clutch.</strong>
</p>

<p>
Our goal is to help players improve their tennis skills, build
confidence, and become stronger competitors on the court.
</p>

<p>
Whether you're learning the fundamentals, preparing for matches,
or looking to take your game to the next level, our training is
designed around each player's individual goals.
</p>

</div>
""", unsafe_allow_html=True)


# -----------------------------
# COACHING PHILOSOPHY
# -----------------------------
st.markdown(
    '<div class="section-title">Our Coaching Philosophy</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="about-card" style="text-align: center;">
        <h3 style="color: #0B3D2E;">🎾 Skill</h3>
        <p>
            Build strong fundamentals and develop the technical
            skills needed to become a better tennis player.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="about-card" style="text-align: center;">
        <h3 style="color: #0B3D2E;">🧠 Mindset</h3>
        <p>
            Develop confidence, focus, and mental toughness
            for challenging moments on the court.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="about-card" style="text-align: center;">
        <h3 style="color: #0B3D2E;">🏆 Competition</h3>
        <p>
            Practice strategies and situations that prepare
            players for competitive matches.
        </p>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------
# MEET THE COACHES
# -----------------------------
st.markdown(
    '<div class="section-title">Meet the Coaches</div>',
    unsafe_allow_html=True
)

st.write(
    "Get to know the coaches behind Clutch Tennis."
)


# -----------------------------
# COACH INFORMATION
# -----------------------------
coaches = [
    {
        "name": "Coach 1",
        "role": "Head Coach",
        "image": "https://placehold.co/500x350?text=Coach+1",
        "qualifications": [
            "Tennis coaching experience",
            "Competitive tennis experience",
            "Player development",
            "Match strategy"
        ]
    },
    {
        "name": "Coach 2",
        "role": "Assistant Coach",
        "image": "https://placehold.co/500x350?text=Coach+2",
        "qualifications": [
            "Tennis coaching experience",
            "Competitive tennis experience",
            "Technical development",
            "Footwork training"
        ]
    },
    {
        "name": "Coach 3",
        "role": "Performance Coach",
        "image": "https://placehold.co/500x350?text=Coach+3",
        "qualifications": [
            "Athletic performance",
            "Movement training",
            "Speed and agility",
            "Player conditioning"
        ]
    },
    {
        "name": "Coach 4",
        "role": "Mental Toughness Coach",
        "image": "https://placehold.co/500x350?text=Coach+4",
        "qualifications": [
            "Mental game development",
            "Match preparation",
            "Confidence building",
            "Competitive mindset"
        ]
    },
    {
        "name": "Coach 5",
        "role": "Match Strategy Coach",
        "image": "https://placehold.co/500x350?text=Coach+5",
        "qualifications": [
            "Match strategy",
            "Tactical development",
            "Competitive experience",
            "Game planning"
        ]
    }
]


# -----------------------------
# FIVE COACH COLUMNS
# -----------------------------
coach_columns = st.columns(5)

for column, coach in zip(coach_columns, coaches):

    with column:

        qualifications_html = ""

        for qualification in coach["qualifications"]:
            qualifications_html += (
                f"<li>{qualification}</li>"
            )

        st.markdown(
            f"""
            <div class="coach-card">

                <img
                    src="{coach["image"]}"
                    style="
                        width: 100%;
                        height: 220px;
                        object-fit: cover;
                        border-radius: 10px;
                    "
                >

                <div class="coach-name">
                    {coach["name"]}
                </div>

                <div class="coach-role">
                    {coach["role"]}
                </div>

                <div class="qualifications">

                    <div class="qualifications-title">
                        Qualifications
                    </div>

                    <ul>
                        {qualifications_html}
                    </ul>

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# -----------------------------
# WHY CLUTCH TENNIS
# -----------------------------
st.markdown(
    '<div class="section-title">Why Clutch Tennis?</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="about-card">

<p>
🎯 <strong>Personalized Training</strong><br>
Training is built around each player's individual goals.
</p>

<p>
💪 <strong>Confidence</strong><br>
Develop the confidence to trust your skills during matches.
</p>

<p>
🧠 <strong>Mental Toughness</strong><br>
Learn how to stay focused and composed in competitive situations.
</p>

<p>
🏆 <strong>Match Preparation</strong><br>
Practice strategies and situations that translate directly
to competitive tennis.
</p>

</div>
""", unsafe_allow_html=True)


# -----------------------------
# BOOK A LESSON
# -----------------------------
st.divider()

st.subheader("Ready to Get Started? 🎾")

st.write(
    "Take the next step and book your Clutch Tennis session."
)

if st.button(
    "Book a Lesson",
    use_container_width=True
):
    st.switch_page("pages/booking.py")
