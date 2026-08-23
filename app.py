import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Clutch Tennis",
    page_icon="🔬",
    layout="wide"
)

st.title("Clutch Tennis")
st.subheader("Train Hard. Play Clutch")
st.write(
    "Personalized tennis coaching focused on improving your skills, "
    "building confidence, and helping you perform when it matters most."
)

if st.button("Book a Lesson"):
    st.success("Unavailable")


st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background-color: #F7F8F5;
        color: #17201C;
    }

    .card-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-top: 20px;
    }

    .card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        text-align: center;
        height: 380px;
    }

    .card-title {
        color: #0B3D2E;
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .card-desc {
        color: #17201C;
        font-size: 0.95rem;
        flex-grow: 1;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .card-price {
        color: #17201C;
        font-size: 0.95rem;
        margin: 15px 0;
    }

    div.stButton > button {
        background-color: #0B3D2E;
        color: #FFFFFF;
        border: none;
    }
</style>
""", unsafe_allow_html=True)


sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSgtx-vuVX2vg5vG-NfSGzB9LyzYXFwQ6or-y0GjdpAWwYCwvh89ueQStE8OYVcbaGgoFsH0IISrNr-/pub?output=csv"

cache_bust_url = sheet_url + "&cachebust=" + str(pd.Timestamp.now().timestamp())

df = pd.read_csv(cache_bust_url)

df.columns = df.columns.str.strip()


# Service Cards
st.markdown("""
<div class="card-grid">
""", unsafe_allow_html=True)

for _, row in df.iterrows():
    st.markdown(f"""
    <div class="card">
        <div class="card-title">{row["Service"]}</div>
        <div class="card-desc">{row["Description"]}</div>
        <div class="card-price">{row["Price"]}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


# Booking Buttons
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button(
        "Book a Private Coaching Lesson",
        use_container_width=True
    ):
        st.switch_page("pages/booking.py")

with col2:
    if st.button(
        "Book a Group Coaching Lesson",
        use_container_width=True
    ):
        st.switch_page("pages/booking.py")

with col3:
    if st.button(
        "Book a Mental Toughness Class",
        use_container_width=True
    ):
        st.switch_page("pages/booking.py")

with col4:
    if st.button(
        "Book a Strategy Class",
        use_container_width=True
    ):
        st.switch_page("pages/booking.py")