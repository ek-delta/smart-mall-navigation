import streamlit as st
import folium
from streamlit_folium import st_folium
import math

st.title("Click Anywhere Map Distance Calculator")

if "points" not in st.session_state:
    st.session_state.points = []

# Create a Leaflet Map
m = folium.Map(location=[20.0, 0.0], zoom_start=2)

# Add markers for selected points
for idx, pt in enumerate(st.session_state.points):
    folium.Marker(pt, popup=f"Point {idx+1}").add_to(m)

if len(st.session_state.points) == 2:
    folium.PolyLine(st.session_state.points, color="red", weight=3).add_to(m)

# Render map and capture click event anywhere
map_data = st_folium(m, width=800, height=500)

# Extract click coordinates
if map_data and map_data.get("last_clicked"):
    click_lat = map_data["last_clicked"]["lat"]
    click_lon = map_data["last_clicked"]["lng"]
    new_pt = (round(click_lat, 4), round(click_lon, 4))
    
    if not st.session_state.points or st.session_state.points[-1] != new_pt:
        if len(st.session_state.points) >= 2:
            st.session_state.points = [new_pt]
        else:
            st.session_state.points.append(new_pt)
        st.rerun()
