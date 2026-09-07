import streamlit as st
import requests
import re
from datetime import datetime
import streamlit.components.v1 as components

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


# -----------------------------
# SESSION STATE
# -----------------------------
if "name_error" not in st.session_state:
    st.session_state["name_error"] = False

if "email_error" not in st.session_state:
    st.session_state["email_error"] = False

if "time_error" not in st.session_state:
    st.session_state["time_error"] = False


# -----------------------------
# DATE
# -----------------------------
preferred_date = st.date_input(
    "Preferred Date"
)


# -----------------------------
# CHECK GOOGLE SHEET AVAILABILITY
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

        try:
            booked_times = (
                availability_response
                .json()
                .get("bookedTimes", [])
            )

        except ValueError:
            booked_times = []

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
# RED BORDER CSS
# -----------------------------
if st.session_state["name_error"]:

    st.markdown(
        """
        <style>
        div[data-testid="stTextInput"]:has(
            input[aria-label="Full Name"]
        ) input {
            border: 2px solid red !important;
            box-shadow: 0 0 0 1px red !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


if st.session_state["email_error"]:

    st.markdown(
        """
        <style>
        div[data-testid="stTextInput"]:has(
            input[aria-label="Your Email Address"]
        ) input {
            border: 2px solid red !important;
            box-shadow: 0 0 0 1px red !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DISCLAIMER
# ============================================================

st.markdown(
    """
    <h3 style="margin-bottom: 5px;">
        Disclaimer & Booking Agreement
    </h3>
    """,
    unsafe_allow_html=True
)

st.write(
    "Please read the entire agreement below before continuing with your booking."
)


# -----------------------------
# SCROLLABLE DISCLAIMER BOX
# -----------------------------
components.html(
    """
    <div id="disclaimerBox"
        style="
            height: 300px;
            overflow-y: auto;
            border: 1px solid #D1D5DB;
            border-radius: 12px;
            padding: 22px;
            background-color: #FFFFFF;
            color: #17201C;
            font-family: Arial, sans-serif;
            line-height: 1.6;
            box-sizing: border-box;
        ">

        <h3 style="color:#0B3D2E; margin-top:0;">
            Clutch Tennis Participation & Booking Disclaimer
        </h3>

        <p>
            Tennis coaching involves physical activity, exercise,
            movement, and participation in tennis-related drills
            and activities. Physical activity involves inherent
            risks, including the possibility of accidents or injuries.
        </p>

        <p>
            By requesting a Clutch Tennis session, you acknowledge
            that tennis and physical activity may involve risks such
            as falls, collisions, strains, sprains, soreness, or
            other injuries. You understand that these risks cannot
            always be completely eliminated even when reasonable
            safety precautions are taken.
        </p>

        <p>
            You agree to follow the instructions, rules, and safety
            guidelines provided by the coach during your session.
            You understand that the coach may modify, pause, or stop
            an activity when the coach believes doing so is appropriate
            for safety, weather, court conditions, or training purposes.
        </p>

        <p>
            You agree to communicate with the coach about any physical
            limitations, injuries, pain, illness, or other concerns
            that could affect your ability to safely participate in a
            session. You should immediately notify the coach if you
            experience significant pain, dizziness, difficulty breathing,
            or otherwise feel unsafe or unable to continue.
        </p>

        <p>
            Outdoor tennis sessions may be affected by weather and
            court conditions. Rain, lightning, extreme temperatures,
            wet courts, unsafe surfaces, or other environmental
            conditions may require a session to be modified,
            postponed, rescheduled, or canceled.
        </p>

        <p>
            Participants are expected to use appropriate footwear
            and clothing and to bring water and any personal tennis
            equipment that they need for the session, unless other
            arrangements have been made with the coach.
        </p>

        <p>
            Participants agree to use tennis equipment, courts, and
            other facilities responsibly and to follow any rules
            established by the facility where the session takes place.
        </p>

        <p>
            Clutch Tennis provides coaching, instruction, practice,
            and training. Participation in a coaching session does
            not guarantee a particular athletic, competitive, ranking,
            or performance result. Player improvement depends on many
            individual factors, including practice, attendance, effort,
            experience, physical ability, and consistency.
        </p>

        <p>
            You understand that coaching advice is intended to support
            tennis development and should be followed responsibly.
            Participants remain responsible for communicating concerns
            and making reasonable decisions about their own participation.
        </p>

        <p>
            If a participant is under 18 years old, a parent or legal
            guardian should review and approve the participant's
            involvement in Clutch Tennis activities and any applicable
            consent or waiver requirements.
        </p>

        <p>
            By continuing with the booking process, you acknowledge
            that you have had an opportunity to read the information
            above and understand that participation in tennis and
            physical activity involves inherent risks.
        </p>

        <p>
            This agreement is intended to communicate important
            information about participation and safety. It should not
            be considered a substitute for professional legal advice,
            and Clutch Tennis should have the final wording reviewed
            by a qualified attorney before relying on it as a legal
            waiver or release.
        </p>

        <hr>

        <p style="
            text-align:center;
            color:#0B3D2E;
            font-weight:bold;
            margin-bottom:0;
        ">
            Please scroll to the bottom of this box to continue.
        </p>

    </div>

    <script>

        const box = document.getElementById("disclaimerBox");

        function checkScroll() {

            const reachedBottom =
                box.scrollTop + box.clientHeight >=
                box.scrollHeight - 5;

            if (reachedBottom) {

                try {

                    window.parent.postMessage(
                        {
                            type: "clutch_disclaimer_read",
                            value: true
                        },
                        "*"
                    );

                } catch (error) {
                    console.log(error);
                }

            }

        }

        box.addEventListener("scroll", checkScroll);

        checkScroll();

    </script>
    """,
    height=320
)


# -----------------------------
# DISCLAIMER AGREEMENT
# -----------------------------
st.markdown(
    """
    <div style="
        background-color:#F7F8F5;
        border-radius:10px;
        padding:12px;
        margin-top:10px;
        margin-bottom:15px;
    ">
    """,
    unsafe_allow_html=True
)

disclaimer_agreed = st.checkbox(
    "I have read the entire Disclaimer & Booking Agreement and agree to it."
)

st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# ============================================================
# BOOKING FORM
# ============================================================

with st.form("booking_form"):

    name = st.text_input(
        "Full Name",
        key="booking_name"
    )

    email = st.text_input(
        "Your Email Address",
        key="booking_email"
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
            available_times,
            key="booking_time"
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


# ============================================================
# VALIDATION
# ============================================================

if submitted:

    # -----------------------------
    # NAME
    # -----------------------------
    name_error = not name.strip()

    # -----------------------------
    # EMAIL
    # -----------------------------
    email_error = (
        not email.strip()
        or not re.match(
            r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
            email
        )
    )

    # -----------------------------
    # TIME
    # -----------------------------
    time_error = not preferred_time

    # -----------------------------
    # DISCLAIMER
    # -----------------------------
    disclaimer_error = not disclaimer_agreed

    # -----------------------------
    # SAVE ERRORS
    # -----------------------------
    st.session_state["name_error"] = name_error
    st.session_state["email_error"] = email_error
    st.session_state["time_error"] = time_error


    # -----------------------------
    # ERROR MESSAGES
    # -----------------------------
    if name_error:

        st.error(
            "❌ Full Name: Please enter your name."
        )

    if email_error:

        st.error(
            "❌ Email: Please enter a valid email address."
        )

    if time_error:

        st.error(
            "❌ Preferred Time: Please choose an available time."
        )

    if disclaimer_error:

        st.error(
            "❌ Disclaimer: Please read and agree to the "
            "Disclaimer & Booking Agreement before submitting."
        )


    # ========================================================
    # SUBMIT IF EVERYTHING IS VALID
    # ========================================================

    if (
        not name_error
        and not email_error
        and not time_error
        and not disclaimer_error
    ):

        with st.spinner(
            "Saving your booking request..."
        ):

            # -----------------------------
            # SHEETMONKEY
            # -----------------------------
            endpoint = (
                "https://api.sheetmonkey.io/form/"
                "fQvQ98iNDidpE7BcoVNnmH"
            )

            # -----------------------------
            # DISCLAIMER TIMESTAMP
            # -----------------------------
            disclaimer_date = datetime.now().strftime(
                "%Y-%m-%d %I:%M:%S %p"
            )

            # -----------------------------
            # BOOKING PAYLOAD
            # -----------------------------
            payload = {

                "Name": name,

                "Email": email,

                "Lesson Type": lesson_type,

                "Preferred Date": str(
                    preferred_date
                ),

                "Preferred Time": str(
                    preferred_time
                ),

                "Notes": notes,

                # Disclaimer information
                "Disclaimer Agreed": "Yes",

                "Disclaimer Date": disclaimer_date,

                "Disclaimer Version": "Version 1.0"
            }


            # -----------------------------
            # SEND TO GOOGLE SHEETS
            # -----------------------------
            try:

                response = requests.post(
                    endpoint,
                    json=payload,
                    headers={
                        "Content-Type": "application/json"
                    },
                    timeout=15
                )

                # -----------------------------
                # SUCCESS
                # -----------------------------
                if response.status_code in [200, 201]:

                    st.success(
                        "Booking request submitted successfully! 🎾"
                    )

                    st.info(
                        "Your booking request has been received."
                    )

                    # Clear validation errors
                    st.session_state["name_error"] = False
                    st.session_state["email_error"] = False
                    st.session_state["time_error"] = False

                # -----------------------------
                # FAILED
                # -----------------------------
                else:

                    st.error(
                        "Submission failed. "
                        "Please check your sheet connection."
                    )

            # -----------------------------
            # NETWORK ERROR
            # -----------------------------
            except Exception:

                st.error(
                    "Network error. Please try again."
                )
