import streamlit as st
from supabase import create_client

st.set_page_config(
    page_title="Clutch Tennis | Sign Up",
    page_icon="🎾"
)

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

st.header("Create Your Account")

nameinput = st.text_input("Enter Your Full Name")
emailinput = st.text_input("Enter Your Email")

passwordinput = st.text_input(
    "Enter Your Password",
    type="password"
)

confirmpassword = st.text_input(
    "Confirm Password",
    type="password"
)

createacc = st.button("Create Account")
login_button = st.button("Back to Login")
if login_button:
    st.switch_page("pages/login.py")

if createacc:
    if not emailinput or not passwordinput or not confirmpassword:
        st.error("Please fill out all fields.")

    elif passwordinput != confirmpassword:
        st.error("Passwords do not match.")

    else:
        try:
            data = supabase.auth.sign_up({
                "email": emailinput,
                "password": passwordinput
            })

            if data.user:
                st.success("Account created successfully! 🎾")
            else:
                st.error("Account could not be created.")

        except Exception:
            st.error("Something went wrong. Please try again.")

back_login = st.button("Back to Login")

if back_login:
    st.switch_page("pages/login.py")
