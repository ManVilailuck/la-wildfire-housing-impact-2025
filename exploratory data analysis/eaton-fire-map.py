import folium
from folium.plugins import MarkerCluster

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

# Add markers to map
for _, row in eaton_fire.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=3,
        color=damage_color(row['* Damage']),
        fill=True,
        fill_opacity=0.7,
        popup=f"{row['* City']} | {row['* Damage']}"
    ).add_to(marker_cluster)

eaton_map.save("/mnt/data/eaton_fire_map.html")
"/mnt/data/eaton_fire_map.html"
