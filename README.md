# 🔥 US Fire Department and Station Registry Map

Welcome to the **US Fire Department and Station Registry Map**, a powerful and interactive Streamlit application that visualizes two comprehensive datasets from the U.S. Fire Administration (USFA).

This project makes it easy to explore and analyze the distribution and key statistics of fire departments and their stations across the United States.

---

## 🛠️ How to Use

### 1. Prerequisites

Before you get started, make sure you have **Python 3.7 or newer** installed. You will also need to install the required libraries:

    pip install streamlit pandas geopy

### 2. Project Setup

Ensure the two CSV files are in the same directory as the `app.py` script. The file names must be exactly:

    usfa-registry-national-1.csv
    usfa-registry-station.csv

### 3. Run the Application

Navigate to the project directory in your terminal and run the following command:

    streamlit run app.py

Your web browser will automatically open a new tab with the application.

### 4. Exploring the App

- **Interactive Map:** The map displays the location of fire department headquarters based on their city and state. You can zoom, pan, and click on individual data points.
- **Filters:** Use the sidebar to filter the data by state and department type (e.g., Volunteer, Career, Mostly volunteer). This allows you to focus on specific regions and types of fire departments.
- **Key Metrics:** The dashboard provides key statistics, such as the total number of departments, stations, and firefighters, which update dynamically based on your filters.

---

## 📈 About the Data

This application uses data from the U.S. Fire Administration's National Fire Department Registry.

- **usfa-registry-national-1.csv:** Contains comprehensive details about fire departments, including their name, address, number of stations, and active firefighter counts by type (career, volunteer, etc.).
- **usfa-registry-station.csv:** Contains specific information about each individual station associated with the departments in the national registry.
