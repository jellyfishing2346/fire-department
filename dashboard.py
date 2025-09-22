import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import numpy as np
import random
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import time
import json

st.markdown("""
    <style>
    /* Improve table readability in light mode */
    .stDataFrame, .stTable, .stMarkdown table {
        color: #222 !important;
        background: #fff !important;
        border-radius: 6px;
        border: 1px solid #ddd !important;
    }
    .stDataFrame th, .stDataFrame td,
    .stTable th, .stTable td,
    .stMarkdown table th, .stMarkdown table td {
        color: #222 !important;
        background: #fff !important;
        border: 1px solid #ddd !important;
        padding: 8px 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Set page config to match NERIS style
st.set_page_config(
    page_title="NERIS Department Dashboard", 
    layout="wide", 
    page_icon="🗺️",
    initial_sidebar_state="expanded"
)

# Initialize session state for real-time features
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()
if 'selected_department' not in st.session_state:
    st.session_state.selected_department = None
if 'verification_queue' not in st.session_state:
    st.session_state.verification_queue = []
if 'recent_activity' not in st.session_state:
    st.session_state.recent_activity = []

# Theme selection in sidebar (Priority 1: Dark/Light Mode)
with st.sidebar:
    st.markdown("### 🎨 Display Settings")
    theme = st.selectbox("Theme", ["Light Mode", "Dark Mode"], key="theme_selector")

# Dynamic CSS based on theme selection
def get_theme_css(theme):
    if theme == "Dark Mode":
        return """
        <style>
            /* Dark theme styling */
            .main {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            
            .stApp {
                background-color: #121212;
            }
            
            .neris-header {
                background-color: #2d2d2d;
                padding: 1rem;
                border-bottom: 1px solid #404040;
                margin-bottom: 0.5rem;
                color: #ffffff;
            }
            
            .stat-card {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                border-radius: 8px;
                padding: 1rem;
                margin: 0.5rem 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.3);
                color: #ffffff;
            }
            
            .department-table {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                border-radius: 8px;
                margin-top: 1rem;
                color: #ffffff;
            }
            
            .activity-feed {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                border-radius: 8px;
                padding: 1rem;
                margin: 0.5rem 0;
                max-height: 200px;
                overflow-y: auto;
            }
            
            .verification-panel {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                border-radius: 8px;
                padding: 1rem;
                margin: 0.5rem 0;
            }
            
            .map-container {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                border-radius: 8px;
                padding: 0.5rem;
            }
            
            .activity-item {
                padding: 0.5rem;
                border-bottom: 1px solid #404040;
                color: #ffffff;
            }
            
            .css-1d391kg {
                background-color: #2d2d2d;
                border-right: 1px solid #404040;
            }
            
            /* Override Streamlit default dark colors */
            .stSelectbox > div > div {
                background-color: #2d2d2d;
                border: 1px solid #404040;
            }
            
            .stTextInput > div > div > input {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                color: #ffffff;
            }
        </style>
        """
    else:  # Light Mode
        return """
        <style>
            /* Light theme styling */
            .main {
                background-color: #ffffff;
                color: #333333;
            }
            
            .stApp {
                background-color: #f8f9fa;
            }
            
            .neris-header {
                background-color: #ffffff;
                padding: 1rem;
                border-bottom: 1px solid #e0e0e0;
                margin-bottom: 0.5rem;
            }
            
            .stat-card {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 1rem;
                margin: 0.5rem 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .department-table {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 1rem;
            }
            
            .activity-feed {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 1rem;
                margin: 0.5rem 0;
                max-height: 200px;
                overflow-y: auto;
            }
            
            .verification-panel {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 1rem;
                margin: 0.5rem 0;
            }
            
            .map-container {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 0.5rem;
            }
            
            .activity-item {
                padding: 0.5rem;
                border-bottom: 1px solid #f0f0f0;
            }
            
            .css-1d391kg {
                background-color: #ffffff;
                border-right: 1px solid #e0e0e0;
            }
        </style>
        """

# Apply theme CSS
st.markdown(get_theme_css(theme), unsafe_allow_html=True)

# Additional shared styling
st.markdown("""
<style>
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        margin: 0;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #666;
        margin: 0;
    }
    
    .verified { color: #1976d2; }
    .unverified { color: #f57c00; }
    .inactive { color: #757575; }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .real-time-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        background-color: #4caf50;
        border-radius: 50%;
        margin-right: 0.5rem;
        animation: pulse 2s infinite;
    }
</style>
""", unsafe_allow_html=True)

# --- Simulated Data Size Control ---
# NOTE: This slider only affects simulated data for demo/testing. Real CSV data is never lost or affected.
with st.sidebar:
    st.markdown('---')
    st.markdown('### ⚙️ Simulation Settings')
    num_simulated_departments = st.slider(
        'Number of Simulated Departments',
        min_value=50, max_value=500, value=100, step=10,
        help='Affects only simulated data for demo/testing. Real CSV data is never lost.'
    )

# Generate realistic department data with enhanced features
@st.cache_data
# Accept num_departments as parameter

def generate_enhanced_neris_data(num_departments=100):
    """Generate department data with verification workflow features. Only affects simulated/demo data."""
    regions = [
        {"state": "NY", "city": "New York", "lat": 40.7128, "lon": -74.0060, "density": "high"},
        {"state": "NY", "city": "Buffalo", "lat": 42.8864, "lon": -78.8784, "density": "medium"},
        {"state": "PA", "city": "Philadelphia", "lat": 39.9526, "lon": -75.1652, "density": "high"},
        {"state": "MA", "city": "Boston", "lat": 42.3601, "lon": -71.0589, "density": "high"},
        {"state": "FL", "city": "Miami", "lat": 25.7617, "lon": -80.1918, "density": "high"},
        {"state": "GA", "city": "Atlanta", "lat": 33.7490, "lon": -84.3880, "density": "high"},
        {"state": "TX", "city": "Houston", "lat": 29.7604, "lon": -95.3698, "density": "high"},
        {"state": "TX", "city": "Dallas", "lat": 32.7767, "lon": -96.7970, "density": "high"},
        {"state": "IL", "city": "Chicago", "lat": 41.8781, "lon": -87.6298, "density": "high"},
        {"state": "OH", "city": "Columbus", "lat": 39.9612, "lon": -82.9988, "density": "medium"},
        {"state": "CA", "city": "Los Angeles", "lat": 34.0522, "lon": -118.2437, "density": "high"},
        {"state": "CA", "city": "San Francisco", "lat": 37.7749, "lon": -122.4194, "density": "high"},
        {"state": "WA", "city": "Seattle", "lat": 47.6062, "lon": -122.3321, "density": "medium"},
        {"state": "CO", "city": "Denver", "lat": 39.7392, "lon": -104.9903, "density": "medium"},
    ]
    
    data = []
    dept_id = 1
    region_cycle = iter(regions * ((num_departments // len(regions)) + 1))
    while len(data) < num_departments:
        region = next(region_cycle)
        if region["density"] == "high":
            num_depts = 1
        elif region["density"] == "medium":
            num_depts = 1
        else:
            num_depts = 1
        for i in range(num_depts):
            if len(data) >= num_departments:
                break
            state_code = f"{random.randint(1, 50):02d}"
            county_code = f"{random.randint(1, 99):03d}"
            dept_code = f"{dept_id:03d}"
            fdid = f"FD{state_code}{county_code}{dept_code}"
            
            # Status distribution
            status_weights = [0.60, 0.30, 0.10]
            onboarding_status = np.random.choice(["CONFIRMED", "UNVERIFIED", "INACTIVE"], p=status_weights)
            
            # Enhanced department data
            dept_types = ["Fire Department", "Fire District", "Volunteer Fire Co.", "Emergency Services"]
            if i == 0:
                dept_name = f"{region['city']} {random.choice(dept_types)}"
            else:
                dept_name = f"{region['city']} {random.choice(['Engine', 'Rescue', 'Ladder', 'Station'])} Co. {i+1}"
            
            # Enhanced fields for workflows
            if onboarding_status == "CONFIRMED":
                incident_count = random.randint(500, 5000)
                user_count = random.randint(5, 25)
                data_quality = random.randint(85, 100)
                api_status = random.choice(["Connected", "Connected", "Pending"])
                verification_score = random.randint(90, 100)
            elif onboarding_status == "UNVERIFIED":
                incident_count = random.randint(100, 1000)
                user_count = random.randint(1, 10)
                data_quality = random.randint(40, 84)
                api_status = random.choice(["Pending", "Failed", "Not Configured"])
                verification_score = random.randint(30, 70)
            else:  # INACTIVE
                incident_count = random.randint(0, 100)
                user_count = random.randint(0, 2)
                data_quality = random.randint(0, 40)
                api_status = "Not Configured"
                verification_score = random.randint(0, 30)
            
            lat_offset = random.uniform(-0.5, 0.5)
            lon_offset = random.uniform(-0.5, 0.5)
            
            data.append({
                "Department_ID": fdid,
                "Department_Name": dept_name,
                "State": region["state"],
                "City": region["city"],
                "Onboarding_Status": onboarding_status,
                "Incident_Count": incident_count,
                "User_Count": user_count,
                "Latitude": region["lat"] + lat_offset,
                "Longitude": region["lon"] + lon_offset,
                "Last_Updated": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
                "Data_Quality_Score": data_quality,
                "API_Status": api_status,
                "Verification_Score": verification_score,
                "Contact_Verified": onboarding_status == "CONFIRMED",
                "Chief_Name": f"Chief {random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Davis', 'Miller'])}",
                "Phone": f"({random.randint(200,999)}) {random.randint(200,999)}-{random.randint(1000,9999)}",
                "Email": f"chief@{dept_name.replace(' ', '').replace('.', '').lower()[:15]}.org"
            })
            dept_id += 1
    
    return pd.DataFrame(data)

# Load data with user-selected department count
@st.cache_data

def load_data(num_departments=100):
    return generate_enhanced_neris_data(num_departments)

data = load_data(num_simulated_departments)

# Priority 2: Real-time activity simulation
def simulate_real_time_activity():
    """Simulate real-time department onboarding activity"""
    current_time = datetime.now()
    
    # Simulate new activity every 30 seconds
    if (current_time - st.session_state.last_update).seconds > 30:
        # Random department activity
        dept = data.sample(1).iloc[0]
        
        activities = [
            f"📋 {dept['Department_Name']} updated contact information",
            f"✅ {dept['Department_Name']} completed API integration",
            f"🔄 {dept['Department_Name']} verification in progress",
            f"📊 {dept['Department_Name']} submitted monthly report",
            f"🆕 New department registered: {dept['Department_Name']}"
        ]
        
        new_activity = {
            "time": current_time.strftime("%H:%M:%S"),
            "activity": random.choice(activities),
            "department": dept['Department_Name'],
            "status": dept['Onboarding_Status']
        }
        
        st.session_state.recent_activity.insert(0, new_activity)
        
        # Keep only last 10 activities
        if len(st.session_state.recent_activity) > 10:
            st.session_state.recent_activity = st.session_state.recent_activity[:10]
        
        st.session_state.last_update = current_time

# Run real-time simulation
simulate_real_time_activity()

# Header section with real-time indicator
header_text_color = '#1a1a1a' if theme == 'Light Mode' else '#fff'
header_bg_color = '#fff' if theme == 'Light Mode' else '#2d2d2d'
header_border_color = '#e0e0e0' if theme == 'Light Mode' else '#404040'

st.markdown(f"""
<div class="neris-header" style="background: {header_bg_color}; border-bottom: 2px solid {header_border_color}; padding: 1.2rem 1rem 1rem 1rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
    <h2 style="margin: 0; color: {header_text_color}; font-weight: 900; font-size: 2.2rem; letter-spacing: -1px;">
        <span class="real-time-indicator"></span>
        <span style='vertical-align: middle;'>🗺️ Fire Department Onboarding Dashboard</span>
    </h2>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.92; color: {header_text_color}; font-weight: 600; font-size: 1.1rem; letter-spacing: 0.01em;">
        National Emergency Response Information System (NERIS) | Live Dashboard
    </p>
</div>
""", unsafe_allow_html=True)

# Calculate enhanced statistics
verified_count = len(data[data['Onboarding_Status'] == 'CONFIRMED'])
unverified_count = len(data[data['Onboarding_Status'] == 'UNVERIFIED'])
inactive_count = len(data[data['Onboarding_Status'] == 'INACTIVE'])
total_incidents = data['Incident_Count'].sum()
avg_data_quality = data['Data_Quality_Score'].mean()
api_connected = len(data[data['API_Status'] == 'Connected'])

# Enhanced sidebar with real-time features
with st.sidebar:
    st.markdown("### 📊 Departments Reporting")
    st.markdown("**Departments**")
    
    # Statistics cards with enhanced metrics
    st.markdown(f"""
    <div class="stat-card">
        <p class="stat-number verified">{verified_count:,}</p>
        <p class="stat-label">Verified Departments</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="stat-card">
        <p class="stat-number unverified">{unverified_count:,}</p>
        <p class="stat-label">Unverified Departments</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="stat-card">
        <p class="stat-number inactive">{inactive_count:,}</p>
        <p class="stat-label">Inactive Departments</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced metrics
    st.markdown("---")
    st.markdown("### 📈 System Health")
    
    st.markdown(f"""
    <div class="stat-card">
        <p class="stat-number" style="color: #4caf50;">{api_connected:,}</p>
        <p class="stat-label">API Connections</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="stat-card">
        <p class="stat-number" style="color: #2196f3;">{avg_data_quality:.1f}%</p>
        <p class="stat-label">Avg Data Quality</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Real-time activity feed
    st.markdown("---")
    st.markdown("### 🔴 Live Activity")
    
    if st.session_state.recent_activity:
        activity_html = '<div class="activity-feed">'
        for activity in st.session_state.recent_activity[:5]:
            activity_html += f"""
            <div class="activity-item">
                <small style="opacity: 0.7;">{activity['time']}</small><br>
                {activity['activity']}
            </div>
            """
        activity_html += '</div>'
        st.markdown(activity_html, unsafe_allow_html=True)
    else:
        st.markdown('<div class="activity-feed"><p>No recent activity</p></div>', unsafe_allow_html=True)
    
    # Auto-refresh toggle (now off by default)
    auto_refresh = st.checkbox("🔄 Auto-refresh", value=False)
    if auto_refresh:
        time.sleep(1)
        st.rerun()

# Main content layout
col1, col2 = st.columns([3, 1])

with col1:
    # Enhanced map with department details
    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    
    m = folium.Map(
        location=[39.8283, -98.5795],
        zoom_start=4,
        tiles='cartodb positron' if theme == "Light Mode" else 'cartodb dark_matter'
    )
    
    # Color mapping
    color_map = {
        "CONFIRMED": "#1976d2",
        "UNVERIFIED": "#f57c00",
        "INACTIVE": "#757575"
    }
    
    # Enhanced markers with more details
    for _, dept in data.iterrows():
        popup_content = f"""
        <div style="width: 300px; font-family: Arial;">
            <h4 style="margin: 0 0 0.5rem 0; color: #333;">{dept['Department_Name']}</h4>
            <p style="margin: 0.2rem 0;"><strong>Department ID:</strong> {dept['Department_ID']}</p>
            <p style="margin: 0.2rem 0;"><strong>Status:</strong> 
                <span style="padding: 2px 6px; border-radius: 4px; background-color: {color_map[dept['Onboarding_Status']]}; color: white; font-size: 0.8rem;">
                    {dept['Onboarding_Status']}
                </span>
            </p>
            <p style="margin: 0.2rem 0;"><strong>Chief:</strong> {dept['Chief_Name']}</p>
            <p style="margin: 0.2rem 0;"><strong>Data Quality:</strong> {dept['Data_Quality_Score']}%</p>
            <p style="margin: 0.2rem 0;"><strong>API Status:</strong> {dept['API_Status']}</p>
            <p style="margin: 0.2rem 0;"><strong>Incidents:</strong> {dept['Incident_Count']:,}</p>
            <p style="margin: 0.2rem 0;"><strong>Users:</strong> {dept['User_Count']}</p>
            <hr style="margin: 0.5rem 0;">
            <small>Click for detailed view</small>
        </div>
        """
        
        folium.CircleMarker(
            location=[dept['Latitude'], dept['Longitude']],
            radius=6 if dept['Onboarding_Status'] == 'CONFIRMED' else 4,
            popup=folium.Popup(popup_content, max_width=350),
            tooltip=f"{dept['Department_Name']} - {dept['Onboarding_Status']}",
            color='white',
            weight=2,
            fillColor=color_map[dept['Onboarding_Status']],
            fillOpacity=0.8
        ).add_to(m)
    
    # Display enhanced map
    map_data = st_folium(m, width=800, height=500, returned_objects=["last_object_clicked"])
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Enhanced layers panel
    if theme == "Light Mode":
        st.markdown('<span class="neris-section-header">🎛️ LAYERS</span>', unsafe_allow_html=True)
    else:
        st.markdown('### 🎛️ LAYERS')
    show_verified = st.checkbox("🔵 Verified Departments", value=True)
    show_unverified = st.checkbox("🟠 Unverified Departments", value=True)  
    show_inactive = st.checkbox("⚫ Inactive", value=True)
    if theme == "Light Mode":
        st.markdown('<span class="neris-label">Basemap</span>', unsafe_allow_html=True)
    st.checkbox("🗺️ Basemap", value=True)
    
    # Enhanced filters
    if theme == "Light Mode":
        st.markdown('<span class="neris-section-header">🔍 FILTERS</span>', unsafe_allow_html=True)
    else:
        st.markdown('### 🔍 FILTERS')
    selected_states = st.multiselect(
        "States" if theme != "Light Mode" else "",
        options=sorted(data['State'].unique()),
        default=[]
    )
    if theme == "Light Mode":
        st.markdown('<span class="neris-label">Min Data Quality %</span>', unsafe_allow_html=True)
    min_data_quality = st.slider("Min Data Quality %" if theme != "Light Mode" else "", 0, 100, 0)
    if theme == "Light Mode":
        st.markdown('<span class="neris-label">API Status</span>', unsafe_allow_html=True)
    api_status_filter = st.multiselect(
        "API Status" if theme != "Light Mode" else "",
        options=data['API_Status'].unique(),
        default=[]
    )
    
    # Priority 4: Verification workflow panel
    st.markdown("---")
    if theme == "Light Mode":
        st.markdown('<span class="neris-section-header">⚡ Quick Actions</span>', unsafe_allow_html=True)
    else:
        st.markdown('### ⚡ Quick Actions')
    
    st.markdown('<div class="verification-panel">', unsafe_allow_html=True)
    
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    if st.button("📊 Export Report", use_container_width=True):
        csv = data.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"neris_departments_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    # Bulk verification tools
    st.markdown("<span style='font-weight: 700; font-size: 1.1rem; color: #1a1a1a; background: #f3f6fa; border-radius: 6px; padding: 4px 12px; display: inline-block; margin-bottom: 0.5rem;'>Bulk Operations</span>", unsafe_allow_html=True)
    if st.button("✅ Verify Selected", use_container_width=True):
        st.success("Batch verification initiated!")
    if st.button("📧 Send Reminders", use_container_width=True):
        st.info("Reminder emails sent to unverified departments!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Apply filters
filtered_data = data.copy()

if not show_verified:
    filtered_data = filtered_data[filtered_data['Onboarding_Status'] != 'CONFIRMED']
if not show_unverified:
    filtered_data = filtered_data[filtered_data['Onboarding_Status'] != 'UNVERIFIED']
if not show_inactive:
    filtered_data = filtered_data[filtered_data['Onboarding_Status'] != 'INACTIVE']

if selected_states:
    filtered_data = filtered_data[filtered_data['State'].isin(selected_states)]

if min_data_quality > 0:
    filtered_data = filtered_data[filtered_data['Data_Quality_Score'] >= min_data_quality]

if api_status_filter:
    filtered_data = filtered_data[filtered_data['API_Status'].isin(api_status_filter)]

# Priority 3: Department detail drill-down
if map_data['last_object_clicked']:
    clicked_lat = map_data['last_object_clicked']['lat']
    clicked_lon = map_data['last_object_clicked']['lng']
    
    # Find closest department
    tolerance = 0.1
    closest_dept = data[
        (abs(data['Latitude'] - clicked_lat) < tolerance) & 
        (abs(data['Longitude'] - clicked_lon) < tolerance)
    ]
    
    if not closest_dept.empty:
        dept = closest_dept.iloc[0]
        st.session_state.selected_department = dept

# Department detail view
if st.session_state.selected_department is not None:
    dept = st.session_state.selected_department
    
    st.markdown("---")
    st.markdown("### 🔍 Department Details")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        **{dept['Department_Name']}**  
        ID: {dept['Department_ID']}  
        Status: {dept['Onboarding_Status']}  
        """)
    
    with col2:
        st.markdown(f"""
        **Contact Information**  
        Chief: {dept['Chief_Name']}  
        Phone: {dept['Phone']}  
        Email: {dept['Email']}  
        """)
    
    with col3:
        st.markdown(f"""
        **System Status**  
        Data Quality: {dept['Data_Quality_Score']}%  
        API Status: {dept['API_Status']}  
        Verification Score: {dept['Verification_Score']}/100  
        """)

# Enhanced department status table
st.markdown("---")
if theme == "Light Mode":
    st.markdown('<span class="neris-section-header">📋 Department Status</span>', unsafe_allow_html=True)
else:
    st.markdown('### 📋 Department Status')

# Table controls
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    rows_per_page = st.selectbox("Rows per page:", [10, 25, 50, 100], index=0)
with col3:
    search_term = st.text_input("🔍 Search departments:", "")

# Apply search filter
if search_term:
    filtered_data = filtered_data[
        filtered_data['Department_Name'].str.contains(search_term, case=False, na=False) |
        filtered_data['Department_ID'].str.contains(search_term, case=False, na=False)
    ]

# Enhanced pagination
total_rows = len(filtered_data)
total_pages = (total_rows - 1) // rows_per_page + 1 if total_rows > 0 else 1

if 'page_number' not in st.session_state:
    st.session_state.page_number = 1

col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])

with col1:
    if st.button("⬅️ Previous") and st.session_state.page_number > 1:
        st.session_state.page_number -= 1

with col5:
    if st.button("Next ➡️") and st.session_state.page_number < total_pages:
        st.session_state.page_number += 1

with col3:
    st.write(f"Page {st.session_state.page_number} of {total_pages} ({total_rows:,} total departments)")

# Display enhanced table
start_idx = (st.session_state.page_number - 1) * rows_per_page
end_idx = start_idx + rows_per_page
page_data = filtered_data.iloc[start_idx:end_idx]

# Enhanced table with more columns
table_data = page_data[[
    'Department_ID', 'Department_Name', 'State', 'Onboarding_Status', 
    'Data_Quality_Score', 'API_Status', 'Incident_Count', 'User_Count'
]].copy()

table_data.columns = [
    'Department ID', 'Department Name', 'State', 'Status', 
    'Data Quality %', 'API Status', 'Incidents', 'Users'
]

# Show a note and use st.table in light mode for better readability
if theme == "Light Mode":
    st.markdown('<div class="neris-info">For best readability, try Dark Mode. Table below uses enhanced contrast.</div>', unsafe_allow_html=True)
    st.table(table_data)
else:
    st.dataframe(
        table_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Status": st.column_config.TextColumn(width="medium"),
            "Data Quality %": st.column_config.NumberColumn(format="%d%%"),
            "Incidents": st.column_config.NumberColumn(format="%d"),
            "Users": st.column_config.NumberColumn(format="%d")
        }
    )

# Enhanced footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: {'#ccc' if theme == 'Dark Mode' else '#666'}; font-size: 0.9rem; padding: 1rem;">
    <p>National Emergency Response Information System (NERIS) | U.S. Fire Administration</p>
    <p><em>Modernizing emergency response data and analytics for America's fire service</em></p>
    <p><small>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Theme: {theme}</small></p>
</div>
""", unsafe_allow_html=True)