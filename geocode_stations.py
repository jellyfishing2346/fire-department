import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time

# Load and clean data
df = pd.read_csv("usfa-registry-station.csv")
df.columns = df.columns.str.strip()

# Setup geocoder
geolocator = Nominatim(user_agent="fire_dept_map_batch")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def get_lat_lon(row):
    address = f"{row['Station Addr1']}, {row['Station City']}, {row['Station State']} {row['Station Zip']}"
    try:
        location = geolocator.geocode(address)
        if location:
            return pd.Series({'lat': location.latitude, 'lon': location.longitude})
    except Exception:
        pass
    return pd.Series({'lat': None, 'lon': None})

# Only geocode if lat/lon not already present
if 'lat' not in df.columns or 'lon' not in df.columns:
    coords = df.apply(get_lat_lon, axis=1)
    df = pd.concat([df, coords], axis=1)
    df.to_csv("usfa-registry-station"
    "-geocoded.csv", index=False)
    print("Geocoding complete! Saved as usfa-registry-station-geocoded.csv")
else:
    print("Latitude/Longitude columns already exist.")
