import streamlit as st
import requests
import csv
from io import StringIO

st.title("🦠 COVID-19 India Case Study")

# Download CSV data
url = "https://data.covid19india.org/csv/latest/states.csv"
response = requests.get(url)

# Read CSV
csv_data = StringIO(response.text)
reader = csv.DictReader(csv_data)

data = list(reader)

# Get unique states
states = sorted(set(row["State"] for row in data))

selected_state = st.selectbox("Select State", states)

# Filter selected state data
state_data = [row for row in data if row["State"] == selected_state]

# Latest record
latest = state_data[-1]

st.header(f"COVID Report - {selected_state}")

st.metric("Confirmed", latest["Confirmed"])
st.metric("Recovered", latest["Recovered"])
st.metric("Deaths", latest["Deceased"])

# Recovery Rate
confirmed = int(latest["Confirmed"]) if latest["Confirmed"] else 0
recovered = int(latest["Recovered"]) if latest["Recovered"] else 0

if confirmed > 0:
    recovery_rate = (recovered / confirmed) * 100
else:
    recovery_rate = 0

st.write(f"### Recovery Rate: {recovery_rate:.2f}%")

# Table
st.subheader("Recent Records")

table_data = []

for row in state_data[-10:]:
    table_data.append({
        "Date": row["Date"],
        "Confirmed": row["Confirmed"],
        "Recovered": row["Recovered"],
        "Deaths": row["Deceased"]
    })

st.table(table_data)

# Chart Data
st.subheader("Confirmed Cases Trend")

confirmed_chart = {}

for row in state_data:
    confirmed_chart[row["Date"]] = int(row["Confirmed"])

st.line_chart(confirmed_chart)

# Case Study
st.subheader("Case Study Conclusion")

st.write(f"""
State: {selected_state}

Total Confirmed Cases: {latest['Confirmed']}

Total Recovered Cases: {latest['Recovered']}

Total Death Cases: {latest['Deceased']}

Recovery Rate: {recovery_rate:.2f}%

This case study analyzes the COVID-19 situation in the selected state using official data.
""")