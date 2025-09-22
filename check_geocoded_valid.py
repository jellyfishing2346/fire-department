import pandas as pd

df = pd.read_csv("usfa-registry-station-geocoded.csv")
valid = df.dropna(subset=["lat", "lon"])
print(f"Total rows: {len(df)}")
print(f"Rows with valid lat/lon: {len(valid)}")
print(valid[["Fire Dept Name", "Station Name", "lat", "lon"]])
