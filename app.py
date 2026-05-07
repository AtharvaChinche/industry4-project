import streamlit as st
import pandas as pd
import random
import time

st.set_page_config(
    page_title="Industry 4.0 Dashboard",
    layout="wide"
)

# ---------------- TITLE ----------------
st.title("🏭 Knowledge Integrated Real-Time Intelligence")
st.subheader("Real-Time Industrial Monitoring Dashboard")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Control Panel")

temperature = st.sidebar.slider(
    "Temperature (°C)",
    20,
    50,
    25
)

pressure = st.sidebar.slider(
    "Pressure (bar)",
    1,
    10,
    3
)

speed = st.sidebar.slider(
    "Machine Speed (RPM)",
    500,
    5000,
    1500
)

# ---------------- STATUS ----------------
if temperature > 35:
    status = "ALERT"
else:
    status = "NORMAL"

# ---------------- TOP METRICS ----------------
col1, col2, col3 = st.columns(3)

col1.metric("Temperature", f"{temperature} °C")
col2.metric("Pressure", f"{pressure} bar")
col3.metric("Speed", f"{speed} RPM")

# ---------------- STATUS BOX ----------------
if status == "ALERT":
    st.error("⚠️ ALERT: High Temperature")
else:
    st.success("✅ System Operating Normally")

# ---------------- LIVE DATA ----------------
st.subheader("📈 Live Machine Analytics")

chart_data = pd.DataFrame({
    "Temperature": [temperature + random.randint(-2, 2) for _ in range(20)],
    "Pressure": [pressure + random.uniform(-0.5, 0.5) for _ in range(20)]
})

st.line_chart(chart_data)

# ---------------- MACHINE TABLE ----------------
st.subheader("🏭 Machine Status Table")

machine_data = pd.DataFrame({
    "Machine": ["Mixer-01", "Boiler-02", "Packaging-03"],
    "Temperature": [
        temperature,
        temperature - 2,
        temperature + 1
    ],
    "Pressure": [
        pressure,
        pressure + 1,
        pressure - 1
    ],
    "Status": [
        status,
        "NORMAL",
        "NORMAL"
    ]
})

st.dataframe(machine_data)

# ---------------- FOOTER ----------------
st.markdown("---")
st.write("Industry 4.0 Cloud Monitoring System")
