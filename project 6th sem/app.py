import streamlit as st

st.title("Industry 4.0 Dashboard")

temperature = st.slider("Temperature", 20, 50, 25)
pressure = st.slider("Pressure", 1, 10, 3)

if temperature > 28:
    st.error("ALERT: High Temperature")
else:
    st.success("System Normal")

st.metric("Temperature", f"{temperature} °C")
st.metric("Pressure", f"{pressure} bar")
