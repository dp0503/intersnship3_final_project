
import streamlit as st
import requests
import csv
from io import StringIO
import streamlit.components.v1 as components
import json

st.set_page_config(
    page_title="COVID-19 India Dashboard",
    layout="wide"
)

st.title("🦠 COVID-19 India Case Study Dashboard")

# Fetch Data
url = "https://data.covid19india.org/csv/latest/states.csv"

try:
    response = requests.get(url)
    response.raise_for_status()

    csv_data = StringIO(response.text)
    reader = csv.DictReader(csv_data)
    data = list(reader)

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# State Selection
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

# Metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Confirmed Cases",
        latest["Confirmed"]
    )

with col2:
    st.metric(
        "Recovered Cases",
        latest["Recovered"]
    )

with col3:
    st.metric(
        "Death Cases",
        latest["Deceased"]
    )

# Recovery Rate
confirmed = int(latest["Confirmed"]) if latest["Confirmed"] else 0
recovered = int(latest["Recovered"]) if latest["Recovered"] else 0

recovery_rate = (
    (recovered / confirmed) * 100
    if confirmed > 0
    else 0
)

st.success(
    f"Recovery Rate: {recovery_rate:.2f}%"
)

# Recent Records Table
st.subheader("📋 Recent Records")

table_data = []

for row in state_data[-10:]:
    table_data.append({
        "Date": row["Date"],
        "Confirmed": row["Confirmed"],
        "Recovered": row["Recovered"],
        "Deaths": row["Deceased"]
    })

st.table(table_data)

# Trend Chart
st.subheader("📈 Confirmed Cases Trend")

chart_data = {}

for row in state_data:
    try:
        chart_data[row["Date"]] = int(row["Confirmed"])
    except:
        pass

st.line_chart(chart_data)

# ---------------------------
# 3D Globe Section
# ---------------------------

st.subheader("🌍 Interactive 3D COVID Globe")

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

    matching = [
        row for row in data
        if row["State"] == state
    ]

    if matching:

        latest_row = matching[-1]

        try:
            cases = int(latest_row["Confirmed"])
        except:
            cases = 0

        globe_data.append({
            "name": state,
            "lat": coords[0],
            "lng": coords[1],
            "cases": cases,
            "size": max(cases / 1000000, 0.5)
        })

points_json = json.dumps(globe_data)

globe_html = f"""
<!DOCTYPE html>
<html>
<head>

<script src="https://unpkg.com/globe.gl"></script>

<style>

body {{
    margin: 0;
    background: transparent;
}}

#globeViz {{
    width: 100%;
    height: 750px;
}}

</style>

</head>

<body>

<div id="globeViz"></div>

<script>

const points = {points_json};

const globe = Globe()
(document.getElementById('globeViz'))

.globeImageUrl(
'https://unpkg.com/three-globe/example/img/earth-blue-marble.jpg'
)

.bumpImageUrl(
'https://unpkg.com/three-globe/example/img/earth-topology.png'
)

.backgroundImageUrl(
'https://unpkg.com/three-globe/example/img/night-sky.png'
)

.pointsData(points)

.pointAltitude(0.18)

.pointRadius('size')

.pointColor(() => '#ff4444')

.pointLabel(d => `
<div style="
padding:12px;
background:white;
color:black;
border-radius:10px;
font-family:Arial;
font-size:14px;
">
<b>${{d.name}}</b><br>
Confirmed Cases: ${{d.cases.toLocaleString()}}
</div>
`)

.animateIn(true);

globe.controls().autoRotate = true;
globe.controls().autoRotateSpeed = 0.4;

globe.pointOfView(
{{
lat: 22,
lng: 78,
altitude: 2.5
}},
3000
);

</script>

</body>
</html>
"""

components.html(
    globe_html,
    height=750
)

# ---------------------------
# Case Study Conclusion
# ---------------------------

st.subheader("📝 Case Study Conclusion")

st.write(f"""
**State:** {selected_state}

**Total Confirmed Cases:** {latest['Confirmed']}

**Total Recovered Cases:** {latest['Recovered']}

**Total Death Cases:** {latest['Deceased']}

**Recovery Rate:** {recovery_rate:.2f}%

This dashboard analyzes COVID-19 data using official India COVID records.
The interactive 3D globe visualizes COVID case distribution across major states of India.
Hover over any marker on the globe to see state information and confirmed case counts.
""")
