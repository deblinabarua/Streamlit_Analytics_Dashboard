import streamlit as st
import requests

st.set_page_config(
    initial_sidebar_state="collapsed",
    layout = "wide"
)

hide_sidebar = """
<style>
    [data-testid = "stSidebar"]{
        display: none;
    }

    [data-testid="stSidebarCollapsedControl"] {
        display: none;
    }
</style>
"""

st.markdown(hide_sidebar, unsafe_allow_html = True)

if "user" not in st.session_state:
    st.error("Please log in first.")
    st.switch_page("Analytics_front.py")

col1, col2 = st.columns([5,1])
with col1:
    st.title("Service Check Dashboard")
    st.write(f"Hello, {st.session_state.user["name"]}")

with col2:
    if st.button("Logout"):
        st.session_state.clear()
        st.switch_page("Analytics_front.py")

category_list = ["ai", "banking", "cloud", "crypto", "dating", "ecommerce", "education", "email", "finance", "fitness", "food", "gambling", "gaming", "messaging", "other", "payment", "productivity", "shipping", "social", "streaming", "telecom", "travel", "vpn"]
try:
    get_category = requests.get("https://isitdownstatus.com/api/v1/services?limit=500").json()
    category_generate = {x.get("category") for x in get_category["data"] if x.get("category")} #set removes duplicates
    category_list = sorted(set(category_list) | category_generate) #| means union
except:
    pass

select_category = st.selectbox("Category", category_list)

down_service = requests.get(f"https://isitdownstatus.com/api/v1/services?category={select_category}&status=down&limit=500").json()
degraded_service = requests.get(f"https://isitdownstatus.com/api/v1/services?category={select_category}&status=degraded&limit=500").json()
operational_service = requests.get(f"https://isitdownstatus.com/api/v1/services?category={select_category}&status=operational&limit=500").json()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Operational")
    if len(operational_service["data"]):
        for service in operational_service["data"]:
            st.write(service["name"])
    else:
        st.caption("No services")

with col2:
    st.subheader("Degraged")
    if len(degraded_service["data"]):
        for service in degraded_service["data"]:
            st.write(service["name"])
    else:
        st.caption("No services")

with col3:
    st.subheader("Down")
    if len(down_service["data"]):
        for service in down_service["data"]:
            st.write(service["name"])
    else:
        st.caption("No services")