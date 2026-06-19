import streamlit as st
import requests
import pandas as pd
import altair as alt

@st.cache_data(ttl = 30)
def fetch_api(url):
    try:
        response = requests.get(url, timeout = 10)
        response.raise_for_status()
        return response.json()
    except Exception:
        return {"data":[]}

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
    st.title("Check by Category")
    st.write(f"Hello, {st.session_state.user['name']}")

with col2:
    if st.button("Logout"):
        st.session_state.clear()
        st.switch_page("Analytics_front.py")

category_list = ["ai", "banking", "cloud", "crypto", "dating", "ecommerce", "education", "email", "finance", "fitness", "food", "gambling", "gaming", "messaging", "other", "payment", "productivity", "shipping", "social", "streaming", "telecom", "travel", "vpn"]
try:
    get_category = fetch_api("https://isitdownstatus.com/api/v1/services?limit=500")
    category_generate = {x.get("category") for x in get_category["data"] if x.get("category")} #set removes duplicates
    category_list = sorted(set(category_list) | category_generate) #| means union
except:
    pass

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    select_category = st.selectbox("Category", category_list)

with st.spinner("Please wait."):
    down_service = fetch_api(f"https://isitdownstatus.com/api/v1/services?category={select_category}&status=down&limit=500")
    degraded_service = fetch_api(f"https://isitdownstatus.com/api/v1/services?category={select_category}&status=degraded&limit=500")
    operational_service = fetch_api(f"https://isitdownstatus.com/api/v1/services?category={select_category}&status=operational&limit=500")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Operational")
    with st.container(height = 300):  
        if len(operational_service.get("data")):
            for service in operational_service["data"]:
                st.write(service["name"])
        else:
            st.caption("No services")

with col2:
    st.subheader("Degraged")
    with st.container(height = 300):
        if len(degraded_service.get("data")):
            for service in degraded_service["data"]:
                st.write(service["name"])
        else:
            st.caption("No services")

with col3:
    st.subheader("Down")
    with st.container(height = 300):
        if len(down_service.get("data")):
            for service in down_service["data"]:
                st.write(service["name"])
        else:
            st.caption("No services")

chart_data = {"Status": ["Operational", "Degraded", "Down"], "Count": [len(operational_service.get("data")), len(degraded_service.get("data")), len(down_service.get("data"))]}
df = pd.DataFrame(chart_data)

chart = (alt.Chart(df).mark_bar().encode(x = alt.X("Status:N"), y = alt.Y("Count:Q", scale = alt.Scale(domain = [0, df["Count"].max()]))))

col1, col2 = st.columns([2, 1])

with col1:

    st.altair_chart(chart.properties(width = "container"), use_container_width = True)

with col2:

    st.metric("Total Services", df["Count"].sum())
