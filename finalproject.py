import streamlit as st
import requests
import csv
from io import StringIO
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="COVID-19 India Dashboard", layout="wide")

st.title("🦠 COVID-19 India Case Study Dashboard")

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

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Confirmed", latest["Confirmed"])

with col2:
    st.metric("Recovered", latest["Recovered"])

with col3:
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

# Line Chart
st.subheader("Confirmed Cases Trend")

confirmed_chart = {}

for row in state_data:
    confirmed_chart[row["Date"]] = int(row["Confirmed"])

st.line_chart(confirmed_chart)

# -----------------------------
# 3D Globe Section
# -----------------------------

st.subheader("🌍 Interactive COVID Globe")

# State Coordinates
state_coordinates = {
    "Gujarat": [23.0225, 72.5714],
    "Maharashtra": [19.0760, 72.8777],
    "Delhi": [28.6139, 77.2090],
    "Rajasthan": [26.9124, 75.7873],
    "Karnataka": [12.9716, 77.5946],
    "Tamil Nadu": [13.0827, 80.2707],
    "Punjab": [30.7333, 76.7794],
    "West Bengal": [22.5726, 88.3639],
    "Uttar Pradesh": [26.8467, 80.9462],
    "Madhya Pradesh": [23.2599, 77.4126]
}

globe_data = []

for state, coords in state_coordinates.items():

    matching = [row for row in data if row["State"] == state]

    if matching:
        latest_row = matching[-1]

        try:
            cases = int(latest_row["Confirmed"])
        except:
            cases = 0

        globe_data.append({
            "State": state,
            "lat": coords[0],
            "lon": coords[1],
            "Cases": cases,
            "radius": max(cases / 50000, 10000)
        })

df = pd.DataFrame(globe_data)

layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position=["lon", "lat"],
    get_radius="radius",
    pickable=True,
    auto_highlight=True,
    stroked=True,
    filled=True
)

view_state = pdk.ViewState(
    latitude=22.5,
    longitude=78.9,
    zoom=3.8,
    pitch=45
)

deck = pdk.Deck(
    map_style="mapbox://styles/mapbox/dark-v10",
    initial_view_state=view_state,
    layers=[layer],
    tooltip={
        "html": """
        <b>{State}</b><br/>
        Confirmed Cases: {Cases}
        """,
        "style": {
            "backgroundColor": "black",
            "color": "white"
        }
    }
)

st.pydeck_chart(deck)

# -----------------------------
# Case Study
# -----------------------------

st.subheader("Case Study Conclusion")

st.write(f"""
**State:** {selected_state}

**Total Confirmed Cases:** {latest['Confirmed']}

**Total Recovered Cases:** {latest['Recovered']}

**Total Death Cases:** {latest['Deceased']}

**Recovery Rate:** {recovery_rate:.2f}%

This case study analyzes COVID-19 data for the selected state using official records. The interactive globe displays COVID case distribution across major Indian states. Hover over a bubble to view state information and confirmed case counts.
""")