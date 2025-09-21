import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os

st.set_page_config(page_title="US Fire Department Map", layout="wide")
st.title("🚒 US Fire Department & Station Map Dashboard")
st.markdown("""
Explore fire departments and stations across the US. Use the filters to focus on specific states or department types. Click on map markers for details!
""")

# Load data (prefer geocoded file)
def load_data():
    geocoded_file = "usfa-registry-station-geocoded.csv"
    base_file = "usfa-registry-station.csv"
    if os.path.exists(geocoded_file):
        df = pd.read_csv(geocoded_file)
    else:
        df = pd.read_csv(base_file)
    df.columns = df.columns.str.strip()
    return df

data = load_data()

# Check for lat/lon columns
lat_col = None
lon_col = None
for c in data.columns:
    if c.lower().replace(' ', '') in ['lat', 'latitude']:
        lat_col = c
    if c.lower().replace(' ', '') in ['lon', 'lng', 'long', 'longitude']:
        lon_col = c

if not lat_col or not lon_col:
    st.error("Latitude/Longitude columns not found! Please run the geocoding script and ensure your CSV has 'lat' and 'lon' columns.")
    st.write(f"Columns found: {list(data.columns)}")
    st.stop()

# Sidebar filters
states = sorted(data['Station State'].dropna().unique())
dept_types = sorted(data['Dept Type'].dropna().unique())

selected_states = st.sidebar.multiselect("Filter by State", states, default=states)
selected_types = st.sidebar.multiselect("Filter by Department Type", dept_types, default=dept_types)

filtered = data[data['Station State'].isin(selected_states) & data['Dept Type'].isin(selected_types)]

# Only use rows with valid lat/lon
filtered = filtered.dropna(subset=[lat_col, lon_col])

# Map
m = folium.Map(location=[39.8283, -98.5795], zoom_start=4, tiles='cartodbpositron')

for _, row in filtered.iterrows():
    popup = f"<b>{row['Fire Dept Name']}</b><br>{row['Station Name']}<br>{row['Station Addr1']}, {row['Station City']}, {row['Station State']} {row['Station Zip']}"
    folium.Marker(
        location=[row[lat_col], row[lon_col]],
        popup=popup,
        icon=folium.Icon(color='red', icon='fire', prefix='fa')
    ).add_to(m)

st_folium(m, width=1100, height=600)

# Stats
st.markdown("---")
st.subheader("Summary Statistics")
st.write(f"**Total Stations Displayed:** {len(filtered)}")
st.write(f"**Unique Departments:** {filtered['Fire Dept Name'].nunique()}")
st.write(f"**States Covered:** {filtered['Station State'].nunique()}")
