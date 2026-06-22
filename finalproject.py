import streamlit as st
import requests
import csv
import json
from io import StringIO
import streamlit.components.v1 as components

st.set_page_config(
    page_title="COVID-19 India Dashboard",
    layout="wide"
)

st.title("🦠 COVID-19 India Case Study")

url = "https://data.covid19india.org/csv/latest/states.csv"

response = requests.get(url)

csv_data = StringIO(response.text)

reader = csv.DictReader(csv_data)

data = list(reader)

states = sorted(set(row["State"] for row in data))

selected_state = st.selectbox(
    "Select State",
    states
)

state_data = [
    row for row in data
    if row["State"] == selected_state
]

latest = state_data[-1]

st.header(f"COVID Report - {selected_state}")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Confirmed", latest["Confirmed"])

with col2:
    st.metric("Recovered", latest["Recovered"])

with col3:
    st.metric("Deaths", latest["Deceased"])

confirmed = int(latest["Confirmed"]) if latest["Confirmed"] else 0
recovered = int(latest["Recovered"]) if latest["Recovered"] else 0

recovery_rate = (
    (recovered / confirmed) * 100
    if confirmed > 0
    else 0
)

st.write(f"### Recovery Rate: {recovery_rate:.2f}%")

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

st.subheader("Confirmed Cases Trend")

chart_data = {}

for row in state_data:
    chart_data[row["Date"]] = int(row["Confirmed"])

st.line_chart(chart_data)

# Globe Data

state_coordinates = {
    "Gujarat":[23.0225,72.5714],
    "Maharashtra":[19.0760,72.8777],
    "Delhi":[28.6139,77.2090],
    "Rajasthan":[26.9124,75.7873],
    "Karnataka":[12.9716,77.5946],
    "Tamil Nadu":[13.0827,80.2707],
    "Punjab":[30.7333,76.7794],
    "West Bengal":[22.5726,88.3639],
    "Uttar Pradesh":[26.8467,80.9462],
    "Madhya Pradesh":[23.2599,77.4126]
}

globe_points = []

for state, coords in state_coordinates.items():

    matching = [
        row for row in data
        if row["State"] == state
    ]

    if matching:

        latest_row = matching[-1]

        globe_points.append({
            "name": state,
            "lat": coords[0],
            "lng": coords[1],
            "cases": int(latest_row["Confirmed"])
        })

with open("templates/globe.html","r",encoding="utf-8") as file:
    html_template = file.read()

html_template = html_template.replace(
    "__POINTS__",
    json.dumps(globe_points)
)

st.subheader("🌍 Interactive COVID Globe")

components.html(
    html_template,
    height=700
)

st.subheader("Case Study Conclusion")

st.write(f'''
State: {selected_state}

Total Confirmed Cases: {latest["Confirmed"]}

Total Recovered Cases: {latest["Recovered"]}

Total Death Cases: {latest["Deceased"]}

Recovery Rate: {recovery_rate:.2f}%
''')

