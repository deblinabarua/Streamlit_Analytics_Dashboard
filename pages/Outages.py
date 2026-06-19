import streamlit as st
from utils import fetch_api, require_login
#list outages, ongoing and resolved, click and show time and description

require_login("pages/Outages.py")
st.session_state["last_page"] = "pages/Outages.py"

st.set_page_config(
    initial_sidebar_state="collapsed",
    layout = "wide"
)

col1, col2 = st.columns([5,1])
with col1:
    st.title("Check Outages")
    st.write(f"Hello, {st.session_state.user['name']}")

with col2:
    if st.button("Logout"):
        st.session_state.clear()
        st.switch_page("Analytics_front.py")

get_outages = fetch_api("https://isitdownstatus.com/api/v1/outages?status=ongoing&limit=100")
get_resolved = fetch_api("https://isitdownstatus.com/api/v1/outages?status=resolved&limit=100")

selected = None

col1, col2 = st.columns(2)
with col1:
    st.subheader("Ongoing Outages")
    #with st.container(height = 300):  
    if len(get_outages.get("data")):
        for service in get_outages["data"]:
            with st.expander(service["service"]["name"]):
                st.write("Status: ", service["status"])
                st.write("Started at: ", service["started_at"])
                st.write("Reports: ", service["peak_reports"])
                st.write("Description: ", service["description"])
    else:
        st.caption("No services")

with col2:
    st.subheader("Resolved Outages")
    #with st.container(height = 300):
    if len(get_resolved.get("data")):
        for service in get_resolved["data"]:
            with st.expander(service["service"]["name"]):
                st.write("Status: ", service["status"])
                st.write("Started at: ", service["started_at"])
                st.write("Resolved at: ", service["resolved_at"])
                st.write("Duration: ", service["duration_minutes"], "min")
                st.write("Reports: ", service["peak_reports"])
                st.write("Description: ", service["description"])
    else:
        st.caption("No services")