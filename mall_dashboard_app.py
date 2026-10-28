import math
import heapq
import random
import streamlit as st
import folium
from streamlit_folium import st_folium

# ==============================================================================
# 1. Translation Table & Localization
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
        "feat_map_title": "🗺️ Folium Map View",
        "feat_map_desc": "Navigate our shopping mall easily with interactive Folium maps supporting click-anywhere pin drops.",
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
        "selected_on_map": "📍 Selected on map: **{location}**",
        "btn_set_start": "🚩 Set as Start",
        "btn_set_dest": "🏁 Set as Destination",
        "btn_cancel": "❌ Cancel",
        "marker_start": " Start",
        "marker_dest": " Destination",
        "intermediate_stops": "📍 Intermediate Stops",
        "stop_lbl": "Stop {idx}",
        "btn_add_stop_manual": "➕ Add Intermediate Stop Manually",
        "btn_reset_all": "🗑️ Reset All",
        "tab_nav_drive_to_spot": "🚗 1. Entrance to Parking Spot",
        "tab_nav_spot_to_exit": "🚪 2. Parking Spot to Exit",
        "header_driving_to_spot": "🚗 Driving to Parking Spot",
        "header_leaving_spot": "🚪 Leaving Parking Spot to Driveway Exit",
        "lbl_entrance_ramp": "🚗 Entrance Ramp",
        "lbl_exit_ramp": "🚗 Exit Ramp",
        "lbl_stairwell": "🪜 Stairwell",
        "lbl_elevator": "🛗 Elevator",
        "lbl_escalator": "🪜 Escalator",
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
        "feat_map_title": "🗺️ Folium 地图视图",
        "feat_map_desc": "基于 Folium 的矢量地图，支持在地图任意位置精准点击选取节点。",
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
        "selected_on_map": "📍 在地图选择：**{location}**",
        "btn_set_start": "🚩 设为起点",
        "btn_set_dest": "🏁 设为终点",
        "btn_cancel": "❌ 取消",
        "marker_start": " 起点",
        "marker_dest": " 终点",
        "intermediate_stops": "📍 途经点 (中转站)",
        "stop_lbl": "途经点 {idx}",
        "btn_add_stop_manual": "➕ 手动添加途经点",
        "btn_reset_all": "🗑️ 重置全部",
        "tab_nav_drive_to_spot": "🚗 1. 入口至停车位",
        "tab_nav_spot_to_exit": "🚪 2. 停车位至出口",
        "header_driving_to_spot": "🚗 驶向停车位",
        "header_leaving_spot": "🚪 离开停车位驶向出口匝道",
        "lbl_entrance_ramp": "🚗 进口匝道",
        "lbl_exit_ramp": "🚗 出口匝道",
        "lbl_stairwell": "🪜 楼梯间",
        "lbl_elevator": "🛗 电梯",
        "lbl_escalator": "🪜 自动扶梯",
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
        "feat_map_title": "🗺️ Pandangan Peta Folium",
        "feat_map_desc": "Pelan tingkat vektor interaktif berasaskan Folium dengan keupayaan klik di mana-mana tempat.",
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
        "selected_on_map": "📍 Dipilih pada peta: **{location}**",
        "btn_set_start": "🚩 Tetapkan sebagai Permulaan",
        "btn_set_dest": "🏁 Tetapkan sebagai Destinasi",
        "btn_cancel": "❌ Batal",
        "marker_start": " Permulaan",
        "marker_dest": " Destinasi",
        "intermediate_stops": "📍 Hentian Antara",
        "stop_lbl": "Hentian {idx}",
        "btn_add_stop_manual": "➕ Tambah Hentian Antara Secara Manual",
        "btn_reset_all": "🗑️ Set Semula Semua",
        "tab_nav_drive_to_spot": "🚗 1. Pintu Masuk ke Petak Meletak Kenderaan",
        "tab_nav_spot_to_exit": "🚪 2. Petak Meletak Kenderaan ke Pintu Keluar",
        "header_driving_to_spot": "🚗 Memandu ke Petak Meletak Kenderaan",
        "header_leaving_spot": "🚪 Meninggalkan Petak Meletak Kenderaan ke Pintu Keluar",
        "lbl_entrance_ramp": "🚗 Ramp Masuk",
        "lbl_exit_ramp": "🚗 Ramp Keluar",
        "lbl_stairwell": "🪜 Tangga",
        "lbl_elevator": "🛗 Lif",
        "lbl_escalator": "🪜 Eskalator",
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

CATEGORY_TRANSLATIONS = {
    "English": {"Apparel": "Apparel", "Electronics": "Electronics", "Jewelry": "Jewelry", "Supermarket": "Supermarket", "Food & Beverage": "Food & Beverage", "Books": "Books", "Cinema": "Cinema", "Arcade": "Arcade", "Restroom": "Restroom", "Facility": "Facility"},
    "Simplified Chinese": {"Apparel": "服装饰品", "Electronics": "电子数码", "Jewelry": "珠宝首饰", "Supermarket": "超级市场", "Food & Beverage": "餐饮美食", "Books": "图书文具", "Cinema": "电影院", "Arcade": "娱乐电玩", "Restroom": "洗手间", "Facility": "公共设施"},
    "Malay": {"Apparel": "Pakaian", "Electronics": "Barangan Elektronik", "Jewelry": "Barang Kemas", "Supermarket": "Pasar Raya", "Food & Beverage": "Makanan & Minuman", "Books": "Buku", "Cinema": "Pawagam", "Arcade": "Pusat Rekreasi", "Restroom": "Tandas", "Facility": "Kemudahan"}
}

if "lang" not in st.session_state: st.session_state.lang = "English"
if "selected_start" not in st.session_state: st.session_state.selected_start = "A_L0_Entrance"
if "selected_dest" not in st.session_state: st.session_state.selected_dest = "A_L0_Lobby"
if "assigned_parking" not in st.session_state: st.session_state.assigned_parking = None
if "entry_path" not in st.session_state: st.session_state.entry_path = []
if "exit_path" not in st.session_state: st.session_state.exit_path = []

LOCATION_ICONS = {
    "Fashion": "👗", "Footwear": "👟", "Electronics": "📱", "Food & Beverage": "🍔",
    "Supermarket": "🛒", "Department Store": "🏬", "Pharmacy & Health": "💊",
    "Entertainment": "🎬", "Services": "🛠️", "Elevator": "🛗", "Escalator": "🪜",
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
    "Mega Supermarket": (0.0, 32.0, 0), "A_L0_Lobby": (0.0, 8.0, 0), "Fashion Hub": (0.0, -16.0, 0),
    "A_L0_Info": (-40.0, 32.0, 0), "A_L0_Entrance": (-40.0, 8.0, 0), "A_L0_Restroom": (40.0, 32.0, 0),
    "A_L0_Elevator": (40.0, 14.0, 0), "A_L0_Escalator": (40.0, 2.0, 0), "A_L0_Stairs": (40.0, -16.0, 0),
    "Jewel Box": (0.0, 32.0, 1), "A_L1_Hallway": (0.0, 8.0, 1), "Book Nook": (-15.0, -16.0, 1),
    "Tech Gadgets": (15.0, -16.0, 1), "A_L1_Restroom": (40.0, 32.0, 1), "A_L1_Elevator": (40.0, 14.0, 1),
    "A_L1_Escalator": (40.0, 2.0, 1), "A_L1_Stairs": (40.0, -16.0, 1),
    "Cineplex Theater": (0.0, 32.0, 2), "VR World & Arcade": (-40.0, 8.0, 2), "B_L2_Corridor": (0.0, 8.0, 2),
    "Sky Food Court": (-15.0, -16.0, 2), "Gourmet Bites": (15.0, -16.0, 2), "B_L2_Restroom": (40.0, 32.0, 2),
    "B_L2_Elevator": (40.0, 14.0, 2), "B_L2_Escalator": (40.0, 2.0, 2), "B_L2_Stairs": (40.0, -16.0, 2),
    "P_L3_Aisle_Main": (0.0, 8.0, 3), "P_L3_Driveway_Entrance": (-40.0, 2.0, 3), "P_L3_Driveway_Exit": (-40.0, 14.0, 3),
    "P1": (-22.5, -16.0, 3), "P2": (-7.5, -16.0, 3), "P3": (7.5, -16.0, 3), "P4": (22.5, -16.0, 3),
    "P5": (-22.5, 32.0, 3), "P6": (-7.5, 32.0, 3), "P7": (7.5, 32.0, 3), "P8": (22.5, 32.0, 3),
    "P_L3_Elevator": (40.0, 14.0, 3), "P_L3_Escalator": (40.0, 2.0, 3), "P_L3_Stairs": (40.0, -16.0, 3)
}

MULTI_CAD_GRAPH = {
    "A_L0_Entrance": {"A_L0_Lobby": 35.0, "Fashion Hub": 27.5},
    "Fashion Hub":   {"A_L0_Entrance": 27.5, "A_L0_Lobby": 37.5},
    "A_L0_Lobby":    {"A_L0_Entrance": 35.0, "Fashion Hub": 37.5, "A_L0_Info": 16.0, "Mega Supermarket": 20.0, "A_L0_Restroom": 15.0, "A_L0_Elevator": 38.0, "A_L0_Stairs": 38.0, "A_L0_Escalator": 33.0},
    "A_L0_Info":     {"A_L0_Lobby": 16.0}, "Mega Supermarket": {"A_L0_Lobby": 20.0},
    "A_L0_Restroom": {"A_L0_Lobby": 15.0}, "A_L0_Elevator": {"A_L0_Lobby": 38.0, "A_L1_Elevator": 15.0},
    "A_L0_Stairs":   {"A_L0_Lobby": 38.0, "A_L1_Stairs": 15.0}, "A_L0_Escalator":{"A_L0_Lobby": 33.0, "A_L1_Escalator": 12.0},
    "A_L1_Elevator": {"A_L0_Elevator": 15.0, "A_L1_Hallway": 38.0, "B_L2_Elevator": 15.0},
    "A_L1_Stairs":   {"A_L0_Stairs": 15.0, "A_L1_Hallway": 38.0, "B_L2_Stairs": 15.0},
    "A_L1_Escalator":{"A_L0_Escalator": 12.0, "A_L1_Hallway": 33.0, "B_L2_Escalator": 12.0},
    "A_L1_Hallway":  {"A_L1_Elevator": 38.0, "A_L1_Stairs": 38.0, "A_L1_Escalator": 33.0, "Tech Gadgets": 37.5, "Jewel Box": 37.5, "Book Nook": 20.0, "A_L1_Restroom": 15.0},
    "Tech Gadgets":  {"A_L1_Hallway": 37.5}, "Jewel Box": {"A_L1_Hallway": 37.5}, "Book Nook": {"A_L1_Hallway": 20.0}, "A_L1_Restroom": {"A_L1_Hallway": 15.0},
    "B_L2_Elevator": {"A_L1_Elevator": 15.0, "B_L2_Corridor": 38.0, "P_L3_Elevator": 15.0},
    "B_L2_Stairs":   {"A_L1_Stairs": 15.0, "B_L2_Corridor": 38.0, "P_L3_Stairs": 15.0},
    "B_L2_Escalator":{"A_L1_Escalator": 12.0, "B_L2_Corridor": 33.0, "P_L3_Escalator": 12.0},
    "B_L2_Corridor": {"B_L2_Elevator": 38.0, "B_L2_Stairs": 38.0, "B_L2_Escalator": 33.0, "Cineplex Theater": 37.5, "VR World & Arcade": 37.5, "Sky Food Court": 20.0, "Gourmet Bites": 20.0, "B_L2_Restroom": 20.0},
    "Cineplex Theater":  {"B_L2_Corridor": 37.5}, "VR World & Arcade": {"B_L2_Corridor": 37.5},
    "Sky Food Court":    {"B_L2_Corridor": 20.0}, "Gourmet Bites":     {"B_L2_Corridor": 20.0}, "B_L2_Restroom":     {"B_L2_Corridor": 20.0},
    "P1": {"P_L3_Aisle_Main": 20.0}, "P2": {"P_L3_Aisle_Main": 20.0}, "P3": {"P_L3_Aisle_Main": 20.0}, "P4": {"P_L3_Aisle_Main": 20.0},
    "P5": {"P_L3_Aisle_Main": 20.0}, "P6": {"P_L3_Aisle_Main": 20.0}, "P7": {"P_L3_Aisle_Main": 20.0}, "P8": {"P_L3_Aisle_Main": 20.0},
    "P_L3_Aisle_Main": {
        "P1": 20.0, "P2": 20.0, "P3": 20.0, "P4": 20.0, "P5": 20.0, "P6": 20.0, "P7": 20.0, "P8": 20.0,
        "P_L3_Elevator": 40.0, "P_L3_Stairs": 40.0, "P_L3_Escalator": 35.0, "P_L3_Driveway_Entrance": 25.0, "P_L3_Driveway_Exit": 25.0,
    },
    "P_L3_Driveway_Entrance": {"P_L3_Aisle_Main": 25.0}, "P_L3_Driveway_Exit": {"P_L3_Aisle_Main": 25.0},
    "P_L3_Elevator": {"P_L3_Aisle_Main": 40.0, "B_L2_Elevator": 15.0}, "P_L3_Stairs":   {"P_L3_Aisle_Main": 40.0, "B_L2_Stairs": 15.0},
    "P_L3_Escalator": {"P_L3_Aisle_Main": 35.0, "B_L2_Escalator": 12.0},
}

PARKING_SLOTS = {
    "P1": {"occupied": False}, "P2": {"occupied": True}, "P3": {"occupied": False}, "P4": {"occupied": False},
    "P5": {"occupied": True},  "P6": {"occupied": False}, "P7": {"occupied": False}, "P8": {"occupied": True},
}

def point_in_polygon(x, y, polygon):
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def find_room_by_coordinate(x, y, z_floor):
    for room_id, poly_info in ROOM_POLYGONS.items():
        room_z = int(MULTI_CAD_NODES.get(room_id, (0, 0, 0))[2])
        if room_z != z_floor:
            continue
        coords = poly_info.get("coords", [])
        if coords and point_in_polygon(x, y, coords):
            return room_id
    return None

def get_nearest_graph_node(x, y, z_floor, graph_nodes):
    closest_node = None
    min_dist = float("inf")
    for node_id, (nx, ny, nz) in graph_nodes.items():
        if int(nz) == int(z_floor):
            dist = math.hypot(x - nx, y - ny)
            if dist < min_dist:
                min_dist = dist
                closest_node = node_id
    return closest_node, min_dist

# ==============================================================================
# 2. Theta* Pathfinding Algorithm
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
# 3. Folium Map Rendering Engine
# ==============================================================================

def render_2d_folium_view(active_floor_z, route_path=None, current_lang="English"):
    m = folium.Map(location=[8, 0], zoom_start=11, crs="Simple", tiles=None)

    floor_rooms = {
        r_id: poly["coords"]
        for r_id, poly in ROOM_POLYGONS.items()
        if poly["z"] == active_floor_z
    }

    # Render CAD Polygons
    for room_id, coords in floor_rooms.items():
        room_info = ROOM_POLYGONS[room_id]
        translated_name = POI_TRANSLATIONS.get(current_lang, {}).get(room_id, room_id)
        folium_coords = [[pt[1], pt[0]] for pt in coords]

        folium.Polygon(
            locations=folium_coords,
            color="#4A5568",
            weight=2,
            fill=True,
            fill_color=room_info.get("color", "#CCCCCC"),
            fill_opacity=0.6,
            tooltip=translated_name,
            popup=translated_name
        ).add_to(m)

        # Label Center
        cx = sum(p[0] for p in coords) / len(coords)
        cy = sum(p[1] for p in coords) / len(coords)
        icon_str = get_location_icon(room_id)

        folium.Marker(
            location=[cy, cx],
            icon=folium.DivIcon(
                html=f'<div style="font-size:11px; font-weight:bold; color:#000000; text-align:center; white-space:nowrap;">'
                     f'{icon_str}<br>{translated_name}</div>'
            )
        ).add_to(m)

    # Render Route Line & Markers
    if route_path:
        floor_path = [node for node in route_path if MULTI_CAD_NODES[node][2] == active_floor_z]

        if len(floor_path) > 1:
            line_pts = [[MULTI_CAD_NODES[node][1], MULTI_CAD_NODES[node][0]] for node in floor_path]
            folium.PolyLine(
                locations=line_pts,
                color="#FF0000",
                weight=5,
                opacity=0.85
            ).add_to(m)

        start_node_id = route_path[0]
        dest_node_id = route_path[-1]

        if MULTI_CAD_NODES[start_node_id][2] == active_floor_z:
            sx, sy, _ = MULTI_CAD_NODES[start_node_id]
            folium.Marker(
                location=[sy, sx],
                popup="Start",
                icon=folium.Icon(color="red", icon="play")
            ).add_to(m)

        if MULTI_CAD_NODES[dest_node_id][2] == active_floor_z:
            dx, dy, _ = MULTI_CAD_NODES[dest_node_id]
            folium.Marker(
                location=[dy, dx],
                popup="Destination",
                icon=folium.Icon(color="green", icon="flag")
            ).add_to(m)

    return m

def render_rooftop_folium_map(assigned_slot=None, route_path=None, current_lang="English"):
    m = folium.Map(location=[8, 0], zoom_start=11, crs="Simple", tiles=None)

    rooftop_rooms = {
        r_id: poly["coords"]
        for r_id, poly in ROOM_POLYGONS.items()
        if poly["z"] == 3
    }

    for room_id, coords in rooftop_rooms.items():
        folium_coords = [[pt[1], pt[0]] for pt in coords]
        folium.Polygon(
            locations=folium_coords,
            color="#4A5568",
            weight=1.5,
            fill=True,
            fill_color="#F0F0F0",
            fill_opacity=0.5
        ).add_to(m)

    for slot_id, details in PARKING_SLOTS.items():
        if slot_id not in MULTI_CAD_NODES: continue
        cx, cy, _ = MULTI_CAD_NODES[slot_id]

        if slot_id == assigned_slot:
            color, status_txt = "#1D4ED8", "ASSIGNED TO YOU"
        elif details["occupied"]:
            color, status_txt = "#B91C1C", "OCCUPIED"
        else:
            color, status_txt = "#15803D", "AVAILABLE"

        box_w, box_h = 3.5, 6.0
        bx = [cx - box_w/2, cx + box_w/2, cx + box_w/2, cx - box_w/2]
        by = [cy - box_h/2, cy - box_h/2, cy + box_h/2, cy + box_h/2]
        slot_poly = [[by[i], bx[i]] for i in range(4)]

        folium.Polygon(
            locations=slot_poly,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=f"Slot {slot_id}: {status_txt}"
        ).add_to(m)

        folium.Marker(
            location=[cy, cx],
            icon=folium.DivIcon(
                html=f'<div style="font-size:10px; font-weight:bold; color:#FFFFFF;">{slot_id}</div>'
            )
        ).add_to(m)

    if route_path:
        rooftop_path = [node for node in route_path if int(MULTI_CAD_NODES[node][2]) == 3]
        if len(rooftop_path) > 1:
            line_pts = [[MULTI_CAD_NODES[n][1], MULTI_CAD_NODES[n][0]] for n in rooftop_path]
            folium.PolyLine(locations=line_pts, color="#2563EB", weight=4).add_to(m)

    return m

# ==============================================================================
# 4. Routing Engine Helpers
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
    elif -67.5 <= angle_diff < -22.5: return lang_dict["slight_right"]
    elif -112.5 <= angle_diff < -67.5: return lang_dict["right"]
    elif -157.5 <= angle_diff < -112.5: return lang_dict["sharp_right"]
    elif 22.5 < angle_diff <= 67.5: return lang_dict["slight_left"]
    elif 67.5 < angle_diff <= 112.5: return lang_dict["left"]
    elif 112.5 < angle_diff <= 157.5: return lang_dict["sharp_left"]
    else: return lang_dict["u_turn"]

def generate_detailed_directions(path, node_coords, lang="English"):
    if not path or len(path) < 2: return []
    directions = []
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
        icon = "↪️" if angle_diff_norm < -22.5 else ("↩️" if angle_diff_norm > 22.5 else "⬆️")
        directions.append({"step": len(directions) + 1, "text": instruction_str, "icon": icon})

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
    total_dist, floors_visited = 0, set()
    for i in range(len(path) - 1):
        curr_node, nxt_node = path[i], path[i+1]
        z1, z2 = MULTI_CAD_NODES[curr_node][2], MULTI_CAD_NODES[nxt_node][2]
        floors_visited.add(z1)
        floors_visited.add(z2)
        if z1 == z2: total_dist += euclidean_distance_3d(curr_node, nxt_node, MULTI_CAD_NODES)
        else: total_dist += 15.0

    return {
        "total_distance": round(total_dist, 1),
        "floors_crossed": max(0, len(floors_visited) - 1),
        "steps": len(path) - 1
    }

def format_location_label(room_id, lang):
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
# 5. Application UI & Navigation Tabs
# ==============================================================================

t = LOCALIZATION[st.session_state.lang]

home_tab_title = {
    "English": "🏠 Home", "Simplified Chinese": "🏠 首页", "Malay": "🏠 Utama"
}.get(st.session_state.lang, "🏠 Home")

tab_home, tab_map, tab_dir, tab_park = st.tabs([home_tab_title, t["tab_nav"], t["tab_directions"], t["tab_parking"]])

if "waypoints" not in st.session_state: st.session_state.waypoints = []

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
    total_locations = len(ROOM_POLYGONS)
    total_floors = len(FLOOR_TRANSLATIONS["English"])
    total_slots = len(PARKING_SLOTS)
    available_slots = sum(1 for s in PARKING_SLOTS.values() if not s["occupied"])

    c1.metric(t["poi_metric"], total_locations)
    c2.metric(t["floors_metric"], total_floors)
    c3.metric(t["spots_metric"], total_slots)
    c4.metric(t["available_metric"], available_slots)

# Mall Map Tab
with tab_map:
    with st.expander(f"⚙️ {t['nav_controls']}", expanded=True):
        room_options = list(ROOM_POLYGONS.keys())
        col_start, col_dest = st.columns(2)

        with col_start:
            start_node = st.selectbox(
                t["start_loc"],
                options=room_options,
                format_func=lambda r: format_location_label(r, st.session_state.lang),
                index=room_options.index(st.session_state.selected_start) if st.session_state.selected_start in room_options else 0,
            )
        with col_dest:
            dest_node = st.selectbox(
                t["dest_loc"],
                options=room_options,
                format_func=lambda r: format_location_label(r, st.session_state.lang),
                index=room_options.index(st.session_state.selected_dest) if st.session_state.selected_dest in room_options else len(room_options)-1,
            )

        st.session_state.selected_start = start_node
        st.session_state.selected_dest = dest_node

        route_pref = st.radio(t["route_type"], options=[t["shortest"], t["accessible"]], horizontal=True)
        accessible_flag = (route_pref == t["accessible"])

        extracted_waypoints = [wp["value"] if isinstance(wp, dict) else wp for wp in st.session_state.waypoints]
        full_route_sequence = [st.session_state.selected_start] + extracted_waypoints + [st.session_state.selected_dest]

        route_display_str = " ➔ ".join([f"`{format_location_label(loc, st.session_state.lang)}`" for loc in full_route_sequence])
        st.markdown(f"**{t['current_route_lbl']}:** {route_display_str}")

    full_path = []
    for i in range(len(full_route_sequence) - 1):
        segment_path = theta_star_3d(full_route_sequence[i], full_route_sequence[i + 1], MULTI_CAD_GRAPH, MULTI_CAD_NODES, accessible_only=accessible_flag)
        if segment_path:
            full_path.extend(segment_path[1:] if full_path else segment_path)
        else:
            full_path = []
            break

    path = full_path

    floor_select = st.selectbox(
        t["active_floor"],
        options=[0, 1, 2, 3],
        format_func=lambda x: get_translated_floor_name(x, lang=st.session_state.lang)
    )

    folium_map = render_2d_folium_view(floor_select, route_path=path, current_lang=st.session_state.lang)
    map_data = st_folium(folium_map, height=550, width=1000)

    # Click Event Handling
    if map_data and map_data.get("last_clicked"):
        click_x, click_y = map_data["last_clicked"]["lng"], map_data["last_clicked"]["lat"]

        room_hit = find_room_by_coordinate(click_x, click_y, floor_select)
        if not room_hit:
            room_hit, _ = get_nearest_graph_node(click_x, click_y, floor_select, MULTI_CAD_NODES)

        if room_hit:
            st.info(f"📍 Clicked Location: **{format_location_label(room_hit, st.session_state.lang)}**")
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button(t["btn_set_start"]):
                    st.session_state.selected_start = room_hit
                    st.rerun()
            with col_b2:
                if st.button(t["btn_set_dest"]):
                    st.session_state.selected_dest = room_hit
                    st.rerun()

# Directions Tab
with tab_dir:
    st.subheader(t["route_summary"])
    if path:
        summary = compute_route_summary(path)
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric(t["total_dist"], f"{summary['total_distance']} m")
        m_col2.metric(t["floors_crossed"], summary["floors_crossed"])
        m_col3.metric(t["total_steps"], summary["steps"])

        st.divider()
        st.subheader(t["turn_by_turn"])
        detailed_steps = generate_detailed_directions(path, MULTI_CAD_NODES, lang=st.session_state.lang)

        for step_info in detailed_steps:
            col_icon, col_text = st.columns([0.1, 0.9])
            with col_icon: st.markdown(f"### {step_info['icon']}")
            with col_text:
                st.markdown(f"**{t['step_lbl']} {step_info['step']}**")
                st.markdown(step_info["text"])
            st.divider()
    else:
        st.warning(t["no_route"])

# Smart Parking Tab
with tab_park:
    st.subheader(t["parking_sec"])
    parkable_spots = [node for node in MULTI_CAD_NODES if node.startswith("P") and node[1:].isdigit()]
    parking_availability = {spot: random.random() < 0.65 for spot in parkable_spots}

    assigned_slot, entry_path, exit_path = find_nearest_available_parking(
        "P_L3_Driveway_Entrance", MULTI_CAD_GRAPH, MULTI_CAD_NODES, availability_map=parking_availability
    )

    if assigned_slot:
        st.success(f"{t['nearest_spot_found']}: `🅿️ {assigned_slot}` ({t['rooftop_lot']})")
        park_map = render_rooftop_folium_map(assigned_slot=assigned_slot, route_path=entry_path, current_lang=st.session_state.lang)
        st_folium(park_map, height=450, width=900)
    else:
        st.error("No parking available.")
