import math
import random
import time
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st

# ==========================================
# 1. PAGE CONFIGURATION & STATE INITIALIZATION
# ==========================================
st.set_page_config(
    page_title="Smart Mall Navigation System",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; color: #1E88E5; font-weight: bold; text-align: center; }
    .sub-header { font-size: 1.1rem; color: #555555; text-align: center; margin-bottom: 20px; }
    .metric-card { background-color: #f8f9fa; border-left: 5px solid #1E88E5; padding: 12px; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "points" not in st.session_state:
    st.session_state.points = []
if "origin" not in st.session_state:
    st.session_state.origin = "Entrance Ground Floor"
if "destination" not in st.session_state:
    st.session_state.destination = "Apple Store"

# ==========================================
# 2. MALL MOCK DATA & NODE GRAPH SETUP
# ==========================================
STORES = {
    "Ground Floor (F0)": {
        "Entrance Ground Floor": (0, 0, 0),
        "Main Atrium": (20, 20, 0),
        "Apple Store": (40, 10, 0),
        "Starbucks": (15, 35, 0),
        "Nike Store": (45, 40, 0),
        "Elevator G": (25, 25, 0),
        "Escalator G": (10, 25, 0)
    },
    "First Floor (F1)": {
        "Zara": (35, 12, 1),
        "Sephora": (18, 38, 1),
        "Food Court": (40, 42, 1),
        "Elevator F1": (25, 25, 1),
        "Escalator F1": (10, 25, 1)
    },
    "Second Floor (F2)": {
        "Cinema VIP": (20, 15, 2),
        "Arcade Zone": (45, 15, 2),
        "Rooftop Parking Entry": (25, 45, 2),
        "Elevator F2": (25, 25, 2),
        "Escalator F2": (10, 25, 2)
    }
}

PARKING_SLOTS = {
    "P-101 (EV Charging)": (10, 45, 2, "Available"),
    "P-102": (15, 45, 2, "Occupied"),
    "P-103": (20, 45, 2, "Available"),
    "P-104 (Handicap)": (30, 45, 2, "Available"),
}

# Flat list of all locations
ALL_LOCATIONS = {}
for floor, nodes in STORES.items():
    for name, coords in nodes.items():
        ALL_LOCATIONS[name] = coords

# Distance Matrix Helper (3D Euclidean for Indoor Routing)
def calculate_3d_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + ((p1[2] - p2[2]) * 8)**2)

# ==========================================
# 3. SIDEBAR NAVIGATION CONTROLS
# ==========================================
st.sidebar.image("https://img.icons8.com/color/96/000000/shopping-mall.png", width=70)
st.sidebar.title("Mall Navigation")

selected_floor = st.sidebar.selectbox("Select View Floor", list(STORES.keys()))

st.sidebar.divider()
st.sidebar.subheader("Route Planner")

# Selection Mode
selection_target = st.sidebar.radio("Map Click Assigns To:", ["Origin", "Destination"])

origin_loc = st.sidebar.selectbox(
    "Origin Point",
    options=list(ALL_LOCATIONS.keys()),
    index=list(ALL_LOCATIONS.keys()).index(st.session_state.origin) if st.session_state.origin in ALL_LOCATIONS else 0,
    key="sb_origin"
)
dest_loc = st.sidebar.selectbox(
    "Destination Point",
    options=list(ALL_LOCATIONS.keys()),
    index=list(ALL_LOCATIONS.keys()).index(st.session_state.destination) if st.session_state.destination in ALL_LOCATIONS else 2,
    key="sb_dest"
)

st.session_state.origin = origin_loc
st.session_state.destination = dest_loc

# Clear points button
if st.sidebar.button("Clear Click Selections"):
    st.session_state.points = []
    st.rerun()

# ==========================================
# 4. MAIN APP TABS
# ==========================================
st.markdown("<div class='main-header'>Smart Indoor Mall Navigation</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Interactive 3D Indoor Pathfinding & Parking System</div>", unsafe_allow_html=True)

tab_map, tab_dir, tab_park = st.tabs(["🗺️ Interactive Mall Map", "🚶 Turn-by-Turn Directions", "🅿️ Smart Parking Integration"])

# ------------------------------------------
# TAB 1: INTERACTIVE MAP (WITH CLICK EVENT CAPTURE)
# ------------------------------------------
with tab_map:
    col_map, col_info = st.columns([3, 1])

    with col_map:
        # Build 2D Floor Plan with Clickable Nodes
        floor_stores = STORES[selected_floor]
        
        fig = go.Figure()

        # 1. Add Floor CAD Outer Boundary Lines
        fig.add_trace(go.Scatter(
            x=[0, 50, 50, 0, 0],
            y=[0, 0, 50, 50, 0],
            fill="toself",
            fillcolor="rgba(240, 242, 246, 0.5)",
            line=dict(color="#1E88E5", width=3),
            name="Floor Boundary",
            hoverinfo="none"
        ))

        # 2. Plot Clickable Store/Node Points
        store_xs = [coord[0] for coord in floor_stores.values()]
        store_ys = [coord[1] for coord in floor_stores.values()]
        store_names = list(floor_stores.keys())

        fig.add_trace(go.Scatter(
            x=store_xs,
            y=store_ys,
            mode="markers+text",
            marker=dict(size=18, color="#1E88E5", symbol="square"),
            text=store_names,
            textposition="top center",
            name="Locations",
            customdata=store_names,
            hoverinfo="text"
        ))

        # 3. Render Route Line if Origin & Destination are calculated
        p1 = ALL_LOCATIONS[st.session_state.origin]
        p2 = ALL_LOCATIONS[st.session_state.destination]
        
        # Current floor level indicator
        fl_index = list(STORES.keys()).index(selected_floor)
        if p1[2] == fl_index or p2[2] == fl_index:
            rx = [p1[0], p2[0]] if p1[2] == fl_index and p2[2] == fl_index else ([p1[0], 25] if p1[2] == fl_index else [25, p2[0]])
            ry = [p1[1], p2[1]] if p1[2] == fl_index and p2[2] == fl_index else ([p1[1], 25] if p1[2] == fl_index else [25, p2[1]])
            
            fig.add_trace(go.Scatter(
                x=rx,
                y=ry,
                mode="lines+markers",
                line=dict(color="#FF4B4B", width=4, dash="dash"),
                marker=dict(size=10, color="#FF4B4B"),
                name="Nav Route"
            ))

        fig.update_layout(
            title=f"Floor Layout — {selected_floor}",
            xaxis=dict(range=[-5, 55], showgrid=False, zeroline=False),
            yaxis=dict(range=[-5, 55], showgrid=False, zeroline=False),
            height=500,
            margin=dict(l=10, r=10, t=40, b=10),
            clickmode="event+select"
        )

        # STREAMLIT NATIVE INTERACTIVE CLICK EVENT CAPTURE
        selected_data = st.plotly_chart(
            fig,
            use_container_width=True,
            on_select="rerun",
            selection_mode="points"
        )

        # Handle Map Click Events to update Origin / Destination
        if selected_data and "selection" in selected_data:
            points_data = selected_data["selection"].get("points", [])
            if points_data:
                clicked_pt = points_data[0]
                point_index = clicked_pt.get("point_index")
                
                if point_index is not None and point_index < len(store_names):
                    clicked_location_name = store_names[point_index]

                    if selection_target == "Origin" and st.session_state.origin != clicked_location_name:
                        st.session_state.origin = clicked_location_name
                        st.rerun()
                    elif selection_target == "Destination" and st.session_state.destination != clicked_location_name:
                        st.session_state.destination = clicked_location_name
                        st.rerun()

    with col_info:
        st.subheader("📍 Active Selection")
        st.markdown(f"**Origin:** `{st.session_state.origin}`")
        st.markdown(f"**Destination:** `{st.session_state.destination}`")
        
        st.divider()
        dist_m = round(calculate_3d_distance(p1, p2), 1)
        est_walk_time = max(1, math.ceil(dist_m / 1.2 / 60))
        
        st.metric("Total Route Distance", f"{dist_m} meters")
        st.metric("Estimated Walk Time", f"{est_walk_time} min")
        
        if p1[2] != p2[2]:
            st.warning(f"⚠️ Multi-floor route detected: Move from Floor {p1[2]} to Floor {p2[2]} using Elevators/Escalators.")

# ------------------------------------------
# TAB 2: TURN-BY-TURN DIRECTIONS
# ------------------------------------------
with tab_dir:
    st.subheader(f"Navigation: {st.session_state.origin} ➔ {st.session_state.destination}")
    
    steps = [
        f"Start at **{st.session_state.origin}**.",
        "Head straight towards the central atrium corridor for 15 meters.",
    ]
    
    if p1[2] != p2[2]:
        steps.append(f"Take Elevator G / Escalator to **Floor {p2[2]}**.")
    
    steps.extend([
        "Turn right near the main retail walkway.",
        f"Arrive at **{st.session_state.destination}** on your left."
    ])

    for i, step in enumerate(steps, 1):
        st.markdown(f"**Step {i}:** {step}")

# ------------------------------------------
# TAB 3: SMART PARKING INTEGRATION
# ------------------------------------------
with tab_park:
    st.subheader("🅿️ Rooftop Smart Parking Availability")
    
    df_park = pd.DataFrame(
        [{"Slot": k, "X": v[0], "Y": v[1], "Status": v[3]} for k, v in PARKING_SLOTS.items()]
    )
    
    st.dataframe(df_park, use_container_width=True)
    
    available_slots = df_park[df_park["Status"] == "Available"]["Slot"].tolist()
    if available_slots:
        selected_slot = st.selectbox("Reserve Parking Slot", available_slots)
        if st.button("Confirm Parking Reservation"):
            st.success(f"Slot `{selected_slot}` successfully reserved! Directions updated.")
    else:
        st.error("No parking slots available at this moment.")

# ==========================================
# 5. FOOTER
# ==========================================
st.divider()
st.caption("Smart Mall Navigation Platform • Native Plotly Grid Click Listener Active")
