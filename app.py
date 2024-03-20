import streamlit as st
import pandas as pd
from src.scraper import scrape 

USER_DATABASE = {
    "admin": "password123",
    "admin2": "password123"
}

def job_search_page():
    st.title('Job Search')

    # Create form elements
    job_name = st.text_input('Job Name').strip().title()
    min_salary = st.number_input('Minimum Salary', min_value=0, value=0, step=500)
    max_salary = st.number_input('Maximum Salary', min_value=0, value=10000, step=500)
    employment_types = ['Permanent', 'Full Time', 'Part Time', 'Contract', 'Flexi-work', 'Temporary', 'Freelance', 'Internship/Attachment']
    selected_employment_types = st.multiselect('Filter Employment Types', employment_types)

    # Submit button
    if st.button('Search'):
        if not job_name:
            st.error('Please enter a job name to proceed.')
        else:
            st.write('Job Name:', job_name)
            st.write('Minimum Salary:', min_salary)
            st.write('Maximum Salary:', max_salary)

            if selected_employment_types == []:
                st.write('Selected Employment Types: None')
            else:
                st.write('Selected Employment Types:', ', '.join(selected_employment_types))

            with st.spinner('Extracting data... Please wait'):
                scraped_data = scrape(job_name, min_salary, max_salary, selected_employment_types)
            
            csv = pd.DataFrame(scraped_data).to_csv(index=False)

            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name= f'{job_name}.csv',
                mime='text/csv',
            )


def verify_login(username, password):
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