import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random
import base64

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'forms' not in st.session_state:
    st.session_state.forms = []
if 'agent_data' not in st.session_state:
    # Generate some sample data
    agents = ['Agent ' + str(i) for i in range(1, 11)]
    st.session_state.agent_data = pd.DataFrame({
        'Agent': agents,
        'Audits': [random.randint(5, 20) for _ in agents],
        'Current Score': [random.randint(70, 100) for _ in agents],
        'Previous Score': [random.randint(70, 100) for _ in agents],
        'Historical Scores': [[random.randint(70, 100) for _ in range(10)] for _ in agents]
    })

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

def login_page():
    set_png_as_page_bg('login.png')

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
    
    form_name = st.text_input("Form Name")
    form_description = st.text_area("Form Description")
    
    question = st.text_input("Add a question")
    if st.button("Add Question"):
        if question:
            st.session_state.questions.append(question)
            st.success(f"Question added: {question}")
        else:
            st.warning("Please enter a question before adding.")
    
    if st.session_state.questions:
        st.write("Current questions:")
        for i, q in enumerate(st.session_state.questions, 1):
            st.write(f"{i}. {q}")
    
    if st.button("Save Form"):
        if form_name and st.session_state.questions:
            new_form = {
                'name': form_name,
                'description': form_description,
                'questions': st.session_state.questions.copy()
            }
            st.session_state.forms.append(new_form)
            st.session_state.questions = []
            st.success(f"Form '{form_name}' saved successfully!")
        else:
            st.warning("Please provide a form name and at least one question.")

def call_assessment():
    st.header("Call Assessment")
    st.write("Assess calls using the designed quality forms.")
    
    if not st.session_state.forms:
        st.warning("No forms available. Please create a form in the Form Designer.")
        return
    
    selected_form = st.selectbox("Select Form", [form['name'] for form in st.session_state.forms])
    selected_form_data = next(form for form in st.session_state.forms if form['name'] == selected_form)
    
    st.write(f"Form Description: {selected_form_data['description']}")
    
    st.audio("https://example.com/path/to/sample_audio.mp3")  # Replace with actual audio file
    
    for i, question in enumerate(selected_form_data['questions'], 1):
        st.write(f"{i}. {question}")
        st.text_input(f"Answer {i}", key=f"answer_{i}")
    
    notes = st.text_area("Assessment Notes")
    
    if st.button("Submit Assessment"):
        st.success("Assessment submitted successfully!")

def reports():
    st.header("Quality Reports")

    df = st.session_state.agent_data
    
    # Calculate variance
    df['Variance'] = df['Current Score'] - df['Previous Score']
    
    # Set evaluation target
    target = st.number_input("Set Evaluation Target", min_value=0, max_value=100, value=85)
    
    # Create table
    st.write("Agent Performance Table")
    for i, row in df.iterrows():
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.write(row['Agent'])
        with col2:
            st.write(f"Audits: {row['Audits']}")
        with col3:
            st.write(f"Score: {row['Current Score']}")
        with col4:
            color = 'green' if row['Variance'] >= 0 else 'red'
            st.markdown(f"Variance: <font color={color}>{row['Variance']}%</font>", unsafe_allow_html=True)
        with col5:
            fig = go.Figure(data=go.Scatter(y=row['Historical Scores'], mode='lines+markers'))
            fig.add_hline(y=target, line_dash="dash", line_color="red")
            fig.update_layout(height=100, margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig, use_container_width=True)

    # Detailed agent view
    st.subheader("Detailed Agent View")
    selected_agent = st.selectbox("Select Agent", df['Agent'])
    agent_data = df[df['Agent'] == selected_agent].iloc[0]
    
    st.write(f"Agent: {selected_agent}")
    st.write(f"Current Score: {agent_data['Current Score']}")
    st.write(f"Previous Score: {agent_data['Previous Score']}")
    st.write(f"Variance: {agent_data['Variance']}")
    
    # Trend chart
    fig = go.Figure(data=go.Scatter(y=agent_data['Historical Scores'], mode='lines+markers'))
    fig.add_hline(y=target, line_dash="dash", line_color="red")
    fig.update_layout(title=f"{selected_agent} Performance Trend", xaxis_title="Evaluations", yaxis_title="Score")
    st.plotly_chart(fig)

def user_management():
    st.header("User Management")
    st.write("Manage users and their roles.")
    
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    role = st.selectbox("Role", ["Admin", "Evaluator", "Agent"])
    
    if st.button("Add User"):
        if new_username and new_password:
            st.success(f"User {new_username} added successfully as {role}!")
        else:
            st.warning("Please provide both username and password.")

def main_app():
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
    if not st.session_state.logged_in:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()
