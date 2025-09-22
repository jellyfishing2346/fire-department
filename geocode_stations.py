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
    # Build the best possible address
    address = f"{row.get('Station Name', '')}, {row.get('Station Addr1', '')}, {row.get('Station City', '')}, {row.get('Station State', '')} {row.get('Station Zip', '')}, USA"
    try:
        location = geocode(address)
        if location:
            return pd.Series({'lat': location.latitude, 'lon': location.longitude})
    except Exception:
        pass
    return pd.Series({'lat': None, 'lon': None})

# Always geocode all rows, add lat/lon columns
coords = df.apply(get_lat_lon, axis=1)
df['lat'] = coords['lat']
df['lon'] = coords['lon']

# Save output with lat/lon columns
df.to_csv("usfa-registry-station-geocoded.csv", index=False)
print("Geocoding complete! Saved as usfa-registry-station-geocoded.csv")
