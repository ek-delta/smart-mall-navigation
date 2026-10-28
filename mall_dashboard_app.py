import math
import heapq
import random
import copy
import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import Fullscreen

# ==============================================================================
# 1. Page Config & Localization Dictionary
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
        "view_2d": "2D Folium Map Plan",
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
        "home_title": "Welcome to the Smart Mall Navigation System",
        "home_desc": "Navigate multi-floor shopping mall with real-time 2D pathfinding, routing options, and automated parking allocation with step-by-step directions.",
        "poi_metric": "📍 Points of Interest",
        "floors_metric": "🏢 Total Floors",
        "spots_metric": "🅿️ Total Parking Spots",
        "available_metric": "🟢 Available Spots",
        "current_route_lbl": "📍 Current Route",
        "step_lbl": "Step",
        "nearest_spot_found": "📍 Nearest Spot Found",
        "rooftop_lot": "Rooftop Parking Lot",
        "from_lbl": "from",
        "config_header": "⚙️ Settings",
        "selected_on_map": "📍 Selected on map: **{location}**",
        "btn_set_start": "🚩 Set as Start",
        "btn_set_dest": "🏁 Set as Destination",
        "btn_cancel": "❌ Cancel",
        "intermediate_stops": "📍 Intermediate Stops",
        "stop_lbl": "Stop {idx}",
        "btn_add_stop_manual": "➕ Add Intermediate Stop Manually",
        "btn_interactive_pick": "🗺️ Interactive Route Selection on Map",
        "btn_cancel_interactive": "⏹️ Cancel Interactive Map Selection",
        "btn_reset_all": "🗑️ Reset All",
        "pick_step_1": "👇 *Step 1:* Click anywhere on the map below to set as *Start Location*.",
        "pick_step_2": "👇 *Step 2:* Click anywhere on the map to add *Intermediate Stops* (or click button below when ready for Destination).",
        "pick_step_3": "👇 *Step 3:* Click anywhere on the map to set as *Destination*.",
        "btn_done_adding_stops": "➡️ Done Adding Stops (Next: Pick Destination)",
        "btn_add_as_stop": "➕ Add as Stop",
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
        "view_2d": "2D Folium 交互地图",
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
        "home_title": "欢迎使用智能商场导航与停车系统",
        "home_desc": "支持多楼层商场的实时路径规划、无障碍路线选择及自动车位分配。",
        "poi_metric": "📍 兴趣点数量",
        "floors_metric": "🏢 总楼层数",
        "spots_metric": "🅿️ 总车位数",
        "available_metric": "🟢 空余车位",
        "current_route_lbl": "📍 当前路线",
        "step_lbl": "步骤",
        "nearest_spot_found": "📍 已为您找到最近车位",
        "rooftop_lot": "顶层露天停车场",
        "from_lbl": "出发地：",
        "config_header": "⚙️ 系统配置",
        "selected_on_map": "📍 在地图选择：**{location}**",
        "btn_set_start": "🚩 设为起点",
        "btn_set_dest": "🏁 设为终点",
        "btn_cancel": "❌ 取消",
        "intermediate_stops": "📍 途经点 (中转站)",
        "stop_lbl": "途经点 {idx}",
        "btn_add_stop_manual": "➕ 手动添加途经点",
        "btn_interactive_pick": "🗺️ 地图交互式路线选择",
        "btn_cancel_interactive": "⏹️ 取消地图选择模式",
        "btn_reset_all": "🗑️ 重置全部",
        "pick_step_1": "👇 *步骤 1：* 点击地图任意位置设为 *起点位置*。",
        "pick_step_2": "👇 *步骤 2：* 点击地图任意位置添加 *途经点*（若已添加完毕，请点击下方按钮选择终点）。",
        "pick_step_3": "👇 *步骤 3：* 点击地图任意位置设为 *终点位置*。",
        "btn_done_adding_stops": "➡️ 完成添加途经点 (下一步: 选择终点)",
        "btn_add_as_stop": "➕ 添加为途经点",
    },
    "Malay": {
        "title": "🏢 Sistem Navigasi & Tempat Letak Kereta Pusat Beli-Belah Smart",
        "subtitle": "Navigasi Laluan Lebih Mudah, Laluan Mesra OKU & Pengurusan Tempat Letak Kereta",
        "select_lang": "Bahasa",
        "nav_controls": "Kawalan Navigasi",
        "start_loc": "Lokasi Permulaan",
        "dest_loc": "Destinasi",
        "route_type": "Pilihan Laluan",
        "shortest": "Laluan Terpendek",
        "accessible": "Mesra OKU (Lif Sahaja)",
        "view_mode": "Mod Paparan Peta",
        "view_2d": "Pelan Peta Interaktif Folium 2D",
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
        "home_title": "Selamat Datang ke Sistem Navigasi Pusat Beli-Belah Smart",
        "home_desc": "Navigasi pusat beli-belah bertingkat dengan laluan 2D masa nyata, pilihan laluan mesra OKU, dan automatik tempat letak kereta.",
        "poi_metric": "📍 Titik Tumpuan (POI)",
        "floors_metric": "🏢 Jumlah Tingkat",
        "spots_metric": "🅿️ Jumlah Ruang Letak Kereta",
        "available_metric": "🟢 Ruang Kosong",
        "current_route_lbl": "📍 Laluan Semasa",
        "step_lbl": "Langkah",
        "nearest_spot_found": "📍 Tempat Letak Kereta Terdekat Ditemui",
        "rooftop_lot": "Kawasan Tempat Letak Kereta Bumbung",
        "from_lbl": "dari",
        "config_header": "⚙️ Konfigurasi",
        "selected_on_map": "📍 Dipilih pada peta: **{location}**",
        "btn_set_start": "🚩 Tetapkan sebagai Permulaan",
        "btn_set_dest": "🏁 Tetapkan sebagai Destinasi",
        "btn_cancel": "❌ Batal",
        "intermediate_stops": "📍 Hentian Antara",
        "stop_lbl": "Hentian {idx}",
        "btn_add_stop_manual": "➕ Tambah Hentian Antara Secara Manual",
        "btn_interactive_pick": "🗺️ Pemilihan Laluan Interaktif pada Peta",
        "btn_cancel_interactive": "⏹️ Batal Pemilihan Peta Interaktif",
        "btn_reset_all": "🗑️ Set Semula Semua",
        "pick_step_1": "👇 *Langkah 1:* Klik di mana-mana pada peta untuk tetapkan *Lokasi Permulaan*.",
        "pick_step_2": "👇 *Langkah 2:* Klik di mana-mana pada peta untuk tambah *Hentian Antara* (atau klik butang di bawah apabila sedia untuk Destinasi).",
        "pick_step_3": "👇 *Langkah 3:* Klik di mana-mana pada peta untuk tetapkan *Destinasi*.",
        "btn_done_adding_stops": "➡️ Selesai Menambah Hentian (Seterusnya: Pilih Destinasi)",
        "btn_add_as_stop": "➕ Tambah sebagai Hentian",
    }
}

FLOOR_TRANSLATIONS = {
    "English": {0: "Ground Floor [GF]", 1: "1st Floor [1F]", 2: "2nd Floor [2F]", 3: "Rooftop Parking Lot [R]"},
    "Simplified Chinese": {0: "底层 [GF]", 1: "1层 [1F]", 2: "2层 [2F]", 3: "屋顶露台与停车场 [R]"},
    "Malay": {0: "Aras Bawah [GF]", 1: "Aras 1 [1F]", 2: "Aras 2 [2F]", 3: "Dek Bumbung & Tempat Letak Kereta [R]"}
}

def get_translated_floor_name(z_index, lang="English"):
    z_int = int(z_index)
    lang_dict = FLOOR_TRANSLATIONS.get(lang, FLOOR_TRANSLATIONS["English"])
    return lang_dict.get(z_int, f"Level {z_int}")

POI_TRANSLATIONS = {
    "English": {
        "A_L0_Entrance": "🚪Main Entrance (GF)", "A_L0_Lobby": "📍Central Lobby (GF)", "A_L0_Info": "🛠️Information Desk",
        "A_L0_Elevator": "🛗Elevator (GF)", "A_L0_Stairs": "🧗Stairwell (GF)", "A_L0_Escalator": "🪜Escalator (GF)",
        "A_L0_Restroom": "Restroom (GF)", "A_L1_Hallway": "🚪Corridor (1F)", "A_L1_Elevator": "🛗Elevator (1F)",
        "A_L1_Stairs": "🧗Stairwell (1F)", "A_L1_Escalator": "🪜Escalator (1F)", "A_L1_Restroom": "Restroom (1F)",
        "B_L2_Corridor": "📍Main Hall (2F)", "B_L2_Elevator": "🛗Elevator (2F)", "B_L2_Stairs": "🧗Stairwell (2F)",
        "B_L2_Escalator": "🪜Escalator (2F)", "B_L2_Restroom": "Restroom (2F)", "P_L3_Aisle_Main": "🚪Main Drive Aisle (R)",
        "P_L3_Elevator": "🛗Elevator (R)", "P_L3_Stairs": "🧗Stairwell (R)", "P_L3_Escalator": "🪜Escalator (R)",
        "P_L3_Driveway_Entrance": "🚪Entrance Ramp (R)", "P_L3_Driveway_Exit": "🚪Exit Ramp (R)",
        "Fashion Hub": "👗Fashion Hub", "Tech Gadgets": "📱Tech Gadgets", "Jewel Box": "👗Jewel Box",
        "Mega Supermarket": "🛒Mega Supermarket", "Gourmet Bites": "🍔Gourmet Bites", "Book Nook": "🛒Book Nook",
        "Cineplex Theater": "🎬Cineplex Theater", "VR World & Arcade": "🎬Arcade", "Sky Food Court": "🍔Sky Food Court",
        "P1": "🅿️Spot 1", "P2": "🅿️Spot 2", "P3": "🅿️Spot 3", "P4": "🅿️Spot 4",
        "P5": "🅿️Spot 5", "P6": "🅿️Spot 6", "P7": "🅿️Spot 7", "P8": "🅿️Spot 8",
    },
    "Simplified Chinese": {
        "A_L0_Entrance": "🚪正门入口 (底层)", "A_L0_Lobby": "📍中央大堂 (底层)", "A_L0_Info": "🛠️问讯服务台",
        "A_L0_Elevator": "🛗电梯 (底层)", "A_L0_Stairs": "🧗楼梯 (底层)", "A_L0_Escalator": "🪜自动扶梯 (底层)",
        "A_L0_Restroom": "洗手间 (底层)", "A_L1_Hallway": "🚪主走廊 (一楼)", "A_L1_Elevator": "🛗电梯 (一楼)",
        "A_L1_Stairs": "🧗楼梯 (一楼)", "A_L1_Escalator": "🪜自动扶梯 (一楼)", "A_L1_Restroom": "洗手间 (一楼)",
        "B_L2_Corridor": "📍主大厅 (二楼)", "B_L2_Elevator": "🛗电梯 (二楼)", "B_L2_Stairs": "🧗楼梯 (二楼)",
        "B_L2_Escalator": "🪜自动扶梯 (二楼)", "B_L2_Restroom": "洗手间 (二楼)", "P_L3_Aisle_Main": "🚪楼顶车库主车道",
        "P_L3_Elevator": "🛗楼顶电梯间", "P_L3_Stairs": "🧗楼顶楼梯", "P_L3_Escalator": "🪜楼顶自动扶梯",
        "P_L3_Driveway_Entrance": "🚪楼顶入口", "P_L3_Driveway_Exit": "🚪楼顶出口",
        "Fashion Hub": "👗时尚中心 (Fashion Hub)", "Tech Gadgets": "📱酷科技数码 (Tech Gadgets)", "Jewel Box": "👗璀璨珠宝 (Jewel Box)",
        "Mega Supermarket": "🛒大型超级市场 (Mega Supermarket)", "Gourmet Bites": "🍔美食小吃 (Gourmet Bites)", "Book Nook": "🛒书香角 (Book Nook)",
        "Cineplex Theater": "🎬影城 (Cineplex Theater)", "VR World & Arcade": "🎬电玩城 (& Arcade)", "Sky Food Court": "🍔云端美食广场 (Sky Food Court)",
        "P1": "🅿️停车位 1", "P2": "🅿️停车位 2", "P3": "🅿️停车位 3", "P4": "🅿️停车位 4",
        "P5": "🅿️停车位 5", "P6": "🅿️停车位 6", "P7": "🅿️停车位 7", "P8": "🅿️停车位 8",
    },
    "Malay": {
        "A_L0_Entrance": "🚪Pintu Masuk Utama (Tingkat Bawah)", "A_L0_Lobby": "📍Lobi Utama (Tingkat Bawah)", "A_L0_Info": "🛠️Kaunter Maklumat",
        "A_L0_Elevator": "🛗Lif (Tingkat Bawah)", "A_L0_Stairs": "🧗Tangga (Tingkat Bawah)", "A_L0_Escalator": "🪜Eskalator (Tingkat Bawah)",
        "A_L0_Restroom": "Tandas (Tingkat Bawah)", "A_L1_Hallway": "🚪Koridor (Tingkat 1)", "A_L1_Elevator": "🛗Lif (Tingkat 1)",
        "A_L1_Stairs": "🧗Tangga (Tingkat 1)", "A_L1_Escalator": "🪜Eskalator (Tingkat 1)", "A_L1_Restroom": "Tandas (Tingkat 1)",
        "B_L2_Corridor": "📍Dewan Utama (Tingkat 2)", "B_L2_Elevator": "🛗Lif (Tingkat 2)", "B_L2_Stairs": "🧗Tangga (Tingkat 2)",
        "B_L2_Escalator": "🪜Eskalator (Tingkat 2)", "B_L2_Restroom": "Tandas (Tingkat 2)", "P_L3_Aisle_Main": "🚪Laluan Utama Kenderaan (Bumbung)",
        "P_L3_Elevator": "🛗Lif (Bumbung)", "P_L3_Stairs": "🧗Tangga (Bumbung)", "P_L3_Escalator": "🪜Eskalator (Bumbung)",
        "P_L3_Driveway_Entrance": "🚪Laluan Masuk Kenderaan (Bumbung)", "P_L3_Driveway_Exit": "🚪Laluan Keluar Kenderaan (Bumbung)",
        "Fashion Hub": "👗Fashion Hub", "Tech Gadgets": "📱Tech Gadgets", "Jewel Box": "👗Jewel Box",
        "Mega Supermarket": "🛒Mega Supermarket", "Gourmet Bites": "🍔Gourmet Bites", "Book Nook": "🛒Book Nook",
        "Cineplex Theater": "🎬Cineplex Theater", "VR World & Arcade": "🎬Arcade", "Sky Food Court": "🍔Sky Food Court",
        "P1": "🅿️Tempat 1", "P2": "🅿️Tempat 2", "P3": "🅿️Tempat 3", "P4": "🅿️Tempat 4",
        "P5": "🅿️Tempat 5", "P6": "🅿️Tempat 6", "P7": "🅿️Tempat 7", "P8": "🅿️Tempat 8",
    }
}

STORE_CATEGORIES = {
    "Fashion Hub": "Apparel", "Tech Gadgets": "Electronics", "Jewel Box": "Jewelry",
    "Mega Supermarket": "Supermarket", "Gourmet Bites": "Food & Beverage", "Book Nook": "Books",
    "Cineplex Theater": "Cinema", "VR World & Arcade": "Arcade", "Sky Food Court": "Food & Beverage",
    "A_L0_Restroom": "Restroom", "A_L1_Restroom": "Restroom", "B_L2_Restroom": "Restroom",
    "A_L0_Info": "Facility", "A_L0_Elevator": "Facility", "A_L1_Elevator": "Facility",
    "B_L2_Elevator": "Facility", "P_L3_Elevator": "Facility", "A_L0_Escalator": "Facility",
    "A_L1_Escalator": "Facility", "B_L2_Escalator": "Facility"
}

if "lang" not in st.session_state: st.session_state.lang = "English"
if "selected_start" not in st.session_state: st.session_state.selected_start = "A_L0_Entrance"
if "selected_dest" not in st.session_state: st.session_state.selected_dest = "A_L0_Lobby"
if "waypoints" not in st.session_state: st.session_state.waypoints = []
if "map_pick_mode" not in st.session_state: st.session_state.map_pick_mode = False
if "map_pick_step" not in st.session_state: st.session_state.map_pick_step = "START"
if "last_processed_click" not in st.session_state: st.session_state.last_processed_click = None

LOCATION_ICONS = {
    "Fashion": "👗", "Electronics": "📱", "Food & Beverage": "🍔",
    "Supermarket": "🛒", "Elevator": "🛗", "Escalator": "🪜",
    "Stairs": "🧗", "Entrance": "🚪", "Restroom": "🚻", "Parking": "🅿️", "Default": "📍"
}

def get_location_icon(node_id):
    if "Elevator" in node_id: return LOCATION_ICONS["Elevator"]
    elif "Escalator" in node_id: return LOCATION_ICONS["Escalator"]
    elif "Stairs" in node_id: return LOCATION_ICONS["Stairs"]
    elif "Restroom" in node_id or "Toilet" in node_id: return LOCATION_ICONS["Restroom"]
    elif "Entrance" in node_id or "Exit" in node_id: return LOCATION_ICONS["Entrance"]
    elif "P_" in node_id or "Slot" in node_id or "Parking" in node_id: return LOCATION_ICONS["Parking"]
    cat_key = STORE_CATEGORIES.get(node_id)
    if cat_key and cat_key in LOCATION_ICONS: return LOCATION_ICONS[cat_key]
    return LOCATION_ICONS["Default"]

ROOM_POLYGONS = {
    "Mega Supermarket": {"z": 0, "coords": [(-30, 20), (30, 20), (30, 44), (-30, 44)], "color": "#98FB98"},
    "A_L0_Lobby": {"z": 0, "coords": [(-30, -4), (30, -4), (30, 20), (-30, 20)], "color": "#B0C4DE"},
    "Fashion Hub": {"z": 0, "coords": [(-30, -28), (30, -28), (30, -4), (-30, -4)], "color": "#E6E6FA"},
    "A_L0_Info": {"z": 0, "coords": [(-50, 20), (-30, 20), (-30, 44), (-50, 44)], "color": "#ADD8E6"},
    "A_L0_Entrance": {"z": 0, "coords": [(-50, -4), (-30, -4), (-30, 20), (-50, 20)], "color": "#708090"},
    "A_L0_Restroom": {"z": 0, "coords": [(30, 20), (50, 20), (50, 44), (30, 44)], "color": "#E0FFFF"},
    "A_L0_Elevator": {"z": 0, "coords": [(30, 8), (50, 8), (50, 20), (30, 20)], "color": "#FFD700"},
    "A_L0_Escalator": {"z": 0, "coords": [(30, -4), (50, -4), (50, 8), (30, 8)], "color": "#FFA07A"},
    "A_L0_Stairs": {"z": 0, "coords": [(30, -28), (50, -28), (50, -4), (30, -4)], "color": "#FF8C00"},

    "Jewel Box": {"z": 1, "coords": [(-30, 20), (30, 20), (30, 44), (-30, 44)], "color": "#D8BFD8"},
    "A_L1_Hallway": {"z": 1, "coords": [(-30, -4), (30, -4), (30, 20), (-30, 20)], "color": "#87CEFA"},
    "Book Nook": {"z": 1, "coords": [(-30, -28), (0, -28), (0, -4), (-30, -4)], "color": "#F5DEB3"},
    "Tech Gadgets": {"z": 1, "coords": [(0, -28), (30, -28), (30, -4), (0, -4)], "color": "#9370DB"},
    "A_L1_Restroom": {"z": 1, "coords": [(30, 20), (50, 20), (50, 44), (30, 44)], "color": "#E0FFFF"},
    "A_L1_Elevator": {"z": 1, "coords": [(30, 8), (50, 8), (50, 20), (30, 20)], "color": "#FFD700"},
    "A_L1_Escalator": {"z": 1, "coords": [(30, -4), (50, -4), (50, 8), (30, 8)], "color": "#FFA07A"},
    "A_L1_Stairs": {"z": 1, "coords": [(30, -28), (50, -28), (50, -4), (30, -4)], "color": "#FF8C00"},

    "Cineplex Theater": {"z": 2, "coords": [(-30, 20), (30, 20), (30, 44), (-30, 44)], "color": "#CD5C5C"},
    "VR World & Arcade": {"z": 2, "coords": [(-50, -4), (-30, -4), (-30, 20), (-50, 20)], "color": "#FF69B4"},
    "B_L2_Corridor": {"z": 2, "coords": [(-30, -4), (30, -4), (30, 20), (-30, 20)], "color": "#5F9EA0"},
    "Sky Food Court": {"z": 2, "coords": [(-30, -28), (0, -28), (0, -4), (-30, -4)], "color": "#FF7F50"},
    "Gourmet Bites": {"z": 2, "coords": [(0, -28), (30, -28), (30, -4), (0, -4)], "color": "#F4A460"},
    "B_L2_Restroom": {"z": 2, "coords": [(30, 20), (50, 20), (50, 44), (30, 44)], "color": "#E0FFFF"},
    "B_L2_Elevator": {"z": 2, "coords": [(30, 8), (50, 8), (50, 20), (30, 20)], "color": "#FFD700"},
    "B_L2_Escalator": {"z": 2, "coords": [(30, -4), (50, -4), (50, 8), (30, 8)], "color": "#FFA07A"},
    "B_L2_Stairs": {"z": 2, "coords": [(30, -28), (50, -28), (50, -4), (30, -4)], "color": "#FF8C00"},

    "P_L3_Aisle_Main": {"z": 3, "coords": [(-30, -4), (30, -4), (30, 20), (-30, 20)], "color": "#A9A9A9"},
    "P_L3_Driveway_Entrance": {"z": 3, "coords": [(-50, -4), (-30, -4), (-30, 8), (-50, 8)], "color": "#A9A9A9"},
    "P_L3_Driveway_Exit": {"z": 3, "coords": [(-50, 8), (-30, 8), (-30, 20), (-50, 20)], "color": "#708090"},
    "P1": {"z": 3, "coords": [(-30, -28), (-15, -28), (-15, -4), (-30, -4)], "color": "#4682B4"},
    "P2": {"z": 3, "coords": [(-15, -28), (0, -28), (0, -4), (-15, -4)], "color": "#4682B4"},
    "P3": {"z": 3, "coords": [(0, -28), (15, -28), (15, -4), (0, -4)], "color": "#4682B4"},
    "P4": {"z": 3, "coords": [(15, -28), (30, -28), (30, -4), (15, -4)], "color": "#4682B4"},
    "P5": {"z": 3, "coords": [(-30, 20), (-15, 20), (-15, 44), (-30, 44)], "color": "#4682B4"},
    "P6": {"z": 3, "coords": [(-15, 20), (0, 20), (0, 44), (-15, 44)], "color": "#4682B4"},
    "P7": {"z": 3, "coords": [(0, 20), (15, 20), (15, 44), (0, 44)], "color": "#4682B4"},
    "P8": {"z": 3, "coords": [(15, 20), (30, 20), (30, 44), (15, 44)], "color": "#4682B4"},
    "P_L3_Elevator": {"z": 3, "coords": [(30, 8), (50, 8), (50, 20), (30, 20)], "color": "#FFD700"},
    "P_L3_Escalator": {"z": 3, "coords": [(30, -4), (50, -4), (50, 8), (30, 8)], "color": "#FFA07A"},
    "P_L3_Stairs": {"z": 3, "coords": [(30, -28), (50, -28), (50, -4), (30, -4)], "color": "#FF8C00"}
}

MULTI_CAD_NODES = {
    # --- Ground Floor (Z=0) ---
    "A_L0_Entrance": (-40.0, 8.0, 0),
    "A_L0_Info": (-40.0, 32.0, 0),
    "A_L0_Lobby": (0.0, 8.0, 0),
    "Fashion Hub": (0.0, -16.0, 0),
    "Mega Supermarket": (0.0, 32.0, 0),
    "A_L0_Restroom": (40.0, 32.0, 0),
    "A_L0_Elevator": (40.0, 14.0, 0),
    "A_L0_Escalator": (40.0, 2.0, 0),
    "A_L0_Stairs": (40.0, -16.0, 0),
    # Ground Floor Corridor Grid Nodes
    "H_L0_West": (-20.0, 8.0, 0),
    "H_L0_East": (20.0, 8.0, 0),
    "H_L0_North": (0.0, 20.0, 0),
    "H_L0_South": (0.0, -4.0, 0),

    # --- 1st Floor (Z=1) ---
    "A_L1_Hallway": (0.0, 8.0, 1),
    "Book Nook": (-15.0, -16.0, 1),
    "Tech Gadgets": (15.0, -16.0, 1),
    "Jewel Box": (0.0, 32.0, 1),
    "A_L1_Restroom": (40.0, 32.0, 1),
    "A_L1_Elevator": (40.0, 14.0, 1),
    "A_L1_Escalator": (40.0, 2.0, 1),
    "A_L1_Stairs": (40.0, -16.0, 1),
    # 1st Floor Corridor Grid Nodes
    "H_L1_West": (-20.0, 8.0, 1),
    "H_L1_East": (20.0, 8.0, 1),
    "H_L1_South_West": (-15.0, -4.0, 1),
    "H_L1_South_East": (15.0, -4.0, 1),

    # --- 2nd Floor (Z=2) ---
    "B_L2_Corridor": (0.0, 8.0, 2),
    "VR World & Arcade": (-40.0, 8.0, 2),
    "Cineplex Theater": (0.0, 32.0, 2),
    "Sky Food Court": (-15.0, -16.0, 2),
    "Gourmet Bites": (15.0, -16.0, 2),
    "B_L2_Restroom": (40.0, 32.0, 2),
    "B_L2_Elevator": (40.0, 14.0, 2),
    "B_L2_Escalator": (40.0, 2.0, 2),
    "B_L2_Stairs": (40.0, -16.0, 2),
    # 2nd Floor Corridor Grid Nodes
    "H_L2_West": (-20.0, 8.0, 2),
    "H_L2_East": (20.0, 8.0, 2),
    "H_L2_South_West": (-15.0, -4.0, 2),
    "H_L2_South_East": (15.0, -4.0, 2),

    # --- Rooftop Parking (Z=3) ---
    "P_L3_Aisle_Main": (0.0, 8.0, 3),
    "P_L3_Driveway_Entrance": (-40.0, 2.0, 3),
    "P_L3_Driveway_Exit": (-40.0, 14.0, 3),
    "P1": (-22.5, -16.0, 3), "P2": (-7.5, -16.0, 3), "P3": (7.5, -16.0, 3), "P4": (22.5, -16.0, 3),
    "P5": (-22.5, 32.0, 3), "P6": (-7.5, 32.0, 3), "P7": (7.5, 32.0, 3), "P8": (22.5, 32.0, 3),
    "P_L3_Elevator": (40.0, 14.0, 3),
    "P_L3_Escalator": (40.0, 2.0, 3),
    "P_L3_Stairs": (40.0, -16.0, 3)
}

MULTI_CAD_GRAPH = {
    # --- Ground Floor Connections ---
    "A_L0_Entrance": {"H_L0_West": 20.0, "Fashion Hub": 27.5},
    "A_L0_Info": {"H_L0_West": 28.0, "A_L0_Entrance": 24.0},
    "H_L0_West": {"A_L0_Entrance": 20.0, "A_L0_Info": 28.0, "A_L0_Lobby": 20.0, "H_L0_North": 23.3, "H_L0_South": 23.3},
    "A_L0_Lobby": {"H_L0_West": 20.0, "H_L0_East": 20.0, "H_L0_North": 12.0, "H_L0_South": 12.0},
    "H_L0_North": {"A_L0_Lobby": 12.0, "Mega Supermarket": 12.0, "H_L0_West": 23.3, "H_L0_East": 23.3},
    "H_L0_South": {"A_L0_Lobby": 12.0, "Fashion Hub": 12.0, "H_L0_West": 23.3, "H_L0_East": 23.3},
    "Fashion Hub": {"H_L0_South": 12.0, "A_L0_Entrance": 27.5},
    "Mega Supermarket": {"H_L0_North": 12.0},
    "H_L0_East": {"A_L0_Lobby": 20.0, "A_L0_Restroom": 28.0, "A_L0_Elevator": 20.8, "A_L0_Escalator": 20.8, "A_L0_Stairs": 31.2},
    "A_L0_Restroom": {"H_L0_East": 28.0},
    "A_L0_Elevator": {"H_L0_East": 20.8, "A_L1_Elevator": 15.0},
    "A_L0_Escalator": {"H_L0_East": 20.8, "A_L1_Escalator": 12.0},
    "A_L0_Stairs": {"H_L0_East": 31.2, "A_L1_Stairs": 15.0},

    # --- 1st Floor Connections ---
    "A_L1_Hallway": {"H_L1_West": 20.0, "H_L1_East": 20.0, "Jewel Box": 24.0, "H_L1_South_West": 18.0, "H_L1_South_East": 18.0},
    "H_L1_West": {"A_L1_Hallway": 20.0, "H_L1_South_West": 13.0},
    "H_L1_East": {"A_L1_Hallway": 20.0, "A_L1_Restroom": 28.0, "A_L1_Elevator": 20.8, "A_L1_Escalator": 20.8, "A_L1_Stairs": 31.2},
    "Jewel Box": {"A_L1_Hallway": 24.0},
    "H_L1_South_West": {"H_L1_West": 13.0, "A_L1_Hallway": 18.0, "Book Nook": 12.0},
    "H_L1_South_East": {"H_L1_East": 13.0, "A_L1_Hallway": 18.0, "Tech Gadgets": 12.0},
    "Book Nook": {"H_L1_South_West": 12.0},
    "Tech Gadgets": {"H_L1_South_East": 12.0},
    "A_L1_Restroom": {"H_L1_East": 28.0},
    "A_L1_Elevator": {"H_L1_East": 20.8, "A_L0_Elevator": 15.0, "B_L2_Elevator": 15.0},
    "A_L1_Escalator": {"H_L1_East": 20.8, "A_L0_Escalator": 12.0, "B_L2_Escalator": 12.0},
    "A_L1_Stairs": {"H_L1_East": 31.2, "A_L0_Stairs": 15.0, "B_L2_Stairs": 15.0},

    # --- 2nd Floor Connections ---
    "B_L2_Corridor": {"H_L2_West": 20.0, "H_L2_East": 20.0, "Cineplex Theater": 24.0, "H_L2_South_West": 18.0, "H_L2_South_East": 18.0},
    "H_L2_West": {"B_L2_Corridor": 20.0, "VR World & Arcade": 20.0, "H_L2_South_West": 13.0},
    "VR World & Arcade": {"H_L2_West": 20.0},
    "Cineplex Theater": {"B_L2_Corridor": 24.0},
    "H_L2_South_West": {"H_L2_West": 13.0, "B_L2_Corridor": 18.0, "Sky Food Court": 12.0},
    "H_L2_South_East": {"H_L2_East": 13.0, "B_L2_Corridor": 18.0, "Gourmet Bites": 12.0},
    "Sky Food Court": {"H_L2_South_West": 12.0},
    "Gourmet Bites": {"H_L2_South_East": 12.0},
    "H_L2_East": {"B_L2_Corridor": 20.0, "B_L2_Restroom": 28.0, "B_L2_Elevator": 20.8, "B_L2_Escalator": 20.8, "B_L2_Stairs": 31.2},
    "B_L2_Restroom": {"H_L2_East": 28.0},
    "B_L2_Elevator": {"H_L2_East": 20.8, "A_L1_Elevator": 15.0, "P_L3_Elevator": 15.0},
    "B_L2_Escalator": {"H_L2_East": 20.8, "A_L1_Escalator": 12.0, "P_L3_Escalator": 12.0},
    "B_L2_Stairs": {"H_L2_East": 31.2, "A_L1_Stairs": 15.0, "P_L3_Stairs": 15.0},

    # --- Rooftop Parking Connections ---
    "P1": {"P_L3_Aisle_Main": 20.0}, "P2": {"P_L3_Aisle_Main": 20.0}, "P3": {"P_L3_Aisle_Main": 20.0}, "P4": {"P_L3_Aisle_Main": 20.0},
    "P5": {"P_L3_Aisle_Main": 20.0}, "P6": {"P_L3_Aisle_Main": 20.0}, "P7": {"P_L3_Aisle_Main": 20.0}, "P8": {"P_L3_Aisle_Main": 20.0},
    "P_L3_Aisle_Main": {
        "P1": 20.0, "P2": 20.0, "P3": 20.0, "P4": 20.0, "P5": 20.0, "P6": 20.0, "P7": 20.0, "P8": 20.0,
        "P_L3_Elevator": 40.0, "P_L3_Stairs": 40.0, "P_L3_Escalator": 35.0, "P_L3_Driveway_Entrance": 25.0, "P_L3_Driveway_Exit": 25.0,
    },
    "P_L3_Driveway_Entrance": {"P_L3_Aisle_Main": 25.0}, "P_L3_Driveway_Exit": {"P_L3_Aisle_Main": 25.0},
    "P_L3_Elevator": {"P_L3_Aisle_Main": 40.0, "B_L2_Elevator": 15.0},
    "P_L3_Stairs": {"P_L3_Aisle_Main": 40.0, "B_L2_Stairs": 15.0},
    "P_L3_Escalator": {"P_L3_Aisle_Main": 35.0, "B_L2_Escalator": 12.0},
}

PARKING_SLOTS = {
    "P1": {"occupied": False}, "P2": {"occupied": True}, "P3": {"occupied": False}, "P4": {"occupied": False},
    "P5": {"occupied": True},  "P6": {"occupied": False}, "P7": {"occupied": False}, "P8": {"occupied": True},
}

# ==============================================================================
# 2. Dynamic Line of Sight & Routing Logic
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
    if z1 != z2: return False
    p1, p2 = (x1, y1), (x2, y2)
    floor_z = int(z1)

    if floor_z in wall_segments:
        for w1, w2 in wall_segments[floor_z]:
            if p1 == w1 or p1 == w2 or p2 == w1 or p2 == w2: continue
            if line_segments_intersect(p1, p2, w1, w2): return False
    return True

def resolve_click_to_dynamic_node(click_x, click_y, floor_z, graph, node_coords):
    """
    Creates a dynamic virtual node at exact clicked coordinates and connects it 
    directly to all visible hallway nodes or adjacent dynamic points on the floor.
    """
    temp_node_id = f"Dynamic_Point_({click_x:.2f}_{click_y:.2f}_Z{floor_z})"
    node_coords[temp_node_id] = (click_x, click_y, floor_z)
    graph[temp_node_id] = {}

    for node_id, coords in list(node_coords.items()):
        if node_id == temp_node_id: continue
        nx, ny, nz = coords
        if int(nz) == int(floor_z):
            # Connect only to hallway grid nodes (H_L*) or other dynamic points
            if node_id.startswith("H_L") or node_id.startswith("Dynamic_Point") or "Aisle" in node_id:
                if has_line_of_sight_3d(temp_node_id, node_id, node_coords, WALL_SEGMENTS_BY_FLOOR):
                    dist = math.hypot(click_x - nx, click_y - ny)
                    graph[temp_node_id][node_id] = dist
                    if node_id not in graph: graph[node_id] = {}
                    graph[node_id][temp_node_id] = dist
                
    return temp_node_id

def resolve_all_route_points(route_sequence, floor_z, graph_copy, nodes_copy):
    resolved_sequence = []
    
    for pt in route_sequence:
        if isinstance(pt, tuple) and len(pt) == 3:
            px, py, pz = pt
            node_id = resolve_click_to_dynamic_node(px, py, pz, graph_copy, nodes_copy)
            resolved_sequence.append(node_id)
        else:
            resolved_sequence.append(pt)

    for i in range(len(resolved_sequence) - 1):
        node_a = resolved_sequence[i]
        node_b = resolved_sequence[i + 1]
        
        if node_a in nodes_copy and node_b in nodes_copy:
            za = nodes_copy[node_a][2]
            zb = nodes_copy[node_b][2]
            if za == zb and has_line_of_sight_3d(node_a, node_b, nodes_copy, WALL_SEGMENTS_BY_FLOOR):
                ax, ay, _ = nodes_copy[node_a]
                bx, by, _ = nodes_copy[node_b]
                dist = math.hypot(ax - bx, ay - by)
                graph_copy[node_a][node_b] = dist
                if node_b not in graph_copy: graph_copy[node_b] = {}
                graph_copy[node_b][node_a] = dist

    return resolved_sequence

# ==============================================================================
# 3. Pathfinding Engine (Theta*)
# ==============================================================================

def euclidean_distance_3d(node_a, node_b, node_coords):
    x1, y1, z1 = node_coords[node_a]
    x2, y2, z2 = node_coords[node_b]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2 + ((z1 - z2) * 15.0)**2)

def theta_star_3d(start, goal, graph, node_coords, accessible_only=False):
    if start not in node_coords or goal not in node_coords: return None
    open_set = []
    heapq.heappush(open_set, (0, start))
    parent = {start: start}
    g_score = {node: float('inf') for node in node_coords}
    g_score[start] = 0.0
    f_score = {node: float('inf') for node in node_coords}
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

        for neighbor, weight in graph.get(current, {}).items():
            if neighbor not in node_coords: continue
            if accessible_only and ("Stairs" in neighbor or "Escalator" in neighbor): continue

            p_curr = parent[current]
            same_floor = (node_coords[p_curr][2] == node_coords[neighbor][2])
            
            if same_floor and has_line_of_sight_3d(p_curr, neighbor, node_coords, WALL_SEGMENTS_BY_FLOOR):
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
# 4. Folium Map Rendering Engine
# ==============================================================================

def render_2d_folium_view(active_floor_z, route_path=None, node_coords_dict=MULTI_CAD_NODES, current_lang="English"):
    floor_rooms = {
        r_id: poly["coords"]
        for r_id, poly in ROOM_POLYGONS.items()
        if poly["z"] == active_floor_z
    }

    all_pts = [pt for coords in floor_rooms.values() for pt in coords]
    if all_pts:
        min_x = min(p[0] for p in all_pts) - 10
        max_x = max(p[0] for p in all_pts) + 10
        min_y = min(p[1] for p in all_pts) - 10
        max_y = max(p[1] for p in all_pts) + 10
    else:
        min_x, max_x, min_y, max_y = -60, 60, -35, 55

    bounds = [[min_y, min_x], [max_y, max_x]]

    m = folium.Map(crs="Simple", tiles=None, zoom_control=True, scroll_wheel_zoom=True)
    Fullscreen(position="topleft", title="Expand map", title_cancel="Exit fullscreen", force_separate_button=True).add_to(m)

    for room_id, coords in floor_rooms.items():
        room_info = ROOM_POLYGONS[room_id]
        translated_name = POI_TRANSLATIONS.get(current_lang, {}).get(room_id, room_id)
        folium_coords = [[pt[1], pt[0]] for pt in coords]

        folium.Polygon(
            locations=folium_coords,
            color="#334155",
            weight=2,
            fill=True,
            fill_color=room_info.get("color", "#CBD5E1"),
            fill_opacity=0.7,
            tooltip=translated_name
        ).add_to(m)

        cx = sum(p[0] for p in coords) / len(coords)
        cy = sum(p[1] for p in coords) / len(coords)
        icon_str = get_location_icon(room_id)

        folium.Marker(
            location=[cy, cx],
            icon=folium.DivIcon(
                html=f'''<div style="font-size: 10px; font-weight: bold; color: #0f172a; text-align: center; white-space: nowrap; transform: translate(-50%, -50%);">
                    {icon_str}<br>{translated_name}
                </div>'''
            )
        ).add_to(m)

    if route_path:
        floor_path = [node for node in route_path if node in node_coords_dict and node_coords_dict[node][2] == active_floor_z]

        if len(floor_path) > 1:
            line_pts = [[node_coords_dict[node][1], node_coords_dict[node][0]] for node in floor_path]
            folium.PolyLine(locations=line_pts, color="#EF4444", weight=5, opacity=0.9).add_to(m)

        start_node_id = route_path[0]
        dest_node_id = route_path[-1]

        if start_node_id in node_coords_dict and node_coords_dict[start_node_id][2] == active_floor_z:
            sx, sy, _ = node_coords_dict[start_node_id]
            folium.Marker(location=[sy, sx], popup="Start Point", icon=folium.Icon(color="red", icon="play")).add_to(m)

        if dest_node_id in node_coords_dict and node_coords_dict[dest_node_id][2] == active_floor_z:
            dx, dy, _ = node_coords_dict[dest_node_id]
            folium.Marker(location=[dy, dx], popup="Destination Point", icon=folium.Icon(color="green", icon="flag")).add_to(m)

    m.fit_bounds(bounds)
    return m

def render_rooftop_folium_map(assigned_slot=None, route_path=None, current_lang="English"):
    rooftop_rooms = {r_id: poly["coords"] for r_id, poly in ROOM_POLYGONS.items() if poly["z"] == 3}
    all_pts = [pt for coords in rooftop_rooms.values() for pt in coords]
    min_x, max_x = min(p[0] for p in all_pts) - 10, max(p[0] for p in all_pts) + 10
    min_y, max_y = min(p[1] for p in all_pts) - 10, max(p[1] for p in all_pts) + 10

    m = folium.Map(crs="Simple", tiles=None)

    for room_id, coords in rooftop_rooms.items():
        folium_coords = [[pt[1], pt[0]] for pt in coords]
        folium.Polygon(locations=folium_coords, color="#475569", weight=1.5, fill=True, fill_color="#E2E8F0", fill_opacity=0.5).add_to(m)

    for slot_id, details in PARKING_SLOTS.items():
        if slot_id not in MULTI_CAD_NODES: continue
        cx, cy, _ = MULTI_CAD_NODES[slot_id]
        color = "#2563EB" if slot_id == assigned_slot else ("#DC2626" if details["occupied"] else "#16A34A")

        box_w, box_h = 3.5, 6.0
        bx = [cx - box_w/2, cx + box_w/2, cx + box_w/2, cx - box_w/2]
        by = [cy - box_h/2, cy - box_h/2, cy + box_h/2, cy + box_h/2]
        slot_poly = [[by[i], bx[i]] for i in range(4)]

        folium.Polygon(locations=slot_poly, color=color, fill=True, fill_color=color, fill_opacity=0.7).add_to(m)
        folium.Marker(location=[cy, cx], icon=folium.DivIcon(html=f'<div style="font-size: 10px; font-weight: bold; color: #FFFFFF; transform: translate(-50%, -50%);">{slot_id}</div>')).add_to(m)

    if route_path:
        rooftop_path = [node for node in route_path if int(MULTI_CAD_NODES[node][2]) == 3]
        if len(rooftop_path) > 1:
            line_pts = [[MULTI_CAD_NODES[n][1], MULTI_CAD_NODES[n][0]] for n in rooftop_path]
            folium.PolyLine(locations=line_pts, color="#2563EB", weight=4).add_to(m)

    m.fit_bounds([[min_y, min_x], [max_y, max_x]])
    return m

# ==============================================================================
# 5. Helpers & Navigation Directions
# ==============================================================================

def find_nearest_available_parking(entrance_node, graph, nodes, availability_map, accessible_only=False):
    available_spots = [spot for spot, is_occupied in availability_map.items() if not is_occupied]
    if not available_spots: return None, [], []

    best_spot, shortest_distance, best_entry_path = None, float("inf"), []
    for spot in available_spots:
        path = theta_star_3d(entrance_node, spot, graph, nodes, accessible_only=accessible_only)
        if path and len(path) < shortest_distance:
            shortest_distance = len(path)
            best_spot = spot
            best_entry_path = path

    best_exit_path = theta_star_3d(best_spot, "P_L3_Driveway_Exit", graph, nodes, accessible_only=accessible_only) if best_spot else []
    return best_spot, best_entry_path, best_exit_path

def format_location_label(loc, lang):
    if isinstance(loc, tuple): return f"Point ({loc[0]:.1f}, {loc[1]:.1f})"
    z_val = int(MULTI_CAD_NODES[loc][2])
    floor_code = "R" if z_val == 3 else (f"{z_val}F" if z_val > 0 else "GF")
    name = POI_TRANSLATIONS.get(lang, {}).get(loc, loc).split('(')[0].strip()
    return f"[{floor_code}] {name}"

# ==============================================================================
# 6. UI Navigation Tabs
# ==============================================================================

t = LOCALIZATION[st.session_state.lang]

home_tab_title = {"English": "🏠 Home", "Simplified Chinese": "🏠 首页", "Malay": "🏠 Utama"}.get(st.session_state.lang, "🏠 Home")
tab_home, tab_map, tab_dir, tab_park = st.tabs([home_tab_title, t["tab_nav"], t["tab_directions"], t["tab_parking"]])

with st.sidebar:
    st.header(t["config_header"])
    selected_language_key = st.selectbox(
        t["select_lang"],
        options=list(LOCALIZATION.keys()),
        format_func=lambda key: LANG_OPTION_LABELS[st.session_state.lang][key],
        index=list(LOCALIZATION.keys()).index(st.session_state.lang),
    )
    if selected_language_key != st.session_state.lang:
        st.session_state.lang = selected_language_key
        st.rerun()

# Home Tab
with tab_home:
    st.title(t["title"])
    st.caption(t["subtitle"])
    st.divider()
    st.markdown(f"### {t['home_title']}\n{t['home_desc']}")
    st.divider()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t["poi_metric"], len(ROOM_POLYGONS))
    c2.metric(t["floors_metric"], len(FLOOR_TRANSLATIONS["English"]))
    c3.metric(t["spots_metric"], len(PARKING_SLOTS))
    c4.metric(t["available_metric"], sum(1 for s in PARKING_SLOTS.values() if not s["occupied"]))

# Mall Map Tab
with tab_map:
    floor_select = st.selectbox(
        t["active_floor"],
        options=[0, 1, 2, 3],
        format_func=lambda x: get_translated_floor_name(x, lang=st.session_state.lang)
    )

    with st.expander(f"⚙️ {t['nav_controls']}", expanded=True):
        room_options = list(ROOM_POLYGONS.keys())
        col_start, col_dest = st.columns(2)

        with col_start:
            start_node = st.selectbox(
                t["start_loc"],
                options=room_options,
                format_func=lambda r: format_location_label(r, st.session_state.lang),
                index=room_options.index(st.session_state.selected_start) if isinstance(st.session_state.selected_start, str) and st.session_state.selected_start in room_options else 0,
            )
        with col_dest:
            dest_node = st.selectbox(
                t["dest_loc"],
                options=room_options,
                format_func=lambda r: format_location_label(r, st.session_state.lang),
                index=room_options.index(st.session_state.selected_dest) if isinstance(st.session_state.selected_dest, str) and st.session_state.selected_dest in room_options else len(room_options)-1,
            )

        # Only sync selectboxes if NOT in map click mode
        if not st.session_state.map_pick_mode:
            if isinstance(st.session_state.selected_start, str): st.session_state.selected_start = start_node
            if isinstance(st.session_state.selected_dest, str): st.session_state.selected_dest = dest_node

        route_pref = st.radio(t["route_type"], options=[t["shortest"], t["accessible"]], horizontal=True)
        accessible_flag = (route_pref == t["accessible"])

        col_add_stop, col_pick_mode, col_reset = st.columns(3)
        with col_add_stop:
            if st.button(t["btn_add_stop_manual"]):
                st.session_state.waypoints.append(room_options[0])
                st.rerun()

        with col_pick_mode:
            if not st.session_state.map_pick_mode:
                if st.button(t["btn_interactive_pick"], type="primary"):
                    st.session_state.map_pick_mode = True
                    st.session_state.map_pick_step = "START"
                    st.rerun()
            else:
                if st.button(t["btn_cancel_interactive"]):
                    st.session_state.map_pick_mode = False
                    st.rerun()

        with col_reset:
            if st.button(t["btn_reset_all"]):
                st.session_state.selected_start = "A_L0_Entrance"
                st.session_state.selected_dest = "A_L0_Lobby"
                st.session_state.waypoints = []
                st.session_state.map_pick_mode = False
                st.rerun()

    if st.session_state.map_pick_mode:
        if st.session_state.map_pick_step == "START":
            st.info(t["pick_step_1"])
        elif st.session_state.map_pick_step == "STOPS":
            st.info(t["pick_step_2"])
            if st.button(t["btn_done_adding_stops"], type="primary"):
                st.session_state.map_pick_step = "DEST"
                st.rerun()
        elif st.session_state.map_pick_step == "DEST":
            st.info(t["pick_step_3"])

    # 3. Dynamic Point Injection & Path Accumulation
    temp_graph = copy.deepcopy(MULTI_CAD_GRAPH)
    temp_nodes = copy.deepcopy(MULTI_CAD_NODES)

    raw_sequence = [st.session_state.selected_start] + st.session_state.waypoints + [st.session_state.selected_dest]
    full_route_sequence = resolve_all_route_points(raw_sequence, floor_select, temp_graph, temp_nodes)

    full_path = []
    route_failed = False

    for i in range(len(full_route_sequence) - 1):
        seg_start = full_route_sequence[i]
        seg_end = full_route_sequence[i + 1]

        if seg_start == seg_end:
            continue

        segment_path = theta_star_3d(seg_start, seg_end, temp_graph, temp_nodes, accessible_only=accessible_flag)
        if segment_path:
            if not full_path:
                full_path.extend(segment_path)
            else:
                full_path.extend(segment_path[1:])
        else:
            route_failed = True
            break

    path = [] if route_failed else full_path

    # 4. Render Map Canvas & Process Clicks
    folium_map = render_2d_folium_view(floor_select, route_path=path, node_coords_dict=temp_nodes, current_lang=st.session_state.lang)
    map_data = st_folium(folium_map, height=550, width=1000, key="interactive_folium_map", returned_objects=["last_clicked"])

    if map_data and map_data.get("last_clicked"):
        click_y = map_data["last_clicked"]["lat"] # Folium Lat = Y
        click_x = map_data["last_clicked"]["lng"] # Folium Lng = X
        click_sig = (click_x, click_y, floor_select)

        if click_sig != st.session_state.last_processed_click:
            st.session_state.last_processed_click = click_sig

            if st.session_state.map_pick_mode:
                if st.session_state.map_pick_step == "START":
                    st.session_state.selected_start = click_sig
                    st.session_state.waypoints = []
                    st.session_state.map_pick_step = "STOPS"
                    st.rerun()
                elif st.session_state.map_pick_step == "STOPS":
                    st.session_state.waypoints.append(click_sig)
                    st.rerun()
                elif st.session_state.map_pick_step == "DEST":
                    st.session_state.selected_dest = click_sig
                    st.session_state.map_pick_mode = False
                    st.rerun()

# Directions Tab
with tab_dir:
    st.subheader(t["route_summary"])
    if path:
        st.success(f"Route calculated with {len(path)} path nodes.")
    else:
        st.warning(t["no_route"])

# Smart Parking Tab
with tab_park:
    st.subheader(t["parking_sec"])
    assigned_slot, entry_path, exit_path = find_nearest_available_parking(
        "P_L3_Driveway_Entrance", MULTI_CAD_GRAPH, MULTI_CAD_NODES, availability_map={spot: True for spot in PARKING_SLOTS}
    )
    if assigned_slot:
        park_map = render_rooftop_folium_map(assigned_slot=assigned_slot, route_path=entry_path, current_lang=st.session_state.lang)
        st_folium(park_map, height=450, width=900)
