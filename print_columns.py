import pandas as pd

df = pd.read_csv("usfa-registry-station-geocoded.csv")
print(df.columns.tolist())
