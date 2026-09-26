import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="CityPulse",
    page_icon="🌆",
    layout="wide"
)

st.title("🌆 CityPulse")
st.subheader("Urban Intelligence & Big Data Analytics")

# Load processed data
zone_data = pd.read_csv("Data/processed/zone_summary.csv")
anomaly_data = pd.read_csv("Data/processed/anomalies.csv")

# Key metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Records", "525,600")

with col2:
    st.metric("City Zones", len(zone_data))

with col3:
    st.metric("Anomalies Detected", len(anomaly_data))

st.divider()

# Zone summary
st.header("📊 City Zone Summary")
st.dataframe(
    zone_data,
    width="stretch"
)

# Traffic
st.header("🚗 Average Traffic by Zone")
st.bar_chart(
    zone_data.set_index("zone")["avg_traffic"]
)

# AQI
st.header("🌫️ Average AQI by Zone")
st.bar_chart(
    zone_data.set_index("zone")["avg_aqi"]
)

# Energy
st.header("⚡ Average Energy Usage by Zone")
st.bar_chart(
    zone_data.set_index("zone")["avg_energy"]
)

# Activity
st.header("👥 Average Activity by Zone")
st.bar_chart(
    zone_data.set_index("zone")["avg_activity"]
)

# Anomalies
st.header("🚨 Detected Anomalies")
st.dataframe(
    anomaly_data.head(50),
    width="stretch"
)