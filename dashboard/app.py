import streamlit as st

st.set_page_config(
    page_title="Fleet Intelligence Platform",
    layout="wide"
)

st.title("🚢 Fleet Intelligence Platform")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Ships Online", 3)

with col2:
    st.metric("Average Speed", "22.5 knots")

with col3:
    st.metric("Average Fuel", "74%")

st.subheader("Fleet Status")

st.write("""
Azure IoT Hub → Stream Analytics → Blob Storage

Telemetry ingestion pipeline is operational.
""")