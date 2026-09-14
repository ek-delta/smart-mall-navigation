import math
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

ALL_LOCATIONS = {}
for floor, nodes in STORES.items():
    for name, coords in nodes.items():
        ALL_LOCATIONS[name] = coords

def calculate_3d_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + ((p1[2] - p2[2]) * 8)**2)

# Find nearest store node when clicking anywhere on the floor grid
def find_nearest_store(click_x, click_y, floor_stores):
    min_dist = float("inf")
    closest_store = None
    for store_name, (sx, sy, _) in floor_stores.items():
        dist = math.hypot(click_x - sx, click_y - sy)
        if dist < min_dist:
            min_dist = dist
            closest_store = store_name
    return closest_store

# ==========================================
# 3. SIDEBAR NAVIGATION CONTROLS
# ==========================================
st.sidebar.image("https://img.icons8.com/color/96/000000/shopping-mall.png", width=70)
st.sidebar.title("Mall Navigation")

selected_floor = st.sidebar.selectbox("Select View Floor", list(STORES.keys()))

st.sidebar.divider()
st.sidebar.subheader("Route Planner")

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

# ==========================================
# 4. MAIN APP TABS
# ==========================================
st.markdown("<div class='main-header'>Smart Indoor Mall Navigation</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Interactive 3D Indoor Pathfinding & Parking System</div>", unsafe_allow_html=True)

tab_map, tab_dir, tab_park = st.tabs(["🗺️ Interactive Mall Map", "🚶 Turn-by-Turn Directions", "🅿️ Smart Parking Integration"])

with tab_map:
    col_map, col_info = st.columns([3, 1])

    with col_map:
        floor_stores = STORES[selected_floor]
        fig = go.Figure()

        # 1. Background Interactive Click Mesh (50x50 Invisible Node Array)
        # This makes ANY point clicked on the floor surface trigger an event
        gx, gy = np.meshgrid(np.linspace(0, 50, 26), np.linspace(0, 50, 26))
        fig.add_trace(go.Scatter(
            x=gx.flatten(),
            y=gy.flatten(),
            mode="markers",
            marker=dict(size=12, color="rgba(0,0,0,0)"),
            name="Floor Click Mesh",
            hoverinfo="none",
            showlegend=False
        ))

        # 2. Add Floor CAD Outer Boundary Lines
        fig.add_trace(go.Scatter(
            x=[0, 50, 50, 0, 0],
            y=[0, 0, 50, 50, 0],
            fill="toself",
            fillcolor="rgba(240, 242, 246, 0.5)",
            line=dict(color="#1E88E5", width=3),
            name="Floor Boundary",
            hoverinfo="none"
        ))

        # 3. Plot Store/Node Points
        store_xs = [coord[0] for coord in floor_stores.values()]
        store_ys = [coord[1] for coord in floor_stores.values()]
        store_names = list(floor_stores.keys())

        fig.add_trace(go.Scatter(
            x=store_xs,
            y=store_ys,
            mode="markers+text",
            marker=dict(size=24, color="#1E88E5", symbol="circle"),
            text=store_names,
            textposition="top center",
            name="Stores & Hubs",
            customdata=store_names,
            hoverinfo="text"
        ))

        # 4. Render Route Line if Origin & Destination are calculated
        p1 = ALL_LOCATIONS[st.session_state.origin]
        p2 = ALL_LOCATIONS[st.session_state.destination]
        
        fl_index = list(STORES.keys()).index(selected_floor)
        if p1[2] == fl_index or p2[2] == fl_index:
            rx = [p1[0], p2[0]] if p1[2] == fl_index and p2[2] == fl_index else ([p1[0], 25] if p1[2] == fl_index else [25, p2[0]])
            ry = [p1[1], p2[1]] if p1[2] == fl_index and p2[2] == fl_index else ([p1[1], 25] if p1[2] == fl_index else [25, p2[1]])
            
            fig.add_trace(go.Scatter(
                x=rx,
                y=ry,
                mode="lines+markers",
                line=dict(color="#FF4B4B", width=4, dash="dash"),
                marker=dict(size=12, color="#FF4B4B"),
                name="Route Path"
            ))

        fig.update_layout(
            title=f"Floor Layout — {selected_floor} (Click anywhere to select)",
            xaxis=dict(range=[-5, 55], showgrid=False, zeroline=False),
            yaxis=dict(range=[-5, 55], showgrid=False, zeroline=False),
            height=520,
            margin=dict(l=10, r=10, t=40, b=10),
            clickmode="event+select"
        )

        # Event Capture
        selected_data = st.plotly_chart(
            fig,
            use_container_width=True,
            on_select="rerun",
            selection_mode="points"
        )

        # Handle Robust Point & Grid Mesh Clicks
        if selected_data and "selection" in selected_data:
            points_data = selected_data["selection"].get("points", [])
            if points_data:
                clicked_pt = points_data[0]
                clicked_x = clicked_pt.get("x")
                clicked_y = clicked_pt.get("y")
                
                # Check if direct store marker or background mesh was clicked
                clicked_store = None
                if "customdata" in clicked_pt:
                    clicked_store = clicked_pt["customdata"]
                elif clicked_x is not None and clicked_y is not None:
                    clicked_store = find_nearest_store(clicked_x, clicked_y, floor_stores)

                if clicked_store:
                    if selection_target == "Origin" and st.session_state.origin != clicked_store:
                        st.session_state.origin = clicked_store
                        st.rerun()
                    elif selection_target == "Destination" and st.session_state.destination != clicked_store:
                        st.session_state.destination = clicked_store
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
