import streamlit as st
from src.scraper import scrape 

USER_DATABASE = {
    "admin": "password123"
}

def job_search_page():
    st.title('Job Search')

    # Create form elements
    job_name = st.text_input('Job Name')
    min_salary = st.number_input('Minimum Salary', min_value=0, step=500)
    max_salary = st.number_input('Maximum Salary', min_value=0, step=500)
    employment_types = ['Permanent', 'Full Time', 'Part Time', 'Contract', 'Flexi-work', 'Temporary', 'Freelance', 'Internship/Attachment']
    selected_employment_types = st.multiselect('Filter Employment Types', employment_types)

    # Submit button
    if st.button('Search'):
        st.write('Job Name:', job_name)
        st.write('Minimum Salary:', min_salary)
        st.write('Maximum Salary:', max_salary)
        st.write('Selected Employment Types:', ', '.join(selected_employment_types))


def verify_login(username, password):
    """Check if the username and password match a user in the database."""
    if username in USER_DATABASE and USER_DATABASE[username] == password:
        return True
    return False

def login_page():
    """The login page interface."""
    st.title("Login Page")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        submitted = st.form_submit_button("Login")
        if submitted:
            if verify_login(username, password):
                # Authentication success
                st.session_state['authenticated'] = True
            else:
                st.error("Incorrect username or password.")

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if st.session_state['authenticated']:
    job_search_page()
else:
    login_page()