import streamlit as st
import requests

st.set_page_config(
    page_title="Book a Lesson | Clutch Tennis",
    page_icon="🎾"
)

st.title("Book Your Tennis Session")
st.write("Fill out the form below to request your lesson.")

with st.form("booking_form"):
    name = st.text_input("Full Name")
    preferred_time = st.selectbox(
    "Preferred Time",
    [
        "9:00 AM",
        "10:00 AM",
        "11:00 AM",
        "12:00 PM",
        "1:00 PM",
        "2:00 PM",
        "3:00 PM",
        "4:00 PM",
        "5:00 PM",
        "6:00 PM",
        "7:00 PM"
    ]
)
    email = st.text_input("Your Email Address")

    lesson_type = st.selectbox(
        "Lesson Type",
        [
            "Private Coaching",
            "Group Coaching",
            "Mental Toughness",
            "Match Play & Strategy"
        ]
    )

    preferred_date = st.date_input("Preferred Date")
    notes = st.text_area("Goals or Special Requests")

    submitted = st.form_submit_button("Submit Booking Request", use_container_width=True)

if submitted:
    if not name or not email:
        st.error("Please fill out both your name and email address.")
    else:
        with st.spinner("Saving your booking request..."):
            endpoint = "https://api.sheetmonkey.io/form/fQvQ98iNDidpE7BcoVNnmH"

            payload = {
                "Name": name,
                "Email": email,
                "Lesson Type": lesson_type,
                "Preferred Date": str(preferred_date),
                "Notes": notes
            }

            try:
                response = requests.post(
                    endpoint, 
                    json=payload, 
                    headers={"Content-Type": "application/json"}
                )

                if response.status_code in [200, 201]:
                    st.success("Booking request submitted successfully!")
                else:
                    st.error("Submission failed. Please check your sheet connection.")
            except Exception:
                st.error("Network error. Please try again.")
