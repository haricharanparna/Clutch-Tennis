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

newpassword = st.text_input(
    "Enter Your New Password",
    type="password"
)

confirmpassword = st.text_input(
    "Confirm Your New Password",
    type="password"
)

resetbutton = st.button(
    "Reset Password",
    use_container_width=True
)

if resetbutton:

    if not newpassword or not confirmpassword:

        st.error(
            "Please fill out both password fields."
        )

    elif newpassword != confirmpassword:

        st.error(
            "Passwords do not match."
        )

    elif len(newpassword) < 6:

        st.error(
            "Password must be at least 6 characters."
        )

    else:

        try:

            supabase.auth.update_user({
                "password": newpassword
            })

            st.success(
                "Password updated successfully! 🎾"
            )

            st.switch_page(
                "pages/login.py"
            )

        except Exception:

            st.error(
                "Unable to reset your password. "
                "Please try again."
            )
