import streamlit as st
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ---------------- AUTO REFRESH ----------------
st_autorefresh(interval=3000, key="refresh")

# ---------------- MONGODB ----------------
MONGO_URI = st.secrets["MONGO_URI"]

client = MongoClient(MONGO_URI)

db = client["industry_db"]
collection = db["machine_logs"]

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Industry 4.0 Control Center",
    layout="wide"
)

# ---------------- TITLE ----------------
st.title("🏭 Knowledge Integrated Real-Time Intelligence")
st.subheader("Industry 4.0 Real-Time Monitoring System")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Machine Control Panel")

machine = st.sidebar.selectbox(
    "Select Machine",
    ["Machine A", "Machine B", "Machine C"]
)

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

# ---------------- CHECK LAST ENTRY ----------------
latest_data = collection.find_one(
    {"machine": machine},
    sort=[("_id", -1)]
)

# ---------------- AUTO SAVE ONLY IF VALUES CHANGE ----------------
if (
    latest_data is None
    or latest_data["temperature"] != temperature
    or latest_data["pressure"] != pressure
    or latest_data["speed"] != speed
):

    data = {
        "machine": machine,
        "time": datetime.now().strftime("%H:%M:%S"),
        "temperature": temperature,
        "pressure": pressure,
        "speed": speed
    }

    collection.insert_one(data)

# ---------------- FETCH LATEST DATA ----------------
latest = collection.find_one(
    {"machine": machine},
    sort=[("_id", -1)]
)

if latest:

    latest_temp = latest["temperature"]
    latest_pressure = latest["pressure"]
    latest_speed = latest["speed"]

    # ---------------- STATUS ----------------
    if latest_temp > 40:
        status = "CRITICAL"

    elif latest_temp > 32:
        status = "WARNING"

    else:
        status = "NORMAL"

    # ---------------- METRICS ----------------
    col1, col2, col3 = st.columns(3)

    col1.metric("🌡️ Temperature", f"{latest_temp} °C")
    col2.metric("⚙️ Pressure", f"{latest_pressure} bar")
    col3.metric("🔄 Speed", f"{latest_speed} RPM")

    # ---------------- ALERTS ----------------
    if status == "CRITICAL":
        st.error("🚨 CRITICAL ALERT: Machine Overheating")

    elif status == "WARNING":
        st.warning("⚠️ WARNING: Temperature Rising")

    else:
        st.success("✅ System Operating Normally")

    # ---------------- ANALYTICS ----------------
    st.subheader("📈 Machine Analytics")

    data_list = list(
        collection.find({"machine": machine})
        .sort("_id", -1)
        .limit(10)
    )

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

    # ---------------- MACHINE LOGS ----------------
    st.subheader("📋 Machine Logs")

    table_data = []

    for item in reversed(data_list):

        table_data.append({
            "Machine": item["machine"],
            "Time": item["time"],
            "Temperature": item["temperature"],
            "Pressure": item["pressure"],
            "Speed": item["speed"]
        })

    st.dataframe(table_data)

else:
    st.warning("No machine data available.")
