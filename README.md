# 🚒 NERIS Fire Department Dashboard

Welcome to the **NERIS Fire Department Dashboard**! 🗺️

A modern, interactive dashboard for visualizing, filtering, and analyzing U.S. fire department data. Built for clarity, speed, and real-time insights—perfect for emergency response analytics, research, and public safety innovation.

---

## ✨ Features

- 🗺️ **Interactive Map**: Visualize fire departments nationwide
- 🔍 **Advanced Filtering**: By state, data quality, API status, and more
- 📊 **Real-Time Simulation**: See onboarding and activity updates live
- 📈 **Summary Stats**: Key metrics at a glance
- 🌓 **Dark/Light Mode**: Custom theming (see note below)
- 📥 **Export Data**: Download filtered results as CSV
- ⚡ **Quick Actions**: Batch verify, send reminders, and more

---

## ⚠️ Light Mode Notice

> **Note:** Light Mode is not fully supported. For the best experience, please use **Dark Mode**.

---

## 🗺️ Data Flow Diagram

```
   ┌──────────────┐        ┌───────────────┐        ┌────────────────────┐
   │  USFA CSV   │──────▶ │ Data Cleaning │──────▶ │   Geocoding/Prep   │
   │   Data      │        │   & Parsing   │        │ (Lat/Lon, Quality) │
   └──────────────┘        └───────────────┘        └────────────────────┘
           │                                              │
           ▼                                              ▼
   ┌────────────────────────────────────────────────────────────┐
   │                Streamlit Dashboard (NERIS)                │
   │ ───────────────────────────────────────────────────────── │
   │  🗺️ Map  🔍 Filters  📊 Stats  ⚡ Real-Time  📥 Export      │
   └────────────────────────────────────────────────────────────┘
           │
           ▼
   ┌────────────────────────────────────────────────────────────┐
   │                User Interface & Analytics                  │
   │   (Interactive Map, Department Details, Quick Actions)     │
   └────────────────────────────────────────────────────────────┘
```

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/jellyfishing2346/fire-department.git
cd fire-department
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the dashboard
```bash
streamlit run dashboard.py
```

---

## 🛠️ Usage
- Use the sidebar to select display settings, filters, and simulation options.
- Click map markers for department details.
- Use quick actions for batch operations.
- Export filtered data as CSV.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Acknowledgments
- U.S. Fire Administration (USFA) for data
- Streamlit, Folium, Plotly, and the open-source community

---

> _Modernizing emergency response data and analytics for America's fire service._
