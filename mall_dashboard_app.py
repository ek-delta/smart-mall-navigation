import streamlit as st
import numpy as np
import plotly.graph_objects as go
import heapq
import math

# ==============================================================================
# 1. Page Configuration & State Setup
# ==============================================================================

st.set_page_config(
    page_title="Rooftop Smart Parking & Navigation",
    page_icon="🚗",
    layout="wide"
)

if "lang" not in st.session_state:
    st.session_state.lang = "en"

# Language Dictionary
TRANSLATIONS = {
    "en": {
        "title": "🚗 Rooftop Smart Parking & Navigation System",
        "subtitle": "Multi-CAD 3D Pathfinding & Parking Allocation Engine",
        "control_panel": "Control Panel",
        "lang_select": "Language / 语言",
        "select_start": "Select Starting Point",
        "select_end": "Select Destination Spot",
        "find_route": "Find Optimal Route",
        "parking_tab": "Rooftop Parking",
        "navigation_tab": "Building Navigation",
        "entry_drive": "Driving to Parking Spot",
        "exit_drive": "Leaving Parking Spot to Exit",
        "parking_route_summary": "Route Summary",
        "dist_to_spot": "Total Distance",
        "floors_to_ascend": "Floors Crossed",
        "total_steps": "Turn Steps",
        "parking_turn_by_turn": "Turn-by-Turn Driving Directions",
        "step_lbl": "Step",
        "no_spots": "⚠️ No available parking spots found on the Rooftop layer.",
        "start_node": "Start Node",
        "end_node": "End Node",
        "path_found": "Optimal Route Calculated Successfully!",
        "no_path": "❌ No valid route could be calculated between the selected points."
    },
    "zh": {
        "title": "🚗 屋顶智能停车场与导航系统",
        "subtitle": "多CAD 3D路径规划与车位分配引擎",
        "control_panel": "控制面板",
        "lang_select": "语言 / Language",
        "select_start": "选择起始点",
        "select_end": "选择目标车位",
        "find_route": "寻找最佳路线",
        "parking_tab": "屋顶停车",
        "navigation_tab": "大楼导航",
        "entry_drive": "行驶至目标车位",
        "exit_drive": "从车位行驶至出口",
        "parking_route_summary": "路线摘要",
        "dist_to_spot": "总距离",
        "floors_to_ascend": "跨越楼层",
        "total_steps": "转弯步数",
        "parking_turn_by_turn": "逐向行驶指引",
        "step_lbl": "步骤",
        "no_spots": "⚠️ 屋顶层未找到可用停车位。",
        "start_node": "起点节点",
        "end_node": "终点节点",
        "path_found": "已成功计算最佳路线！",
        "no_path": "❌ 无法在选定点之间计算有效路线。"
    }
}

t = TRANSLATIONS[st.session_state.lang]

# ==============================================================================
# 2. Data Structures & Multi-CAD Node Network
# ==============================================================================

MULTI_CAD_NODES = {
    "ENTRY_GATE": {"x": 10, "y": 10, "z": 0, "type": "gate", "name_en": "Main Entry Ramp", "name_zh": "主入口匝道"},
    "RAMP_1": {"x": 25, "y": 30, "z": 5, "type": "ramp", "name_en": "Ramp Floor 1 to 2", "name_zh": "1至2层匝道"},
    "RAMP_2": {"x": 45, "y": 50, "z": 10, "type": "ramp", "name_en": "Ramp Floor 2 to Roof", "name_zh": "2至屋顶匝道"},
    "EXIT_GATE": {"x": 90, "y": 90, "z": 0, "type": "gate", "name_en": "Main Exit Ramp", "name_zh": "主出口匝道"},
    
    # Parking Slots on Rooftop (z = 10)
    "SLOT_A1": {"x": 55, "y": 60, "z": 10, "type": "slot", "occupied": False, "name_en": "Parking Spot A1", "name_zh": "停车位 A1"},
    "SLOT_A2": {"x": 65, "y": 60, "z": 10, "type": "slot", "occupied": True, "name_en": "Parking Spot A2", "name_zh": "停车位 A2"},
    "SLOT_B1": {"x": 55, "y": 75, "z": 10, "type": "slot", "occupied": False, "name_en": "Parking Spot B1", "name_zh": "停车位 B1"},
    "SLOT_B2": {"x": 65, "y": 75, "z": 10, "type": "slot", "occupied": False, "name_en": "Parking Spot B2", "name_zh": "停车位 B2"},
    "SLOT_C1": {"x": 75, "y": 60, "z": 10, "type": "slot", "occupied": True, "name_en": "Parking Spot C1", "name_zh": "停车位 C1"},
}

CAD_GRAPH = {
    "ENTRY_GATE": ["RAMP_1"],
    "RAMP_1": ["ENTRY_GATE", "RAMP_2"],
    "RAMP_2": ["RAMP_1", "SLOT_A1", "SLOT_A2", "SLOT_B1", "SLOT_B2", "SLOT_C1"],
    "SLOT_A1": ["RAMP_2", "EXIT_GATE"],
    "SLOT_A2": ["RAMP_2", "EXIT_GATE"],
    "SLOT_B1": ["RAMP_2", "EXIT_GATE"],
    "SLOT_B2": ["RAMP_2", "EXIT_GATE"],
    "SLOT_C1": ["RAMP_2", "EXIT_GATE"],
    "EXIT_GATE": []
}

# ==============================================================================
# 3. Pathfinding Algorithm (3D Theta* / A*)
# ==============================================================================

def euclidean_distance_3d(node1, node2):
    return math.sqrt(
        (node1["x"] - node2["x"]) ** 2 +
        (node1["y"] - node2["y"]) ** 2 +
        (node1["z"] - node2["z"]) ** 2
    )

def theta_star_search(graph, nodes, start_key, end_key):
    if start_key not in nodes or end_key not in nodes:
        return []
        
    open_set = []
    heapq.heappush(open_set, (0, start_key))
    
    came_from = {}
    g_score = {node: float('inf') for node in nodes}
    g_score[start_key] = 0
    
    f_score = {node: float('inf') for node in nodes}
    f_score[start_key] = euclidean_distance_3d(nodes[start_key], nodes[end_key])
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == end_key:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start_key)
            return path[::-1]
            
        for neighbor in graph.get(current, []):
            tentative_g = g_score[current] + euclidean_distance_3d(nodes[current], nodes[neighbor])
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + euclidean_distance_3d(nodes[neighbor], nodes[end_key])
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
                
    return []

# ==============================================================================
# 4. Route Summary & Direction Generators
# ==============================================================================

def compute_route_summary(path_keys):
    if not path_keys or len(path_keys) < 2:
        return {"total_distance": 0, "floors_crossed": 0, "steps": 0}
        
    total_dist = 0
    for i in range(len(path_keys) - 1):
        n1 = MULTI_CAD_NODES[path_keys[i]]
        n2 = MULTI_CAD_NODES[path_keys[i+1]]
        total_dist += euclidean_distance_3d(n1, n2)
        
    start_z = MULTI_CAD_NODES[path_keys[0]]["z"]
    end_z = MULTI_CAD_NODES[path_keys[-1]]["z"]
    floors = abs(end_z - start_z) // 5
    
    return {
        "total_distance": round(total_dist, 1),
        "floors_crossed": int(floors),
        "steps": len(path_keys)
    }

def generate_detailed_directions(path_keys, nodes, lang="en"):
    directions = []
    for i, key in enumerate(path_keys):
        node = nodes[key]
        name = node[f"name_{lang}"]
        
        if i == 0:
            icon = "🛫"
            text = f"Start at **{name}**" if lang == "en" else f"从 **{name}** 出发"
        elif i == len(path_keys) - 1:
            icon = "🏁"
            text = f"Arrive at destination: **{name}**" if lang == "en" else f"到达目的地: **{name}**"
        else:
            if node["type"] == "ramp":
                icon = "↗️"
                text = f"Take ramp at **{name}** to reach level Z={node['z']}m" if lang == "en" else f"驶入 **{name}** 前往高度 Z={node['z']}米"
            else:
                icon = "➡️"
                text = f"Proceed through **{name}**" if lang == "en" else f"穿过 **{name}**"
                
        directions.append({"step": i + 1, "icon": icon, "text": text})
    return directions

# ==============================================================================
# 5. Map Rendering Engine (Plotly 3D)
# ==============================================================================

def render_rooftop_parking_map(assigned_slot=None, route_path=None, current_lang="en"):
    fig = go.Figure()
    
    # Plot Parking Slots
    for key, node in MULTI_CAD_NODES.items():
        if node["type"] == "slot":
            color = "red" if node["occupied"] else "green"
            if key == assigned_slot:
                color = "gold"
            
            fig.add_trace(go.Scatter3d(
                x=[node["x"]], y=[node["y"]], z=[node["z"]],
                mode="markers+text",
                marker=dict(size=12, color=color, symbol="square"),
                text=[node[f"name_{current_lang}"]],
                textposition="top center",
                name=node[f"name_{current_lang}"]
            ))
        else:
            fig.add_trace(go.Scatter3d(
                x=[node["x"]], y=[node["y"]], z=[node["z"]],
                mode="markers",
                marker=dict(size=8, color="blue"),
                name=node[f"name_{current_lang}"]
            ))

    # Plot Route Path
    if route_path:
        rx = [MULTI_CAD_NODES[k]["x"] for k in route_path]
        ry = [MULTI_CAD_NODES[k]["y"] for k in route_path]
        rz = [MULTI_CAD_NODES[k]["z"] for k in route_path]
        
        fig.add_trace(go.Scatter3d(
            x=rx, y=ry, z=rz,
            mode="lines+markers",
            line=dict(color="deepskyblue", width=6),
            marker=dict(size=6, color="cyan"),
            name="Route"
        ))

    fig.update_layout(
        scene=dict(
            xaxis_title="X (m)",
            yaxis_title="Y (m)",
            zaxis_title="Z (m)",
            aspectmode="data"
        ),
        margin=dict(l=0, r=0, b=0, t=30),
        height=500
    )
    return fig

# ==============================================================================
# 6. Streamlit User Interface
# ==============================================================================

st.title(t["title"])
st.caption(t["subtitle"])

# Sidebar Control Panel
with st.sidebar:
    st.header(t["control_panel"])
    lang_choice = st.selectbox(t["lang_select"], options=["en", "zh"], index=0 if st.session_state.lang == "en" else 1)
    if lang_choice != st.session_state.lang:
        st.session_state.lang = lang_choice
        st.rerun()

# Determine parking allocation
available_slots = [k for k, v in MULTI_CAD_NODES.items() if v["type"] == "slot" and not v["occupied"]]
assigned_slot = available_slots[0] if available_slots else None

if assigned_slot:
    entry_path = theta_star_search(CAD_GRAPH, MULTI_CAD_NODES, "ENTRY_GATE", assigned_slot)
    exit_path = theta_star_search(CAD_GRAPH, MULTI_CAD_NODES, assigned_slot, "EXIT_GATE")
else:
    entry_path, exit_path = [], []

# Layout Tabs
tab_entry, tab_exit = st.tabs([t["entry_drive"], t["exit_drive"]])

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
        p_col1.metric(
            t["dist_to_spot"], f"{entry_summary['total_distance']} m"
        )
        p_col2.metric(
            t["floors_to_ascend"], entry_summary["floors_crossed"]
        )
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
        e_col1.metric(
            t["dist_to_spot"], f"{exit_summary['total_distance']} m"
        )
        e_col2.metric(
            t["floors_to_ascend"], exit_summary["floors_crossed"]
        )
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

if not assigned_slot:
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
