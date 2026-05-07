import streamlit as st
from pymongo import MongoClient
from datetime import datetime
import time

# MongoDB Connection
MONGO_URI = "YOUR_MONGODB_CONNECTION_STRING"

client = MongoClient(MONGO_URI)
db = client["industry_db"]
collection = db["machine_data"]

st.set_page_config(page_title="Industry 4.0 Dashboard", layout="wide")

st.title("🏭 Knowledge Integrated Real-Time Intelligence")

tab1, tab2 = st.tabs(["Control Panel", "Monitoring Dashboard"])

# ---------------- CONTROL PANEL ----------------
with tab1:
    st.header("🛠️ Machine Control Panel")

    temperature = st.slider("Temperature (°C)", 20, 50, 25)
    pressure = st.slider("Pressure (bar)", 1, 10, 3)

    if st.button("Send Data"):
        data = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "temperature": temperature,
            "pressure": pressure
        }

        collection.insert_one(data)

        st.success("Data Updated Successfully")

# ---------------- DASHBOARD ----------------
with tab2:
    st.header("📊 Real-Time Monitoring Dashboard")

    TEMP_LIMIT = 28

    placeholder = st.empty()

    while True:
        latest = collection.find_one(sort=[("_id", -1)])

        if latest:
            temp = latest["temperature"]
            pressure = latest["pressure"]
            current_time = latest["time"]

            status = "ALERT" if temp > TEMP_LIMIT else "NORMAL"

            with placeholder.container():
                col1, col2 = st.columns(2)

                col1.metric("Temperature", f"{temp} °C")
                col2.metric("Pressure", f"{pressure} bar")

                st.write("Last Update:", current_time)

                if status == "ALERT":
                    st.error("⚠️ ALERT: High Temperature")
                else:
                    st.success("✅ System Normal")

        time.sleep(1)