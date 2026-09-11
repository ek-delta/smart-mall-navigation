import math
import heapq
import streamlit as st
import plotly.graph_objects as go
from geopy.distance import geodesic

# ==========================================
# 1. PAGE CONFIGURATION & LOCALIZATION
# ==========================================
st.set_page_config(
    page_title="Indoor Navigation & Map Distance Calculator",
    page_icon="🗺️",
    layout="wide"
)

# Translations dictionary
TRANSLATIONS = {
    "English": {
        "title": "🗺️ Indoor Navigation & Distance Calculator",
        "subtitle": "Calculate exact point-to-point map distance or navigate indoor facilities.",
        "tab_home": "🏠 Dashboard",
        "tab_map": "🗺️ Interactive Map",
        "tab_dir": "📋 Directions",
        "tab_park": "🅿️ Parking Guidance",
        "view_2d": "2D CAD View",
        "view_3d": "3D Isometric View",
        "active_floor": "Select Floor Layer",
        "measure_mode": "📍 Free-Click Distance Measurement",
        "route_mode": "🧭 Room-to-Room Pathfinding",
        "current_route_lbl": "Current Route",
        "calc_dist_lbl": "Point-to-Point Exact Distance",
        "reset_btn": "Reset Selection Points",
        "clear_picks": "Clear Clicked Points",
        "p1_sel": "Point 1 selected",
        "p2_sel": "Point 2 selected",
        "prompt_p2": "Click a second point on the map to calculate exact distance.",
        "dist_calc_success": "Distance Calculated!",
        "km_unit": "Kilometers (Geodesic)",
        "mi_unit": "Miles (Geodesic)",
        "euclidean_unit": "Euclidean Map Units",
        "no_route": "No route selected or target unreachable.",
    },
    "Español": {
        "title": "🗺️ Navegación Interior y Calculadora de Distancia",
        "subtitle": "Calcule la distancia exacta entre puntos o navegue por las instalaciones.",
        "tab_home": "🏠 Panel Principal",
        "tab_map": "🗺️ Mapa Interactivo",
        "tab_dir": "📋 Instrucciones",
        "tab_park": "🅿️ Guía de Estacionamiento",
        "view_2d": "Vista CAD 2D",
        "view_3d": "Vista Isométrica 3D",
        "active_floor": "Seleccionar Planta",
        "measure_mode": "📍 Medición de Distancia Libre",
        "route_mode": "🧭 Navegación entre Salas",
        "current_route_lbl": "Ruta Actual",
        "calc_dist_lbl": "Distancia Exacta Entre Puntos",
        "reset_btn": "Restablecer Puntos",
        "clear_picks": "Limpiar Selección",
        "p1_sel": "Punto 1 seleccionado",
        "p2_sel": "Punto 2 seleccionado",
        "prompt_p2": "Haga clic en un segundo punto para calcular la distancia.",
        "dist_calc_success": "¡Distancia Calculada!",
        "km_unit": "Kilómetros (Geodésica)",
        "mi_unit": "Millas (Geodésica)",
        "euclidean_unit": "Unidades de Mapa Euclídeas",
        "no_route": "No hay ruta seleccionada o el destino es inalcanzable.",
    }
}

# ==========================================
# 2. SESSION STATE INITIALIZATION
# ==========================================
if "lang" not in st.session_state:
    st.session_state.lang = "English"

if "clicked_points" not in st.session_state:
    st.session_state.clicked_points = []  # Stores free click tuples: (x, y, floor)

if "start_node" not in st.session_state:
    st.session_state.start_node = "GF_LOBBY"

if "dest_node" not in st.session_state:
    st.session_state.dest_node = "2F_RESTROOM"

if "map_mode" not in st.session_state:
    st.session_state.map_mode = "Measure"

t = TRANSLATIONS[st.session_state.lang]

# ==========================================
# 3. GLOBAL CUSTOM CSS & THEME STYLING
# ==========================================
st.markdown(
    """
    <style>
    /* Primary Action & Brand Styling */
    .stButton>button {
        background-color: #D32F2F;
        color: white;
        border-radius: 6px;
        font-weight: 600;
        border: none;
    }
    .stButton>button:hover {
        background-color: #B71C1C;
        color: white;
    }

    /* Orange Side Cards / Highlight Containers */
    .orange-card {
        background-color: #FFF3E0;
        border-left: 5px solid #FF6700;
        padding: 14px;
        border-radius: 6px;
        margin-bottom: 12px;
    }
    
    /* Custom Pink Route Summary Container */
    .pink-route-banner {
        background-color: #E91E63;
        color: #FFFFFF;
        padding: 12px 16px;
        border-radius: 8px;
        font-size: 0.95rem;
        margin-top: 10px;
        margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.15);
    }
    
    /* Style code elements inside custom pink route banner */
    .pink-route-banner code {
        background-color: rgba(255, 255, 255, 0.25) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================
# 4. ORIGINAL STORES & POI DATASETS (UNTOUCHED)
# ==========================================
NODES = {
    "GF_LOBBY": {"name": "Main Entrance Lobby", "floor": 0, "x": 10.0, "y": 10.0, "z": 0.0, "cat": "Lobby"},
    "GF_INFO": {"name": "Information Desk", "floor": 0, "x": 25.0, "y": 20.0, "z": 0.0, "cat": "Service"},
    "GF_ELEVATOR": {"name": "Ground Floor Elevator", "floor": 0, "x": 50.0, "y": 50.0, "z": 0.0, "cat": "Transport"},
    "1F_ELEVATOR": {"name": "First Floor Elevator", "floor": 1, "x": 50.0, "y": 50.0, "z": 4.0, "cat": "Transport"},
    "1F_CAFE": {"name": "Central Cafe", "floor": 1, "x": 70.0, "y": 30.0, "z": 4.0, "cat": "Dining"},
    "1F_STORE_A": {"name": "Tech World Store", "floor": 1, "x": 30.0, "y": 80.0, "z": 4.0, "cat": "Retail"},
    "2F_ELEVATOR": {"name": "Second Floor Elevator", "floor": 2, "x": 50.0, "y": 50.0, "z": 8.0, "cat": "Transport"},
    "2F_RESTROOM": {"name": "Restroom Hub 2F", "floor": 2, "x": 85.0, "y": 85.0, "z": 8.0, "cat": "Amenity"},
    "2F_CINEMA": {"name": "Multiplex Cinema", "floor": 2, "x": 20.0, "y": 60.0, "z": 8.0, "cat": "Entertainment"},
    "R_PARKING_ENTRANCE": {"name": "Rooftop Deck Entrance", "floor": 3, "x": 50.0, "y": 50.0, "z": 12.0, "cat": "Parking"},
    "R_SLOT_A1": {"name": "Parking Slot A1", "floor": 3, "x": 15.0, "y": 25.0, "z": 12.0, "cat": "Parking Slot"},
    "R_SLOT_B4": {"name": "Parking Slot B4", "floor": 3, "x": 80.0, "y": 75.0, "z": 12.0, "cat": "Parking Slot"},
}

GRAPH = {
    "GF_LOBBY": ["GF_INFO"],
    "GF_INFO": ["GF_LOBBY", "GF_ELEVATOR"],
    "GF_ELEVATOR": ["GF_INFO", "1F_ELEVATOR"],
    "1F_ELEVATOR": ["GF_ELEVATOR", "1F_CAFE", "1F_STORE_A", "2F_ELEVATOR"],
    "1F_CAFE": ["1F_ELEVATOR"],
    "1F_STORE_A": ["1F_ELEVATOR"],
    "2F_ELEVATOR": ["1F_ELEVATOR", "2F_RESTROOM", "2F_CINEMA", "R_PARKING_ENTRANCE"],
    "2F_RESTROOM": ["2F_ELEVATOR"],
    "2F_CINEMA": ["2F_ELEVATOR"],
    "R_PARKING_ENTRANCE": ["2F_ELEVATOR", "R_SLOT_A1", "R_SLOT_B4"],
    "R_SLOT_A1": ["R_PARKING_ENTRANCE"],
    "R_SLOT_B4": ["R_PARKING_ENTRANCE"],
}

MAP_GEO_REF = {
    "lat_base": 3.1390,
    "lon_base": 101.6869,
    "scale": 0.0001
}

# ==========================================
# 5. HELPER FUNCTIONS & PATHFINDING
# ==========================================
def format_location_label(node_key, lang="English"):
    """Formats location identifiers with clean floor badges."""
    node = NODES.get(node_key, {})
    name = node.get("name", node_key)
    flr = node.get("floor", 0)
    flr_str = "GF" if flr == 0 else f"{flr}F" if flr < 3 else "R"
    return f"[{flr_str}] {name}"

def compute_3d_distance(n1_key, n2_key):
    """Calculates Euclidean distance between two node keys."""
    p1, p2 = NODES[n1_key], NODES[n2_key]
    return math.sqrt((p1['x'] - p2['x'])**2 + (p1['y'] - p2['y'])**2 + (p1['z'] - p2['z'])**2)

def theta_star_3d(start_key, target_key):
    """3D Pathfinding algorithm returning sequence of node keys."""
    open_set = []
    heapq.heappush(open_set, (0, start_key))
    came_from = {}
    g_score = {node: float('inf') for node in NODES}
    g_score[start_key] = 0

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == target_key:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]

        for neighbor in GRAPH.get(current, []):
            tentative_g = g_score[current] + compute_3d_distance(current, neighbor)
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + compute_3d_distance(neighbor, target_key)
                heapq.heappush(open_set, (f_score, neighbor))
    return []

def node_to_geo(x, y):
    """Converts local CAD (x, y) coordinates to Lat/Lon for distance calculation."""
    lat = MAP_GEO_REF["lat_base"] + (y * MAP_GEO_REF["scale"])
    lon = MAP_GEO_REF["lon_base"] + (x * MAP_GEO_REF["scale"])
    return (lat, lon)

def render_orange_card(title, content):
    """Custom UI component rendering an orange highlighted card."""
    st.markdown(
        f"""
        <div class="orange-card">
            <h4 style="margin:0 0 8px 0; color:#FF6700;">{title}</h4>
            <div>{content}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================
# 6. UNTOUCHED CAD & MAP LAYOUT RENDERING
# ==========================================
def render_2d_cad_view(floor_num, route_nodes=None, clicked_points=None):
    """Generates 2D Plotly figure preserving the exact CAD map layout."""
    fig = go.Figure()

    # Outer Building Perimeter
    fig.add_trace(go.Scatter(
        x=[0, 100, 100, 0, 0],
        y=[0, 0, 100, 100, 0],
        mode="lines",
        line=dict(color="#B0BEC5", width=3),
        name="Floor Boundary"
    ))

    # Render Floor Nodes & Labels
    floor_nodes = {k: v for k, v in NODES.items() if v["floor"] == floor_num}
    if floor_nodes:
        fig.add_trace(go.Scatter(
            x=[v["x"] for v in floor_nodes.values()],
            y=[v["y"] for v in floor_nodes.values()],
            mode="markers+text",
            marker=dict(size=14, color="#1976D2"),
            text=[v["name"] for v in floor_nodes.values()],
            textposition="top center",
            name="Locations"
        ))

    # Overlay Room-to-Room Path (if active)
    if route_nodes:
        r_x = [NODES[k]["x"] for k in route_nodes if NODES[k]["floor"] == floor_num]
        r_y = [NODES[k]["y"] for k in route_nodes if NODES[k]["floor"] == floor_num]
        if len(r_x) > 1:
            fig.add_trace(go.Scatter(
                x=r_x, y=r_y,
                mode="lines+markers",
                line=dict(color="#D32F2F", width=4),
                marker=dict(size=8, color="#D32F2F"),
                name="Calculated Path"
            ))

    # Overlay Exact Picked Points & Distance Line
    if clicked_points:
        cp_x = [p[0] for p in clicked_points if len(p) < 3 or p[2] == floor_num]
        cp_y = [p[1] for p in clicked_points if len(p) < 3 or p[2] == floor_num]
        if cp_x:
            fig.add_trace(go.Scatter(
                x=cp_x, y=cp_y,
                mode="markers+lines",
                marker=dict(size=12, color="#E91E63", symbol="cross"),
                line=dict(width=3, color="#E91E63", dash="dash"),
                name="Exact Clicked Points"
            ))

    fig.update_layout(
        xaxis=dict(range=[-5, 105], showgrid=True, zeroline=False),
        yaxis=dict(range=[-5, 105], showgrid=True, zeroline=False, scaleanchor="x", scaleratio=1),
        margin=dict(l=10, r=10, b=10, t=10),
        height=600,
        showlegend=True,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FAFAFA"
    )
    return fig

def render_3d_isometric_view(route_nodes=None):
    """Renders 3D isometric representation (Layout untouched)."""
    fig = go.Figure()

    # Draw floor planes
    for flr in range(4):
        z_val = flr * 4
        fig.add_trace(go.Mesh3d(
            x=[0, 100, 100, 0],
            y=[0, 0, 100, 100],
            z=[z_val, z_val, z_val, z_val],
            opacity=0.1,
            color="#90A4AE",
            name=f"Floor {flr}"
        ))

    # Draw Nodes
    x_n = [v["x"] for v in NODES.values()]
    y_n = [v["y"] for v in NODES.values()]
    z_n = [v["z"] for v in NODES.values()]
    txt = [v["name"] for v in NODES.values()]

    fig.add_trace(go.Scatter3d(
        x=x_n, y=y_n, z=z_n,
        mode="markers+text",
        marker=dict(size=6, color="#1976D2"),
        text=txt,
        textposition="top center",
        name="Nodes"
    ))

    # Draw Route Path
    if route_nodes:
        rx = [NODES[k]["x"] for k in route_nodes]
        ry = [NODES[k]["y"] for k in route_nodes]
        rz = [NODES[k]["z"] for k in route_nodes]
        fig.add_trace(go.Scatter3d(
            x=rx, y=ry, z=rz,
            mode="lines+markers",
            line=dict(color="#D32F2F", width=6),
            marker=dict(size=8, color="#D32F2F"),
            name="Active Route"
        ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[0, 100]),
            yaxis=dict(range=[0, 100]),
            zaxis=dict(range=[0, 16]),
            aspectratio=dict(x=1, y=1, z=0.4)
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        height=650
    )
    return fig

# ==========================================
# 7. MAIN LAYOUT & STREAMLIT APP STRUCTURE
# ==========================================
st.sidebar.title("🌐 Settings & Preferences")
st.session_state.lang = st.sidebar.selectbox("Language / Idioma", options=["English", "Español"])

st.title(t["title"])
st.caption(t["subtitle"])

tab_home, tab_map, tab_dir, tab_park = st.tabs([
    t["tab_home"], t["tab_map"], t["tab_dir"], t["tab_park"]
])

# ------------------------------------------
# TAB 1: DASHBOARD
# ------------------------------------------
with tab_home:
    st.subheader("System Overview")
    
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Total Defined POIs", len(NODES))
    col_b.metric("Floors Mapped", "4 (GF, 1F, 2F, Rooftop)")
    col_c.metric("Active Parking Slots", "2 Available")
    
    st.write("---")
    
    render_orange_card(
        "Interactive Dual-Mode Navigation",
        "Switch seamlessly between point-and-click distance measurement or room-to-room pathfinding."
    )
    
    with st.expander("📂 View Location Directory"):
        for k, v in NODES.items():
            st.write(f"• **{format_location_label(k, st.session_state.lang)}** - Category: `{v['cat']}` (X: {v['x']}, Y: {v['y']})")

# ------------------------------------------
# TAB 2: INTERACTIVE MAP (WITH PINK BANNER & NATIVE CLICKS)
# ------------------------------------------
with tab_map:
    col_ctrl1, col_ctrl2 = st.columns([2, 2])
    
    with col_ctrl1:
        st.session_state.map_mode = st.radio(
            "Select Interaction Mode",
            options=[t["measure_mode"], t["route_mode"]],
            horizontal=True
        )

    with col_ctrl2:
        view_type = st.radio(
            "Visualization Mode",
            options=[t["view_2d"], t["view_3d"]],
            horizontal=True
        )

    full_route_sequence = []
    
    # --------------------------------------
    # ROOM-TO-ROOM ROUTE MODE
    # --------------------------------------
    if t["route_mode"] in st.session_state.map_mode:
        c1, c2 = st.columns(2)
        with c1:
            st.session_state.start_node = st.selectbox(
                "Starting Point",
                options=list(NODES.keys()),
                format_func=lambda x: format_location_label(x, st.session_state.lang),
                index=0
            )
        with c2:
            st.session_state.dest_node = st.selectbox(
                "Destination Point",
                options=list(NODES.keys()),
                format_func=lambda x: format_location_label(x, st.session_state.lang),
                index=7
            )

        full_route_sequence = theta_star_3d(st.session_state.start_node, st.session_state.dest_node)

        # Pink background with white text banner for room-to-room navigation
        if full_route_sequence:
            route_display_str = " ➔ ".join([
                f"<code>{format_location_label(loc, st.session_state.lang)}</code>"
                for loc in full_route_sequence
            ])

            st.markdown(
                f"""
                <div class="pink-route-banner">
                    <strong>{t['current_route_lbl']}:</strong> {route_display_str}
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.warning(t["no_route"])

    # --------------------------------------
    # RENDER MAP VIEWS (NATIVE EVENT HANDLING)
    # --------------------------------------
    if view_type == t["view_2d"]:
        selected_floor = st.slider("Select Floor Level", min_value=0, max_value=3, value=0, format="Floor %d")
        
        fig_2d = render_2d_cad_view(
            floor_num=selected_floor,
            route_nodes=full_route_sequence if t["route_mode"] in st.session_state.map_mode else None,
            clicked_points=st.session_state.clicked_points if t["measure_mode"] in st.session_state.map_mode else None
        )

        # Native Streamlit Chart Render with Selection Event Listener
        map_event = st.plotly_chart(
            fig_2d,
            use_container_width=True,
            on_select="rerun",
            selection_mode="points",
            key=f"native_map_floor_{selected_floor}"
        )

        # Extract selected coordinates in free measurement mode
        if t["measure_mode"] in st.session_state.map_mode and map_event:
            selection_data = map_event.get("selection", {}).get("points", [])
            if selection_data:
                pt_info = selection_data[0]
                raw_x = pt_info.get("x")
                raw_y = pt_info.get("y")

                if raw_x is not None and raw_y is not None:
                    new_pt = (round(raw_x, 2), round(raw_y, 2), selected_floor)
                    if not st.session_state.clicked_points or st.session_state.clicked_points[-1] != new_pt:
                        st.session_state.clicked_points.append(new_pt)
                        if len(st.session_state.clicked_points) > 2:
                            st.session_state.clicked_points = st.session_state.clicked_points[-2:]
                        st.rerun()

    else:
        # 3D Isometric View Render
        fig_3d = render_3d_isometric_view(
            route_nodes=full_route_sequence if t["route_mode"] in st.session_state.map_mode else None
        )
        st.plotly_chart(fig_3d, use_container_width=True)

    # --------------------------------------
    # FREE-CLICK DISTANCE RESULTS & PINK BANNER
    # --------------------------------------
    if t["measure_mode"] in st.session_state.map_mode:
        st.write("---")
        st.subheader(f"📏 {t['calc_dist_lbl']}")
        
        pts = st.session_state.clicked_points
        if len(pts) == 1:
            st.info(f"📍 **{t['p1_sel']}**: X={pts[0][0]}, Y={pts[0][1]} (Floor {pts[0][2]})")
            st.warning(t["prompt_p2"])

        elif len(pts) == 2:
            p1, p2 = pts[0], pts[1]
            
            # Map distance (Euclidean in CAD units)
            euclidean_dist = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 + ((p2[2] - p1[2]) * 4)**2)
            
            # Real-world Geodesic calculation
            geo_p1 = node_to_geo(p1[0], p1[1])
            geo_p2 = node_to_geo(p2[0], p2[1])
            dist_km = geodesic(geo_p1, geo_p2).kilometers
            dist_mi = geodesic(geo_p1, geo_p2).miles

            st.success(f"📏 **{t['dist_calc_success']}**")
            
            res_col1, res_col2, res_col3 = st.columns(3)
            res_col1.metric(t["euclidean_unit"], f"{euclidean_dist:.2f} m")
            res_col2.metric(t["km_unit"], f"{dist_km:.4f} km")
            res_col3.metric(t["mi_unit"], f"{dist_mi:.4f} mi")

            # Route Path Display overlay in Pink Banner (for exact clicked points)
            click_route_str = f"<code>Point 1 (X:{p1[0]}, Y:{p1[1]})</code> ➔ <code>Point 2 (X:{p2[0]}, Y:{p2[1]})</code>"
            st.markdown(
                f"""
                <div class="pink-route-banner">
                    <strong>{t['current_route_lbl']}:</strong> {click_route_str}
                </div>
                """,
                unsafe_allow_html=True,
            )

        if st.button(t["clear_picks"]):
            st.session_state.clicked_points = []
            st.rerun()

# ------------------------------------------
# TAB 3: DIRECTIONS & TURN-BY-TURN
# ------------------------------------------
with tab_dir:
    st.subheader("📋 Step-by-Step Directions")
    
    if full_route_sequence and len(full_route_sequence) > 1:
        for idx in range(len(full_route_sequence) - 1):
            curr_n = full_route_sequence[idx]
            next_n = full_route_sequence[idx + 1]
            dist = compute_3d_distance(curr_n, next_n)
            
            st.markdown(f"**Step {idx + 1}:** Proceed from **{format_location_label(curr_n, st.session_state.lang)}** to **{format_location_label(next_n, st.session_state.lang)}**")
            st.caption(f"Segment distance: {dist:.1f} meters")
            st.divider()
    else:
        st.info("Select a route in the Interactive Map tab to generate turn-by-turn directions.")

# ------------------------------------------
# TAB 4: PARKING GUIDANCE
# ------------------------------------------
with tab_park:
    st.subheader("🅿️ Rooftop Parking Direct Navigation")
    
    park_slot = st.selectbox(
        "Select Target Parking Slot",
        options=["R_SLOT_A1", "R_SLOT_B4"],
        format_func=lambda x: format_location_label(x, st.session_state.lang)
    )
    
    if st.button("Guide Me to Selected Slot"):
        st.session_state.start_node = "GF_LOBBY"
        st.session_state.dest_node = park_slot
        st.session_state.map_mode = t["route_mode"]
        st.success(f"Route set to {format_location_label(park_slot, st.session_state.lang)}! Switch to Interactive Map tab to view standard path.")

# ==========================================
# 8. FOOTER METADATA
# ==========================================
st.write("---")
st.caption("Indoor Navigation Engine v2.5 • Native Streamlit & Plotly Integration")
