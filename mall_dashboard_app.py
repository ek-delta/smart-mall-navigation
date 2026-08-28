import math
import heapq
import os
import streamlit as st
import plotly.graph_objects as go

# ==============================================================================
# 1. Translation table
# ==============================================================================

st.set_page_config(
    page_title="Multi-Floor Indoor Navigation Engine",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

LANG_OPTION_LABELS = {
    "English": {"English": "English", "Simplified Chinese": "Simplified Chinese", "Malay": "Malay"},
    "Simplified Chinese": {"English": "英语 (English)", "Simplified Chinese": "简体中文", "Malay": "马来语 (Bahasa Melayu)"},
    "Malay": {"English": "Bahasa Inggeris (English)", "Simplified Chinese": "Bahasa Cina Ringkas", "Malay": "Bahasa Melayu"}
}

LOCALIZATION = {
    "English": {
        "title": "🏢 Smart Mall Navigation & Parking System",
        "subtitle": "Indoor Pathfinding, Efficient Routing & Smart Parking",
        "select_lang": "Language",
        "nav_controls": "Navigation Controls",
        "start_loc": "Start Location",
        "dest_loc": "Destination",
        "route_type": "Routing Preference",
        "shortest": "Shortest Path",
        "accessible": "Accessible (Elevators Only)",
        "view_mode": "Map Display Mode",
        "view_2d": "2D Vector Plan",
        "view_3d": "3D Isometric View",
        "active_floor": "Select Floor",
        "tab_nav": "🗺️ Mall Map",
        "tab_directions": "🧭 Directions",
        "tab_parking": "🅿️ Smart Parking",
        "route_summary": "Route Summary",
        "total_dist": "Total Distance",
        "floors_crossed": "Floors Crossed",
        "total_steps": "Total Steps",
        "turn_by_turn": "Step-by-Step Directions",
        "no_route": "No route available between selected points.",
        "parking_sec": "Smart Parking Allocation",
        "home_title": "🏢 Welcome to the Smart Mall Navigation System",
        "home_desc": "Navigate multi-floor shopping mall with real-time 2D and 3D pathfinding, routing options, and automated parking allocation with step-by-step directions.",
        "poi_metric": "📍 Points of Interest",
        "floors_metric": "🏢 Total Floors",
        "spots_metric": "🅿️ Total Parking Spots",
        "available_metric": "🟢 Available Spots",
        "feat_map_title": "🗺️ 2D / 3D Map View",
        "feat_map_desc": "Navigate our shopping mall easily with 2D and 3D maps.",
        "feat_turn_title": "🧭 Turn-by-Turn",
        "feat_turn_desc": "Get step-by-step directions to your destination.",
        "feat_park_title": "🅿️ Smart Parking",
        "feat_park_desc": "View real-time parking availability and get directions to your assigned spot.",
        "current_route_lbl": "📍 Current Route",
        "step_lbl": "Step",
        "nearest_spot_found": "📍 Nearest Spot Found",
        "rooftop_lot": "Rooftop Parking Lot",
        "from_lbl": "from",
        "parking_route_summary": "🧭 Route Summary to Parking Spot",
        "parking_turn_by_turn": "🚗 Turn-by-Turn Directions to Parking Spot",
        "dist_to_spot": "Distance to Spot",
        "floors_to_ascend": "Floors to Ascend",
        "config_header": "⚙️ Settings",
    },
    "Simplified Chinese": {
        "title": "🏢 智能商场导航与停车系统",
        "subtitle": "室内路径规划、无障碍导航与智能停车管理",
        "select_lang": "语言选择",
        "nav_controls": "导航设置",
        "start_loc": "起点位置",
        "dest_loc": "终点位置",
        "route_type": "路线偏好",
        "shortest": "最短路线",
        "accessible": "无障碍路线 (仅限电梯)",
        "view_mode": "地图显示模式",
        "view_2d": "2D 平面矢量图",
        "view_3d": "3D 等轴测视图",
        "active_floor": "选择楼层",
        "tab_nav": "🗺️ 导航地图",
        "tab_directions": "🧭 分步导航",
        "tab_parking": "🅿️ 智能停车",
        "route_summary": "路线总览",
        "total_dist": "总距离",
        "floors_crossed": "跨越楼层",
        "total_steps": "总步数",
        "turn_by_turn": "详细指引",
        "no_route": "所选地点之间未找到可用路线。",
        "parking_sec": "智能车位分配",
        "home_title": "🏢 欢迎使用智能商场导航与停车系统",
        "home_desc": "支持多楼层商场的实时 2D 与 3D 路径规划、无障碍路线选择及自动车位分配。",
        "poi_metric": "📍 兴趣点数量",
        "floors_metric": "🏢 总楼层数",
        "spots_metric": "🅿️ 总车位数",
        "available_metric": "🟢 空余车位",
        "feat_map_title": "🗺️ 2D / 3D 地图视图",
        "feat_map_desc": "可交互的 2D 楼层矢量图与多楼层 3D 等轴立体投影切换。",
        "feat_turn_title": "🧭 逐向导航",
        "feat_turn_desc": "提供精确转向角度、跨楼层换乘指引与距离统计的分步指引。",
        "feat_park_title": "🅿️ 智能停车",
        "feat_park_desc": "实时查看车位占用状态，并自动规划直达分配车位的最优路线。",
        "current_route_lbl": "📍 当前路线",
        "step_lbl": "步骤",
        "nearest_spot_found": "📍 已为您找到最近车位",
        "rooftop_lot": "顶层露天停车场",
        "from_lbl": "出发地：",
        "parking_route_summary": "🧭 车位导航路线总览",
        "parking_turn_by_turn": "🚗 前往车位逐向导航",
        "dist_to_spot": "到达车位距离",
        "floors_to_ascend": "上升楼层",
        "config_header": "⚙️ 系统配置",
    },
    "Malay": {
        "title": "🏢 Sistem Navigasi & Tempat Letak Kereta Pusat Beli-Belah Smart",
        "subtitle": "Navigasi Laluan 3D Lebih Mudah, Laluan Mesra OKU & Pengurusan Tempat Letak Kereta",
        "select_lang": "Bahasa",
        "nav_controls": "Kawalan Navigasi",
        "start_loc": "Lokasi Permulaan",
        "dest_loc": "Destinasi",
        "route_type": "Pilihan Laluan",
        "shortest": "Laluan Terpendek",
        "accessible": "Mesra OKU (Lif Sahaja)",
        "view_mode": "Mod Paparan Peta",
        "view_2d": "Pelan Vektor 2D",
        "view_3d": "Pandangan Isometrik 3D",
        "active_floor": "Pilih Tingkat",
        "tab_nav": "🗺️ Peta Navigasi",
        "tab_directions": "🧭 Arah Langkah demi Langkah",
        "tab_parking": "🅿️ Tempat Letak Kereta",
        "route_summary": "Ringkasan Laluan",
        "total_dist": "Jumlah Jarak",
        "floors_crossed": "Tingkat Dilalui",
        "total_steps": "Jumlah Langkah",
        "turn_by_turn": "Arah Langkah demi Langkah",
        "no_route": "Tiada laluan dijumpai antara lokasi yang dipilih.",
        "parking_sec": "Peruntukan Tempat Letak Kereta",
        "home_title": "🏢 Selamat Datang ke Sistem Navigasi Pusat Beli-Belah Smart",
        "home_desc": "Navigasi pusat beli-belah bertingkat dengan laluan 3D masa nyata, pilihan laluan mesra OKU, dan automatik tempat letak kereta.",
        "poi_metric": "📍 Titik Tumpuan (POI)",
        "floors_metric": "🏢 Jumlah Tingkat",
        "spots_metric": "🅿️ Jumlah Ruang Letak Kereta",
        "available_metric": "🟢 Ruang Kosong",
        "feat_map_title": "🗺️ Pandangan Peta 2D / 3D",
        "feat_map_desc": "Pelan vektor tingkat 2D interaktif dan paparan isometrik 3D bertingkat.",
        "feat_turn_title": "🧭 Arah Langkah demi Langkah",
        "feat_turn_desc": "Panduan langkah demi langkah dengan sudut arah, transit tingkat, dan jarak.",
        "feat_park_title": "🅿️ Tempat Letak Kereta Smart",
        "feat_park_desc": "Lihat status ruang letak kereta secara masa nyata dan dapatkan laluan ke petak anda.",
        "current_route_lbl": "📍 Laluan Semasa",
        "step_lbl": "Langkah",
        "nearest_spot_found": "📍 Tempat Letak Kereta Terdekat Ditemui",
        "rooftop_lot": "Kawasan Tempat Letak Kereta Bumbung",
        "from_lbl": "dari",
        "parking_route_summary": "🧭 Ringkasan Laluan ke Tempat Letak Kereta",
        "parking_turn_by_turn": "🚗 Arah Langkah demi Langkah ke Tempat Letak Kereta",
        "dist_to_spot": "Jarak ke Tempat Letak Kereta",
        "floors_to_ascend": "Tingkat Perlu Naik",
        "config_header": "⚙️ Konfigurasi",
    }
}

FLOOR_TRANSLATIONS = {
    "English": {
        0: "Ground Floor [GF]",
        1: "1st Floor [1F]",
        2: "2nd Floor [2F]",
        3: "Rooftop Parking Lot [R]"
    },
    "Simplified Chinese": {
        0: "底层 [GF}",
        1: "1层 [1F]",
        2: "2层 [2F]",
        3: "屋顶露台与停车场 [R]"
    },
    "Malay": {
        0: "Aras Bawah [GF]",
        1: "Aras 1 [1F]",
        2: "Aras 2 [2F]",
        3: "Dek Bumbung & Tempat Letak Kereta [R]"
    }
}

def get_translated_floor_name(z_index, lang="English"):
    z_int = int(z_index)
    lang_dict = FLOOR_TRANSLATIONS.get(lang, FLOOR_TRANSLATIONS["English"])
    return lang_dict.get(z_int, f"Level {z_int}")

FLOOR_NAMES = FLOOR_TRANSLATIONS["English"]

POI_TRANSLATIONS = {
    "English": {
        "A_L0_Entrance": "🚪Main Entrance (GF)",
        "A_L0_Lobby": "📍Central Lobby (GF)",
        "A_L0_Info": "🛠️Information Desk",
        "A_L0_Elevator": "🛗Elevator (GF)",
        "A_L0_Stairs": "🧗Stairwell (GF)",
        "A_L0_Escalator": "🪜Escalator (GF)",
        "A_L0_Restroom": "🚻Restroom (GF)",
        "A_L1_Hallway": "🚪Corridor (1F)",
        "A_L1_Elevator": "🛗Elevator (1F)",
        "A_L1_Stairs": "🧗Stairwell (1F)",
        "A_L1_Escalator": "🪜Escalator (1F)",
        "A_L1_Restroom": "🚻Restroom (1F)",
        "B_L2_Corridor": "📍Main Hall (2F)",
        "B_L2_Elevator": "🛗Elevator (2F)",
        "B_L2_Stairs": "🧗Stairwell (2F)",
        "B_L2_Escalator": "🪜Escalator (2F)",
        "B_L2_Restroom": "🚻Restroom (2F)",
        "P_L3_Aisle_Main": "🚪Main Drive Aisle (R)",
        "P_L3_Elevator": "🛗Elevator (R)",
        "P_L3_Stairs": "🧗Stairwell (R)",
        "Fashion Hub": "👗Fashion Hub",
        "Tech Gadgets": "📱Tech Gadgets",
        "Jewel Box": "👗Jewel Box",
        "Mega Supermarket": "🛒Mega Supermarket",
        "Gourmet Bites": "🍔Gourmet Bites",
        "Book Nook": "🛒Book Nook",
        "Cineplex Theater": "🎬Cineplex Theater",
        "VR World & Arcade": "🎬Arcade",
        "Sky Food Court": "🍔Sky Food Court",
        "P1": "🅿️Spot 1", "P2": "🅿️Spot 2",
        "P3": "🅿️Spot 3", "P4": "🅿️Spot 4",
        "P5": "🅿️Spot 5", "P6": "🅿️Spot 6",
        "P7": "🅿️Spot 7", "P8": "🅿️Spot 8",
    },
    "Simplified Chinese": {
        "A_L0_Entrance": "🚪正门入口 (底层)",
        "A_L0_Lobby": "📍中央大堂 (底层)",
        "A_L0_Info": "🛠️问讯服务台",
        "A_L0_Elevator": "🛗电梯 (底层)",
        "A_L0_Stairs": "🧗楼梯 (底层)",
        "A_L0_Escalator": "🪜自动扶梯 (底层)",
        "A_L0_Restroom": "🚻洗手间 (底层)",
        "A_L1_Hallway": "🚪主走廊 (一楼)",
        "A_L1_Elevator": "🛗电梯 (一楼)",
        "A_L1_Stairs": "🧗楼梯 (一楼)",
        "A_L1_Escalator": "🪜自动扶梯 (一楼)",
        "A_L1_Restroom": "🚻洗手间 (一楼)",
        "B_L2_Corridor": "📍主大厅 (二楼)",
        "B_L2_Elevator": "🛗电梯 (二楼)",
        "B_L2_Stairs": "🧗楼梯 (二楼)",
        "B_L2_Escalator": "🪜自动扶梯 (二楼)",
        "B_L2_Restroom": "🚻洗手间 (二楼)",
        "P_L3_Aisle_Main": "🚪楼顶车库主车道",
        "P_L3_Elevator": "🛗楼顶电梯间",
        "P_L3_Stairs": "🧗楼顶楼梯",
        "Fashion Hub": "👗时尚中心 (Fashion Hub)",
        "Tech Gadgets": "📱酷科技数码 (Tech Gadgets)",
        "Jewel Box": "👗璀璨珠宝 (Jewel Box)",
        "Mega Supermarket": "🛒大型超级市场 (Mega Supermarket)",
        "Gourmet Bites": "🍔美食小吃 (Gourmet Bites)",
        "Book Nook": "🛒书香角 (Book Nook)",
        "Cineplex Theater": "🎬影城 (Cineplex Theater)",
        "VR World & Arcade": "🎬电玩城 (& Arcade)",
        "Sky Food Court": "🍔云端美食广场 (Sky Food Court)",
        "P1": "🅿️停车位 1", "P2": "🅿️停车位 2",
        "P3": "🅿️停车位 3", "P4": "🅿️停车位 4",
        "P5": "🅿️停车位 5", "P6": "🅿️停车位 6",
        "P7": "🅿️停车位 7", "P8": "🅿️停车位 8",
    },
    "Malay": {
        "A_L0_Entrance": "🚪Pintu Masuk Utama (Tingkat Bawah)",
        "A_L0_Lobby": "📍Lobi Utama (Tingkat Bawah)",
        "A_L0_Info": "🛠️Kaunter Maklumat",
        "A_L0_Elevator": "🛗Lif (Tingkat Bawah)",
        "A_L0_Stairs": "🧗Tangga (Tingkat Bawah)",
        "A_L0_Escalator": "🪜Eskalator (Tingkat Bawah)",
        "A_L0_Restroom": "🚻Tandas (Tingkat Bawah)",
        "A_L1_Hallway": "🚪Koridor (Tingkat 1)",
        "A_L1_Elevator": "🛗Lif (Tingkat 1)",
        "A_L1_Stairs": "🧗Tangga (Tingkat 1)",
        "A_L1_Escalator": "🪜Eskalator (Tingkat 1)",
        "A_L1_Restroom": "🚻Tandas (Tingkat 1)",
        "B_L2_Corridor": "📍Dewan Utama (Tingkat 2)",
        "B_L2_Elevator": "🛗Lif (Tingkat 2)",
        "B_L2_Stairs": "🧗Tangga (Tingkat 2)",
        "B_L2_Escalator": "🪜Eskalator (Tingkat 2)",
        "B_L2_Restroom": "🚻Tandas (Tingkat 2)",
        "P_L3_Aisle_Main": "🚪Laluan Utama Kenderaan (Bumbung)",
        "P_L3_Elevator": "🛗Lif (Bumbung)",
        "P_L3_Stairs": "🧗Tangga (Bumbung)",
        "Fashion Hub": "👗Fashion Hub",
        "Tech Gadgets": "📱Tech Gadgets",
        "Jewel Box": "👗Jewel Box",
        "Mega Supermarket": "🛒Mega Supermarket",
        "Gourmet Bites": "🍔Gourmet Bites",
        "Book Nook": "🛒Book Nook",
        "Cineplex Theater": "🎬Cineplex Theater",
        "VR World & Arcade": "🎬Arcade",
        "Sky Food Court": "🍔Sky Food Court",
        "P1": "🅿️Tempat 1", "P2": "🅿️Tempat 2",
        "P3": "🅿️Tempat 3", "P4": "🅿️Tempat 4",
        "P5": "🅿️Tempat 5", "P6": "🅿️Tempat 6",
        "P7": "🅿️Tempat 7", "P8": "🅿️Tempat 8",
    }
}

STORE_CATEGORIES = {
    "Fashion Hub": "Apparel",
    "Tech Gadgets": "Electronics",
    "Jewel Box": "Jewelry",
    "Mega Supermarket": "Supermarket",
    "Gourmet Bites": "Food & Beverage",
    "Book Nook": "Books",
    "Cineplex Theater": "Cinema",
    "VR World & Arcade": "Arcade",
    "Sky Food Court": "Food & Beverage",
    "A_L0_Restroom": "Restroom",
    "A_L1_Restroom": "Restroom",
    "B_L2_Restroom": "Restroom",
    "A_L0_Info": "Facility",
    "A_L0_Elevator": "Facility",
    "A_L1_Elevator": "Facility",
    "B_L2_Elevator": "Facility",
    "P_L3_Elevator": "Facility",
    "A_L0_Escalator": "Facility",
    "A_L1_Escalator": "Facility",
    "B_L2_Escalator": "Facility"
}

CATEGORY_TRANSLATIONS = {
    "English": {
        "Apparel": "Apparel",
        "Electronics": "Electronics",
        "Jewelry": "Jewelry",
        "Supermarket": "Supermarket",
        "Food & Beverage": "Food & Beverage",
        "Books": "Books",
        "Cinema": "Cinema",
        "Arcade": "Arcade",
        "Restroom": "Restroom",
        "Facility": "Facility"
    },
    "Simplified Chinese": {
        "Apparel": "服装饰品",
        "Electronics": "电子数码",
        "Jewelry": "珠宝首饰",
        "Supermarket": "超级市场",
        "Food & Beverage": "餐饮美食",
        "Books": "图书文具",
        "Cinema": "电影院",
        "Arcade": "娱乐电玩",
        "Restroom": "洗手间",
        "Facility": "公共设施"
    },
    "Malay": {
        "Apparel": "Pakaian",
        "Electronics": "Barangan Elektronik",
        "Jewelry": "Barang Kemas",
        "Supermarket": "Pasar Raya",
        "Food & Beverage": "Makanan & Minuman",
        "Books": "Buku",
        "Cinema": "Pawagam",
        "Arcade": "Pusat Rekreasi",
        "Restroom": "Tandas",
        "Facility": "Kemudahan"
    }
}

if "lang" not in st.session_state:
    st.session_state.lang = "English"
if "selected_start" not in st.session_state:
    st.session_state.selected_start = "A_L0_Entrance"
if "selected_dest" not in st.session_state:
    st.session_state.selected_dest = "P1"
if "assigned_parking" not in st.session_state:
    st.session_state.assigned_parking = None

if "clicked_location" not in st.session_state:
    st.session_state.clicked_location = None

DATASET_PATHS = ["/content/drive/MyDrive/FYP Smart Navigation/train-00", "./train-01", "./test-00"]

# ==============================================================================
# 2. Navigation nodes and boundaries
# ==============================================================================

LOCATION_ICONS = {
    "Fashion": "👗",
    "Footwear": "👟",
    "Electronics": "📱",
    "Food & Beverage": "🍔",
    "Supermarket": "🛒",
    "Department Store": "🏬",
    "Pharmacy & Health": "💊",
    "Entertainment": "🎬",
    "Services": "🛠️",
    "Elevator": "🛗",
    "Escalator": "🪜",
    "Stairs": "🧗",
    "Entrance": "🚪",
    "Restroom": "🚻",
    "Parking": "🅿️",
    "Default": "📍"
}

def get_location_icon(node_id):
    if "Elevator" in node_id:
        return LOCATION_ICONS["Elevator"]
    elif "Escalator" in node_id:
        return LOCATION_ICONS["Escalator"]
    elif "Stairs" in node_id:
        return LOCATION_ICONS["Stairs"]
    elif "Restroom" in node_id or "Toilet" in node_id:
        return LOCATION_ICONS["Restroom"]
    elif "Entrance" in node_id or "Exit" in node_id:
        return LOCATION_ICONS["Entrance"]
    elif "P_" in node_id or "Slot" in node_id or "Parking" in node_id:
        return LOCATION_ICONS["Parking"]

    cat_key = STORE_CATEGORIES.get(node_id)
    if cat_key and cat_key in LOCATION_ICONS:
        return LOCATION_ICONS[cat_key]

    return LOCATION_ICONS["Default"]

ROOM_POLYGONS = {
    # Ground floor
    "A_L0_Info": {
        "z": 0,
        "coords": [(-45, 18), (-30, 18), (-30, 30), (-45, 30)],
        "color": "#ADD8E6"
    },
    "A_L0_Entrance": {
        "z": 0,
        "coords": [(-45, -2), (-30, -2), (-30, 14), (-45, 14)],
        "color": "#708090"
    },
    "Mega Supermarket": {
        "z": 0,
        "coords": [(-25, 18), (25, 18), (25, 38), (-25, 38)],
        "color": "#98FB98"
    },
    "A_L0_Lobby": {
        "z": 0,
        "coords": [(-25, -2), (25, -2), (25, 14), (-25, 14)],
        "color": "#B0C4DE"
    },
    "Fashion Hub": {
        "z": 0,
        "coords": [(-25, -22), (25, -22), (25, -6), (-25, -6)],
        "color": "#E6E6FA"
    },
    "A_L0_Restroom": {
        "z": 0,
        "coords": [(30, 20), (42, 20), (42, 32), (30, 32)],
        "color": "#E0FFFF"
    },
    "A_L0_Elevator": {
        "z": 0,
        "coords": [(30, 6), (42, 6), (42, 18), (30, 18)],
        "color": "#FFD700"
    },
    "A_L0_Escalator": {
        "z": 0,
        "coords": [(30, -8), (42, -8), (42, 4), (30, 4)],
        "color": "#FFA07A"
    },
    "A_L0_Stairs": {
        "z": 0,
        "coords": [(30, -22), (42, -22), (42, -10), (30, -10)],
        "color": "#FF8C00"
    },

    # 1st floor
    "A_L1_Hallway":    {"z": 1, "coords": [(30, 10), (80, 10), (80, 60), (30, 60)], "color": "#87CEFA"},
    "Tech Gadgets":    {"z": 1, "coords": [(10, 10), (30, 10), (30, 35), (10, 35)], "color": "#9370DB"},
    "Jewel Box":       {"z": 1, "coords": [(10, 35), (30, 35), (30, 60), (10, 60)], "color": "#D8BFD8"},
    "Book Nook":       {"z": 1, "coords": [(35, 15), (55, 15), (55, 35), (35, 35)], "color": "#F5DEB3"},
    "A_L1_Elevator":   {"z": 1, "coords": [(80, 50), (95, 50), (95, 65), (80, 65)], "color": "#FFD700"},
    "A_L1_Stairs":     {"z": 1, "coords": [(80, 10), (95, 10), (95, 25), (80, 25)], "color": "#FF8C00"},
    "A_L1_Escalator":  {"z": 1, "coords": [(80, 30), (95, 30), (95, 45), (80, 45)], "color": "#FFA07A"},
    "A_L1_Restroom":   {"z": 1, "coords": [(35, 40), (50, 40), (50, 55), (35, 55)], "color": "#E0FFFF"},

    # 2nd floor
    "B_L2_Corridor":   {"z": 2, "coords": [(30, 10), (80, 10), (80, 60), (30, 60)], "color": "#5F9EA0"},
    "Cineplex Theater":{"z": 2, "coords": [(10, 10), (30, 10), (30, 35), (10, 35)], "color": "#CD5C5C"},
    "VR World & Arcade":{"z": 2, "coords": [(10, 35), (30, 35), (30, 60), (10, 60)], "color": "#FF69B4"},
    "Sky Food Court":  {"z": 2, "coords": [(35, 15), (75, 15), (75, 35), (35, 35)], "color": "#FF7F50"},
    "Gourmet Bites":   {"z": 2, "coords": [(35, 40), (55, 40), (55, 55), (35, 55)], "color": "#F4A460"},
    "B_L2_Elevator":   {"z": 2, "coords": [(80, 50), (95, 50), (95, 65), (80, 65)], "color": "#FFD700"},
    "B_L2_Stairs":     {"z": 2, "coords": [(80, 10), (95, 10), (95, 25), (80, 25)], "color": "#FF8C00"},
    "B_L2_Escalator":  {"z": 2, "coords": [(80, 30), (95, 30), (95, 45), (80, 45)], "color": "#FFA07A"},
    "B_L2_Restroom":   {"z": 2, "coords": [(60, 40), (75, 40), (75, 55), (60, 55)], "color": "#E0FFFF"},

    # Parking lot
    "P_L3_Aisle_Main": {"z": 3, "coords": [(10, 30), (95, 30), (95, 45), (10, 45)], "color": "#A9A9A9"},
    "P_L3_Elevator":   {"z": 3, "coords": [(80, 50), (95, 50), (95, 65), (80, 65)], "color": "#FFD700"},
    "P_L3_Stairs":     {"z": 3, "coords": [(80, 10), (95, 10), (95, 25), (80, 25)], "color": "#FF8C00"},
    "P1":              {"z": 3, "coords": [(10, 10), (25, 10), (25, 28), (10, 28)], "color": "#4682B4"},
    "P2":              {"z": 3, "coords": [(27, 10), (42, 10), (42, 28), (27, 28)], "color": "#4682B4"},
    "P3":              {"z": 3, "coords": [(44, 10), (59, 10), (59, 28), (44, 28)], "color": "#4682B4"},
    "P4":              {"z": 3, "coords": [(61, 10), (76, 10), (76, 28), (61, 28)], "color": "#4682B4"},
    "P5":              {"z": 3, "coords": [(10, 47), (25, 47), (25, 65), (10, 65)], "color": "#4682B4"},
    "P6":              {"z": 3, "coords": [(27, 47), (42, 47), (42, 65), (27, 65)], "color": "#4682B4"},
    "P7":              {"z": 3, "coords": [(44, 47), (59, 47), (59, 65), (44, 65)], "color": "#4682B4"},
    "P8":              {"z": 3, "coords": [(61, 47), (76, 47), (76, 65), (61, 65)], "color": "#4682B4"},
}

MULTI_CAD_NODES = {
    # Ground floor
    "A_L0_Info": [-37.5, 24.0, 0],
    "A_L0_Entrance": [-37.5, 6.0, 0],
    "Mega Supermarket": [0.0, 28.0, 0],
    "A_L0_Lobby": [0.0, 6.0, 0],
    "Fashion Hub": [0.0, -14.0, 0],
    "A_L0_Restroom": [36.0, 26.0, 0],
    "A_L0_Elevator": [36.0, 12.0, 0],
    "A_L0_Escalator": [36.0, -2.0, 0],
    "A_L0_Stairs": [36.0, -16.0, 0],

    # 1st floor
    "A_L1_Hallway":    (55.0, 35.0, 1.0), "Tech Gadgets": (20.0, 22.5, 1.0), "Jewel Box": (20.0, 47.5, 1.0),
    "Book Nook":       (45.0, 25.0, 1.0), "A_L1_Restroom": (42.5, 47.5, 1.0),
    "A_L1_Elevator":   (87.5, 57.5, 1.0), "A_L1_Stairs": (87.5, 17.5, 1.0), "A_L1_Escalator": (87.5, 37.5, 1.0),

    # 2nd floor
    "B_L2_Corridor":   (55.0, 35.0, 2.0), "Cineplex Theater": (20.0, 22.5, 2.0), "VR World & Arcade": (20.0, 47.5, 2.0),
    "Sky Food Court":  (55.0, 25.0, 2.0), "Gourmet Bites": (45.0, 47.5, 2.0), "B_L2_Restroom": (67.5, 47.5, 2.0),
    "B_L2_Elevator":   (87.5, 57.5, 2.0), "B_L2_Stairs": (87.5, 17.5, 2.0), "B_L2_Escalator": (87.5, 37.5, 2.0),

    # Parking lot
    "P1": (17.5, 19.0, 3.0), "P2": (34.5, 19.0, 3.0), "P3": (51.5, 19.0, 3.0), "P4": (68.5, 19.0, 3.0),
    "P5": (17.5, 56.0, 3.0), "P6": (34.5, 56.0, 3.0), "P7": (51.5, 56.0, 3.0), "P8": (68.5, 56.0, 3.0),
    "P_L3_Aisle_Main": (52.5, 37.5, 3.0),
    "P_L3_Elevator":   (87.5, 57.5, 3.0),
    "P_L3_Stairs":     (87.5, 17.5, 3.0),
}

# Neighbouring nodes
MULTI_CAD_GRAPH = {
    # Ground floor
    "A_L0_Entrance": {"A_L0_Lobby": 35.0, "Fashion Hub": 27.5},
    "Fashion Hub":   {"A_L0_Entrance": 27.5, "A_L0_Lobby": 37.5},
    "A_L0_Lobby":    {"A_L0_Entrance": 35.0, "Fashion Hub": 37.5, "A_L0_Info": 16.0, "Mega Supermarket": 20.0, "A_L0_Restroom": 15.0, "A_L0_Elevator": 38.0, "A_L0_Stairs": 38.0, "A_L0_Escalator": 33.0},
    "A_L0_Info":     {"A_L0_Lobby": 16.0},
    "Mega Supermarket": {"A_L0_Lobby": 20.0},
    "A_L0_Restroom": {"A_L0_Lobby": 15.0},
    "A_L0_Elevator": {"A_L0_Lobby": 38.0, "A_L1_Elevator": 15.0},
    "A_L0_Stairs":   {"A_L0_Lobby": 38.0, "A_L1_Stairs": 15.0},
    "A_L0_Escalator":{"A_L0_Lobby": 33.0, "A_L1_Escalator": 12.0},

    # 1st floor
    "A_L1_Elevator": {"A_L0_Elevator": 15.0, "A_L1_Hallway": 38.0, "B_L2_Elevator": 15.0},
    "A_L1_Stairs":   {"A_L0_Stairs": 15.0, "A_L1_Hallway": 38.0, "B_L2_Stairs": 15.0},
    "A_L1_Escalator":{"A_L0_Escalator": 12.0, "A_L1_Hallway": 33.0, "B_L2_Escalator": 12.0},
    "A_L1_Hallway":  {"A_L1_Elevator": 38.0, "A_L1_Stairs": 38.0, "A_L1_Escalator": 33.0, "Tech Gadgets": 37.5, "Jewel Box": 37.5, "Book Nook": 20.0, "A_L1_Restroom": 15.0},
    "Tech Gadgets":  {"A_L1_Hallway": 37.5},
    "Jewel Box":     {"A_L1_Hallway": 37.5},
    "Book Nook":     {"A_L1_Hallway": 20.0},
    "A_L1_Restroom": {"A_L1_Hallway": 15.0},

    # 2nd floor
    "B_L2_Elevator": {"A_L1_Elevator": 15.0, "B_L2_Corridor": 38.0, "P_L3_Elevator": 15.0},
    "B_L2_Stairs":   {"A_L1_Stairs": 15.0, "B_L2_Corridor": 38.0, "P_L3_Stairs": 15.0},
    "B_L2_Escalator":{"A_L1_Escalator": 12.0, "B_L2_Corridor": 33.0},
    "B_L2_Corridor": {"B_L2_Elevator": 38.0, "B_L2_Stairs": 38.0, "B_L2_Escalator": 33.0, "Cineplex Theater": 37.5, "VR World & Arcade": 37.5, "Sky Food Court": 20.0, "Gourmet Bites": 20.0, "B_L2_Restroom": 20.0},
    "Cineplex Theater":  {"B_L2_Corridor": 37.5},
    "VR World & Arcade": {"B_L2_Corridor": 37.5},
    "Sky Food Court":    {"B_L2_Corridor": 20.0},
    "Gourmet Bites":     {"B_L2_Corridor": 20.0},
    "B_L2_Restroom":     {"B_L2_Corridor": 20.0},

    # Parking lot
    "P1": {"P_L3_Aisle_Main": 20.0}, "P2": {"P_L3_Aisle_Main": 20.0},
    "P3": {"P_L3_Aisle_Main": 20.0}, "P4": {"P_L3_Aisle_Main": 20.0},
    "P5": {"P_L3_Aisle_Main": 20.0}, "P6": {"P_L3_Aisle_Main": 20.0},
    "P7": {"P_L3_Aisle_Main": 20.0}, "P8": {"P_L3_Aisle_Main": 20.0},
    "P_L3_Aisle_Main": {
        "P1": 20.0, "P2": 20.0, "P3": 20.0, "P4": 20.0,
        "P5": 20.0, "P6": 20.0, "P7": 20.0, "P8": 20.0,
        "P_L3_Elevator": 40.0, "P_L3_Stairs": 40.0
    },
    "P_L3_Elevator": {"P_L3_Aisle_Main": 40.0, "B_L2_Elevator": 15.0},
    "P_L3_Stairs":   {"P_L3_Aisle_Main": 40.0, "B_L2_Stairs": 15.0},
}

PARKING_SLOTS = {
    "P1": {"occupied": False}, "P2": {"occupied": True},
    "P3": {"occupied": False}, "P4": {"occupied": False},
    "P5": {"occupied": True},  "P6": {"occupied": False},
    "P7": {"occupied": False}, "P8": {"occupied": True},
}

def get_floor_bounds(floor_z):
    floor_rooms = [info for info in ROOM_POLYGONS.values() if info["z"] == floor_z]
    if not floor_rooms:
        return (0, 100, 0, 100)

    all_x = [pt[0] for room in floor_rooms for pt in room["coords"]]
    all_y = [pt[1] for room in floor_rooms for pt in room["coords"]]
    padding = 15
    return (min(all_x) - padding, max(all_x) + padding, min(all_y) - padding, max(all_y) + padding)

# ==============================================================================
# 3. Theta* pathfinding algorithm
# ==============================================================================

def extract_wall_segments(room_polygons):
    walls_by_floor = {}
    for room_info in room_polygons.values():
        z = room_info["z"]
        coords = room_info["coords"]
        if z not in walls_by_floor:
            walls_by_floor[z] = []
        num_pts = len(coords)
        for i in range(num_pts):
            walls_by_floor[z].append((coords[i], coords[(i + 1) % num_pts]))
    return walls_by_floor

WALL_SEGMENTS_BY_FLOOR = extract_wall_segments(ROOM_POLYGONS)

def line_segments_intersect(p1, p2, p3, p4):
    def ccw(a, b, c):
        return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])
    return (ccw(p1, p3, p4) != ccw(p2, p3, p4)) and (ccw(p1, p2, p3) != ccw(p1, p2, p4))

def has_line_of_sight_3d(node_a, node_b, node_coords, wall_segments):
    x1, y1, z1 = node_coords[node_a]
    x2, y2, z2 = node_coords[node_b]

    if z1 != z2:
        return False

    p1, p2 = (x1, y1), (x2, y2)
    floor_z = int(z1)

    if floor_z in wall_segments:
        for w1, w2 in wall_segments[floor_z]:
            if p1 == w1 or p1 == w2 or p2 == w1 or p2 == w2:
                continue
            if line_segments_intersect(p1, p2, w1, w2):
                return False
    return True

def euclidean_distance_3d(node_a, node_b, node_coords):
    x1, y1, z1 = node_coords[node_a]
    x2, y2, z2 = node_coords[node_b]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2 + ((z1 - z2) * 15.0)**2)

def theta_star_3d(start, goal, graph, node_coords, accessible_only=False):
    open_set = []
    heapq.heappush(open_set, (0, start))

    parent = {start: start}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0.0

    f_score = {node: float('inf') for node in graph}
    f_score[start] = euclidean_distance_3d(start, goal, node_coords)

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current != parent[current]:
                path.append(current)
                current = parent[current]
            path.append(start)
            return path[::-1]

        for neighbor, weight in graph[current].items():
            if accessible_only and ("Stairs" in neighbor or "Escalator" in neighbor):
                continue

            p_curr = parent[current]

            if has_line_of_sight_3d(p_curr, neighbor, node_coords, WALL_SEGMENTS_BY_FLOOR):
                candidate_g = g_score[p_curr] + euclidean_distance_3d(p_curr, neighbor, node_coords)
                if candidate_g < g_score[neighbor]:
                    parent[neighbor] = p_curr
                    g_score[neighbor] = candidate_g
                    f_score[neighbor] = candidate_g + euclidean_distance_3d(neighbor, goal, node_coords)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
            else:
                candidate_g = g_score[current] + weight
                if candidate_g < g_score[neighbor]:
                    parent[neighbor] = current
                    g_score[neighbor] = candidate_g
                    f_score[neighbor] = candidate_g + euclidean_distance_3d(neighbor, goal, node_coords)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None

# ==============================================================================
# 4. Map generation with Plotly
# ==============================================================================

def add_location_icons_to_2d_map(fig, active_floor_index, lang="English"):
    x_coords, y_coords, icon_labels, hover_texts = [], [], [], []

    for room_id, details in ROOM_POLYGONS.items():
        if room_id not in MULTI_CAD_NODES:
            continue

        node_z = MULTI_CAD_NODES[room_id][2]
        if int(node_z) == active_floor_index:
            x, y, _ = MULTI_CAD_NODES[room_id]
            icon = get_location_icon(room_id)
            room_name = POI_TRANSLATIONS.get(lang, {}).get(room_id, room_id)

            x_coords.append(x)
            y_coords.append(y)
            icon_labels.append(icon)
            hover_texts.append(f"{icon} {room_name}")

    fig.add_trace(
        go.Scatter(
            x=x_coords,
            y=y_coords,
            mode="text",
            text=icon_labels,
            textposition="middle center",
            textfont=dict(size=18),
            hoverinfo="text",
            hovertext=hover_texts,
            name="Location Icons",
            showlegend=False
        )
    )
    return fig

def add_location_icons_to_3d_map(fig, lang="English"):
    x_coords, y_coords, z_coords, icon_labels, hover_texts = [], [], [], [], []

    for room_id, coords in MULTI_CAD_NODES.items():
        x, y, z = coords
        icon = get_location_icon(room_id)
        room_name = POI_TRANSLATIONS.get(lang, {}).get(room_id, room_id)

        x_coords.append(x)
        y_coords.append(y)
        z_coords.append(z + 0.3)
        icon_labels.append(icon)
        hover_texts.append(f"{icon} {room_name}")

    fig.add_trace(
        go.Scatter3d(
            x=x_coords,
            y=y_coords,
            z=z_coords,
            mode="text",
            text=icon_labels,
            textfont=dict(size=14),
            hoverinfo="text",
            hovertext=hover_texts,
            name="3D Location Icons",
            showlegend=False
        )
    )
    return fig

def draw_polygon_shape(coords, fill_color, opacity=0.3, line_color="#333333"):
    x_pts = [p[0] for p in coords] + [coords[0][0]]
    y_pts = [p[1] for p in coords] + [coords[0][1]]
    return go.Scatter(
        x=x_pts, y=y_pts,
        fill="toself",
        fillcolor=fill_color,
        opacity=opacity,
        line=dict(color=line_color, width=2),
        hoverinfo="text",
        mode="lines"
    )

def render_2d_cad_view(active_floor_z, route_path=None, current_lang="English"):
    fig = go.Figure()

    floor_rooms = {
        r_id: poly["coords"]
        for r_id, poly in ROOM_POLYGONS.items()
        if poly["z"] == active_floor_z
    }

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
                customdata=[room_id] * len(x_coords),
                showlegend=False,
            )
        )

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

                x_mid = x_start + 0.6 * (x_end - x_start)
                y_mid = y_start + 0.6 * (y_end - y_start)

                fig.add_annotation(
                    x=x_mid,
                    y=y_mid,
                    ax=x_start,
                    ay=y_start,
                    xref="x",
                    yref="y",
                    axref="x",
                    ayref="y",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1.5,
                    arrowwidth=2.5,
                    arrowcolor="#CC0000"
                )

        start_node_id = route_path[0]
        dest_node_id = route_path[-1]

        if MULTI_CAD_NODES[start_node_id][2] == active_floor_z:
            start_x, start_y, _ = MULTI_CAD_NODES[start_node_id]
            fig.add_trace(
                go.Scatter(
                    x=[start_x],
                    y=[start_y],
                    mode="markers+text",
                    marker=dict(size=14, color="#FF0000", symbol="circle", line=dict(color="#8B0000", width=2)),
                    text=[" Start"],
                    textposition="top right",
                    textfont=dict(color="#FF0000", size=12, family="Arial Black"),
                    name="Start Location",
                    showlegend=False
                )
            )

        if MULTI_CAD_NODES[dest_node_id][2] == active_floor_z:
            dest_x, dest_y, _ = MULTI_CAD_NODES[dest_node_id]
            fig.add_trace(
                go.Scatter(
                    x=[dest_x],
                    y=[dest_y],
                    mode="markers+text",
                    marker=dict(size=14, color="#00FF00", symbol="circle", line=dict(color="#006600", width=2)),
                    text=[" Destination"],
                    textposition="top right",
                    textfont=dict(color="#00AA00", size=12, family="Arial Black"),
                    name="Destination",
                    showlegend=False
                )
            )

    for room_id, coords in floor_rooms.items():
        translated_name = POI_TRANSLATIONS.get(current_lang, {}).get(room_id, room_id)
        cx = sum([p[0] for p in coords]) / len(coords)
        cy = sum([p[1] for p in coords]) / len(coords)

        fig.add_trace(
            go.Scatter(
                x=[cx],
                y=[cy],
                text=[translated_name],
                mode="text",
                textfont=dict(
                    color="#000000",
                    size=12,
                    family="Arial Black, sans-serif"
                ),
                hoverinfo="text",
                showlegend=False
            )
        )

    min_x, max_x, min_y, max_y = get_floor_bounds(active_floor_z)

    fig.update_layout(
        height=650,  
        margin=dict(l=15, r=15, t=30, b=15),
        showlegend=False,
        plot_bgcolor="#FFB6C1",
        paper_bgcolor="#FFB6C1",
        xaxis=dict(range=[min_x - 5, max_x + 5], showgrid=True, zeroline=True, gridcolor="#E2E8F0"),
        yaxis=dict(range=[min_y - 5, max_y + 5], showgrid=True, zeroline=True, gridcolor="#E2E8F0", scaleanchor="x")
    )
    return fig

def render_3d_isometric_view(route_path=None, current_lang="English"):
    fig = go.Figure()

    for room_id, info in ROOM_POLYGONS.items():
        z_level = info["z"] * 40
        coords = info["coords"]

        x_pts = [p[0] for p in coords] + [coords[0][0]]
        y_pts = [p[1] for p in coords] + [coords[0][1]]
        z_pts = [z_level] * len(x_pts)

        translated_name = POI_TRANSLATIONS.get(current_lang, {}).get(room_id, room_id)

        fig.add_trace(go.Scatter3d(
            x=x_pts, y=y_pts, z=z_pts,
            mode="lines",
            line=dict(color=info["color"], width=4),
            name=translated_name,
            showlegend=False
        ))

    if route_path and len(route_path) > 0:
        sx, sy, sz = MULTI_CAD_NODES[route_path[0]]
        dx, dy, dz = MULTI_CAD_NODES[route_path[-1]]

        fig.add_trace(
            go.Scatter3d(
                x=[sx], y=[sy], z=[sz * 40],
                mode="markers+text",
                marker=dict(size=8, color="#FF0000"),
                text=["Start"],
                textposition="top center",
                textfont=dict(color="#FF0000", size=11),
                showlegend=False
            )
        )

        fig.add_trace(
            go.Scatter3d(
                x=[dx], y=[dy], z=[dz * 40],
                mode="markers+text",
                marker=dict(size=8, color="#00FF00"),
                text=["Destination"],
                textposition="top center",
                textfont=dict(color="#00AA00", size=11),
                showlegend=False
            )
        )

    if route_path and len(route_path) > 1:
        rx = [MULTI_CAD_NODES[n][0] for n in route_path]
        ry = [MULTI_CAD_NODES[n][1] for n in route_path]
        rz = [MULTI_CAD_NODES[n][2] * 40 for n in route_path]

        fig.add_trace(go.Scatter3d(
            x=rx, y=ry, z=rz,
            mode="lines+markers",
            line=dict(color="#FF0000", width=6),
            marker=dict(size=6, color="#8B0000"),
            name="Route Path"
        ))

        cone_x, cone_y, cone_z = [], [], []
        cone_u, cone_v, cone_w = [], [], []

        for i in range(len(route_path) - 1):
            x1, y1, z1_idx = MULTI_CAD_NODES[route_path[i]]
            x2, y2, z2_idx = MULTI_CAD_NODES[route_path[i+1]]
            z1, z2 = z1_idx * 40, z2_idx * 40

            cone_x.append(x1 + 0.6 * (x2 - x1))
            cone_y.append(y1 + 0.6 * (y2 - y1))
            cone_z.append(z1 + 0.6 * (z2 - z1))

            cone_u.append(x2 - x1)
            cone_v.append(y2 - y1)
            cone_w.append(z2 - z1)

        if cone_x:
            fig.add_trace(go.Cone(
                x=cone_x, y=cone_y, z=cone_z,
                u=cone_u, v=cone_v, w=cone_w,
                colorscale=[[0, '#CC0000'], [1, '#CC0000']],
                showscale=False, sizemode="absolute", sizeref=8, anchor="tip"
            ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(title="X (m)", backgroundcolor="#F8FAFC"),
            yaxis=dict(title="Y (m)", backgroundcolor="#F8FAFC"),
            zaxis=dict(title="Floor Level", backgroundcolor="#F8FAFC"),
            aspectmode="data"
        ),
        height=680,  
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return fig

def render_rooftop_parking_map(assigned_slot=None, route_path=None, current_lang="English"):
    fig = go.Figure()

    rooftop_rooms = {
        r_id: poly["coords"]
        for r_id, poly in ROOM_POLYGONS.items()
        if poly["z"] == 3
    }

    for room_id, coords in rooftop_rooms.items():
        x_coords = [c[0] for c in coords] + [coords[0][0]]
        y_coords = [c[1] for c in coords] + [coords[0][1]]

        fig.add_trace(
            go.Scatter(
                x=x_coords,
                y=y_coords,
                fill="toself",
                fillcolor="rgba(240, 240, 240, 0.5)",
                line=dict(color="#4A5568", width=1.5),
                hoverinfo="text",
                text=POI_TRANSLATIONS.get(current_lang, {}).get(
                    room_id, room_id
                ),
                showlegend=False,
            )
        )

    for slot_id, details in PARKING_SLOTS.items():
        if slot_id not in MULTI_CAD_NODES:
            continue

        cx, cy, _ = MULTI_CAD_NODES[slot_id]

        if slot_id == assigned_slot:
            fill_color = "rgba(59, 130, 246, 0.85)"
            border_color = "#1D4ED8"
            status_txt = "ASSIGNED TO YOU"
        elif details["occupied"]:
            fill_color = "rgba(239, 68, 68, 0.7)"
            border_color = "#B91C1C"
            status_txt = "OCCUPIED"
        else:
            fill_color = "rgba(34, 197, 94, 0.7)"
            border_color = "#15803D"
            status_txt = "AVAILABLE"

        box_w, box_h = 3.5, 6.0
        bx = [
            cx - box_w / 2, cx + box_w / 2, cx + box_w / 2,
            cx - box_w / 2, cx - box_w / 2
        ]
        by = [
            cy - box_h / 2, cy - box_h / 2, cy + box_h / 2,
            cy + box_h / 2, cy - box_h / 2
        ]

        fig.add_trace(
            go.Scatter(
                x=bx, y=by,
                fill="toself",
                fillcolor=fill_color,
                line=dict(color=border_color, width=2),
                hoverinfo="text",
                text=f"Slot {slot_id}: {status_txt}",
                showlegend=False
            )
        )

        fig.add_trace(
            go.Scatter(
                x=[cx], y=[cy],
                text=[slot_id],
                mode="text",
                textfont=dict(color="#FFFFFF", size=11, family="Arial Black"),
                hoverinfo="none",
                showlegend=False
            )
        )

    if route_path:
        rooftop_path = [node for node in route_path if int(MULTI_CAD_NODES[node][2]) == 3]
        if len(rooftop_path) > 1:
            px = [MULTI_CAD_NODES[n][0] for n in rooftop_path]
            py = [MULTI_CAD_NODES[n][1] for n in rooftop_path]
            fig.add_trace(
                go.Scatter(
                    x=px, y=py,
                    mode="lines+markers",
                    line=dict(color="#2563EB", width=4),
                    marker=dict(size=8, color="#1E40AF"),
                    name="Parking Route"
                )
            )

            for i in range(len(rooftop_path) - 1):
                x_start, y_start, _ = MULTI_CAD_NODES[rooftop_path[i]]
                x_end, y_end, _ = MULTI_CAD_NODES[rooftop_path[i + 1]]

                x_mid = x_start + 0.6 * (x_end - x_start)
                y_mid = y_start + 0.6 * (y_end - y_start)

                fig.add_annotation(
                    x=x_mid, y=y_mid,
                    ax=x_start, ay=y_start,
                    xref="x", yref="y", axref="x", ayref="y",
                    showarrow=True, arrowhead=2, arrowsize=1.5,
                    arrowwidth=2.5, arrowcolor="#1D4ED8"
                )

    min_x, max_x, min_y, max_y = get_floor_bounds(3)

    fig.update_layout(
        xaxis=dict(range=[min_x, max_x], showgrid=True, zeroline=False),
        yaxis=dict(range=[min_y, max_y], showgrid=True, zeroline=False, scaleanchor="x"),
        height=480,
        margin=dict(l=10, r=10, t=20, b=10),
        showlegend=False,
        plot_bgcolor="#F8F9FA"
    )
    return fig

# ==============================================================================
# 5. Step-by-step directions and smart parking
# ==============================================================================

def find_nearest_available_parking(start_node, graph, node_coords, accessible_only=False):
    available_slots = [
        slot_id for slot_id, details in PARKING_SLOTS.items()
        if not details.get("occupied", False) and slot_id in node_coords
    ]

    if not available_slots:
        return None, []

    nearest_slot = None
    shortest_path = []
    min_dist = float("inf")

    for slot_id in available_slots:
        path = theta_star_3d(start_node, slot_id, graph, node_coords, accessible_only=accessible_only)
        if path:
            dist = compute_route_summary(path)["total_distance"]
            if dist < min_dist:
                min_dist = dist
                nearest_slot = slot_id
                shortest_path = path

    return nearest_slot, shortest_path

def calculate_heading_angle(node_a, node_b, node_coords):
    x1, y1, _ = node_coords[node_a]
    x2, y2, _ = node_coords[node_b]
    return math.degrees(math.atan2(y2 - y1, x2 - x1)) % 360

def format_turn_instruction(angle_diff, distance, target_name, lang="English"):
    angle_diff = (angle_diff + 180) % 360 - 180

    phrases = {
        "English": {
            "straight": f"Continue straight for {distance:.1f}m towards {target_name}",
            "slight_right": f"Veer slightly right and walk {distance:.1f}m to {target_name}",
            "right": f"Turn right and walk {distance:.1f}m to {target_name}",
            "sharp_right": f"Make a sharp right turn and head {distance:.1f}m towards {target_name}",
            "slight_left": f"Veer slightly left and walk {distance:.1f}m to {target_name}",
            "left": f"Turn left and walk {distance:.1f}m to {target_name}",
            "sharp_left": f"Make a sharp left turn and head {distance:.1f}m towards {target_name}",
            "u_turn": f"Make a U-turn and walk {distance:.1f}m towards {target_name}"
        },
        "Simplified Chinese": {
            "straight": f"直行 {distance:.1f} 米，前往 {target_name}",
            "slight_right": f"向右前方偏转，步行 {distance:.1f} 米到达 {target_name}",
            "right": f"右转并步行 {distance:.1f} 米到达 {target_name}",
            "sharp_right": f"向右急转，步行 {distance:.1f} 米前往 {target_name}",
            "slight_left": f"向左前方偏转，步行 {distance:.1f} 米到达 {target_name}",
            "left": f"左转并步行 {distance:.1f} 米到达 {target_name}",
            "sharp_left": f"向左急转，步行 {distance:.1f} 米前往 {target_name}",
            "u_turn": f"掉头并步行 {distance:.1f} 米前往 {target_name}"
        },
        "Malay": {
            "straight": f"Jalan terus sejauh {distance:.1f}m ke {target_name}",
            "slight_right": f"Belok sedikit ke kanan dan jalan {distance:.1f}m ke {target_name}",
            "right": f"Belok kanan dan jalan {distance:.1f}m ke {target_name}",
            "sharp_right": f"Belok tajam ke kanan dan jalan {distance:.1f}m ke {target_name}",
            "slight_left": f"Belok sedikit ke kiri dan jalan {distance:.1f}m ke {target_name}",
            "left": f"Belok kiri dan jalan {distance:.1f}m ke {target_name}",
            "sharp_left": f"Belok tajam ke kiri dan jalan {distance:.1f}m ke {target_name}",
            "u_turn": f"Buat pusingan U dan jalan {distance:.1f}m ke {target_name}"
        }
    }

    lang_dict = phrases.get(lang, phrases["English"])

    if -22.5 <= angle_diff <= 22.5: return lang_dict["straight"]
    elif 22.5 < angle_diff <= 67.5: return lang_dict["slight_right"]
    elif 67.5 < angle_diff <= 112.5: return lang_dict["right"]
    elif 112.5 < angle_diff <= 157.5: return lang_dict["sharp_right"]
    elif -67.5 <= angle_diff < -22.5: return lang_dict["slight_left"]
    elif -112.5 <= angle_diff < -67.5: return lang_dict["left"]
    elif -157.5 <= angle_diff < -112.5: return lang_dict["sharp_left"]
    else: return lang_dict["u_turn"]

def generate_detailed_directions(path, node_coords, lang="English"):
    if not path or len(path) < 2: return []

    directions = []

    start_icon = get_location_icon(path[0])
    dest_icon = get_location_icon(path[1])

    start_poi = f"{POI_TRANSLATIONS.get(lang, {}).get(path[0], path[0])}"
    first_dest_poi = f"{POI_TRANSLATIONS.get(lang, {}).get(path[1], path[1])}"
    init_dist = euclidean_distance_3d(path[0], path[1], node_coords)

    start_text = {
        "English": f"Start at **{start_poi}** and head towards **{first_dest_poi}** ({init_dist:.1f}m).",
        "Simplified Chinese": f"从 **{start_poi}** 出发，前往 **{first_dest_poi}**（{init_dist:.1f} 米）。",
        "Malay": f"Mula di **{start_poi}** dan menuju ke **{first_dest_poi}** ({init_dist:.1f}m)."
    }
    directions.append({"step": 1, "text": start_text.get(lang, start_text["English"]), "icon": "🛫"})

    for i in range(1, len(path) - 1):
        prev_node, curr_node, next_node = path[i - 1], path[i], path[i + 1]

        curr_icon = get_location_icon(curr_node)
        next_icon = get_location_icon(next_node)

        curr_poi = f"{POI_TRANSLATIONS.get(lang, {}).get(curr_node, curr_node)}"
        next_poi = f"{POI_TRANSLATIONS.get(lang, {}).get(next_node, next_node)}"

        z_curr, z_next = node_coords[curr_node][2], node_coords[next_node][2]

        if z_curr != z_next:
            target_floor_label = get_translated_floor_name(z_next, lang=lang)
            if "Elevator" in curr_node or "Elevator" in next_node:
                trans_text = {
                    "English": f"Take the **Elevator** at {curr_poi} to **{target_floor_label}**.",
                    "Simplified Chinese": f"在 {curr_poi} 乘坐**电梯**到达 **{target_floor_label}**。",
                    "Malay": f"Naik **Lif** di {curr_poi} ke **{target_floor_label}**."
                }
                icon = "🛗"
            elif "Escalator" in curr_node or "Escalator" in next_node:
                trans_text = {
                    "English": f"Take the **Escalator** at {curr_poi} to **{target_floor_label}**.",
                    "Simplified Chinese": f"在 {curr_poi} 乘坐**自动扶梯**到达 **{target_floor_label}**。",
                    "Malay": f"Gunakan **Eskalator** di {curr_poi} ke **{target_floor_label}**."
                }
                icon = "🪜"
            else:
                trans_text = {
                    "English": f"Take the **Stairs** at {curr_poi} to **{target_floor_label}**.",
                    "Simplified Chinese": f"在 {curr_poi} 使用**安全楼梯**到达 **{target_floor_label}**。",
                    "Malay": f"Gunakan **Tangga** di {curr_poi} ke **{target_floor_label}**."
                }
                icon = "🧗"

            directions.append({"step": len(directions) + 1, "text": trans_text.get(lang, trans_text["English"]), "icon": icon})
            continue

        prev_heading = calculate_heading_angle(prev_node, curr_node, node_coords)
        next_heading = calculate_heading_angle(curr_node, next_node, node_coords)
        angle_diff = next_heading - prev_heading

        step_dist = euclidean_distance_3d(curr_node, next_node, node_coords)
        instruction_str = format_turn_instruction(angle_diff, step_dist, f"**{next_poi}**", lang=lang)

        angle_diff_norm = (angle_diff + 180) % 360 - 180
        icon = "↪️" if angle_diff_norm > 22.5 else ("↩️" if angle_diff_norm < -22.5 else "⬆️")

        directions.append({"step": len(directions) + 1, "text": instruction_str, "icon": icon})

    final_icon = get_location_icon(path[-1])
    final_poi = f"{POI_TRANSLATIONS.get(lang, {}).get(path[-1], path[-1])}"
    arrival_text = {
        "English": f"You have arrived at your destination: **{final_poi}**.",
        "Simplified Chinese": f"您已到达目的地：**{final_poi}**。",
        "Malay": f"Anda telah tiba di destinasi: **{final_poi}**."
    }
    directions.append({"step": len(directions) + 1, "text": arrival_text.get(lang, arrival_text["English"]), "icon": "🏁"})

    return directions

def compute_route_summary(path):
    if not path or len(path) < 2: return {"total_distance": 0, "floors_crossed": 0, "steps": 0}

    total_dist = 0
    floors_visited = set()

    for i in range(len(path) - 1):
        curr_node, nxt_node = path[i], path[i+1]
        z1, z2 = MULTI_CAD_NODES[curr_node][2], MULTI_CAD_NODES[nxt_node][2]

        floors_visited.add(z1)
        floors_visited.add(z2)

        if z1 == z2:
            total_dist += euclidean_distance_3d(curr_node, nxt_node, MULTI_CAD_NODES)
        else:
            total_dist += 15.0

    return {
        "total_distance": round(total_dist, 1),
        "floors_crossed": max(0, len(floors_visited) - 1),
        "steps": len(path) - 1
    }

def format_location_label(room_id, lang):
    icon = get_location_icon(room_id)
    z_val = int(MULTI_CAD_NODES[room_id][2])
    floor_code = "R" if z_val == 3 else (f"{z_val}F" if z_val > 0 else "GF")
    name = POI_TRANSLATIONS.get(lang, {}).get(room_id, room_id)
    clean_name = name.split('(')[0].strip()

    cat_key = STORE_CATEGORIES.get(room_id)
    if cat_key:
        cat_name = CATEGORY_TRANSLATIONS.get(lang, {}).get(cat_key, cat_key)
        return f"[{floor_code}] {clean_name} ({cat_name})"

    return f"[{floor_code}] {clean_name}"

# ==============================================================================
# 6. UI configuration
# ==============================================================================

t = LOCALIZATION[st.session_state.lang]

st.title(t["title"])
st.caption(t["subtitle"])

with st.sidebar:
    st.header(
        t["config_header"]
    )
    selected_language_key = st.selectbox(
        t["select_lang"],
        options=list(LOCALIZATION.keys()),
        format_func=lambda key: LANG_OPTION_LABELS[st.session_state.lang][key],
        index=list(LOCALIZATION.keys()).index(st.session_state.lang)
    )
    if selected_language_key != st.session_state.lang:
        st.session_state.lang = selected_language_key
        st.rerun()

with st.expander(f"⚙️ {t['nav_controls']}", expanded=True):
    col_start, col_dest = st.columns(2)
    room_options = list(ROOM_POLYGONS.keys())

    with col_start:
        start_node = st.selectbox(
            t["start_loc"],
            options=room_options,
            format_func=lambda room_id: format_location_label(room_id, st.session_state.lang),
            index=room_options.index(st.session_state.selected_start) if st.session_state.selected_start in room_options else 0
        )
    with col_dest:
        dest_node = st.selectbox(
            t["dest_loc"],
            options=room_options,
            format_func=lambda room_id: format_location_label(room_id, st.session_state.lang),
            index=room_options.index(st.session_state.selected_dest) if st.session_state.selected_dest in room_options else len(room_options) - 1
        )

    st.session_state.selected_start = start_node
    st.session_state.selected_dest = dest_node

    route_pref = st.radio(
        t["route_type"],
        options=[t["shortest"], t["accessible"]],
        horizontal=True
    )
    accessible_flag = (route_pref == t["accessible"])

    st.info(
        f"{t['current_route_lbl']}: `{format_location_label(st.session_state.selected_start, st.session_state.lang)}` ➔ `{format_location_label(st.session_state.selected_dest, st.session_state.lang)}`"
    )

path = theta_star_3d(
    st.session_state.selected_start,
    st.session_state.selected_dest,
    MULTI_CAD_GRAPH,
    MULTI_CAD_NODES,
    accessible_only=accessible_flag
)

nearest_slot_id, parking_path = find_nearest_available_parking(
    st.session_state.selected_start,
    MULTI_CAD_GRAPH,
    MULTI_CAD_NODES,
    accessible_only=accessible_flag
)
st.session_state.assigned_parking = nearest_slot_id

home_tab_title = {
    "English": "🏠 Home",
    "Simplified Chinese": "🏠 首页",
    "Malay": "🏠 Halaman Utama",
}.get(st.session_state.lang, "🏠 Home")

tab_home, tab_map, tab_dir, tab_park = st.tabs([
    home_tab_title,
    t["tab_nav"],
    t["tab_directions"],
    t["tab_parking"],
])

# Home page tab
with tab_home:
    st.markdown(f"""
    ### {t['home_title']}
    {t['home_desc']}
    """)

    st.divider()

    col_f1, col_f2, col_f3 = st.columns(3)

    with col_f1:
        st.subheader(t["feat_map_title"])
        st.write(t["feat_map_desc"])

    with col_f2:
        st.subheader(t["feat_turn_title"])
        st.write(t["feat_turn_desc"])

    with col_f3:
        st.subheader(t["feat_park_title"])
        st.write(t["feat_park_desc"])

    st.divider()

    c1, c2, c3, c4 = st.columns(4)
    total_locations = len(ROOM_POLYGONS)
    total_floors = len(FLOOR_TRANSLATIONS["English"])
    total_slots = len(PARKING_SLOTS) if "PARKING_SLOTS" in globals() else 0
    available_slots = (
        sum(1 for s in PARKING_SLOTS.values() if not s["occupied"])
        if "PARKING_SLOTS" in globals()
        else 0
    )

    c1.metric(t["poi_metric"], total_locations)
    c2.metric(t["floors_metric"], total_floors)
    c3.metric(t["spots_metric"], total_slots)
    c4.metric(t["available_metric"], available_slots)

    st.divider()

    category_header = {
        "English": "🏷️ Store Directory by Category",
        "Simplified Chinese": "🏷️ 分类店铺指南",
        "Malay": "🏷️ Direktori Kedai Mengikut Kategori"
    }.get(st.session_state.lang, "🏷️ Store Directory by Category")

    st.subheader(category_header)

    if "STORE_CATEGORIES" in globals() and STORE_CATEGORIES:
        categorized_stores = {}
        for room_id, cat_key in STORE_CATEGORIES.items():
            categorized_stores.setdefault(cat_key, []).append(room_id)

        for cat_key, room_ids in categorized_stores.items():
            translated_cat = CATEGORY_TRANSLATIONS.get(st.session_state.lang, {}).get(cat_key, cat_key)

            with st.expander(f"📁 **{translated_cat}** ({len(room_ids)})", expanded=True):
                store_cols = st.columns(2)
                for idx, room_id in enumerate(room_ids):
                    col = store_cols[idx % 2]

                    icon = get_location_icon(room_id)
                    z_val = int(MULTI_CAD_NODES[room_id][2]) if room_id in MULTI_CAD_NODES else 0
                    floor_code = "R" if z_val == 3 else (f"{z_val}F" if z_val > 0 else "GF")

                    raw_name = POI_TRANSLATIONS.get(st.session_state.lang, {}).get(room_id, room_id)
                    clean_name = raw_name.split('(')[0].strip()

                    col.markdown(f"- **{clean_name}** `[{floor_code}]`")
    else:
        st.info("No store categories defined.")

    st.divider()



# Mall map tab
with tab_map:
    view_type = st.radio(
        t["view_mode"],
        options=[t["view_2d"], t["view_3d"]],
        horizontal=True
    )

    selected_data = None

    if view_type == t["view_2d"]:
        floor_select = st.selectbox(
            t["active_floor"],
            options=[0, 1, 2, 3],
            format_func=lambda x: get_translated_floor_name(x, lang=st.session_state.lang)
        )
        fig_2d = render_2d_cad_view(floor_select, route_path=path, current_lang=st.session_state.lang)

        selected_data = st.plotly_chart(
            fig_2d,
            use_container_width=True,
            on_select="rerun",
            selection_mode="points"
        )
    else:
        fig_3d = render_3d_isometric_view(route_path=path, current_lang=st.session_state.lang)
        selected_data = st.plotly_chart(
            fig_3d,
            use_container_width=True,
            on_select="rerun",
            selection_mode="points"
        )

    if selected_data and "selection" in selected_data and selected_data["selection"]["points"]:
        point = selected_data["selection"]["points"][0]
        clicked_id = None

        if "customdata" in point and point["customdata"]:
            clicked_id = point["customdata"]
        elif "text" in point:
            raw_text = point["text"]
            for room_key in ROOM_POLYGONS.keys():
                t_name = POI_TRANSLATIONS.get(st.session_state.lang, {}).get(room_key, room_key)
                if t_name == raw_text or room_key == raw_text:
                    clicked_id = room_key
                    break

        if clicked_id and clicked_id in ROOM_POLYGONS:
            st.session_state.clicked_location = clicked_id

    if st.session_state.clicked_location:
        loc_id = st.session_state.clicked_location
        loc_name = POI_TRANSLATIONS.get(st.session_state.lang, {}).get(loc_id, loc_id)

        st.info(f"📍 Selected on map: **{loc_name}**")
        col_btn1, col_btn2, col_btn3 = st.columns(3)

        with col_btn1:
            if st.button("🚩 Set as Start", key="btn_set_start", use_container_width=True):
                st.session_state.selected_start = loc_id
                st.session_state.clicked_location = None
                st.rerun()

        with col_btn2:
            if st.button("🏁 Set as Destination", key="btn_set_dest", use_container_width=True):
                st.session_state.selected_dest = loc_id
                st.session_state.clicked_location = None
                st.rerun()

        with col_btn3:
            if st.button("❌ Cancel", key="btn_cancel_select", use_container_width=True):
                st.session_state.clicked_location = None
                st.rerun()

# Directions tab
with tab_dir:
    st.subheader(t["route_summary"])
    if path:
        summary = compute_route_summary(path)
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

# Parking tab
with tab_park:
    st.subheader(t["parking_sec"])

    assigned_slot = st.session_state.get("assigned_parking", None)

    if assigned_slot:
        start_label = format_location_label(st.session_state.selected_start, st.session_state.lang)
        slot_icon = get_location_icon(assigned_slot)
        st.success(f"{t['nearest_spot_found']}: `{slot_icon} {assigned_slot}` ({t['rooftop_lot']}) {t['from_lbl']} `{start_label}`")

        fig_parking = render_rooftop_parking_map(
            assigned_slot=assigned_slot,
            route_path=parking_path,
            current_lang=st.session_state.lang
        )
        st.plotly_chart(fig_parking, use_container_width=True)

        if parking_path:
            p_summary = compute_route_summary(parking_path)
            st.markdown("---")
            st.subheader(t["parking_route_summary"])

            p_col1, p_col2, p_col3 = st.columns(3)
            p_col1.metric(t["dist_to_spot"], f"{p_summary['total_distance']} m")
            p_col2.metric(t["floors_to_ascend"], p_summary["floors_crossed"])
            p_col3.metric(t["total_steps"], p_summary["steps"])

            st.markdown("---")
            st.subheader(t["parking_turn_by_turn"])
            parking_steps = generate_detailed_directions(parking_path, MULTI_CAD_NODES, lang=st.session_state.lang)

            for step_info in parking_steps:
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
            current_lang=st.session_state.lang
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
        st.caption("📐 **Vector Processing:** FloorPlanCAD Parser (DXF/SVG Topology)")
    with foot_col3:
        st.caption("🌐 **Localization:** Active Multilingual Engine")

if __name__ == "__main__":
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
    render_system_footer()
