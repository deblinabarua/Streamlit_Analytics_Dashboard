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