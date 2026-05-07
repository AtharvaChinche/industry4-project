import streamlit as st
import pandas as pd
import random
from pymongo import MongoClient
from datetime import datetime

# ---------------- MONGODB ----------------
MONGO_URI = st.secrets["MONGO_URI"]

client = MongoClient(MONGO_URI)

db = client["industry_db"]
collection = db["machine_logs"]

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="Industry 4.0 Dashboard",
    layout="wide"
)

st.title("🏭 Knowledge Integrated Real-Time Intelligence")
st.subheader("Real-Time Industrial Monitoring System")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Machine Control Panel")

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

# ---------------- SAVE BUTTON ----------------
if st.sidebar.button("Update Machine Data"):

    data = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "temperature": temperature,
        "pressure": pressure,
        "speed": speed
    }

    collection.insert_one(data)

    st.sidebar.success("Data Stored Successfully")

# ---------------- FETCH LATEST DATA ----------------
latest = collection.find_one(sort=[("_id", -1)])

if latest:

    latest_temp = latest["temperature"]
    latest_pressure = latest["pressure"]
    latest_speed = latest["speed"]

    # ---------------- STATUS ----------------
    if latest_temp > 35:
        status = "ALERT"
    else:
        status = "NORMAL"

    # ---------------- METRICS ----------------
    col1, col2, col3 = st.columns(3)

    col1.metric("Temperature", f"{latest_temp} °C")
    col2.metric("Pressure", f"{latest_pressure} bar")
    col3.metric("Speed", f"{latest_speed} RPM")

    # ---------------- ALERT ----------------
    if status == "ALERT":
        st.error("⚠️ ALERT: High Temperature")
    else:
        st.success("✅ System Operating Normally")

    # ---------------- HISTORY ----------------
    st.subheader("📈 Machine Analytics")

    data_list = list(collection.find().sort("_id", -1).limit(10))

    temp_list = []
    pressure_list = []

    for item in reversed(data_list):
        temp_list.append(item["temperature"])
        pressure_list.append(item["pressure"])

    chart_data = pd.DataFrame({
        "Temperature": temp_list,
        "Pressure": pressure_list
    })

    st.line_chart(chart_data)

    # ---------------- TABLE ----------------
    st.subheader("📋 Recent Machine Logs")

    table_data = []

    for item in reversed(data_list):
        table_data.append({
            "Time": item["time"],
            "Temperature": item["temperature"],
            "Pressure": item["pressure"],
            "Speed": item["speed"]
        })

    st.dataframe(table_data)

else:
    st.warning("No machine data available yet.")
