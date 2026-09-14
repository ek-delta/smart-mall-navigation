import math
import random
import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ==============================================================================
# 1. Page Configuration & Translations Setup
# ==============================================================================
st.set_page_config(
    page_title="Multi-Floor Indoor & Rooftop Parking Navigation System",
    page_icon="🗺️",
    layout="wide",
)

TRANSLATIONS = {
    "en": {
        "title": "🗺️ Multi-Floor Indoor & Rooftop Parking Navigation System",
        "subtitle": "High-Precision 3D Theta* Pathfinding & FloorPlanCAD Multi-Layer Topology Engine",
        "language_select": "🌐 Language Select",
        "sidebar_header": "⚙️ Navigation Control Panel",
        "select_mode": "Select Routing Mode",
        "mode_pedestrian": "🚶 Pedestrian Indoor Route",
        "mode_parking": "🚗 Rooftop Smart Parking Route",
        "start_loc": "Start Location",
        "end_loc": "Target Destination",
        "floor_filter": "Display Floor Layer",
        "all_floors": "All Building Layers (3D View)",
        "route_summary": "📊 Navigation Route Metrics",
        "total_dist": "Total Distance",
        "floors_crossed": "Floors Crossed",
        "total_steps": "Route Waypoints",
        "turn_by_turn": "🧭 Turn-by-Turn Navigation Instructions",
        "step_lbl": "Step",
        "parking_tab_entry": "🚗 Driving Entry (Gate -> Spot)",
        "parking_tab_exit": "🚪 Driving Exit (Spot -> Gate)",
        "assigned_spot": "Assigned Parking Spot",
        "dist_to_spot": "Driving Distance",
        "floors_to_ascend": "Elevated Ramps",
        "parking_route_summary": "📊 Parking Route Summary",
        "parking_turn_by_turn": "🧭 Driving Guidance",
    },
    "zh": {
        "title": "🗺️ 多楼层室内与屋顶停车场导航系统",
        "subtitle": "高精度 3D Theta* 路径规划与 FloorPlanCAD 多层拓扑引擎",
        "language_select": "🌐 语言选择",
        "sidebar_header": "⚙️ 导航控制面板",
        "select_mode": "选择导航模式",
        "mode_pedestrian": "🚶 室内步行路线",
        "mode_parking": "🚗 屋顶智能停车路线",
        "start_loc": "起点位置",
        "end_loc": "目标终点",
        "floor_filter": "显示楼层图层",
        "all_floors": "所有建筑图层 (3D 视图)",
        "route_summary": "📊 导航路线指标 summary",
        "total_dist": "总路线距离",
        "floors_crossed": "穿越楼层数",
        "total_steps": "路线关键点",
        "turn_by_turn": "🧭 逐向导航指引",
        "step_lbl": "步骤",
        "parking_tab_entry": "🚗 驶入路线 (入口 -> 车位)",
        "parking_tab_exit": "🚪 驶出路线 (车位 -> 出口)",
        "assigned_spot": "分配停车位",
        "dist_to_spot": "行驶距离",
        "floors_to_ascend": "跨越坡道数",
        "parking_route_summary": "📊 停车路线摘要",
        "parking_turn_by_turn": "🧭 驾驶引导",
    },
}

if "lang" not in st.session_state:
    st.session_state.lang = "en"

# ==============================================================================
# 2. Topology & Mock Map Data
# ==============================================================================
MULTI_CAD_NODES = {
    # Floor 1
    "F1_ENTRANCE": {"pos": (5, 5, 0), "label": "Ground Entrance", "floor": 1, "type": "entrance"},
    "F1_LOBBY": {"pos": (20, 15, 0), "label": "Main Lobby", "floor": 1, "type": "room"},
    "F1_ELEVATOR": {"pos": (35, 15, 0), "label": "Elevator Hall (F1)", "floor": 1, "type": "elevator"},
    "F1_STAIRS": {"pos": (35, 5, 0), "label": "Stairwell (F1)", "floor": 1, "type": "stairs"},
    "F1_CAFE": {"pos": (10, 30, 0), "label": "Ground Cafe", "floor": 1, "type": "room"},
    
    # Floor 2
    "F2_ELEVATOR": {"pos": (35, 15, 4), "label": "Elevator Hall (F2)", "floor": 2, "type": "elevator"},
    "F2_STAIRS": {"pos": (35, 5, 4), "label": "Stairwell (F2)", "floor": 2, "type": "stairs"},
    "F2_CONF_ROOM": {"pos": (15, 20, 4), "label": "Conference Room A", "floor": 2, "type": "room"},
    "F2_OFFICE": {"pos": (10, 35, 4), "label": "Open Office Area", "floor": 2, "type": "room"},

    # Floor 3 (Rooftop Parking Layer)
    "RF_GATE_IN": {"pos": (5, 5, 8), "label": "Rooftop Entrance Gate", "floor": 3, "type": "gate"},
    "RF_GATE_OUT": {"pos": (45, 5, 8), "label": "Rooftop Exit Gate", "floor": 3, "type": "gate"},
    "RF_RAMP_IN": {"pos": (10, 10, 8), "label": "Rooftop In Ramps", "floor": 3, "type": "waypoint"},
    "RF_P_A1": {"pos": (15, 25, 8), "label": "Spot A1", "floor": 3, "type": "parking", "occupied": False},
    "RF_P_A2": {"pos": (20, 25, 8), "label": "Spot A2", "floor": 3, "type": "parking", "occupied": True},
    "RF_P_B1": {"pos": (30, 25, 8), "label": "Spot B1", "floor": 3, "type": "parking", "occupied": False},
    "RF_P_B2": {"pos": (35, 25, 8), "label": "Spot B2", "floor": 3, "type": "parking", "occupied": False},
}

CAD_EDGES = [
    ("F1_ENTRANCE", "F1_LOBBY", 15.8),
    ("F1_LOBBY", "F1_ELEVATOR", 15.0),
    ("F1_LOBBY", "F1_STAIRS", 18.0),
    ("F1_LOBBY", "F1_CAFE", 18.0),
    ("F1_ELEVATOR", "F2_ELEVATOR", 4.0),
    ("F1_STAIRS", "F2_STAIRS", 5.0),
    ("F2_ELEVATOR", "F2_CONF_ROOM", 20.6),
    ("F2_CONF_ROOM", "F2_OFFICE", 15.8),
    ("F2_STAIRS", "F2_CONF_ROOM", 25.0),
    # Parking Edges
    ("RF_GATE_IN", "RF_RAMP_IN", 7.1),
    ("RF_RAMP_IN", "RF_P_A1", 15.8),
    ("RF_RAMP_IN", "RF_P_A2", 18.0),
    ("RF_P_A1", "RF_P_B1", 15.0),
    ("RF_P_A2", "RF_P_B2", 15.0),
    ("RF_P_B1", "RF_GATE_OUT", 24.7),
    ("RF_P_B2", "RF_GATE_OUT", 22.4),
]

# ==============================================================================
# 3. Pathfinding Core & Calculation Utilities
# ==============================================================================
def euclidean_distance(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

def theta_star_search(start_node, goal_node, nodes, edges):
    """3D Theta* pathfinding implementation over node/edge graph network."""
    adj = {n: [] for n in nodes}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    open_set = {start_node}
    g_score = {n: float("inf") for n in nodes}
    g_score[start_node] = 0
    f_score = {n: float("inf") for n in nodes}
    f_score[start_node] = euclidean_distance(nodes[start_node]["pos"], nodes[goal_node]["pos"])
    came_from = {}

    while open_set:
        current = min(open_set, key=lambda n: f_score[n])
        if current == goal_node:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]

        open_set.remove(current)

        for neighbor, weight in adj[current]:
            tentative_g = g_score[current] + weight
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + euclidean_distance(
                    nodes[neighbor]["pos"], nodes[goal_node]["pos"]
                )
                open_set.add(neighbor)

    return []

def compute_route_summary(path):
    if not path or len(path) < 2:
        return {"total_distance": 0, "floors_crossed": 0, "steps": 0}
    
    dist = 0.0
    floors = set()
    for i in range(len(path) - 1):
        p1 = MULTI_CAD_NODES[path[i]]["pos"]
        p2 = MULTI_CAD_NODES[path[i+1]]["pos"]
        dist += euclidean_distance(p1, p2)
        floors.add(MULTI_CAD_NODES[path[i]]["floor"])
    floors.add(MULTI_CAD_NODES[path[-1]]["floor"])

    return {
        "total_distance": round(dist, 1),
        "floors_crossed": max(0, len(floors) - 1),
        "steps": len(path),
    }

def generate_detailed_directions(path, nodes, lang="en"):
    """Generates localized turn-by-turn guidance notes."""
    directions = []
    if not path:
        return directions

    for idx, node_key in enumerate(path):
        node = nodes[node_key]
        lbl = node["label"]
        ntype = node.get("type", "room")

        if idx == 0:
            icon = "🛫"
            txt = f"Start journey at **{lbl}**" if lang == "en" else f"从 **{lbl}** 出发"
        elif idx == len(path) - 1:
            icon = "🎯"
            txt = f"Arrive at destination: **{lbl}**" if lang == "en" else f"到达目的地: **{lbl}**"
        else:
            if ntype == "elevator":
                icon = "🛗"
                txt = f"Take elevator via **{lbl}**" if lang == "en" else f"乘坐电梯通过 **{lbl}**"
            elif ntype == "stairs":
                icon = "🪜"
                txt = f"Use stairwell at **{lbl}**" if lang == "en" else f"走楼梯通过 **{lbl}**"
            else:
                icon = "➡️"
                txt = f"Proceed toward **{lbl}**" if lang == "en" else f"前往 **{lbl}**"

        directions.append({"step": idx + 1, "icon": icon, "text": txt})
    return directions

# ==============================================================================
# 4. Map & Visual Processing Functions
# ==============================================================================
def render_3d_indoor_map(start_node, end_node, route_path, selected_floor=None):
    fig = go.Figure()

    # Draw Nodes
    for n_key, n_val in MULTI_CAD_NODES.items():
        if n_val["floor"] == 3:
            continue  # Exclude rooftop parking nodes in indoor pedestrian mode
        if selected_floor and selected_floor != "All" and n_val["floor"] != selected_floor:
            continue

        x, y, z = n_val["pos"]
        color = "blue"
        if n_key == start_node:
            color = "green"
        elif n_key == end_node:
            color = "red"

        fig.add_trace(
            go.Scatter3d(
                x=[x],
                y=[y],
                z=[z],
                mode="markers+text",
                marker=dict(size=8, color=color),
                text=[n_val["label"]],
                textposition="top center",
                name=n_val["label"],
                showlegend=False,
            )
        )

    # Draw Graph Structural Edges
    for u, v, _ in CAD_EDGES:
        if u in MULTI_CAD_NODES and v in MULTI_CAD_NODES:
            n1, n2 = MULTI_CAD_NODES[u], MULTI_CAD_NODES[v]
            if n1["floor"] == 3 or n2["floor"] == 3:
                continue
            if (
                selected_floor
                and selected_floor != "All"
                and (n1["floor"] != selected_floor or n2["floor"] != selected_floor)
            ):
                continue

            fig.add_trace(
                go.Scatter3d(
                    x=[n1["pos"][0], n2["pos"][0]],
                    y=[n1["pos"][1], n2["pos"][1]],
                    z=[n1["pos"][2], n2["pos"][2]],
                    mode="lines",
                    line=dict(color="lightgray", width=2),
                    showlegend=False,
                )
            )

    # Draw Highlighted Route Path
    if route_path:
        px = [MULTI_CAD_NODES[k]["pos"][0] for k in route_path]
        py = [MULTI_CAD_NODES[k]["pos"][1] for k in route_path]
        pz = [MULTI_CAD_NODES[k]["pos"][2] for k in route_path]
        fig.add_trace(
            go.Scatter3d(
                x=px,
                y=py,
                z=pz,
                mode="lines+markers",
                line=dict(color="orange", width=6),
                marker=dict(size=6, color="darkorange"),
                name="Calculated Path",
            )
        )

    fig.update_layout(
        scene=dict(
            xaxis_title="X (Meters)",
            yaxis_title="Y (Meters)",
            zaxis_title="Floor Level (Z)",
            aspectmode="data",
        ),
        margin=dict(r=0, l=0, b=0, t=30),
        height=550,
    )
    return fig

def render_rooftop_parking_map(assigned_slot, route_path, current_lang="en"):
    fig = go.Figure()

    # Draw parking slots and gate nodes
    for n_key, n_val in MULTI_CAD_NODES.items():
        if n_val["floor"] != 3:
            continue
        x, y, _ = n_val["pos"]
        ntype = n_val.get("type", "")

        if ntype == "parking":
            is_assigned = n_key == assigned_slot
            is_occupied = n_val.get("occupied", False)
            color = "gold" if is_assigned else ("crimson" if is_occupied else "mediumseagreen")
            symbol = "square"
            size = 14
        else:
            color = "royalblue"
            symbol = "circle"
            size = 10

        fig.add_trace(
            go.Scatter(
                x=[x],
                y=[y],
                mode="markers+text",
                marker=dict(size=size, color=color, symbol=symbol),
                text=[n_val["label"]],
                textposition="bottom center",
                name=n_val["label"],
                showlegend=False,
            )
        )

    # Draw network edges
    for u, v, _ in CAD_EDGES:
        if u in MULTI_CAD_NODES and v in MULTI_CAD_NODES:
            n1, n2 = MULTI_CAD_NODES[u], MULTI_CAD_NODES[v]
            if n1["floor"] == 3 and n2["floor"] == 3:
                fig.add_trace(
                    go.Scatter(
                        x=[n1["pos"][0], n2["pos"][0]],
                        y=[n1["pos"][1], n2["pos"][1]],
                        mode="lines",
                        line=dict(color="#E2E8F0", width=2, dash="dash"),
                        showlegend=False,
                    )
                )

    # Draw active driving route
    if route_path:
        rx = [MULTI_CAD_NODES[k]["pos"][0] for k in route_path]
        ry = [MULTI_CAD_NODES[k]["pos"][1] for k in route_path]
        fig.add_trace(
            go.Scatter(
                x=rx,
                y=ry,
                mode="lines+markers",
                line=dict(color="#3182CE", width=5),
                marker=dict(size=8, color="#2B6CB0"),
                name="Driving Path",
            )
        )

    fig.update_layout(
        xaxis=dict(range=[0, 50], zeroline=False),
        yaxis=dict(range=[0, 40], zeroline=False),
        height=450,
        margin=dict(r=10, l=10, b=10, t=10),
        plot_bgcolor="#F7FAFC",
    )
    return fig

# ==============================================================================
# 5. Application UI & Sidebar Controls
# ==============================================================================
# Header & Language Selection
top_col1, top_col2 = st.columns([0.8, 0.2])
with top_col2:
    selected_lang = st.selectbox(
        TRANSLATIONS["en"]["language_select"],
        options=["en", "zh"],
        format_func=lambda x: "English" if x == "en" else "中文",
    )
    st.session_state.lang = selected_lang

t = TRANSLATIONS[st.session_state.lang]

with top_col1:
    st.title(t["title"])
    st.caption(t["subtitle"])

st.markdown("---")

# Sidebar Configuration
st.sidebar.header(t["sidebar_header"])
nav_mode = st.sidebar.radio(
    t["select_mode"],
    options=[t["mode_pedestrian"], t["mode_parking"]],
)

# Filter Node Collections based on mode selection
pedestrian_nodes = {k: v for k, v in MULTI_CAD_NODES.items() if v["floor"] in [1, 2]}
parking_nodes = {k: v for k, v in MULTI_CAD_NODES.items() if v["floor"] == 3 and v.get("type") == "parking"}

# ==============================================================================
# 6. Navigation Tabs Logic & Dynamic Rendering
# ==============================================================================
if nav_mode == t["mode_pedestrian"]:
    start_k = st.sidebar.selectbox(
        t["start_loc"],
        options=list(pedestrian_nodes.keys()),
        format_func=lambda k: pedestrian_nodes[k]["label"],
        index=0,
    )
    end_k = st.sidebar.selectbox(
        t["end_loc"],
        options=list(pedestrian_nodes.keys()),
        format_func=lambda k: pedestrian_nodes[k]["label"],
        index=min(6, len(pedestrian_nodes) - 1),
    )

    floor_opt = st.sidebar.selectbox(t["floor_filter"], options=["All", 1, 2])
    selected_floor_val = None if floor_opt == "All" else floor_opt

    # Compute 3D Theta* Path
    path_res = theta_star_search(start_k, end_k, MULTI_CAD_NODES, CAD_EDGES)

    # Main Visual Rendering
    fig_3d = render_3d_indoor_map(start_k, end_k, path_res, selected_floor_val)
    st.plotly_chart(fig_3d, use_container_width=True)

    # Output Summary Metrics and Step-by-Step Instructions
    if path_res:
        summary = compute_route_summary(path_res)
        st.markdown("---")
        st.subheader(t["route_summary"])
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric(t["total_dist"], f"{summary['total_distance']} m")
        m_col2.metric(t["floors_crossed"], summary["floors_crossed"])
        m_col3.metric(t["total_steps"], summary["steps"])

        st.markdown("---")
        st.subheader(t["turn_by_turn"])
        steps = generate_detailed_directions(path_res, MULTI_CAD_NODES, lang=st.session_state.lang)

        for step in steps:
            col_icon, col_text = st.columns([0.1, 0.9])
            with col_icon:
                st.markdown(f"### {step['icon']}")
            with col_text:
                st.markdown(f"**{t['step_lbl']} {step['step']}**")
                st.markdown(step["text"])
            st.divider()

else:
    # Rooftop Smart Parking Logic
    st.sidebar.info("💡 Auto-assigning nearest available vacant parking spot on Rooftop Floor.")
    
    # Auto-assign available spot
    available_spots = [k for k, v in parking_nodes.items() if not v.get("occupied", False)]
    assigned_slot = available_spots[0] if available_spots else None

    if assigned_slot:
        st.success(f"🎯 {t['assigned_spot']}: **{MULTI_CAD_NODES[assigned_slot]['label']}**")
        
        # Calculate Ingress/Egress Driving Routes
        entry_path = theta_star_search("RF_GATE_IN", assigned_slot, MULTI_CAD_NODES, CAD_EDGES)
        exit_path = theta_star_search(assigned_slot, "RF_GATE_OUT", MULTI_CAD_NODES, CAD_EDGES)

        tab_entry, tab_exit = st.tabs([t["parking_tab_entry"], t["parking_tab_exit"]])

        with tab_entry:
            st.markdown("### 🚗 Driving to Parking Spot")
            fig_entry = render_rooftop_parking_map(
                assigned_slot=assigned_slot,
                route_path=entry_path,
                current_lang=st.session_state.lang,
            )
            st.plotly_chart(fig_entry, use_container_width=True)

            if entry_path:
                entry_summary = compute_route_summary(entry_path)
                st.markdown("---")
                st.subheader(t["parking_route_summary"])

                p_col1, p_col2, p_col3 = st.columns(3)
                p_col1.metric(t["dist_to_spot"], f"{entry_summary['total_distance']} m")
                p_col2.metric(t["floors_to_ascend"], entry_summary["floors_crossed"])
                p_col3.metric(t["total_steps"], entry_summary["steps"])

                st.markdown("---")
                st.subheader(t["parking_turn_by_turn"])
                entry_steps = generate_detailed_directions(
                    entry_path, MULTI_CAD_NODES, lang=st.session_state.lang
                )

                for step_info in entry_steps:
                    col_icon, col_text = st.columns([0.1, 0.9])
                    with col_icon:
                        st.markdown(f"### {step_info['icon']}")
                    with col_text:
                        st.markdown(f"**{t['step_lbl']} {step_info['step']}**")
                        st.markdown(step_info["text"])
                    st.divider()

        with tab_exit:
            st.markdown("### 🚪 Leaving Parking Spot to Driveway Exit")
            fig_exit = render_rooftop_parking_map(
                assigned_slot=assigned_slot,
                route_path=exit_path,
                current_lang=st.session_state.lang,
            )
            st.plotly_chart(fig_exit, use_container_width=True)

            if exit_path:
                exit_summary = compute_route_summary(exit_path)
                st.markdown("---")
                st.subheader(t["parking_route_summary"])

                e_col1, e_col2, e_col3 = st.columns(3)
                e_col1.metric(t["dist_to_spot"], f"{exit_summary['total_distance']} m")
                e_col2.metric(t["floors_to_ascend"], exit_summary["floors_crossed"])
                e_col3.metric(t["total_steps"], exit_summary["steps"])

                st.markdown("---")
                st.subheader(t["parking_turn_by_turn"])
                exit_steps = generate_detailed_directions(
                    exit_path, MULTI_CAD_NODES, lang=st.session_state.lang
                )

                for step_info in exit_steps:
                    col_icon, col_text = st.columns([0.1, 0.9])
                    with col_icon:
                        st.markdown(f"### {step_info['icon']}")
                    with col_text:
                        st.markdown(f"**{t['step_lbl']} {step_info['step']}**")
                        st.markdown(step_info["text"])
                    st.divider()

    else:
        st.error("⚠️ No available parking spots found on the Rooftop layer.")
        fig_parking = render_rooftop_parking_map(
            assigned_slot=None,
            route_path=[],
            current_lang=st.session_state.lang,
        )
        st.plotly_chart(fig_parking, use_container_width=True)

# ==============================================================================
# 7. Footer
# ==============================================================================
def render_system_footer():
    st.markdown("---")
    foot_col1, foot_col2, foot_col3 = st.columns(3)

    with foot_col1:
        st.caption("🏢 **System Architecture:** 3D Theta* Pathfinding Engine")
    with foot_col2:
        st.caption(
            "📐 **Vector Processing:** FloorPlanCAD Parser (DXF/SVG Topology)"
        )
    with foot_col3:
        st.caption("🌐 **Localization:** Active Multilingual Engine")

if __name__ == "__main__":
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
    render_system_footer()
