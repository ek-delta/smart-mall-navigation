import math
import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Map Distance Calculator", layout="wide")
st.title("Map Coordinate Distance Calculator")

# 1. Initialize session state
if "points" not in st.session_state:
    st.session_state.points = []

# Action button
if st.button("Clear Selected Points"):
    st.session_state.points = []
    st.rerun()

# Dynamic function lookup for Plotly 6.0+ (scatter_map) vs 5.x (scatter_mapbox)
scatter_func = getattr(px, "scatter_map", getattr(px, "scatter_mapbox", None))
line_func = getattr(px, "line_map", getattr(px, "line_mapbox", None))

# 2. Build map dataframe from stored points
if st.session_state.points:
    df_points = pd.DataFrame(st.session_state.points, columns=["lat", "lon"])
    df_points["label"] = [f"Point {i+1}" for i in range(len(df_points))]
else:
    # Dummy row to initialize canvas view center
    df_points = pd.DataFrame([{"lat": 20.0, "lon": 0.0, "label": "Center"}])

# 3. Render base Map figure
fig = scatter_func(
    df_points if st.session_state.points else df_points.head(0),
    lat="lat",
    lon="lon",
    hover_name="label" if st.session_state.points else None,
    zoom=2,
    size_max=15
)

# Connect points with a line if 2 points are selected
if len(st.session_state.points) == 2 and line_func:
    fig.add_trace(
        line_func(
            df_points, 
            lat="lat", 
            lon="lon"
        ).data[0]
    )

# Compatible layout setup
layout_updates = {
    "margin": dict(l=0, r=0, t=0, b=0),
    "height": 550,
    "clickmode": "event+select"
}

# Apply map style safely depending on engine version
if hasattr(px, "scatter_map"):
    layout_updates["map_style"] = "open-street-map"
else:
    layout_updates["mapbox_style"] = "open-street-map"

fig.update_layout(**layout_updates)

# 4. Streamlit interactive event capture
selected_data = st.plotly_chart(
    fig,
    use_container_width=True,
    on_select="rerun",
    selection_mode="points"
)

# 5. Handle point clicks
if selected_data and "selection" in selected_data:
    points_data = selected_data["selection"].get("points", [])
    if points_data:
        clicked_pt = points_data[0]
        lat = clicked_pt.get("lat")
        lon = clicked_pt.get("lon")

        if lat is not None and lon is not None:
            new_pt = (round(lat, 4), round(lon, 4))
            
            if not st.session_state.points or st.session_state.points[-1] != new_pt:
                if len(st.session_state.points) >= 2:
                    st.session_state.points = [new_pt]
                else:
                    st.session_state.points.append(new_pt)
                st.rerun()

# 6. Haversine Calculation
st.divider()
if len(st.session_state.points) == 1:
    st.info(f"📍 **Point 1 selected:** {st.session_state.points[0]}. Click anywhere on the map for Point 2.")

elif len(st.session_state.points) == 2:
    pt1, pt2 = st.session_state.points
    col1, col2, col3 = st.columns(3)
    
    col1.metric("Point 1 (Lat, Lon)", f"{pt1[0]}, {pt1[1]}")
    col2.metric("Point 2 (Lat, Lon)", f"{pt2[0]}, {pt2[1]}")

    lat1, lon1 = math.radians(pt1[0]), math.radians(pt1[1])
    lat2, lon2 = math.radians(pt2[0]), math.radians(pt2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))
    km = 6371 * c
    miles = km * 0.621371

    col3.metric("Distance", f"{km:.2f} km", f"{miles:.2f} mi")
