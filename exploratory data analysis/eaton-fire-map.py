'''
this file outputs the damages done by the eaton fire and maps it out based on different levels of damage on the map.
'''

import pandas as pd
import folium
from folium.plugins import MarkerCluster

# Load the dataset (update the path if needed)
df = pd.read_csv("datasets/b8aeb030-140d-43d2-aa29-1a80862e3d62.csv")  # Ensure correct path

# Convert date column to datetime
df['Incident Start Date'] = pd.to_datetime(df['Incident Start Date'], errors='coerce')

# Filter for fires in January 2025
jan_2025_fires = df[
    (df['Incident Start Date'].dt.year == 2025) &
    (df['Incident Start Date'].dt.month == 1)
]

# Filter to just Eaton Fire
eaton_fire = jan_2025_fires[jan_2025_fires['* Incident Name'] == 'Eaton']

# Base map centered on Eaton Fire area (Altadena/Pasadena)
center_lat = eaton_fire['Latitude'].mean()
center_lon = eaton_fire['Longitude'].mean()
eaton_map = folium.Map(location=[center_lat, center_lon], zoom_start=12)

# Create a marker cluster for visualization
marker_cluster = MarkerCluster().add_to(eaton_map)

# Define a color function for damage levels
def damage_color(damage):
    if "Destroyed" in damage:
        return "red"
    elif "Affected" in damage:
        return "orange"
    elif "No Damage" in damage:
        return "green"
    else:
        return "gray"

# Add markers to the map
for _, row in eaton_fire.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=3,
        color=damage_color(row['* Damage']),
        fill=True,
        fill_opacity=0.7,
        popup=f"{row['* City']} | {row['* Damage']}"
    ).add_to(marker_cluster)

# Save the map
eaton_map.save("exploratory data analysis/eaton_fire_map.html")  # Adjust path if needed

print("Eaton Fire map has been successfully created!")