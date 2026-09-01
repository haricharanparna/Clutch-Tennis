import streamlit as st
from supabase import create_client

st.set_page_config(
    page_title="Clutch Tennis | Reset Password",
    page_icon="🎾"
)

# Connect to Supabase
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

st.title("Clutch Tennis 🎾")
st.header("Reset Your Password")

st.write("Enter your new password below.")

# New password
newpassword = st.text_input(
    "Enter Your New Password",
    type="password"
)

# Confirm password
confirmpassword = st.text_input(
    "Confirm Your New Password",
    type="password"
)

# Reset password button
resetbutton = st.button(
    "Reset Password",
    use_container_width=True
)

if resetbutton:

    # Make sure both fields are filled out
    if not newpassword or not confirmpassword:
        st.error("Please fill out both password fields.")

    # Check that passwords match
    elif newpassword != confirmpassword:
        st.error("Passwords do not match.")

    # Check password length
    elif len(newpassword) < 6:
        st.error(
            "Password must be at least 6 characters."
        )

    else:

        try:
            # Update the user's password
            supabase.auth.update_user({
                "password": newpassword
            })

            st.success(
                "Password updated successfully! 🎾"
            )

            st.info(
                "You can now log in with your new password."
            )

            # Go back to Login
            st.switch_page("pages/login.py")

        except Exception:
            st.error(
                "Unable to reset your password. "
                "Please try again."
            )
