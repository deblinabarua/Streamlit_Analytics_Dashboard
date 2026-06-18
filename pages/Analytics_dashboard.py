'''
import streamlit as st
import kagglehub

from kagglehub import KaggleDatasetAdapter

if "user" not in st.session_state:
    st.error("Please login first.")
    st.stop()

@st.cache_data
def load_data():

    return (
        kagglehub.load_dataset(

            KaggleDatasetAdapter.PANDAS,

            "rupsarroy/rainfall-dataset-uttar-pradesh-20052025",

            "UP_rainfall_dataset.csv"

        )
    )

df = load_data()
col1, col2 = st.columns([5,1])
with col1:
    st.title("Uttar Pradesh Rainfall Analytics Dashboard")
    st.write(f"Hello, {st.session_state.user["name"]}")

with col2:
    if st.button("Logout"):
        st.session_state.clear()
        st.switch_page("Analytics_front.py")



year = st.selectbox("Select Year", sorted(df["YEAR"].unique()))
month = st.selectbox("Select Month", sorted(df["MO"].unique()))
filtered = df[(df["YEAR"] == year) & (df["MO"] == month)]

col1, col2, col3 = st.columns(3)
col1.metric("Avg Rainfall", round(filtered["PRECTOTCORR"].mean(), 2))
col2.metric("Avg Humidity", round(filtered["RH2M"].mean(), 1))
col3.metric("Avg Wind", round(filtered["WS50M"].mean(), 1))

st.subheader("Daily Rainfall")
chart = filtered.set_index("DY")["PRECTOTCORR"]
st.line_chart(chart)

st.subheader("Pressure")
st.line_chart(filtered.set_index("DY")["PS"])

st.subheader("Top Rainfall Days")
top = filtered.sort_values("PRECTOTCORR", ascending = False).head(10)
st.dataframe(top)

st.subheader("Weather Relationships")
st.dataframe(filtered.corr(numeric_only = True))
'''
import streamlit as st
import requests
import pandas as pd

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

slug = st.text_input("Enter a service: ")
if slug:
    get_data = requests.get(f"https://isitdownstatus.com/api/v1/status/{slug}").json()

    col1, col2, col3 = st.columns(3)
    col1.metric("Current Status", get_data["data"]["status"].upper())
    col2.metric("Number of Reports in the Last Hour", get_data["data"]["report_count_1h"])
    col3.metric("Number of Reports in Last 24 Hours", get_data["data"]["report_count_24h"])    

get_service_data = requests.get(f"https://isitdownstatus.com/api/v1/services").json()
df = pd.DataFrame(get_service_data["data"])

status_counts = df["status"].value_counts()
st.bar_chart(status_counts)

category = df["category"].value_counts()
st.bar_chart(category)

top_bad_service = df.sort_values("report_count_24h", ascending = False).head(10)

st.dataframe(top_bad_service[["name", "report_count_24h"]])

get_outage_data = requests.get(f"https://isitdownstatus.com/api/v1/outages").json()
outages = pd.DataFrame(get_outage_data["data"])
col1, col2, col3 = st.columns(3)
col1.metric("Active Outages", len(outages))
col2.metric("Peak Reports", outages["peak_reports"].max())
col3.metric("Average Reports", outages["peak_reports"].mean())

top_affected = outages.groupby(outages["service"].apply(lambda x : x["name"])).size()
st.bar_chart(top_affected)

src = outages["source"].value_counts()
st.bar_chart(src)