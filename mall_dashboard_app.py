import math
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Map Distance Calculator", layout="wide")
st.title("Map Coordinate Distance Calculator")

# 1. Initialize session state for storing clicked coordinates
if "points" not in st.session_state:
    st.session_state.points = []

# Action buttons to reset or manage points
col_btn1, col_btn2 = st.columns([1, 5])
with col_btn1:
    if st.button("Clear Selected Points"):
        st.session_state.points = []
        st.rerun()

# 2. Render base Mapbox map figure
fig = go.Figure()

# Add existing markers if any points are selected
if st.session_state.points:
    lats = [pt[0] for pt in st.session_state.points]
    lons = [pt[1] for pt in st.session_state.points]
    labels = [f"Point {i+1}" for i in range(len(st.session_state.points))]
    
    # Plot line between points if 2 points are selected
    if len(st.session_state.points) == 2:
        fig.add_trace(
            go.Scattermapbox(
                lat=lats,
                lon=lons,
                mode="lines",
                line=dict(width=3, color="red"),
                hoverinfo="none",
                showlegend=False
            )
        )

    # Plot point markers
    fig.add_trace(
        go.Scattermapbox(
            lat=lats,
            lon=lons,
            mode="markers+text",
            marker=dict(size=14, color=["#00FF00", "#FF0000"][:len(lats)]),
            text=labels,
            textposition="top center",
            hoverinfo="text",
            showlegend=False
        )
    )

# Map layout configuration
fig.update_layout(
    mapbox=dict(
        style="open-street-map",
        zoom=2,
        center=dict(lat=20, lon=0)
    ),
    margin=dict(l=0, r=0, t=0, b=0),
    height=550,
    clickmode="event+select"
)

# 3. Handle click/selection anywhere using Streamlit native event listener
selected_data = st.plotly_chart(
    fig,
    use_container_width=True,
    on_select="rerun",  # Triggers rerun on click/selection events
    selection_mode="points"
)

# 4. Process clicked coordinate payload
if selected_data and "selection" in selected_data:
    points_data = selected_data["selection"].get("points", [])
    if points_data:
        clicked_pt = points_data[0]
        # Extract lat/lon regardless of whether an existing point or map mesh was clicked
        lat = clicked_pt.get("lat")
        lon = clicked_pt.get("lon")

        if lat is not None and lon is not None:
            new_pt = (round(lat, 4), round(lon, 4))
            
            # Avoid duplicate triggers for the same point
            if not st.session_state.points or st.session_state.points[-1] != new_pt:
                if len(st.session_state.points) >= 2:
                    st.session_state.points = [new_pt]
                else:
                    st.session_state.points.append(new_pt)
                st.rerun()

# 5. Calculate & Display Haversine distance
st.divider()
if len(st.session_state.points) == 1:
    st.info(f"📍 **Point 1 selected:** {st.session_state.points[0]}. Click anywhere on the map for Point 2.")

elif len(st.session_state.points) == 2:
    pt1, pt2 = st.session_state.points
    col1, col2, col3 = st.columns(3)
    
    col1.metric("Point 1 (Lat, Lon)", f"{pt1[0]}, {pt1[1]}")
    col2.metric("Point 2 (Lat, Lon)", f"{pt2[0]}, {pt2[1]}")

    # Haversine formula calculation
    lat1, lon1 = math.radians(pt1[0]), math.radians(pt1[1])
    lat2, lon2 = math.radians(pt2[0]), math.radians(pt2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))
    km = 6371 * c  # Earth radius in kilometers
    miles = km * 0.621371

    col3.metric("Distance", f"{km:.2f} km", f"{miles:.2f} mi")
