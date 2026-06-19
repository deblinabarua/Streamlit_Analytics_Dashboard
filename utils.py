import streamlit as st
import requests

@st.cache_data(ttl = 30)
def fetch_api(url):
    try:
        response = requests.get(url, timeout = 10)
        response.raise_for_status()
        return response.json()
    except Exception:
        return {"data":[]}
    
def require_login(current_page):
    st.session_state["next_page"] = current_page
    if not st.session_state.get("logged_in"):
        st.switch_page("Analytics_front.py")