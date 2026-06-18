'''
import streamlit as st
import re
from werkzeug.security import generate_password_hash, check_password_hash 
from database import SessionLocal, Registration, Login_logs
from sqlalchemy import select

db = SessionLocal()

col1, col2 = st.columns(2)
with col1:
    with st.form("Registration"):

        st.title("Registration for Analytics")

        name = st.text_input("Enter name: ")
        username = st.text_input("Enter username: ")
        password = st.text_input("Enter password: ", type = "password")

        register = st.form_submit_button("Register")

        if register: 
            person = db.execute(select(Registration).where(Registration.username == username)).scalar_one_or_none()
            if person is not None:
                st.error("Username already exists.")
            elif not(len(password) >= 8) or not (re.search(r'\d', password)) or not(re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=/\\[\]~`]', password)):
                st.error("The password must be atleast 8 characters long and it must contain a number and a special symbol.")
            else:
                hash_pass = generate_password_hash(password)
                db.add(Registration(username = username, name = name, password = hash_pass))
                db.commit()
                st.success("Registration Completed")

with col2:

    with st.form("Login User"):

        st.title("Login for Analytics")

        username = st.text_input("Enter username: ")
        password = st.text_input("Enter password: ", type = "password")

        login = st.form_submit_button("Login")

        if login:
            person = db.execute(select(Registration).where(Registration.username == username)).scalar_one_or_none()
            if person is None:
                st.error("Incorrect username or password.")
            elif not check_password_hash(person.password, password):
                st.error("Incorrect username or password.")
            else:
                st.success("Login scuccessful.")
                st.session_state.logged_in = True
                st.session_state.user = {"username": person.username, "name": person.name}
                log = Login_logs(user_id = person.id)
                db.add(log)
                db.commit()
                st.switch_page("pages/Analytics_dashboard.py")
'''
import streamlit as st
import re
from werkzeug.security import generate_password_hash, check_password_hash 
from database import SessionLocal, Registration, Login_logs
from sqlalchemy import select

db = SessionLocal()

st.set_page_config(
    initial_sidebar_state="collapsed"
)

if "user" in st.session_state:
    st.error("You are already logged in.")
    st.switch_page("pages/Analytics_dashboard.py")

st.title("Analytics")
tab1, tab2, tab3 = st.tabs(["Homepage", "Register", "Login"])

with tab1:
    st.header("Analytics of Something")
    st.text("Using this free api, you can view and navigate through all the data easily.")

with tab2:
    with st.form("Registration"):
        st.header("Register as a New User")
        name = st.text_input("Enter name: ")
        username = st.text_input("Enter username: ")
        password = st.text_input("Enter password: ", type = "password")

        register = st.form_submit_button("Register")

        if register: 
            person = db.execute(select(Registration).where(Registration.username == username)).scalar_one_or_none()
            if person is not None:
                st.error("Username already exists.")
            elif not(len(password) >= 8) or not (re.search(r'\d', password)) or not(re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=/\\[\]~`]', password)):
                st.error("The password must be atleast 8 characters long and it must contain a number and a special symbol.")
            else:
                hash_pass = generate_password_hash(password)
                db.add(Registration(username = username, name = name, password = hash_pass))
                db.commit()
                st.success("Registration Completed")

with tab3:
    with st.form("Login User"):
        st.header("Log in to your Account")
        username = st.text_input("Enter username: ")
        password = st.text_input("Enter password: ", type = "password")

        login = st.form_submit_button("Login")

        if login:
            person = db.execute(select(Registration).where(Registration.username == username)).scalar_one_or_none()
            if person is None:
                st.error("Incorrect username or password.")
            elif not check_password_hash(person.password, password):
                st.error("Incorrect username or password.")
            else:
                st.success("Login scuccessful.")
                st.session_state.logged_in = True
                st.session_state.user = {"username": person.username, "name": person.name}
                log = Login_logs(user_id = person.id)
                db.add(log)
                db.commit()
                st.switch_page("pages/Analytics_dashboard.py")