import streamlit as st
import requests
import re

st.set_page_config(
    page_title="Book a Lesson | Clutch Tennis",
    page_icon="🎾"
)

# -----------------------------
# LOGIN PROTECTION
# -----------------------------
if not st.session_state.get("logged_in", False):
    st.switch_page("pages/login.py")

# -----------------------------
# PAGE
# -----------------------------
st.title("Book Your Tennis Session")
st.write("Fill out the form below to request your lesson.")

# -----------------------------
# AVAILABILITY
# -----------------------------
availability_url = (
    "https://script.google.com/macros/s/"
    "AKfycbxclfNHxhTVJeXhwsN14---f3qdq0fGedhzZANjNZ4b3dp202xyVzhx5FGqVDha5aKBhQ/"
    "exec"
)

times = [
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

# Date is outside the form so changing it updates available times
preferred_date = st.date_input(
    "Preferred Date"
)

# -----------------------------
# CHECK GOOGLE SHEET
# -----------------------------
try:

    availability_response = requests.get(
        availability_url,
        params={
            "date": str(preferred_date)
        },
        timeout=10
    )

    if availability_response.status_code == 200:

        booked_times = (
            availability_response
            .json()
            .get("bookedTimes", [])
        )

    else:
        booked_times = []

except Exception:
    booked_times = []

available_times = [
    time
    for time in times
    if time not in booked_times
]

# -----------------------------
# BOOKING FORM
# -----------------------------
with st.form("booking_form"):

    name = st.text_input(
        "Full Name"
    )

    email = st.text_input(
        "Your Email Address"
    )

    lesson_type = st.selectbox(
        "Lesson Type",
        [
            "Private Coaching",
            "Group Coaching",
            "Mental Toughness",
            "Match Play & Strategy"
        ]
    )

    if available_times:

        preferred_time = st.selectbox(
            "Preferred Time",
            available_times
        )

    else:

        st.warning(
            "There are no available times for this date."
        )

        preferred_time = None

    notes = st.text_area(
        "Goals or Special Requests"
    )

    submitted = st.form_submit_button(
        "Submit Booking Request",
        use_container_width=True
    )

# -----------------------------
# SUBMIT BOOKING
# -----------------------------
if submitted:

    if not name or not email:

        st.error(
            "Please fill out both your name and email address."
        )

    # Check if the email has a valid format
    elif not re.match(
        r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
        email
    ):

        st.error(
            "Please enter a valid email address."
        )

    elif not preferred_time:

        st.error(
            "Please choose an available time."
        )

    else:

        with st.spinner(
            "Saving your booking request..."
        ):

            endpoint = (
                "https://api.sheetmonkey.io/form/"
                "fQvQ98iNDidpE7BcoVNnmH"
            )

            payload = {
                "Name": name,
                "Email": email,
                "Lesson Type": lesson_type,
                "Preferred Date": str(preferred_date),
                "Preferred Time": str(preferred_time),
                "Notes": notes
            }

            try:

                response = requests.post(
                    endpoint,
                    json=payload,
                    headers={
                        "Content-Type": "application/json"
                    }
                )

                if response.status_code in [200, 201]:

                    st.success(
                        "Booking request submitted successfully! 🎾"
                    )

                else:

                    st.error(
                        "Submission failed. "
                        "Please check your sheet connection."
                    )

            except Exception:

                st.error(
                    "Network error. Please try again."
                )
