# 🚒 Fire Department Data & Dashboard

Welcome to the Fire Department Data & Dashboard project! This project visualizes US fire department and station data on an interactive map using Python and Streamlit.

---

## 🗺️ Dashboard Features

- **Interactive Map:**
  - Visualize fire stations across the US
  - Filter by state, department type, and more
  - Click on markers for department/station details
- **Summary Statistics:**
  - Number of stations, types, and personnel
- **Modern UI:**
  - Clean, responsive, and visually appealing

---

## 📊 Example Data

| Fire Dept Name | Station Name | Station Address | City | State | Zip |
|---------------|-------------|----------------|------|-------|-----|
| Abbeville Fire Department | Central Station | 210 W Vermillion ST | Abbeville | LA | 70510-4612 |
| 3-G Volunteer Fire Company, Inc. | 3-G Volunteer Fire Company, Inc. | Brantingham RD | Brantingham | NY | 13312 |

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd fire-department
```

### 2. Install requirements
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit app
```bash
streamlit run dashboard.py
```

---

## 🛠️ Requirements
- Python 3.8+
- Streamlit
- pandas
- geopy (for geocoding addresses)
- folium or pydeck (for mapping)

Install all with:
```bash
pip install streamlit pandas geopy folium
```

---

## 📂 File Structure

```
fire-department/
├── dashboard.py           # Streamlit dashboard app
├── requirements.txt       # Python dependencies
├── usfa-registry-national.csv
├── usfa-registry-station.csv
└── README.md
```

---

## ✨ Screenshots

![Dashboard Screenshot](assets/dashboard-screenshot.png)

---

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License
[MIT](LICENSE)
