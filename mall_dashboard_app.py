import math
import heapq
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from geopy.distance import geodesic
from streamlit_plotly_events import plotly_events

# ==============================================================================
# 1. PAGE CONFIGURATION & CUSTOM STYLING
# ==============================================================================
st.set_page_config(
    page_title="Indoor Navigation & Map Calculator",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Theme Color Variables */
    :root {
        --primary-red: #D32F2F;
        --secondary-orange: #FF6700;
        --pink-banner: #E91E63;
    }

    /* Main Container Adjustments */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    /* Primary Headers */
    h1, h2, h3 {
        color: var(--primary-red);
        font-weight: 700;
    }

    /* Pink Route Banner (Custom Requested Background) */
    .custom-route-banner {
        background-color: var(--pink-banner);
        color: #FFFFFF;
        padding: 14px 18px;
        border-radius: 8px;
        font-size: 1rem;
        margin-top: 10px;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.15);
    }
    
    .custom-route-banner code {
        background-color: rgba(255, 255, 255, 0.25) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        font-weight: bold;
    }

    /* Orange Feature Cards */
    .orange-card {
        background-color: #FFF3E0;
        border-left: 5px solid var(--secondary-orange);
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 15px;
    }

    /* Custom Buttons */
    .stButton>button {
        border-radius: 6px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. SESSION STATE INITIALIZATION
# ==============================================================================
if "lang" not in st.session_state:
    st.session_state.lang = "English"

if "clicked_points" not in st.session_state:
    st.session_state.clicked_points = []  # Stores raw (x, y, floor) exact clicks

if "nav_mode" not in st.session_state:
    st.session_state.nav_mode = "POI Navigation"  # Options: 'POI Navigation' or 'Free Pick Distance'

if "start_poi" not in st.session_state:
    st.session_state.start_poi = "ENTRANCE_MAIN"

if "dest_poi" not in st.session_state:
    st.session_state.dest_poi = "STORE_TECH"

# ==============================================================================
# 3. TRANSLATION & DICTIONARY CONFIGURATION
# ==============================================================================
TRANSLATIONS = {
    "English": {
        "title": "🗺️ Indoor Navigation & Map Calculator",
        "subtitle": "Interactive CAD mapping, 3D routing, and high-precision spatial distance calculation.",
        "current_route_lbl": "Current Selected Route",
        "free_click_lbl": "Exact Click Points",
        "view_2d": "2D CAD View",
        "view_3d": "3D Isometric View",
        "active_floor": "Select Active Floor",
        "mode_select": "Select Interaction Mode",
        "mode_poi": "Structured Store Navigation",
        "mode_free": "Free-Click Distance Pick (No Node Snapping)",
        "reset_btn": "Reset Click Points",
        "calc_dist_lbl": "Direct Measured Distance",
        "total_floors": "Total Floors",
        "total_pois": "Total POIs",
        "parking_spots": "Parking Spots Available",
    },
    "Spanish": {
        "title": "🗺️ Navegación Interior y Calculadora de Mapas",
        "subtitle": "Mapeo CAD interactivo, enrutamiento 3D y cálculo de distancia espacial.",
        "current_route_lbl": "Ruta Seleccionada Actual",
        "free_click_lbl": "Puntos de Clic Exactos",
        "view_2d": "Vista CAD 2D",
        "view_3d": "Vista Isométrica 3D",
        "active_floor": "Seleccionar Planta Activa",
        "mode_select": "Seleccionar Modo de Interacción",
        "mode_poi": "Navegación Estructurada de Tiendas",
        "mode_free": "Selección de Distancia Libre (Sin ajuste de nodos)",
        "reset_btn": "Restablecer Puntos",
        "calc_dist_lbl": "Distancia Directa Medida",
        "total_floors": "Pisos Totales",
        "total_pois": "POIs Totales",
        "parking_spots": "Plazas de Aparcamiento Disponibles",
    }
}

# Language translations helper
def get_text(key):
    return TRANSLATIONS.get(st.session_state.lang, TRANSLATIONS["English"]).get(key, key)

# ==============================================================================
# 4. MOCK DATA & GRAPH MODEL
# ==============================================================================
FLOOR_HEIGHT_METERS = 4.5

# Floor layout definitions & POI nodes (X, Y, Floor)
MOCK_NODES = {
    "ENTRANCE_MAIN": {"x": 10, "y": 10, "z": 0, "name": "Main Entrance", "category": "Entrance"},
    "LOBBY_GF": {"x": 25, "y": 25, "z": 0, "name": "Ground Lobby", "category": "Lobby"},
    "STORE_GROCERY": {"x": 75, "y": 20, "z": 0, "name": "Hypermarket Superstore", "category": "Shopping"},
    "ELEVATOR_GF": {"x": 50, "y": 50, "z": 0, "name": "Central Elevator (GF)", "category": "Elevator"},
    "ESCALATOR_GF": {"x": 80, "y": 50, "z": 0, "name": "Escalator to 1F", "category": "Escalator"},
    
    "ELEVATOR_1F": {"x": 50, "y": 50, "z": 1, "name": "Central Elevator (1F)", "category": "Elevator"},
    "ESCALATOR_1F": {"x": 80, "y": 50, "z": 1, "name": "Escalator to 2F", "category": "Escalator"},
    "STORE_FASHION": {"x": 20, "y": 75, "z": 1, "name": "Fashion Boutique", "category": "Shopping"},
    "STORE_TECH": {"x": 80, "y": 80, "z": 1, "name": "Tech & Gadgets Hub", "category": "Shopping"},
    "FOOD_COURT": {"x": 40, "y": 25, "z": 1, "name": "Gourmet Food Court", "category": "Dining"},
    
    "ELEVATOR_2F": {"x": 50, "y": 50, "z": 2, "name": "Central Elevator (2F)", "category": "Elevator"},
    "CINEMA_HALL": {"x": 30, "y": 70, "z": 2, "name": "Cineplex Theater", "category": "Entertainment"},
    "ROOFTOP_PARK": {"x": 50, "y": 20, "z": 3, "name": "Rooftop Parking Slot P-12", "category": "Parking"}
}

# Navigation Graph (Edges with cost)
GRAPH_EDGES = [
    ("ENTRANCE_MAIN", "LOBBY_GF", 1),
    ("LOBBY_GF", "STORE_GROCERY", 1),
    ("LOBBY_GF", "ELEVATOR_GF", 1),
    ("STORE_GROCERY", "ESCALATOR_GF", 1),
    ("ELEVATOR_GF", "ELEVATOR_1F", 2),
    ("ESCALATOR_GF", "ESCALATOR_1F", 2),
    ("ELEVATOR_1F", "STORE_FASHION", 1),
    ("ELEVATOR_1F", "STORE_TECH", 1),
    ("STORE_FASHION", "FOOD_COURT", 1),
    ("ESCALATOR_1F", "STORE_TECH", 1),
    ("ELEVATOR_1F", "ELEVATOR_2F", 2),
    ("ELEVATOR_2F", "CINEMA_HALL", 1),
    ("ELEVATOR_2F", "ROOFTOP_PARK", 3)
]

def format_location_label(node_key, lang="English"):
    if node_key in MOCK_NODES:
        node = MOCK_NODES[node_key]
        floor_prefix = f"[{'GF' if node['z']==0 else f'{node['z']}F'}]"
        return f"{floor_prefix} {node['name']}"
    return str(node_key)

# ==============================================================================
# 5. ROUTING & DISTANCE ALGORITHMS
# ==============================================================================
def euclidean_distance_3d(p1, p2):
    """Calculates real-world metric distance incorporating floor elevation."""
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dz = (p2[2] - p1[2]) * FLOOR_HEIGHT_METERS
    return math.sqrt(dx**2 + dy**2 + dz**2)

def dijkstra_shortest_path(start_node, dest_node):
    """Computes shortest node path using Dijkstra algorithm."""
    adj = {}
    for u, v, w in GRAPH_EDGES:
        adj.setdefault(u, []).append((v, w))
        adj.setdefault(v, []).append((u, w))

    queue = [(0, start_node, [])]
    seen = set()

    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node not in seen:
            seen.add(node)
            path = path + [node]
            if node == dest_node:
                return path

            for next_node, weight in adj.get(node, []):
                if next_node not in seen:
                    heapq.heappush(queue, (cost + weight, next_node, path))
    return []

def compute_route_summary(route_nodes):
    if len(route_nodes) < 2:
        return 0, 0, 0
    
    total_dist = 0
    floor_changes = 0
    
    for i in range(len(route_nodes) - 1):
        n1 = MOCK_NODES[route_nodes[i]]
        n2 = MOCK_NODES[route_nodes[i+1]]
        p1 = (n1['x'], n1['y'], n1['z'])
        p2 = (n2['x'], n2['y'], n2['z'])
        
        total_dist += euclidean_distance_3d(p1, p2)
        if n1['z'] != n2['z']:
            floor_changes += abs(n1['z'] - n2['z'])
            
    steps = int(total_dist / 0.75) # Approx 0.75 meters per step
    return round(total_dist, 2), floor_changes, steps

# ==============================================================================
# 6. PLOTLY MAP GENERATORS
# ==============================================================================
def render_2d_cad_view(floor_num, route_path=None, picked_points=None):
    fig = go.Figure()

    # 1. Base CAD Plane Clickable Area (Invisible mesh capturing all clicks)
    fig.add_trace(go.Scatter(
        x=[0, 100, 100, 0, 0],
        y=[0, 0, 100, 100, 0],
        fill="toself",
        fillcolor="rgba(245, 245, 245, 0.8)",
        line=dict(color="#CCCCCC", width=1),
        hoverinfo="none",
        showlegend=False,
        name="Floor Base"
    ))

    # 2. Draw Floor POI Nodes
    floor_pois = {k: v for k, v in MOCK_NODES.items() if v['z'] == floor_num}
    
    x_coords = [v['x'] for v in floor_pois.values()]
    y_coords = [v['y'] for v in floor_pois.values()]
    labels = [v['name'] for v in floor_pois.values()]
    
    fig.add_trace(go.Scatter(
        x=x_coords,
        y=y_coords,
        mode="markers+text",
        marker=dict(size=14, color="#D32F2F", symbol="square"),
        text=labels,
        textposition="top center",
        name="Stores & POIs"
    ))

    # 3. Draw Path Route Overlay if active
    if route_path:
        rx, ry = [], []
        for r_node in route_path:
            if MOCK_NODES[r_node]['z'] == floor_num:
                rx.append(MOCK_NODES[r_node]['x'])
                ry.append(MOCK_NODES[r_node]['y'])
        
        if len(rx) > 1:
            fig.add_trace(go.Scatter(
                x=rx, y=ry,
                mode="lines+markers",
                line=dict(color="#FF6700", width=4, dash="solid"),
                marker=dict(size=8, color="#FF6700"),
                name="Nav Path"
            ))

    # 4. Draw Free Picked Custom Points (Pink Lines & Pins)
    if picked_points:
        current_floor_picks = [p for p in picked_points if p[2] == floor_num]
        px = [p[0] for p in current_floor_picks]
        py = [p[1] for p in current_floor_picks]
        
        fig.add_trace(go.Scatter(
            x=px, y=py,
            mode="markers+lines+text",
            marker=dict(size=16, color="#E91E63", symbol="x"),
            line=dict(width=3, color="#E91E63", dash="dash"),
            text=[f"P{i+1}" for i in range(len(px))],
            textposition="bottom center",
            name="Exact Picked Points"
        ))

    fig.update_layout(
        xaxis=dict(range=[-5, 105], showgrid=True, zeroline=False),
        yaxis=dict(range=[-5, 105], showgrid=True, zeroline=False, scaleanchor="x", scaleratio=1),
        margin=dict(l=10, r=10, b=10, t=10),
        height=550,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    return fig

def render_3d_isometric_view(route_path=None):
    fig = go.Figure()

    # Draw stacked floor layers
    for f in range(4):
        # Draw floor planes
        fig.add_trace(go.Scatter3d(
            x=[0, 100, 100, 0, 0],
            y=[0, 0, 100, 100, 0],
            z=[f*FLOOR_HEIGHT_METERS]*5,
            mode="lines",
            line=dict(color="#BDBDBD", width=2),
            showlegend=False
        ))

    # Plot POIs in 3D
    x3, y3, z3, labels = [], [], [], []
    for k, v in MOCK_NODES.items():
        x3.append(v['x'])
        y3.append(v['y'])
        z3.append(v['z'] * FLOOR_HEIGHT_METERS)
        labels.append(v['name'])

    fig.add_trace(go.Scatter3d(
        x=x3, y=y3, z=z3,
        mode="markers+text",
        marker=dict(size=6, color="#D32F2F"),
        text=labels,
        textposition="top center",
        name="All POIs"
    ))

    # Route line in 3D
    if route_path and len(route_path) > 1:
        rx = [MOCK_NODES[n]['x'] for n in route_path]
        ry = [MOCK_NODES[n]['y'] for n in route_path]
        rz = [MOCK_NODES[n]['z'] * FLOOR_HEIGHT_METERS for n in route_path]

        fig.add_trace(go.Scatter3d(
            x=rx, y=ry, z=rz,
            mode="lines+markers",
            line=dict(color="#FF6700", width=6),
            marker=dict(size=8, color="#E91E63"),
            name="3D Route Path"
        ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[-5, 105]),
            yaxis=dict(range=[-5, 105]),
            zaxis=dict(range=[-2, 20], title="Elevation (m)"),
            aspectmode="manual",
            aspectratio=dict(x=1, y=1, z=0.4)
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        height=600
    )
    return fig

# ==============================================================================
# 7. UI LAYOUT & SIDEBAR
# ==============================================================================

# Sidebar Configuration
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/map-navigation.png", width=64)
    st.title("Navigation Panel")
    
    # Language selector
    st.session_state.lang = st.selectbox("🌐 Language / Idioma", ["English", "Spanish"])
    t = TRANSLATIONS[st.session_state.lang]

    st.markdown("---")
    
    # Mode Switcher
    st.session_state.nav_mode = st.radio(
        get_text("mode_select"),
        [get_text("mode_poi"), get_text("mode_free")]
    )
    
    st.markdown("---")

    if st.session_state.nav_mode == get_text("mode_poi"):
        st.subheader("📍 Select Navigation Target")
        poi_keys = list(MOCK_NODES.keys())
        
        st.session_state.start_poi = st.selectbox(
            "Start Location:", 
            poi_keys, 
            index=poi_keys.index(st.session_state.start_poi),
            format_func=lambda x: format_location_label(x, st.session_state.lang)
        )
        
        st.session_state.dest_poi = st.selectbox(
            "Destination:", 
            poi_keys, 
            index=poi_keys.index(st.session_state.dest_poi),
            format_func=lambda x: format_location_label(x, st.session_state.lang)
        )
    else:
        st.subheader("📏 Free Distance Picking")
        st.write("Click anywhere on the **2D CAD Map** to record precise coordinates without snapping to pre-defined store nodes.")
        
        if st.button(get_text("reset_btn"), use_container_width=True):
            st.session_state.clicked_points = []
            st.rerun()

# Dynamic Header
st.title(get_text("title"))
st.caption(get_text("subtitle"))

# Main Tabs Setup
tab_home, tab_map, tab_dir, tab_park = st.tabs([
    "🏠 Overview Dashboard", 
    "🗺️ Interactive Map & Pick", 
    "📋 Turn-by-Turn Directions", 
    "🅿️ Parking Guidance"
])

# ------------------------------------------------------------------------------
# TAB 1: OVERVIEW DASHBOARD
# ------------------------------------------------------------------------------
with tab_home:
    col1, col2, col3 = st.columns(3)
    col1.metric(get_text("total_floors"), "4 Floors (GF - 3F)")
    col2.metric(get_text("total_pois"), f"{len(MOCK_NODES)} Locations")
    col3.metric(get_text("parking_spots"), "42 Available")
    
    st.markdown("---")
    
    st.markdown("""
    <div class="orange-card">
        <h4>💡 Map Usage Guide</h4>
        <ul>
            <li><b>Structured Navigation:</b> Pick start/end stores from the sidebar to calculate Dijkstra multi-floor paths.</li>
            <li><b>Free Click Distance:</b> Switch mode in the sidebar, open the 2D CAD view, and click any 2 exact spots to measure direct Euclidean distance!</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("🏬 View Full Store & POI Directory"):
        df_pois = pd.DataFrame.from_dict(MOCK_NODES, orient="index")
        st.dataframe(df_pois[["name", "category", "z", "x", "y"]], use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 2: INTERACTIVE MAP & FREE CLICK DISTANCE
# ------------------------------------------------------------------------------
with tab_map:
    # Compute standard route
    full_route_sequence = dijkstra_shortest_path(st.session_state.start_poi, st.session_state.dest_poi)

    # --------------------------------------------------------------------------
    # PINK BANNER INTEGRATION
    # --------------------------------------------------------------------------
    if st.session_state.nav_mode == get_text("mode_poi"):
        route_display_str = " ➔ ".join([
            f"<code>{format_location_label(loc, st.session_state.lang)}</code>"
            for loc in full_route_sequence
        ])
        
        st.markdown(
            f"""
            <div class="custom-route-banner">
                <strong>{get_text('current_route_lbl')}:</strong> {route_display_str}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        # Banner for Free-Click Mode
        picks_str = " ➔ ".join([
            f"<code>({p[0]:.1f}, {p[1]:.1f}, Floor {int(p[2])})</code>"
            for p in st.session_state.clicked_points
        ]) if st.session_state.clicked_points else "<i>None (Click on the 2D map below)</i>"

        st.markdown(
            f"""
            <div class="custom-route-banner">
                <strong>{get_text('free_click_lbl')}:</strong> {picks_str}
            </div>
            """,
            unsafe_allow_html=True
        )

    # Map Display Controls
    col_view, col_floor = st.columns([1, 1])
    with col_view:
        view_mode = st.radio("Display Projection", [get_text("view_2d"), get_text("view_3d")], horizontal=True)
    
    if view_mode == get_text("view_2d"):
        with col_floor:
            active_floor = st.selectbox(get_text("active_floor"), [0, 1, 2, 3], format_func=lambda x: f"Floor {x}")

        fig_2d = render_2d_cad_view(
            active_floor, 
            route_path=full_route_sequence if st.session_state.nav_mode == get_text("mode_poi") else None,
            picked_points=st.session_state.clicked_points
        )

        # ----------------------------------------------------------------------
        # STREAMLIT-PLOTLY-EVENTS INTEGRATION (Exact Click Distance Picker)
        # ----------------------------------------------------------------------
        if st.session_state.nav_mode == get_text("mode_free"):
            selected_data = plotly_events(fig_2d, click_event=True, override_height=550, key=f"plotly_2d_f{active_floor}")

            if selected_data:
                click_info = selected_data[0]
                click_x = click_info.get("x")
                click_y = click_info.get("y")

                if click_x is not None and click_y is not None:
                    new_point = (round(click_x, 2), round(click_y, 2), float(active_floor))

                    # Prevent duplicate sequential point registrations on rerenders
                    if not st.session_state.clicked_points or st.session_state.clicked_points[-1] != new_point:
                        st.session_state.clicked_points.append(new_point)
                        
                        # Restrict to last two exact points for point-to-point calculation
                        if len(st.session_state.clicked_points) > 2:
                            st.session_state.clicked_points = st.session_state.clicked_points[-2:]
                        st.rerun()
        else:
            st.plotly_chart(fig_2d, use_container_width=True)

    else:
        fig_3d = render_3d_isometric_view(
            route_path=full_route_sequence if st.session_state.nav_mode == get_text("mode_poi") else None
        )
        st.plotly_chart(fig_3d, use_container_width=True)

    # --------------------------------------------------------------------------
    # DISTANCE RESULTS DISPLAY
    # --------------------------------------------------------------------------
    st.markdown("---")
    
    if st.session_state.nav_mode == get_text("mode_free"):
        if len(st.session_state.clicked_points) == 1:
            st.info(f"📍 **Point 1 Picked**: {st.session_state.clicked_points[0]}. Click a second location on the map.")
        elif len(st.session_state.clicked_points) == 2:
            pt1, pt2 = st.session_state.clicked_points
            calc_dist = euclidean_distance_3d(pt1, pt2)
            
            st.success("📏 **Exact Free-Click Distance Calculated!**")
            m1, m2, m3 = st.columns(3)
            m1.metric("Direct Line Distance", f"{calc_dist:.2f} meters")
            m2.metric("Approx. Walk Steps", f"{int(calc_dist / 0.75)} steps")
            m3.metric("Floor Difference", f"{abs(pt1[2] - pt2[2]):.0f} floor(s)")
    else:
        tot_dist, f_changes, steps = compute_route_summary(full_route_sequence)
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Route Distance", f"{tot_dist} meters")
        m2.metric("Estimated Walk Steps", f"{steps} steps")
        m3.metric("Elevator/Escalator Transfers", f"{f_changes}")

# ------------------------------------------------------------------------------
# TAB 3: TURN-BY-TURN DIRECTIONS
# ------------------------------------------------------------------------------
with tab_dir:
    st.subheader("📋 Step-by-Step Directions")
    full_route_sequence = dijkstra_shortest_path(st.session_state.start_poi, st.session_state.dest_poi)
    
    if full_route_sequence:
        for idx, node_key in enumerate(full_route_sequence):
            node_info = MOCK_NODES[node_key]
            
            if idx == 0:
                st.markdown(f"🚩 **Start at**: `{node_info['name']}` (Floor {node_info['z']})")
            elif idx == len(full_route_sequence) - 1:
                st.markdown(f"🏁 **Arrive at**: `{node_info['name']}` (Floor {node_info['z']})")
            else:
                prev_node = MOCK_NODES[full_route_sequence[idx - 1]]
                if prev_node['z'] != node_info['z']:
                    st.markdown(f"🛗 **Take elevator/escalator** from Floor {prev_node['z']} to Floor {node_info['z']} (`{node_info['name']}`)")
                else:
                    st.markdown(f"➡️ Walk towards `{node_info['name']}`")
    else:
        st.warning("No route selected.")

# ------------------------------------------------------------------------------
# TAB 4: PARKING GUIDANCE
# ------------------------------------------------------------------------------
with tab_park:
    st.subheader("🅿️ Rooftop Parking Guidance System")
    st.write("Navigate from the mall main entrance directly to available parking spaces.")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("""
        <div class="orange-card">
            <h4>Slot P-12 Reserved</h4>
            <p>Status: <b>AVAILABLE</b></p>
            <p>Floor: Level 3 (Rooftop Deck)</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_p2:
        if st.button("Set Parking Slot P-12 as Destination", use_container_width=True):
            st.session_state.dest_poi = "ROOFTOP_PARK"
            st.session_state.nav_mode = get_text("mode_poi")
            st.success("Destination set to Rooftop Parking!")
            st.rerun()

# ==============================================================================
# 8. FOOTER
# ==============================================================================
st.markdown("---")
st.caption("Indoor Navigation & CAD Map Calculator App • Streamlit + Plotly Engine")
