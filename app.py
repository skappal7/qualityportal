import streamlit as st

def set_bg_hack(main_bg):
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("{main_bg}");
             background-size: cover;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

def login_page():
    # Set the background image for the login page
    set_bg_hack("https://www.canva.com/design/DAGL9S_l410/WzaXQv7gZBwnlq2oILaVzA/view")

    st.markdown(
        """
        <style>
        .login-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .login-box {
            background-color: rgba(255, 255, 255, 0.8);
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        with st.form("login_form", clear_on_submit=True):
            st.markdown('<div class="login-box">', unsafe_allow_html=True)
            st.title("Humach Quality Portal")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login")
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if submit_button:
        if username == "humach" and password == "password":
            st.session_state.logged_in = True
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

def home_page():
    st.header("Welcome to Humach Quality Portal")
    st.write("This is the home page of the quality assurance application.")

def form_designer():
    st.header("Quality Form Designer")
    st.write("Here you can design your quality assessment forms.")
    # Add form designer functionality
    st.text_input("Form Name")
    st.text_area("Form Description")
    st.button("Add Question")
    st.button("Save Form")

def call_assessment():
    st.header("Call Assessment")
    st.write("Assess calls using the designed quality forms.")
    # Add call assessment functionality
    st.selectbox("Select Form", ["Form 1", "Form 2", "Form 3"])
    st.audio("sample_audio.mp3")  # Replace with actual audio file
    st.text_area("Assessment Notes")
    st.button("Submit Assessment")

def reports():
    st.header("Quality Reports")
    st.write("Generate and view reports based on quality parameters.")
    # Add reporting functionality
    st.date_input("Start Date")
    st.date_input("End Date")
    st.multiselect("Select Agents", ["Agent 1", "Agent 2", "Agent 3"])
    st.button("Generate Report")

def user_management():
    st.header("User Management")
    st.write("Manage users and their roles.")
    # Add user management functionality
    st.text_input("New Username")
    st.text_input("New Password", type="password")
    st.selectbox("Role", ["Admin", "Evaluator", "Agent"])
    st.button("Add User")

def main_app():
    # Remove any background image set during login
    st.markdown(
        """
        <style>
        .stApp {
            background-image: none;
            background-color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.title("Humach Quality Portal")
    
    menu = ["Home", "Form Designer", "Call Assessment", "Reports", "User Management"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Home":
        home_page()
    elif choice == "Form Designer":
        form_designer()
    elif choice == "Call Assessment":
        call_assessment()
    elif choice == "Reports":
        reports()
    elif choice == "User Management":
        user_management()

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()
