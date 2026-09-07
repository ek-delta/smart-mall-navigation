import math
import streamlit as st
import plotly.graph_objects as go

# ==============================================================================
# 1. Page & App Configuration
# ==============================================================================
st.set_page_config(
    page_title="3D Indoor Navigation & Rooftop Parking",
    page_icon="🗺️",
    layout="wide"
)

# ==============================================================================
# 2. Localization Data Structures
# ==============================================================================
LOCALIZATION = {
    "English": {
        "title": "🏢 Indoor Navigation System",
        "select_start": "Select Starting Point",
        "select_dest": "Select Destination",
        "route_summary": "Route Summary",
        "total_dist": "Total Distance",
        "floors_crossed": "Floors Crossed",
        "total_steps": "Estimated Steps",
        "turn_by_turn": "Turn-by-Turn Directions",
        "step_lbl": "Step",
        "no_route": "Please select a valid Start and Destination to compute a route.",
        "parking_sec": "Rooftop Parking Assignment",
        "nearest_spot_found": "Assigned Parking Spot",
        "rooftop_lot": "Rooftop Lot",
        "parking_route_summary": "Parking Leg Summary",
        "dist_to_spot": "Distance to Spot",
        "floors_to_ascend": "Floors to Ascend",
        "parking_turn_by_turn": "Parking Turn-by-Turn",
        "selected_on_map": "📍 Selected on map point: **{location}** (at x: {x:.1f}, y: {y:.1f})",
        "btn_set_start": "🚩 Set as Start",
        "btn_set_dest": "🏁 Set as Destination",
        "btn_cancel": "❌ Cancel",
        "tab_map": "🗺️ 2D Interactive Map",
        "tab_dir": "🧭 Navigation Directions",
        "tab_park": "🅿️ Rooftop Parking",
    },
    "Simplified Chinese": {
        "title": "🏢 室内导航与屋顶停车系统",
        "select_start": "选择起点",
        "select_dest": "选择终点",
        "route_summary": "路线总览",
        "total_dist": "总距离",
        "floors_crossed": "跨越楼层",
        "total_steps": "预计步数",
        "turn_by_turn": "逐向导航指引",
        "step_lbl": "步骤",
        "no_route": "请选择有效的起点和终点以计算路线。",
        "parking_sec": "屋顶停车分配",
        "nearest_spot_found": "分配的停车位",
        "rooftop_lot": "屋顶停车场",
        "parking_route_summary": "停车路线摘要",
        "dist_to_spot": "至车位距离",
        "floors_to_ascend": "需上升楼层",
        "parking_turn_by_turn": "停车路线导航",
        "selected_on_map": "📍 已在地图上选择点：**{location}** (坐标 x: {x:.1f}, y: {y:.1f})",
        "btn_set_start": "🚩 设为起点",
        "btn_set_dest": "🏁 设为终点",
        "btn_cancel": "❌ 取消",
        "tab_map": "🗺️ 2D 交互式地图",
        "tab_dir": "🧭 导航路线指引",
        "tab_park": "🅿️ 屋顶停车",
    },
    "Malay": {
        "title": "🏢 Sistem Navigasi Dalam Bangunan",
        "select_start": "Pilih Titik Mula",
        "select_dest": "Pilih Destinasi",
        "route_summary": "Ringkasan Laluan",
        "total_dist": "Jumlah Jarak",
        "floors_crossed": "Tingkat Merentasi",
        "total_steps": "Anggaran Langkah",
        "turn_by_turn": "Arah Navigasi Terperinci",
        "step_lbl": "Langkah",
        "no_route": "Sila pilih Permulaan dan Destinasi yang sah untuk mengira laluan.",
        "parking_sec": "Tugasan Tempat Letak Kereta Bumbung",
        "nearest_spot_found": "Petak Letak Kereta Ditetapkan",
        "rooftop_lot": "Kawasan Bumbung",
        "parking_route_summary": "Ringkasan Laluan Tempat Letak Kereta",
        "dist_to_spot": "Jarak ke Petak",
        "floors_to_ascend": "Tingkat Perlu Dinaiki",
        "parking_turn_by_turn": "Arah Tempat Letak Kereta",
        "selected_on_map": "📍 Dipilih pada titik peta: **{location}** (pada x: {x:.1f}, y: {y:.1f})",
        "btn_set_start": "🚩 Tetapkan sebagai Permulaan",
        "btn_set_dest": "🏁 Tetapkan sebagai Destinasi",
        "btn_cancel": "❌ Batal",
        "tab_map": "🗺️ Peta Interaktif 2D",
        "tab_dir": "🧭 Arah Navigasi",
        "tab_park": "🅿️ Tempat Letak Kereta Bumbung",
    }
}

POI_TRANSLATIONS = {
    "English": {
        "ENTRANCE_L1": "Main Entrance (L1)",
        "CAFE_L1": "Artisan Coffee Cafe",
        "STORE_A_L1": "Tech & Electronics Store",
        "STORE_B_L1": "Fashion Apparel Outlet",
        "RESTROOM_L1": "Ground Floor Restrooms",
        "ELEVATOR_L1": "Main Elevator (L1)",
        "STAIRS_L1": "Central Stairs (L1)",
        "LOBBY_L2": "Level 2 Central Atrium",
        "STORE_C_L2": "Bookstore & Stationery",
        "STORE_D_L2": "Home & Living Superstore",
        "FOOD_COURT_L2": "Gourmet Food Court",
        "ELEVATOR_L2": "Main Elevator (L2)",
        "STAIRS_L2": "Central Stairs (L2)",
        "PARKING_A1": "Parking Slot A-01",
        "PARKING_A2": "Parking Slot A-02",
        "PARKING_EXIT": "Rooftop Driveway Exit"
    },
    "Simplified Chinese": {
        "ENTRANCE_L1": "正门主入口 (一楼)",
        "CAFE_L1": "精品咖啡馆",
        "STORE_A_L1": "数码电子体验店",
        "STORE_B_L1": "潮流服饰专卖店",
        "RESTROOM_L1": "一楼公共卫生间",
        "ELEVATOR_L1": "主电梯 (一楼)",
        "STAIRS_L1": "中央楼梯 (一楼)",
        "LOBBY_L2": "二楼中央中庭",
        "STORE_C_L2": "人文书店与文具",
        "STORE_D_L2": "家居生活馆",
        "FOOD_COURT_L2": "美食广场",
        "ELEVATOR_L2": "主电梯 (二楼)",
        "STAIRS_L2": "中央楼梯 (二楼)",
        "PARKING_A1": "停车位 A-01",
        "PARKING_A2": "停车位 A-02",
        "PARKING_EXIT": "屋顶车道出口"
    },
    "Malay": {
        "ENTRANCE_L1": "Pintu Masuk Utama (L1)",
        "CAFE_L1": "Kafe Kopi Artisan",
        "STORE_A_L1": "Kedai Barangan Elektronik",
        "STORE_B_L1": "Kedai Pakaian Fesyen",
        "RESTROOM_L1": "Tandas Aras Bawah",
        "ELEVATOR_L1": "Lif Utama (L1)",
        "STAIRS_L1": "Tangga Tengah (L1)",
        "LOBBY_L2": "Atrium Tengah Aras 2",
        "STORE_C_L2": "Kedai Buku & Alat Tulis",
        "STORE_D_L2": "Gedung Barangan Rumah",
        "FOOD_COURT_L2": "Medan Selera Gourmet",
        "ELEVATOR_L2": "Lif Utama (L2)",
        "STAIRS_L2": "Tangga Tengah (L2)",
        "PARKING_A1": "Petak Letak Kereta A-01",
        "PARKING_A2": "Petak Letak Kereta A-02",
        "PARKING_EXIT": "Pintu Keluar Bumbung"
    }
}

# ==============================================================================
# 3. Graph & CAD Layout Mock Data
# ==============================================================================
# Format: node_id -> [x, y, z_floor]
MULTI_CAD_NODES = {
    "ENTRANCE_L1": [2.0, 2.0, 1],
    "CAFE_L1": [6.0, 4.0, 1],
    "STORE_A_L1": [15.0, 5.0, 1],
    "STORE_B_L1": [22.0, 6.0, 1],
    "RESTROOM_L1": [24.0, 18.0, 1],
    "ELEVATOR_L1": [12.0, 12.0, 1],
    "STAIRS_L1": [18.0, 12.0, 1],
    
    "LOBBY_L2": [10.0, 10.0, 2],
    "STORE_C_L2": [4.0, 18.0, 2],
    "STORE_D_L2": [22.0, 16.0, 2],
    "FOOD_COURT_L2": [15.0, 4.0, 2],
    "ELEVATOR_L2": [12.0, 12.0, 2],
    "STAIRS_L2": [18.0, 12.0, 2],

    "PARKING_A1": [8.0, 8.0, 3],
    "PARKING_A2": [20.0, 8.0, 3],
    "PARKING_EXIT": [25.0, 22.0, 3]
}

# Node Adjacency Graph for Pathfinding
GRAPH_EDGES = {
    # Floor 1 internal
    "ENTRANCE_L1": ["CAFE_L1", "ELEVATOR_L1"],
    "CAFE_L1": ["ENTRANCE_L1", "STORE_A_L1"],
    "STORE_A_L1": ["CAFE_L1", "STORE_B_L1", "ELEVATOR_L1"],
    "STORE_B_L1": ["STORE_A_L1", "RESTROOM_L1", "STAIRS_L1"],
    "RESTROOM_L1": ["STORE_B_L1"],
    "ELEVATOR_L1": ["ENTRANCE_L1", "STORE_A_L1", "ELEVATOR_L2"],  # Elevator connects L1 to L2
    "STAIRS_L1": ["STORE_B_L1", "STAIRS_L2"],                    # Stairs connect L1 to L2

    # Floor 2 internal
    "LOBBY_L2": ["STORE_C_L2", "FOOD_COURT_L2", "ELEVATOR_L2"],
    "STORE_C_L2": ["LOBBY_L2", "STORE_D_L2"],
    "STORE_D_L2": ["STORE_C_L2", "STAIRS_L2"],
    "FOOD_COURT_L2": ["LOBBY_L2", "ELEVATOR_L2"],
    "ELEVATOR_L2": ["ELEVATOR_L1", "LOBBY_L2", "FOOD_COURT_L2", "PARKING_A1"],
    "STAIRS_L2": ["STAIRS_L1", "STORE_D_L2"],

    # Floor 3 (Rooftop Parking)
    "PARKING_A1": ["ELEVATOR_L2", "PARKING_A2"],
    "PARKING_A2": ["PARKING_A1", "PARKING_EXIT"],
    "PARKING_EXIT": ["PARKING_A2"]
}

# Polygons for 2D Map Display
ROOM_POLYGONS = {
    "ENTRANCE_L1": {"z": 1, "color": "rgba(239, 68, 68, 0.4)", "coords": [(0, 0), (5, 0), (5, 5), (0, 5)]},
    "CAFE_L1": {"z": 1, "color": "rgba(245, 158, 11, 0.4)", "coords": [(5, 0), (10, 0), (10, 8), (5, 8)]},
    "STORE_A_L1": {"z": 1, "color": "rgba(59, 130, 246, 0.4)", "coords": [(10, 0), (20, 0), (20, 9), (10, 9)]},
    "STORE_B_L1": {"z": 1, "color": "rgba(16, 185, 129, 0.4)", "coords": [(20, 0), (28, 0), (28, 10), (20, 10)]},
    "RESTROOM_L1": {"z": 1, "color": "rgba(139, 92, 246, 0.4)", "coords": [(20, 15), (28, 15), (28, 22), (20, 22)]},
    "ELEVATOR_L1": {"z": 1, "color": "rgba(107, 114, 128, 0.5)", "coords": [(10, 10), (14, 10), (14, 14), (10, 14)]},
    "STAIRS_L1": {"z": 1, "color": "rgba(156, 163, 175, 0.5)", "coords": [(16, 10), (20, 10), (20, 14), (16, 14)]},

    "LOBBY_L2": {"z": 2, "color": "rgba(236, 72, 153, 0.4)", "coords": [(7, 7), (14, 7), (14, 14), (7, 14)]},
    "STORE_C_L2": {"z": 2, "color": "rgba(99, 102, 241, 0.4)", "coords": [(0, 14), (8, 14), (8, 22), (0, 22)]},
    "STORE_D_L2": {"z": 2, "color": "rgba(20, 184, 166, 0.4)", "coords": [(18, 12), (26, 12), (26, 20), (18, 20)]},
    "FOOD_COURT_L2": {"z": 2, "color": "rgba(249, 115, 22, 0.4)", "coords": [(10, 0), (20, 0), (20, 7), (10, 7)]},
    "ELEVATOR_L2": {"z": 2, "color": "rgba(107, 114, 128, 0.5)", "coords": [(10, 10), (14, 10), (14, 14), (10, 14)]},
    "STAIRS_L2": {"z": 2, "color": "rgba(156, 163, 175, 0.5)", "coords": [(16, 10), (20, 10), (20, 14), (16, 14)]},

    "PARKING_A1": {"z": 3, "color": "rgba(34, 197, 94, 0.4)", "coords": [(4, 4), (12, 4), (12, 12), (4, 12)]},
    "PARKING_A2": {"z": 3, "color": "rgba(34, 197, 94, 0.4)", "coords": [(16, 4), (24, 4), (24, 12), (16, 12)]},
    "PARKING_EXIT": {"z": 3, "color": "rgba(239, 68, 68, 0.6)", "coords": [(22, 18), (28, 18), (28, 24), (22, 24)]}
}

# ==============================================================================
# 4. Helper & Pathfinding Functions
# ==============================================================================
def get_location_icon(loc_id: str) -> str:
    if "CAFE" in loc_id: return "☕"
    if "STORE" in loc_id: return "🛍️"
    if "RESTROOM" in loc_id: return "🚻"
    if "ELEVATOR" in loc_id: return "🛗"
    if "STAIRS" in loc_id: return "🪜"
    if "PARKING" in loc_id: return "🅿️"
    if "FOOD" in loc_id: return "🍲"
    return "📍"

def wrap_text_to_fit(text: str, max_chars_per_line: int) -> str:
    words = text.split()
    if not words:
        return ""
    lines, current_line, current_len = [], [], 0
    for word in words:
        if current_len + len(word) <= max_chars_per_line or not current_line:
            current_line.append(word)
            current_len += len(word) + 1
        else:
            lines.append(" ".join(current_line))
            current_line, current_len = [word], len(word) + 1
    if current_line:
        lines.append(" ".join(current_line))
    return "<b>" + "<br>".join(lines) + "</b>"

def calculate_optimal_font_size(bbox_w: float, bbox_h: float, text: str) -> tuple[int, int]:
    min_dim = min(bbox_w, bbox_h)
    if min_dim < 2.0: font_size = 7
    elif min_dim < 4.0: font_size = 8
    elif min_dim < 7.0: font_size = 10
    else: font_size = 12
    max_chars_per_line = max(4, int(bbox_w * (8.5 / font_size)))
    return font_size, max_chars_per_line

def find_nearest_node(x: float, y: float, z: int) -> tuple[str, float]:
    nearest_id = None
    min_dist = float("inf")
    for node_id, coords in MULTI_CAD_NODES.items():
        if coords[2] == z:
            dist = math.hypot(x - coords[0], y - coords[1])
            if dist < min_dist:
                min_dist = dist
                nearest_id = node_id
    return nearest_id, min_dist

def compute_theta_star_path(start_node: str, end_node: str) -> list[str]:
    """A* / Theta* Pathfinding implementation over the graph structure."""
    if start_node not in MULTI_CAD_NODES or end_node not in MULTI_CAD_NODES:
        return []
    
    import heapq
    open_set = [(0, start_node)]
    came_from = {}
    g_score = {node: float("inf") for node in MULTI_CAD_NODES}
    g_score[start_node] = 0

    def heuristic(n1, n2):
        c1, c2 = MULTI_CAD_NODES[n1], MULTI_CAD_NODES[n2]
        return math.sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 + ((c1[2]-c2[2])*10)**2)

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == end_node:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]

        for neighbor in GRAPH_EDGES.get(current, []):
            tentative_g = g_score[current] + heuristic(current, neighbor)
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, end_node)
                heapq.heappush(open_set, (f_score, neighbor))
    return []

def compute_route_summary(path: list[str]) -> dict:
    if not path or len(path) < 2:
        return {"total_distance": 0.0, "floors_crossed": 0, "steps": 0}
    
    dist = 0.0
    floors = set()
    for i in range(len(path) - 1):
        c1, c2 = MULTI_CAD_NODES[path[i]], MULTI_CAD_NODES[path[i+1]]
        dist += math.hypot(c1[0] - c2[0], c1[1] - c2[1])
        floors.add(c1[2])
        floors.add(c2[2])

    return {
        "total_distance": round(dist, 1),
        "floors_crossed": max(0, len(floors) - 1),
        "steps": int(dist * 1.3)
    }

def compute_route_summary_from_points(path: list[str], start_point=None, dest_point=None) -> dict:
    summary = compute_route_summary(path)
    extra_dist = 0.0
    if start_point and path:
        nx, ny, _ = MULTI_CAD_NODES[path[0]]
        extra_dist += math.hypot(start_point["x"] - nx, start_point["y"] - ny)
    if dest_point and path:
        nx, ny, _ = MULTI_CAD_NODES[path[-1]]
        extra_dist += math.hypot(dest_point["x"] - nx, dest_point["y"] - ny)

    summary["total_distance"] = round(summary["total_distance"] + extra_dist, 1)
    summary["steps"] = int(summary["total_distance"] * 1.3)
    return summary

def generate_detailed_directions(path: list[str], nodes: dict, lang="English") -> list[dict]:
    steps = []
    if not path:
        return steps
    
    for i in range(len(path)):
        node_id = path[i]
        icon = get_location_icon(node_id)
        translated = POI_TRANSLATIONS.get(lang, {}).get(node_id, node_id)
        
        if i == 0:
            text = f"Start at **{translated}**."
        elif i == len(path) - 1:
            text = f"Arrive at your destination: **{translated}**."
        else:
            prev_z = nodes[path[i-1]][2]
            curr_z = nodes[node_id][2]
            if curr_z > prev_z:
                text = f"Take elevator/stairs up to Floor {curr_z} at **{translated}**."
            elif curr_z < prev_z:
                text = f"Take elevator/stairs down to Floor {curr_z} at **{translated}**."
            else:
                text = f"Proceed towards **{translated}**."

        steps.append({"step": i + 1, "icon": icon, "text": text})
    return steps

def get_floor_bounds(z: int):
    xs, ys = [], []
    for poly in ROOM_POLYGONS.values():
        if poly["z"] == z:
            for pt in poly["coords"]:
                xs.append(pt[0])
                ys.append(pt[1])
    if not xs:
        return 0, 30, 0, 30
    return min(xs), max(xs), min(ys), max(ys)

# ==============================================================================
# 5. 2D Map Rendering Function
# ==============================================================================
def render_2d_cad_view(active_floor_z, route_path=None, current_lang="English", clicked_point=None):
    fig = go.Figure()
    floor_rooms = {r_id: poly["coords"] for r_id, poly in ROOM_POLYGONS.items() if poly["z"] == active_floor_z}

    # Render Room Polygons
    for room_id, coords in floor_rooms.items():
        x_coords = [c[0] for c in coords] + [coords[0][0]]
        y_coords = [c[1] for c in coords] + [coords[0][1]]
        room_info = ROOM_POLYGONS[room_id]
        translated_name = POI_TRANSLATIONS.get(current_lang, {}).get(room_id, room_id)

        fig.add_trace(
            go.Scatter(
                x=x_coords,
                y=y_coords,
                fill="toself",
                fillcolor=room_info.get("color", "rgba(200, 200, 200, 0.3)"),
                line=dict(color="#4A5568", width=1.5),
                hoverinfo="text",
                text=translated_name,
                customdata=[[room_id, c[0], c[1]] for c in coords] + [[room_id, coords[0][0], coords[0][1]]],
                showlegend=False,
            )
        )

    # Render Bold Room / POI Labels
    for room_id, coords in floor_rooms.items():
        translated_name = POI_TRANSLATIONS.get(current_lang, {}).get(room_id, room_id)
        xs, ys = [p[0] for p in coords], [p[1] for p in coords]
        min_x, max_x, min_y, max_y = min(xs), max(xs), min(ys), max(ys)
        cx, cy = (min_x + max_x) / 2.0, (min_y + max_y) / 2.0
        bbox_w, bbox_h = max_x - min_x, max_y - min_y

        if bbox_w < 0.6 or bbox_h < 0.6:
            continue

        font_size, max_chars = calculate_optimal_font_size(bbox_w, bbox_h, translated_name)
        wrapped_label = wrap_text_to_fit(translated_name, max_chars_per_line=max_chars)

        fig.add_annotation(
            x=cx,
            y=cy,
            text=wrapped_label,
            showarrow=False,
            font=dict(size=font_size, color="#000000", family="Arial Black, Impact, sans-serif"),
            align="center",
            valign="middle",
            captureevents=False
        )

    # Render Arbitrary User Click Point Marker
    if clicked_point and clicked_point.get("z") == active_floor_z:
        fig.add_trace(
            go.Scatter(
                x=[clicked_point["x"]],
                y=[clicked_point["y"]],
                mode="markers",
                marker=dict(size=16, color="#00E5FF", symbol="cross", line=dict(color="#0088A0", width=3)),
                name="Clicked Point",
                hovertext=f"Clicked ({clicked_point['x']:.2f}, {clicked_point['y']:.2f})",
                showlegend=False
            )
        )

    # Render Route Path
    if route_path:
        floor_path = [node for node in route_path if MULTI_CAD_NODES[node][2] == active_floor_z]

        if len(floor_path) > 1:
            path_x = [MULTI_CAD_NODES[node][0] for node in floor_path]
            path_y = [MULTI_CAD_NODES[node][1] for node in floor_path]

            fig.add_trace(
                go.Scatter(
                    x=path_x,
                    y=path_y,
                    mode="lines+markers",
                    line=dict(color="#FF0000", width=4, dash="solid"),
                    marker=dict(size=8, color="#8B0000"),
                    name="Route Path",
                    showlegend=False
                )
            )

            for i in range(len(floor_path) - 1):
                x_start, y_start, _ = MULTI_CAD_NODES[floor_path[i]]
                x_end, y_end, _ = MULTI_CAD_NODES[floor_path[i + 1]]

                fig.add_annotation(
                    x=x_start + 0.6 * (x_end - x_start),
                    y=y_start + 0.6 * (y_end - y_start),
                    ax=x_start,
                    ay=y_start,
                    xref="x", yref="y", axref="x", ayref="y",
                    showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=2.5, arrowcolor="#CC0000"
                )

        start_node_id, dest_node_id = route_path[0], route_path[-1]

        if MULTI_CAD_NODES[start_node_id][2] == active_floor_z:
            start_x, start_y, _ = MULTI_CAD_NODES[start_node_id]
            fig.add_trace(
                go.Scatter(
                    x=[start_x], y=[start_y], mode="markers+text",
                    marker=dict(size=14, color="#FF0000", symbol="circle", line=dict(color="#8B0000", width=2)),
                    text=[" Start"], textposition="top right", textfont=dict(color="#FF0000", size=12, family="Arial Black"),
                    showlegend=False
                )
            )

        if MULTI_CAD_NODES[dest_node_id][2] == active_floor_z:
            dest_x, dest_y, _ = MULTI_CAD_NODES[dest_node_id]
            fig.add_trace(
                go.Scatter(
                    x=[dest_x], y=[dest_y], mode="markers+text",
                    marker=dict(size=14, color="#00FF00", symbol="circle", line=dict(color="#006600", width=2)),
                    text=[" Destination"], textposition="top right", textfont=dict(color="#00AA00", size=12, family="Arial Black"),
                    showlegend=False
                )
            )

    min_x, max_x, min_y, max_y = get_floor_bounds(active_floor_z)
    fig.update_layout(
        height=600,
        margin=dict(l=15, r=15, t=30, b=15),
        showlegend=False,
        clickmode="event+select",
        plot_bgcolor="#1E293B",
        paper_bgcolor="#0F172A",
        xaxis=dict(range=[min_x - 3, max_x + 3], showgrid=False, zeroline=False),
        yaxis=dict(range=[min_y - 3, max_y + 3], showgrid=False, zeroline=False, scaleanchor="x")
    )
    return fig

def render_rooftop_parking_map(assigned_slot=None, route_path=None, current_lang="English"):
    return render_2d_cad_view(active_floor_z=3, route_path=route_path, current_lang=current_lang)

# ==============================================================================
# 6. Session State Initialization
# ==============================================================================
if "lang" not in st.session_state:
    st.session_state.lang = "English"
if "current_floor" not in st.session_state:
    st.session_state.current_floor = 1
if "selected_start" not in st.session_state:
    st.session_state.selected_start = "ENTRANCE_L1"
if "selected_dest" not in st.session_state:
    st.session_state.selected_dest = "FOOD_COURT_L2"
if "clicked_location" not in st.session_state:
    st.session_state.clicked_location = None
if "custom_click_point" not in st.session_state:
    st.session_state.custom_click_point = None
if "assigned_parking" not in st.session_state:
    st.session_state.assigned_parking = "PARKING_A1"

t = LOCALIZATION[st.session_state.lang]

# ==============================================================================
# 7. Sidebar Controls
# ==============================================================================
st.sidebar.title("⚙️ Options")
st.session_state.lang = st.sidebar.selectbox("🌐 Language / 语言 / Bahasa", ["English", "Simplified Chinese", "Malay"])
t = LOCALIZATION[st.session_state.lang]

st.sidebar.subheader("📍 Navigation Selection")
all_pois = list(MULTI_CAD_NODES.keys())

st.session_state.selected_start = st.sidebar.selectbox(
    t["select_start"],
    all_pois,
    index=all_pois.index(st.session_state.selected_start) if st.session_state.selected_start in all_pois else 0,
    format_func=lambda x: f"{get_location_icon(x)} {POI_TRANSLATIONS[st.session_state.lang].get(x, x)}"
)

st.session_state.selected_dest = st.sidebar.selectbox(
    t["select_dest"],
    all_pois,
    index=all_pois.index(st.session_state.selected_dest) if st.session_state.selected_dest in all_pois else 1,
    format_func=lambda x: f"{get_location_icon(x)} {POI_TRANSLATIONS[st.session_state.lang].get(x, x)}"
)

st.session_state.current_floor = st.sidebar.radio("🏢 Floor Level", [1, 2, 3], format_func=lambda z: f"Floor {z}" if z < 3 else "Floor 3 (Rooftop)")

# Calculate standard path
path = compute_theta_star_path(st.session_state.selected_start, st.session_state.selected_dest)
st.session_state.entry_path = compute_theta_star_path("ENTRANCE_L1", st.session_state.assigned_parking)
st.session_state.exit_path = compute_theta_star_path(st.session_state.assigned_parking, "PARKING_EXIT")

# ==============================================================================
# 8. Main Application Interface
# ==============================================================================
st.title(t["title"])

tab_map, tab_dir, tab_park = st.tabs([t["tab_map"], t["tab_dir"], t["tab_park"]])

# ------------------------------------------------------------------------------
# TAB 1: 2D INTERACTIVE MAP
# ------------------------------------------------------------------------------
with tab_map:
    # 1. Selection Banner
    if st.session_state.clicked_location and st.session_state.custom_click_point:
        loc_id = st.session_state.clicked_location
        click_pt = st.session_state.custom_click_point
        loc_name = POI_TRANSLATIONS.get(st.session_state.lang, {}).get(loc_id, loc_id)

        st.info(t["selected_on_map"].format(location=loc_name, x=click_pt["x"], y=click_pt["y"]))
        col_btn1, col_btn2, col_btn3 = st.columns(3)

        with col_btn1:
            if st.button(t["btn_set_start"], key="btn_set_start", use_container_width=True):
                st.session_state.selected_start = loc_id
                st.session_state.clicked_location = None
                st.rerun()

        with col_btn2:
            if st.button(t["btn_set_dest"], key="btn_set_dest", use_container_width=True):
                st.session_state.selected_dest = loc_id
                st.session_state.clicked_location = None
                st.rerun()

        with col_btn3:
            if st.button(t["btn_cancel"], key="btn_cancel_select", use_container_width=True):
                st.session_state.clicked_location = None
                st.session_state.custom_click_point = None
                st.rerun()

    # 2. Interactive Map Render
    fig = render_2d_cad_view(
        active_floor_z=st.session_state.current_floor,
        route_path=path,
        current_lang=st.session_state.lang,
        clicked_point=st.session_state.get("custom_click_point", None)
    )

    event_data = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="map_2d_interactive")

    # 3. Handle Interactive Clicks Anywhere on Map
    if event_data and "selection" in event_data and event_data["selection"]["points"]:
        pt = event_data["selection"]["points"][0]
        click_x, click_y = pt["x"], pt["y"]
        active_z = st.session_state.current_floor

        nearest_node, offset_dist = find_nearest_node(click_x, click_y, active_z)

        st.session_state.custom_click_point = {
            "x": click_x, "y": click_y, "z": active_z,
            "nearest_node": nearest_node, "offset_dist": offset_dist
        }
        st.session_state.clicked_location = nearest_node
        st.rerun()

# ------------------------------------------------------------------------------
# TAB 2: DIRECTIONS & SUMMARY
# ------------------------------------------------------------------------------
with tab_dir:
    st.subheader(t["route_summary"])
    if path:
        summary = compute_route_summary_from_points(
            path,
            start_point=st.session_state.custom_click_point if st.session_state.selected_start == st.session_state.clicked_location else None
        )
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric(t["total_dist"], f"{summary['total_distance']} m")
        m_col2.metric(t["floors_crossed"], summary["floors_crossed"])
        m_col3.metric(t["total_steps"], summary["steps"])

        st.markdown("---")
        st.subheader(t["turn_by_turn"])
        detailed_steps = generate_detailed_directions(path, MULTI_CAD_NODES, lang=st.session_state.lang)

        for step_info in detailed_steps:
            col_icon, col_text = st.columns([0.1, 0.9])
            with col_icon:
                st.markdown(f"### {step_info['icon']}")
            with col_text:
                st.markdown(f"**{t['step_lbl']} {step_info['step']}**")
                st.markdown(step_info["text"])
            st.divider()
    else:
        st.warning(t["no_route"])

# ------------------------------------------------------------------------------
# TAB 3: ROOFTOP PARKING
# ------------------------------------------------------------------------------
with tab_park:
    st.subheader(t["parking_sec"])
    assigned_slot = st.session_state.get("assigned_parking", None)
    entry_path = st.session_state.get("entry_path", [])
    exit_path = st.session_state.get("exit_path", [])

    if assigned_slot:
        slot_icon = get_location_icon(assigned_slot)
        st.success(f"{t['nearest_spot_found']}: `{slot_icon} {assigned_slot}` ({t['rooftop_lot']})")

        tab_entry, tab_exit = st.tabs(["🚗 1. Entrance to Parking Spot", "🚪 2. Parking Spot to Exit"])

        with tab_entry:
            st.markdown("### 🚗 Driving to Parking Spot")
            fig_entry = render_rooftop_parking_map(
                assigned_slot=assigned_slot,
                route_path=entry_path,
                current_lang=st.session_state.lang
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
                entry_steps = generate_detailed_directions(entry_path, MULTI_CAD_NODES, lang=st.session_state.lang)

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
                current_lang=st.session_state.lang
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
                exit_steps = generate_detailed_directions(exit_path, MULTI_CAD_NODES, lang=st.session_state.lang)

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

# ==============================================================================
# 9. System Footer
# ==============================================================================
def render_system_footer():
    st.markdown("---")
    foot_col1, foot_col2, foot_col3 = st.columns(3)
    with foot_col1:
        st.caption("🏢 **System Architecture:** 3D Theta* Pathfinding Engine")
    with foot_col2:
        st.caption("📐 **Vector Processing:** FloorPlanCAD Parser (DXF/SVG Topology)")
    with foot_col3:
        st.caption("🌐 **Localization:** Active Multilingual Engine")

render_system_footer()
