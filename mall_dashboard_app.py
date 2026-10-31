import math
import heapq
import copy
import streamlit as st
import folium
import plotly.graph_objects as go
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
        "home_title": "Welcome to the Smart Mall Navigation System",
        "home_desc": "Navigate multi-floor shopping mall with real-time 2D and 3D pathfinding, routing options, and automated parking allocation with step-by-step directions.",
        "poi_metric": "📍 Points of Interest",
        "floors_metric": "🏢 Total Floors",
        "spots_metric": "🅿️ Total Parking Spots",
        "available_metric": "🟢 Available Spots",
        "feat_map_title": "🗺️ 2D / 3D Map View",
        "feat_map_desc": "Explore every floor on an interactive 2D map or a 3D isometric view. Click anywhere on the 2D map to plan a route.",
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
        "btn_interactive_pick": "🗺️ Interactive Route Selection on Map",
        "btn_cancel_interactive": "⏹️ Cancel Interactive Map Selection",
        "btn_reset_all": "🗑️ Reset All",
        "pick_step_1": "👇 *Step 1:* Click anywhere on the map below to set as *Start Location*.",
        "pick_step_2": "👇 *Step 2:* Click anywhere on the map to add *Intermediate Stops* (or click button below when ready for Destination).",
        "pick_step_3": "👇 *Step 3:* Click anywhere on the map to set as *Destination*.",
        "pick_3d_notice": "Interactive map selection works on the 2D map. Switch to the 2D view to click points.",
        "btn_done_adding_stops": "➡️ Done Adding Stops (Next: Pick Destination)",
        "btn_add_as_stop": "➕ Add as Stop",
        "btn_keep_start": "⏭️ Keep Current Start",
        "btn_keep_dest": "⏭️ Keep Current Destination",
        "lbl_current": "Current",
        "footer_arch": "🏢 System Architecture: 3D Theta* Pathfinding Engine",
        "footer_vector": "📐 Map Rendering: Folium & Plotly",
        "footer_lang": "🌐 Localization: Multilingual Engine",
        "tab_nav_drive_to_spot": "🚗 1. Entrance to Parking Spot",
        "tab_nav_spot_to_exit": "🚪 2. Parking Spot to Exit",
        "header_driving_to_spot": "🚗 Driving to Parking Spot",
        "header_leaving_spot": "🚪 Leaving Parking Spot to Driveway Exit",
        "lbl_entrance_ramp": "🚗 Entrance Ramp",
        "lbl_exit_ramp": "🚗 Exit Ramp",
        "lbl_stairwell": "🪜 Stairwell",
        "lbl_elevator": "🛗 Elevator",
        "lbl_escalator": "🪜 Escalator",
        "no_parking": "⚠️ No available parking spots found on the Rooftop layer.",
        "show_doors": "Show entry/exit points",
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
        "home_title": "欢迎使用智能商场导航与停车系统",
        "home_desc": "支持多楼层商场的实时 2D 与 3D 路径规划、无障碍路线选择及自动车位分配。",
        "poi_metric": "📍 兴趣点数量",
        "floors_metric": "🏢 总楼层数",
        "spots_metric": "🅿️ 总车位数",
        "available_metric": "🟢 空余车位",
        "feat_map_title": "🗺️ 2D / 3D 地图视图",
        "feat_map_desc": "在交互式 2D 地图或 3D 等轴视图中浏览各楼层，点击 2D 地图任意位置即可规划路线。",
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
        "btn_interactive_pick": "🗺️ 地图交互式路线选择",
        "btn_cancel_interactive": "⏹️ 取消地图选择模式",
        "btn_reset_all": "🗑️ 重置全部",
        "pick_step_1": "👇 *步骤 1：* 点击地图任意位置设为 *起点位置*。",
        "pick_step_2": "👇 *步骤 2：* 点击地图任意位置添加 *途经点*（若已添加完毕，请点击下方按钮选择终点）。",
        "pick_step_3": "👇 *步骤 3：* 点击地图任意位置设为 *终点位置*。",
        "pick_3d_notice": "交互式地图选点仅支持 2D 地图，请切换到 2D 视图后再点击。",
        "btn_done_adding_stops": "➡️ 完成添加途经点 (下一步: 选择终点)",
        "btn_add_as_stop": "➕ 添加为途经点",
        "btn_keep_start": "⏭️ 保留当前起点",
        "btn_keep_dest": "⏭️ 保留当前终点",
        "lbl_current": "当前",
        "footer_arch": "🏢 系统架构: 3D Theta* 路径规划引擎",
        "footer_vector": "📐 地图渲染: Folium 与 Plotly",
        "footer_lang": "🌐 多语言支持: 多语种引擎",
        "tab_nav_drive_to_spot": "🚗 1. 入口至停车位",
        "tab_nav_spot_to_exit": "🚪 2. 停车位至出口",
        "header_driving_to_spot": "🚗 驶向停车位",
        "header_leaving_spot": "🚪 离开停车位驶向出口匝道",
        "lbl_entrance_ramp": "🚗 进口匝道",
        "lbl_exit_ramp": "🚗 出口匝道",
        "lbl_stairwell": "🪜 楼梯间",
        "lbl_elevator": "🛗 电梯",
        "lbl_escalator": "🪜 自动扶梯",
        "no_parking": "⚠️ 屋顶停车场暂无可用车位。",
        "show_doors": "显示出入口",
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
        "home_title": "Selamat Datang ke Sistem Navigasi Pusat Beli-Belah Smart",
        "home_desc": "Navigasi pusat beli-belah bertingkat dengan laluan 2D dan 3D masa nyata, pilihan laluan mesra OKU, dan automatik tempat letak kereta.",
        "poi_metric": "📍 Titik Tumpuan (POI)",
        "floors_metric": "🏢 Jumlah Tingkat",
        "spots_metric": "🅿️ Jumlah Ruang Letak Kereta",
        "available_metric": "🟢 Ruang Kosong",
        "feat_map_title": "🗺️ Pandangan Peta 2D / 3D",
        "feat_map_desc": "Terokai setiap tingkat pada peta 2D interaktif atau paparan isometrik 3D. Klik di mana-mana pada peta 2D untuk merancang laluan.",
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
        "btn_interactive_pick": "🗺️ Pemilihan Laluan Interaktif pada Peta",
        "btn_cancel_interactive": "⏹️ Batal Pemilihan Peta Interaktif",
        "btn_reset_all": "🗑️ Set Semula Semua",
        "pick_step_1": "👇 *Langkah 1:* Klik di mana-mana pada peta untuk tetapkan *Lokasi Permulaan*.",
        "pick_step_2": "👇 *Langkah 2:* Klik di mana-mana pada peta untuk tambah *Hentian Antara* (atau klik butang di bawah apabila sedia untuk Destinasi).",
        "pick_step_3": "👇 *Langkah 3:* Klik di mana-mana pada peta untuk tetapkan *Destinasi*.",
        "pick_3d_notice": "Pemilihan peta interaktif berfungsi pada peta 2D. Tukar ke paparan 2D untuk mengklik titik.",
        "btn_done_adding_stops": "➡️ Selesai Menambah Hentian (Seterusnya: Pilih Destinasi)",
        "btn_add_as_stop": "➕ Tambah sebagai Hentian",
        "btn_keep_start": "⏭️ Kekalkan Permulaan Semasa",
        "btn_keep_dest": "⏭️ Kekalkan Destinasi Semasa",
        "lbl_current": "Semasa",
        "footer_arch": "🏢 Seni Bina Sistem: Enjin Laluan 3D Theta*",
        "footer_vector": "📐 Pemaparan Peta: Folium & Plotly",
        "footer_lang": "🌐 Lokalisasi: Enjin Pelbagai Bahasa",
        "tab_nav_drive_to_spot": "🚗 1. Pintu Masuk ke Petak Meletak Kenderaan",
        "tab_nav_spot_to_exit": "🚪 2. Petak Meletak Kenderaan ke Pintu Keluar",
        "header_driving_to_spot": "🚗 Memandu ke Petak Meletak Kenderaan",
        "header_leaving_spot": "🚪 Meninggalkan Petak Meletak Kenderaan ke Pintu Keluar",
        "lbl_entrance_ramp": "🚗 Ramp Masuk",
        "lbl_exit_ramp": "🚗 Ramp Keluar",
        "lbl_stairwell": "🪜 Tangga",
        "lbl_elevator": "🛗 Lif",
        "lbl_escalator": "🪜 Eskalator",
        "no_parking": "⚠️ Tiada ruang letak kereta kosong di aras bumbung.",
        "show_doors": "Tunjuk titik masuk/keluar",
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

def floor_code_for(z_val):
    z_int = int(z_val)
    return "R" if z_int == 3 else (f"{z_int}F" if z_int > 0 else "GF")

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

# Labels for nodes that are not named rooms (clicked points and corridor junctions)
POINT_LABELS = {"English": "Point", "Simplified Chinese": "自选点", "Malay": "Titik"}
JUNCTION_LABELS = {
    "English": "Corridor Junction",
    "Simplified Chinese": "走廊交汇处",
    "Malay": "Persimpangan Koridor",
}
DOOR_LABELS = {
    "English": "Entry/Exit",
    "Simplified Chinese": "出入口",
    "Malay": "Pintu Masuk/Keluar",
}
DYNAMIC_PREFIX = "Dynamic_Point_"
DOOR_PREFIX = "Door_"

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
    "English": {
        "Apparel": "Apparel", "Electronics": "Electronics", "Jewelry": "Jewelry", "Supermarket": "Supermarket",
        "Food & Beverage": "Food & Beverage", "Books": "Books", "Cinema": "Cinema", "Arcade": "Arcade",
        "Restroom": "Restroom", "Facility": "Facility"
    },
    "Simplified Chinese": {
        "Apparel": "服装饰品", "Electronics": "电子数码", "Jewelry": "珠宝首饰", "Supermarket": "超级市场",
        "Food & Beverage": "餐饮美食", "Books": "图书文具", "Cinema": "电影院", "Arcade": "娱乐电玩",
        "Restroom": "洗手间", "Facility": "公共设施"
    },
    "Malay": {
        "Apparel": "Pakaian", "Electronics": "Barangan Elektronik", "Jewelry": "Barang Kemas", "Supermarket": "Pasar Raya",
        "Food & Beverage": "Makanan & Minuman", "Books": "Buku", "Cinema": "Pawagam", "Arcade": "Pusat Rekreasi",
        "Restroom": "Tandas", "Facility": "Kemudahan"
    }
}

if "lang" not in st.session_state: st.session_state.lang = "English"
if "selected_start" not in st.session_state: st.session_state.selected_start = "A_L0_Entrance"
if "selected_dest" not in st.session_state: st.session_state.selected_dest = "A_L0_Lobby"
if "waypoints" not in st.session_state: st.session_state.waypoints = []
if "waypoint_counter" not in st.session_state: st.session_state.waypoint_counter = 0
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
    # Ground Floor
    "A_L0_Entrance": (-40.0, 8.0, 0), "A_L0_Info": (-40.0, 32.0, 0), "A_L0_Lobby": (0.0, 8.0, 0),
    "Fashion Hub": (0.0, -16.0, 0), "Mega Supermarket": (0.0, 32.0, 0), "A_L0_Restroom": (40.0, 32.0, 0),
    "A_L0_Elevator": (40.0, 14.0, 0), "A_L0_Escalator": (40.0, 2.0, 0), "A_L0_Stairs": (40.0, -16.0, 0),
    "H_L0_West": (-20.0, 8.0, 0), "H_L0_East": (20.0, 8.0, 0), "H_L0_North": (0.0, 20.0, 0), "H_L0_South": (0.0, -4.0, 0),

    # 1st Floor
    "A_L1_Hallway": (0.0, 8.0, 1), "Book Nook": (-15.0, -16.0, 1), "Tech Gadgets": (15.0, -16.0, 1),
    "Jewel Box": (0.0, 32.0, 1), "A_L1_Restroom": (40.0, 32.0, 1), "A_L1_Elevator": (40.0, 14.0, 1),
    "A_L1_Escalator": (40.0, 2.0, 1), "A_L1_Stairs": (40.0, -16.0, 1),
    "H_L1_West": (-20.0, 8.0, 1), "H_L1_East": (20.0, 8.0, 1), "H_L1_South_West": (-15.0, -4.0, 1), "H_L1_South_East": (15.0, -4.0, 1),

    # 2nd Floor
    "B_L2_Corridor": (0.0, 8.0, 2), "VR World & Arcade": (-40.0, 8.0, 2), "Cineplex Theater": (0.0, 32.0, 2),
    "Sky Food Court": (-15.0, -16.0, 2), "Gourmet Bites": (15.0, -16.0, 2), "B_L2_Restroom": (40.0, 32.0, 2),
    "B_L2_Elevator": (40.0, 14.0, 2), "B_L2_Escalator": (40.0, 2.0, 2), "B_L2_Stairs": (40.0, -16.0, 2),
    "H_L2_West": (-20.0, 8.0, 2), "H_L2_East": (20.0, 8.0, 2), "H_L2_South_West": (-15.0, -4.0, 2), "H_L2_South_East": (15.0, -4.0, 2),

    # Rooftop Parking
    "P_L3_Aisle_Main": (0.0, 8.0, 3), "P_L3_Driveway_Entrance": (-40.0, 2.0, 3), "P_L3_Driveway_Exit": (-40.0, 14.0, 3),
    "P1": (-22.5, -16.0, 3), "P2": (-7.5, -16.0, 3), "P3": (7.5, -16.0, 3), "P4": (22.5, -16.0, 3),
    "P5": (-22.5, 32.0, 3), "P6": (-7.5, 32.0, 3), "P7": (7.5, 32.0, 3), "P8": (22.5, 32.0, 3),
    "P_L3_Elevator": (40.0, 14.0, 3), "P_L3_Escalator": (40.0, 2.0, 3), "P_L3_Stairs": (40.0, -16.0, 3)
}

MULTI_CAD_GRAPH = {
    # Ground Floor
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

    # 1st Floor
    "A_L1_Hallway": {"H_L1_West": 20.0, "H_L1_East": 20.0, "Jewel Box": 24.0, "H_L1_South_West": 18.0, "H_L1_South_East": 18.0},
    "H_L1_West": {"A_L1_Hallway": 20.0, "H_L1_South_West": 13.0},
    "H_L1_East": {"A_L1_Hallway": 20.0, "A_L1_Restroom": 28.0, "A_L1_Elevator": 20.8, "A_L1_Escalator": 20.8, "A_L1_Stairs": 31.2},
    "Jewel Box": {"A_L1_Hallway": 24.0},
    "H_L1_South_West": {"H_L1_West": 13.0, "A_L1_Hallway": 18.0, "Book Nook": 12.0},
    "H_L1_South_East": {"H_L1_East": 13.0, "A_L1_Hallway": 18.0, "Tech Gadgets": 12.0},
    "Book Nook": {"H_L1_South_West": 12.0}, "Tech Gadgets": {"H_L1_South_East": 12.0},
    "A_L1_Restroom": {"H_L1_East": 28.0},
    "A_L1_Elevator": {"H_L1_East": 20.8, "A_L0_Elevator": 15.0, "B_L2_Elevator": 15.0},
    "A_L1_Escalator": {"H_L1_East": 20.8, "A_L0_Escalator": 12.0, "B_L2_Escalator": 12.0},
    "A_L1_Stairs": {"H_L1_East": 31.2, "A_L0_Stairs": 15.0, "B_L2_Stairs": 15.0},

    # 2nd Floor
    "B_L2_Corridor": {"H_L2_West": 20.0, "H_L2_East": 20.0, "Cineplex Theater": 24.0, "H_L2_South_West": 18.0, "H_L2_South_East": 18.0},
    "H_L2_West": {"B_L2_Corridor": 20.0, "VR World & Arcade": 20.0, "H_L2_South_West": 13.0},
    "VR World & Arcade": {"H_L2_West": 20.0}, "Cineplex Theater": {"B_L2_Corridor": 24.0},
    "H_L2_South_West": {"H_L2_West": 13.0, "B_L2_Corridor": 18.0, "Sky Food Court": 12.0},
    "H_L2_South_East": {"H_L2_East": 13.0, "B_L2_Corridor": 18.0, "Gourmet Bites": 12.0},
    "Sky Food Court": {"H_L2_South_West": 12.0}, "Gourmet Bites": {"H_L2_South_East": 12.0},
    "H_L2_East": {"B_L2_Corridor": 20.0, "B_L2_Restroom": 28.0, "B_L2_Elevator": 20.8, "B_L2_Escalator": 20.8, "B_L2_Stairs": 31.2},
    "B_L2_Restroom": {"H_L2_East": 28.0},
    "B_L2_Elevator": {"H_L2_East": 20.8, "A_L1_Elevator": 15.0, "P_L3_Elevator": 15.0},
    "B_L2_Escalator": {"H_L2_East": 20.8, "A_L1_Escalator": 12.0, "P_L3_Escalator": 12.0},
    "B_L2_Stairs": {"H_L2_East": 31.2, "A_L1_Stairs": 15.0, "P_L3_Stairs": 15.0},

    # Rooftop Parking
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

# ------------------------------------------------------------------------------
# Entry/exit points (doors)
# room id -> (x, y, node the door opens onto). Each (x, y) sits on the room's
# boundary. Rooms that don't touch a corridor open onto the neighbouring room
# they are actually reached through.
# ------------------------------------------------------------------------------
DOORS = {
    # Ground Floor
    "Fashion Hub": (0.0, -4.0, "H_L0_South"),
    "Mega Supermarket": (0.0, 20.0, "H_L0_North"),
    "A_L0_Entrance": (-30.0, 8.0, "H_L0_West"),
    "A_L0_Info": (-40.0, 20.0, "A_L0_Entrance"),
    "A_L0_Elevator": (30.0, 14.0, "H_L0_East"),
    "A_L0_Escalator": (30.0, 2.0, "H_L0_East"),
    "A_L0_Stairs": (40.0, -4.0, "A_L0_Escalator"),
    "A_L0_Restroom": (40.0, 20.0, "A_L0_Elevator"),

    # 1st Floor
    "Jewel Box": (0.0, 20.0, "A_L1_Hallway"),
    "Book Nook": (-15.0, -4.0, "H_L1_South_West"),
    "Tech Gadgets": (15.0, -4.0, "H_L1_South_East"),
    "A_L1_Elevator": (30.0, 14.0, "H_L1_East"),
    "A_L1_Escalator": (30.0, 2.0, "H_L1_East"),
    "A_L1_Stairs": (40.0, -4.0, "A_L1_Escalator"),
    "A_L1_Restroom": (40.0, 20.0, "A_L1_Elevator"),

    # 2nd Floor
    "Cineplex Theater": (0.0, 20.0, "B_L2_Corridor"),
    "VR World & Arcade": (-30.0, 8.0, "H_L2_West"),
    "Sky Food Court": (-15.0, -4.0, "H_L2_South_West"),
    "Gourmet Bites": (15.0, -4.0, "H_L2_South_East"),
    "B_L2_Elevator": (30.0, 14.0, "H_L2_East"),
    "B_L2_Escalator": (30.0, 2.0, "H_L2_East"),
    "B_L2_Stairs": (40.0, -4.0, "B_L2_Escalator"),
    "B_L2_Restroom": (40.0, 20.0, "B_L2_Elevator"),

    # Rooftop Parking
    "P_L3_Driveway_Entrance": (-30.0, 2.0, "P_L3_Aisle_Main"),
    "P_L3_Driveway_Exit": (-30.0, 14.0, "P_L3_Aisle_Main"),
    "P1": (-22.5, -4.0, "P_L3_Aisle_Main"), "P2": (-7.5, -4.0, "P_L3_Aisle_Main"),
    "P3": (7.5, -4.0, "P_L3_Aisle_Main"), "P4": (22.5, -4.0, "P_L3_Aisle_Main"),
    "P5": (-22.5, 20.0, "P_L3_Aisle_Main"), "P6": (-7.5, 20.0, "P_L3_Aisle_Main"),
    "P7": (7.5, 20.0, "P_L3_Aisle_Main"), "P8": (22.5, 20.0, "P_L3_Aisle_Main"),
    "P_L3_Elevator": (30.0, 14.0, "P_L3_Aisle_Main"),
    "P_L3_Escalator": (30.0, 2.0, "P_L3_Aisle_Main"),
    "P_L3_Stairs": (40.0, -4.0, "P_L3_Escalator"),
}

def install_doors(nodes, graph, doors, rooms):
    """Add a door node per room and reroute the room's same-floor links through it."""
    # Pass 1: drop direct same-floor links of every door room (floor-to-floor links stay)
    for room_id in doors:
        z = rooms[room_id]["z"]
        for nb in list(graph.get(room_id, {})):
            if nb in nodes and nodes[nb][2] == z:
                graph[room_id].pop(nb)
                graph.get(nb, {}).pop(room_id, None)

    # Pass 2: room <-> door <-> the node the door opens onto
    for room_id, (dx, dy, link) in doors.items():
        z = rooms[room_id]["z"]
        door_id = f"{DOOR_PREFIX}{room_id}"
        nodes[door_id] = (float(dx), float(dy), z)

        rx, ry, _ = nodes[room_id]
        lx, ly, _ = nodes[link]
        d_room = math.hypot(dx - rx, dy - ry)
        d_link = math.hypot(dx - lx, dy - ly)

        graph.setdefault(room_id, {})[door_id] = d_room
        graph.setdefault(door_id, {})[room_id] = d_room
        graph[door_id][link] = d_link
        graph.setdefault(link, {})[door_id] = d_link

install_doors(MULTI_CAD_NODES, MULTI_CAD_GRAPH, DOORS, ROOM_POLYGONS)

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

def find_room_at(px, py, pz):
    """Return the id of the room polygon on floor pz that contains point (px, py), or None."""
    for room_id, info in ROOM_POLYGONS.items():
        if int(info["z"]) != int(pz):
            continue
        coords = info["coords"]
        inside = False
        j = len(coords) - 1
        for i in range(len(coords)):
            xi, yi = coords[i]
            xj, yj = coords[j]
            if (yi > py) != (yj > py) and px < (xj - xi) * (py - yi) / (yj - yi) + xi:
                inside = not inside
            j = i
        if inside:
            return room_id
    return None

def resolve_all_route_points(route_sequence, floor_z, graph_copy, nodes_copy):
    """
    Resolves route sequence. Connects dynamic click points directly to each other
    if line-of-sight is clear, or to any visible nodes on the floor. A click inside
    a room bypasses that room's centre node and links straight to the nodes the
    centre connects to, so the route goes only to the clicked point.
    """
    resolved_sequence = []

    for pt in route_sequence:
        if isinstance(pt, tuple) and len(pt) == 3:
            px, py, pz = pt
            temp_id = f"{DYNAMIC_PREFIX}({px:.2f}_{py:.2f}_Z{pz})"
            nodes_copy[temp_id] = (px, py, pz)
            graph_copy[temp_id] = {}

            def link(n_id):
                nx, ny, _ = nodes_copy[n_id]
                dist = math.hypot(px - nx, py - ny)
                graph_copy[temp_id][n_id] = dist
                graph_copy.setdefault(n_id, {})[temp_id] = dist

            skip_nodes = {temp_id}
            room_id = find_room_at(px, py, pz)
            room_door = f"{DOOR_PREFIX}{room_id}" if room_id else None

            if room_door and room_door in nodes_copy:
                # Click is inside a room with a door: the only way in or out
                # is through that room's entry/exit point.
                link(room_door)
            else:
                # Click is in a corridor/hub: bypass the room's centre node and
                # connect straight to the nodes the centre connects to.
                if room_id and room_id in MULTI_CAD_GRAPH:
                    skip_nodes.add(room_id)
                    for nb in MULTI_CAD_GRAPH[room_id]:
                        if nb in nodes_copy and int(nodes_copy[nb][2]) == int(pz):
                            link(nb)

                # Also connect to any other node with clear line of sight
                for n_id, coords in list(nodes_copy.items()):
                    if n_id in skip_nodes or n_id.startswith(DYNAMIC_PREFIX):
                        continue
                    if int(coords[2]) == int(pz):
                        if has_line_of_sight_3d(temp_id, n_id, nodes_copy, WALL_SEGMENTS_BY_FLOOR):
                            link(n_id)

            resolved_sequence.append(temp_id)
        else:
            resolved_sequence.append(pt)

    # Link consecutive dynamic click points directly if line of sight is clear
    for i in range(len(resolved_sequence) - 1):
        nA, nB = resolved_sequence[i], resolved_sequence[i + 1]
        if nA in nodes_copy and nB in nodes_copy:
            if nodes_copy[nA][2] == nodes_copy[nB][2]:
                if has_line_of_sight_3d(nA, nB, nodes_copy, WALL_SEGMENTS_BY_FLOOR):
                    ax, ay, _ = nodes_copy[nA]
                    bx, by, _ = nodes_copy[nB]
                    dist = math.hypot(ax - bx, ay - by)
                    graph_copy.setdefault(nA, {})[nB] = dist
                    graph_copy.setdefault(nB, {})[nA] = dist

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
# 4. Map Rendering (Folium 2D, Plotly 3D, Folium Rooftop)
# ==============================================================================

def add_door_markers_2d(m, floor_z, lang="English", radius=5):
    door_lbl = DOOR_LABELS.get(lang, DOOR_LABELS["English"])
    for room_id, (dx, dy, _link) in DOORS.items():
        if int(ROOM_POLYGONS[room_id]["z"]) != int(floor_z):
            continue
        name = POI_TRANSLATIONS.get(lang, {}).get(room_id, room_id).split("(")[0].strip()
        folium.CircleMarker(
            location=[dy, dx], radius=radius, color="#065F46", weight=2,
            fill=True, fill_color="#34D399", fill_opacity=1.0,
            tooltip=f"{name} – {door_lbl}"
        ).add_to(m)

def render_2d_folium_view(active_floor_z, route_path=None, node_coords_dict=MULTI_CAD_NODES, current_lang="English",
                          stop_ids=None, show_dest=True, show_doors=True):
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

    if show_doors:
        add_door_markers_2d(m, active_floor_z, current_lang)

    if route_path:
        floor_path = [node for node in route_path if node in node_coords_dict and node_coords_dict[node][2] == active_floor_z]

        if len(floor_path) > 1:
            line_pts = [[node_coords_dict[node][1], node_coords_dict[node][0]] for node in floor_path]
            folium.PolyLine(locations=line_pts, color="#EF4444", weight=5, opacity=0.9).add_to(m)

        start_node_id = route_path[0]
        dest_node_id = route_path[-1]

        # Intermediate stops
        for idx, stop_id in enumerate(stop_ids or [], start=1):
            if stop_id in node_coords_dict and node_coords_dict[stop_id][2] == active_floor_z:
                stx, sty, _ = node_coords_dict[stop_id]
                folium.Marker(location=[sty, stx], popup=f"Stop {idx}", icon=folium.Icon(color="orange", icon="info-sign")).add_to(m)

        if start_node_id in node_coords_dict and node_coords_dict[start_node_id][2] == active_floor_z:
            sx, sy, _ = node_coords_dict[start_node_id]
            folium.Marker(location=[sy, sx], popup="Start Point", icon=folium.Icon(color="red", icon="play")).add_to(m)

        if show_dest and len(route_path) > 1 and dest_node_id in node_coords_dict and node_coords_dict[dest_node_id][2] == active_floor_z:
            dx, dy, _ = node_coords_dict[dest_node_id]
            folium.Marker(location=[dy, dx], popup="Destination Point", icon=folium.Icon(color="green", icon="flag")).add_to(m)

    m.fit_bounds(bounds)
    return m

def render_3d_isometric_view(route_path=None, node_coords=None, current_lang="English", show_doors=True):
    node_coords = node_coords or MULTI_CAD_NODES
    fig = go.Figure()
    lang_dict = LOCALIZATION.get(current_lang, LOCALIZATION["English"])

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

    if show_doors:
        door_lbl = DOOR_LABELS.get(current_lang, DOOR_LABELS["English"])
        d_x, d_y, d_z, d_text = [], [], [], []
        for room_id, (dx, dy, _link) in DOORS.items():
            name = POI_TRANSLATIONS.get(current_lang, {}).get(room_id, room_id).split("(")[0].strip()
            d_x.append(dx)
            d_y.append(dy)
            d_z.append(ROOM_POLYGONS[room_id]["z"] * 40)
            d_text.append(f"{name} – {door_lbl}")
        fig.add_trace(go.Scatter3d(
            x=d_x, y=d_y, z=d_z,
            mode="markers",
            marker=dict(size=4, color="#10B981"),
            hovertext=d_text,
            hoverinfo="text",
            showlegend=False
        ))

    if route_path and len(route_path) > 0:
        sx, sy, sz = node_coords[route_path[0]]
        fig.add_trace(go.Scatter3d(
            x=[sx], y=[sy], z=[sz * 40],
            mode="markers+text",
            marker=dict(size=8, color="#FF0000"),
            text=[lang_dict["marker_start"].strip()],
            textposition="top center",
            textfont=dict(color="#FF0000", size=11),
            showlegend=False
        ))

        if len(route_path) > 1:
            dx, dy, dz = node_coords[route_path[-1]]
            fig.add_trace(go.Scatter3d(
                x=[dx], y=[dy], z=[dz * 40],
                mode="markers+text",
                marker=dict(size=8, color="#00FF00"),
                text=[lang_dict["marker_dest"].strip()],
                textposition="top center",
                textfont=dict(color="#00AA00", size=11),
                showlegend=False
            ))

    if route_path and len(route_path) > 1:
        rx = [node_coords[n][0] for n in route_path]
        ry = [node_coords[n][1] for n in route_path]
        rz = [node_coords[n][2] * 40 for n in route_path]

        fig.add_trace(go.Scatter3d(
            x=rx, y=ry, z=rz,
            mode="lines+markers",
            line=dict(color="#FF0000", width=6),
            marker=dict(size=6, color="#8B0000"),
            name="Route Path",
            showlegend=False
        ))

        cone_x, cone_y, cone_z = [], [], []
        cone_u, cone_v, cone_w = [], [], []

        for i in range(len(route_path) - 1):
            x1, y1, z1_idx = node_coords[route_path[i]]
            x2, y2, z2_idx = node_coords[route_path[i + 1]]
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
                showscale=False, sizemode="absolute", sizeref=30, anchor="tip"
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

def add_parking_infrastructure_markers(m, lang="English"):
    feature_nodes = {
        "P_L3_Driveway_Entrance": "lbl_entrance_ramp",
        "P_L3_Driveway_Exit": "lbl_exit_ramp",
        "P_L3_Stairs": "lbl_stairwell",
        "P_L3_Elevator": "lbl_elevator",
        "P_L3_Escalator": "lbl_escalator",
    }
    lang_dict = LOCALIZATION.get(lang, LOCALIZATION["English"])

    for node_id, trans_key in feature_nodes.items():
        if node_id in MULTI_CAD_NODES:
            x, y, _ = MULTI_CAD_NODES[node_id]
            label_text = lang_dict.get(trans_key, node_id)
            folium.Marker(
                location=[y, x],
                icon=folium.DivIcon(
                    html=f'''<div style="font-size: 11px; font-weight: bold; color: #000000; background: rgba(255,255,255,0.95);
                        border: 2px solid #1976D2; border-radius: 4px; padding: 2px 6px; white-space: nowrap;
                        transform: translate(-50%, -50%);">{label_text}</div>'''
                )
            ).add_to(m)

def render_rooftop_folium_map(assigned_slot=None, route_path=None, current_lang="English", route_color="#2563EB"):
    rooftop_rooms = {r_id: poly["coords"] for r_id, poly in ROOM_POLYGONS.items() if poly["z"] == 3}
    all_pts = [pt for coords in rooftop_rooms.values() for pt in coords]
    min_x, max_x = min(p[0] for p in all_pts) - 10, max(p[0] for p in all_pts) + 10
    min_y, max_y = min(p[1] for p in all_pts) - 10, max(p[1] for p in all_pts) + 10

    m = folium.Map(crs="Simple", tiles=None)

    for room_id, coords in rooftop_rooms.items():
        folium_coords = [[pt[1], pt[0]] for pt in coords]
        folium.Polygon(
            locations=folium_coords, color="#475569", weight=1.5, fill=True, fill_color="#E2E8F0", fill_opacity=0.5,
            tooltip=POI_TRANSLATIONS.get(current_lang, {}).get(room_id, room_id)
        ).add_to(m)

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
            folium.PolyLine(locations=line_pts, color=route_color, weight=4).add_to(m)

    add_door_markers_2d(m, 3, current_lang, radius=3)
    add_parking_infrastructure_markers(m, current_lang)

    m.fit_bounds([[min_y, min_x], [max_y, max_x]])
    return m

# ==============================================================================
# 5. Helpers, Parking Allocation & Navigation Directions
# ==============================================================================

def path_length(path, nodes):
    return sum(euclidean_distance_3d(a, b, nodes) for a, b in zip(path, path[1:]))

def find_nearest_available_parking(entrance_node, graph, nodes, availability_map, accessible_only=False):
    """availability_map maps spot id -> is_occupied (True means taken)."""
    available_spots = [spot for spot, is_occupied in availability_map.items() if not is_occupied]
    if not available_spots: return None, [], []

    best_spot, shortest_distance, best_entry_path = None, float("inf"), []
    for spot in available_spots:
        path = theta_star_3d(entrance_node, spot, graph, nodes, accessible_only=accessible_only)
        if path:
            dist = path_length(path, nodes)
            if dist < shortest_distance:
                shortest_distance = dist
                best_spot = spot
                best_entry_path = path

    best_exit_path = theta_star_3d(best_spot, "P_L3_Driveway_Exit", graph, nodes, accessible_only=accessible_only) if best_spot else []
    return best_spot, best_entry_path, best_exit_path

def format_location_label(loc, lang):
    if isinstance(loc, tuple):
        point_lbl = POINT_LABELS.get(lang, "Point")
        return f"[{floor_code_for(loc[2])}] {point_lbl} ({loc[0]:.1f}, {loc[1]:.1f})"

    floor_code = floor_code_for(MULTI_CAD_NODES[loc][2])
    name = POI_TRANSLATIONS.get(lang, {}).get(loc, loc)
    clean_name = name.split('(')[0].strip()

    cat_key = STORE_CATEGORIES.get(loc)
    if cat_key:
        cat_name = CATEGORY_TRANSLATIONS.get(lang, {}).get(cat_key, cat_key)
        return f"[{floor_code}] {clean_name} ({cat_name})"
    return f"[{floor_code}] {clean_name}"

def get_node_display_name(node_id, lang, node_coords):
    """Readable name for any route node, including clicked points and corridor junctions."""
    if node_id.startswith(DYNAMIC_PREFIX):
        x, y, z = node_coords[node_id]
        return f"📍{POINT_LABELS.get(lang, 'Point')} ({x:.1f}, {y:.1f})"
    if node_id.startswith(DOOR_PREFIX):
        room_id = node_id[len(DOOR_PREFIX):]
        room_name = POI_TRANSLATIONS.get(lang, {}).get(room_id, room_id).split("(")[0].strip()
        return f"{room_name} ({DOOR_LABELS.get(lang, DOOR_LABELS['English'])})"
    if node_id.startswith("H_L"):
        return JUNCTION_LABELS.get(lang, JUNCTION_LABELS["English"])
    return POI_TRANSLATIONS.get(lang, {}).get(node_id, node_id)

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

    if -22.5 <= angle_diff <= 22.5:
        return lang_dict["straight"]
    elif -67.5 <= angle_diff < -22.5:
        return lang_dict["slight_right"]
    elif -112.5 <= angle_diff < -67.5:
        return lang_dict["right"]
    elif -157.5 <= angle_diff < -112.5:
        return lang_dict["sharp_right"]
    elif 22.5 < angle_diff <= 67.5:
        return lang_dict["slight_left"]
    elif 67.5 < angle_diff <= 112.5:
        return lang_dict["left"]
    elif 112.5 < angle_diff <= 157.5:
        return lang_dict["sharp_left"]
    else:
        return lang_dict["u_turn"]

def dedupe_path(path, node_coords):
    """Drop consecutive nodes at identical coordinates (e.g. a door sitting on a corridor junction)."""
    cleaned = []
    for node in path or []:
        if cleaned and node_coords[cleaned[-1]] == node_coords[node]:
            if node == path[-1]:
                cleaned[-1] = node
            continue
        cleaned.append(node)
    return cleaned

def generate_detailed_directions(path, node_coords, lang="English"):
    path = dedupe_path(path, node_coords)
    if len(path) < 2: return []

    directions = []

    start_poi = get_node_display_name(path[0], lang, node_coords)
    first_dest_poi = get_node_display_name(path[1], lang, node_coords)
    init_dist = euclidean_distance_3d(path[0], path[1], node_coords)

    start_text = {
        "English": f"Start at **{start_poi}** and head towards **{first_dest_poi}** ({init_dist:.1f}m).",
        "Simplified Chinese": f"从 **{start_poi}** 出发，前往 **{first_dest_poi}**（{init_dist:.1f} 米）。",
        "Malay": f"Mula di **{start_poi}** dan menuju ke **{first_dest_poi}** ({init_dist:.1f}m)."
    }
    directions.append({"step": 1, "text": start_text.get(lang, start_text["English"]), "icon": "🛫"})

    for i in range(1, len(path) - 1):
        prev_node, curr_node, next_node = path[i - 1], path[i], path[i + 1]

        curr_poi = get_node_display_name(curr_node, lang, node_coords)
        next_poi = get_node_display_name(next_node, lang, node_coords)

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

        next_heading = calculate_heading_angle(curr_node, next_node, node_coords)
        if node_coords[prev_node][2] != node_coords[curr_node][2]:
            # Just arrived from another floor: there is no meaningful incoming heading
            prev_heading = next_heading
        else:
            prev_heading = calculate_heading_angle(prev_node, curr_node, node_coords)
        angle_diff = next_heading - prev_heading

        step_dist = euclidean_distance_3d(curr_node, next_node, node_coords)
        instruction_str = format_turn_instruction(angle_diff, step_dist, f"**{next_poi}**", lang=lang)

        angle_diff_norm = (angle_diff + 180) % 360 - 180
        icon = "↪️" if angle_diff_norm < -22.5 else ("↩️" if angle_diff_norm > 22.5 else "⬆️")

        directions.append({"step": len(directions) + 1, "text": instruction_str, "icon": icon})

    final_poi = get_node_display_name(path[-1], lang, node_coords)
    arrival_text = {
        "English": f"You have arrived at your destination: **{final_poi}**.",
        "Simplified Chinese": f"您已到达目的地：**{final_poi}**。",
        "Malay": f"Anda telah tiba di destinasi: **{final_poi}**."
    }
    directions.append({"step": len(directions) + 1, "text": arrival_text.get(lang, arrival_text["English"]), "icon": "🏁"})

    return directions

def compute_route_summary(path, node_coords):
    path = dedupe_path(path, node_coords)
    if len(path) < 2: return {"total_distance": 0, "floors_crossed": 0, "steps": 0}

    total_dist = 0
    floors_visited = set()

    for i in range(len(path) - 1):
        curr_node, nxt_node = path[i], path[i + 1]
        z1, z2 = node_coords[curr_node][2], node_coords[nxt_node][2]

        floors_visited.add(z1)
        floors_visited.add(z2)

        if z1 == z2:
            total_dist += euclidean_distance_3d(curr_node, nxt_node, node_coords)
        else:
            total_dist += 15.0

    return {
        "total_distance": round(total_dist, 1),
        "floors_crossed": max(0, len(floors_visited) - 1),
        "steps": len(path) - 1
    }

def render_direction_steps(steps, step_label):
    for step_info in steps:
        col_icon, col_text = st.columns([0.1, 0.9])
        with col_icon:
            st.markdown(f"### {step_info['icon']}")
        with col_text:
            st.markdown(f"**{step_label} {step_info['step']}**")
            st.markdown(step_info["text"])
        st.divider()

# ==============================================================================
# 6. UI Styling & Navigation Tabs
# ==============================================================================

st.markdown(
    """
    <style>
    /* top header bar */
    header[data-testid="stHeader"] {
        background-color: #D32F2F !important; /* Deep Red */
    }

    /* sidebar */
    section[data-testid="stSidebar"] {
        background-color: #FF6700 !important; /* Orange */
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown p {
        color: #000000 !important;
    }

    button[kind="primary"] {
        background-color: #D32F2F !important;
        color: #FFFFFF !important;
        border: 1px solid #D32F2F !important;
        font-weight: 600 !important;
    }

    button[kind="primary"]:hover {
        background-color: #E55451 !important;
        border: 1px solid #E55451 !important;
        color: #FFFFFF !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def render_orange_card(title, desc):
    card_html = f"""
    <div style="
        background-color: #FF6700;
        border: 2px solid #FF6700;
        border-radius: 12px;
        padding: 18px 16px;
        margin-bottom: 10px;
        color: #000000;
        height: 100%;
    ">
        <h3 style="color: #000000 !important; margin-top: 0; margin-bottom: 8px; font-size: 1.2rem; font-weight: 700;">{title}</h3>
        <p style="color: #000000 !important; margin: 0; font-size: 0.95rem; line-height: 1.4;">{desc}</p>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

t = LOCALIZATION[st.session_state.lang]
lang_now = st.session_state.lang

home_tab_title = {"English": "🏠 Home", "Simplified Chinese": "🏠 首页", "Malay": "🏠 Utama"}.get(lang_now, "🏠 Home")
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

# ------------------------------------------------------------------------------
# Home Tab
# ------------------------------------------------------------------------------
with tab_home:
    st.title(t["title"])
    st.caption(t["subtitle"])
    st.divider()
    st.markdown(f"### {t['home_title']}\n{t['home_desc']}")
    st.divider()

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        render_orange_card(t["feat_map_title"], t["feat_map_desc"])
    with col_f2:
        render_orange_card(t["feat_turn_title"], t["feat_turn_desc"])
    with col_f3:
        render_orange_card(t["feat_park_title"], t["feat_park_desc"])

    st.divider()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t["poi_metric"], len(ROOM_POLYGONS))
    c2.metric(t["floors_metric"], len(FLOOR_TRANSLATIONS["English"]))
    c3.metric(t["spots_metric"], len(PARKING_SLOTS))
    c4.metric(t["available_metric"], sum(1 for s in PARKING_SLOTS.values() if not s["occupied"]))

    st.divider()

    category_header = {
        "English": "🏷️ Store Directory by Category",
        "Simplified Chinese": "🏷️ 分类店铺指南",
        "Malay": "🏷️ Direktori Kedai Mengikut Kategori",
    }.get(lang_now, "🏷️ Store Directory by Category")

    st.subheader(category_header)

    if STORE_CATEGORIES:
        categorized_stores = {}
        for room_id, cat_key in STORE_CATEGORIES.items():
            categorized_stores.setdefault(cat_key, []).append(room_id)

        st.markdown(
            """
            <style>
            div[data-testid="stExpander"] details summary {
              background-color: #D32F2F !important;
              color: #FFFFFF !important;
              border-radius: 8px 8px 0px 0px !important;
              padding: 10px 16px !important;
            }

            div[data-testid="stExpander"] details summary p,
            div[data-testid="stExpander"] details summary svg {
              color: #FFFFFF !important;
              fill: #FFFFFF !important;
              font-weight: bold !important;
            }

            div[data-testid="stExpander"] details div[data-testid="stExpanderDetails"] {
              background-color: #FF6700 !important;
              border-radius: 0px 0px 8px 8px !important;
              padding: 16px !important;
              border: 1px solid #E65100 !important;
              color: #000000 !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        for cat_key, room_ids in categorized_stores.items():
            translated_cat = CATEGORY_TRANSLATIONS.get(lang_now, {}).get(cat_key, cat_key)

            with st.expander(f"📁 **{translated_cat}** ({len(room_ids)})", expanded=True):
                store_cols = st.columns(2)
                for idx, room_id in enumerate(room_ids):
                    col = store_cols[idx % 2]
                    z_val = int(MULTI_CAD_NODES[room_id][2]) if room_id in MULTI_CAD_NODES else 0
                    raw_name = POI_TRANSLATIONS.get(lang_now, {}).get(room_id, room_id)
                    clean_name = raw_name.split("(")[0].strip()
                    col.markdown(f"- **{clean_name}** `[{floor_code_for(z_val)}]`")
    else:
        st.info("No store categories defined.")

# ------------------------------------------------------------------------------
# Mall Map Tab
# ------------------------------------------------------------------------------
CUSTOM_OPTION = "__CUSTOM_POINT__"

with tab_map:
    # Migrate any legacy plain-string waypoints into {"id", "value"} objects
    if st.session_state.waypoints and not isinstance(st.session_state.waypoints[0], dict):
        migrated_wps = []
        for raw_wp in st.session_state.waypoints:
            st.session_state.waypoint_counter += 1
            migrated_wps.append({"id": st.session_state.waypoint_counter, "value": raw_wp})
        st.session_state.waypoints = migrated_wps

    room_options = list(ROOM_POLYGONS.keys())

    def location_selectbox(label, session_key, fallback_index):
        """Selectbox for a start/destination that may currently be a clicked map point."""
        current = st.session_state[session_key]
        is_custom = isinstance(current, tuple)
        options = ([CUSTOM_OPTION] if is_custom else []) + room_options

        def fmt(opt):
            if opt == CUSTOM_OPTION:
                return format_location_label(current, st.session_state.lang)
            return format_location_label(opt, st.session_state.lang)

        if is_custom:
            index = 0
        else:
            index = room_options.index(current) if current in room_options else fallback_index

        chosen = st.selectbox(label, options=options, format_func=fmt, index=index)
        if chosen != CUSTOM_OPTION:
            st.session_state[session_key] = chosen

    with st.expander(f"⚙️ {t['nav_controls']}", expanded=True):
        col_start, col_dest = st.columns(2)
        with col_start:
            location_selectbox(t["start_loc"], "selected_start", 0)
        with col_dest:
            location_selectbox(t["dest_loc"], "selected_dest", len(room_options) - 1)

        # ---- Intermediate stops (manual rooms or clicked points) ----
        if st.session_state.waypoints:
            st.markdown(t["intermediate_stops"])

            def move_waypoint(idx, direction):
                target_idx = idx - 1 if direction == "up" else idx + 1
                wps = st.session_state.waypoints
                wps[idx], wps[target_idx] = wps[target_idx], wps[idx]

            def remove_waypoint(idx):
                st.session_state.waypoints.pop(idx)

            def update_waypoint_value(wp_obj_id, widget_key):
                val = st.session_state[widget_key]
                for item in st.session_state.waypoints:
                    if item["id"] == wp_obj_id:
                        item["value"] = val
                        break

            for idx, wp_obj in enumerate(st.session_state.waypoints):
                wp_id = wp_obj["id"]
                wp_val = wp_obj["value"]
                widget_key = f"waypoint_select_obj_{wp_id}"

                wp_col1, wp_col_up, wp_col_dn, wp_col_del = st.columns([0.65, 0.11, 0.11, 0.13])

                with wp_col1:
                    if isinstance(wp_val, tuple):
                        st.markdown(f"**{t['stop_lbl'].format(idx=idx + 1)}**")
                        st.markdown(f"`{format_location_label(wp_val, st.session_state.lang)}`")
                    else:
                        st.selectbox(
                            t["stop_lbl"].format(idx=idx + 1),
                            options=room_options,
                            index=room_options.index(wp_val) if wp_val in room_options else 0,
                            format_func=lambda r_id: format_location_label(r_id, st.session_state.lang),
                            key=widget_key,
                            on_change=update_waypoint_value,
                            args=(wp_id, widget_key),
                        )

                with wp_col_up:
                    st.write("")
                    st.write("")
                    st.button("⬆️", key=f"move_up_wp_{wp_id}", disabled=(idx == 0),
                              on_click=move_waypoint, args=(idx, "up"))

                with wp_col_dn:
                    st.write("")
                    st.write("")
                    st.button("⬇️", key=f"move_dn_wp_{wp_id}", disabled=(idx == len(st.session_state.waypoints) - 1),
                              on_click=move_waypoint, args=(idx, "down"))

                with wp_col_del:
                    st.write("")
                    st.write("")
                    st.button("❌", key=f"remove_wp_{wp_id}", on_click=remove_waypoint, args=(idx,))

        if st.button(t["btn_add_stop_manual"], type="primary", key="add_waypoint"):
            default_wp = room_options[1] if len(room_options) > 1 else room_options[0]
            st.session_state.waypoint_counter += 1
            st.session_state.waypoints.append({"id": st.session_state.waypoint_counter, "value": default_wp})
            st.rerun()

        st.markdown("---")

        route_pref = st.radio(t["route_type"], options=[t["shortest"], t["accessible"]], horizontal=True)
        accessible_flag = (route_pref == t["accessible"])

        extracted_waypoints = [wp["value"] for wp in st.session_state.waypoints]

        # While picking on the map the destination isn't chosen yet, so the
        # route ends at the last clicked point instead of a stale destination.
        if st.session_state.map_pick_mode:
            raw_sequence = [st.session_state.selected_start] + extracted_waypoints
        else:
            raw_sequence = [st.session_state.selected_start] + extracted_waypoints + [st.session_state.selected_dest]

        route_display_str = " ➔ ".join(f"`{format_location_label(loc, st.session_state.lang)}`" for loc in raw_sequence)
        st.markdown(
            f"""
            <div style="background-color: #E91E63; color: #FFFFFF; padding: 12px 16px; border-radius: 8px;
                        font-size: 0.95rem; margin-top: 10px; margin-bottom: 10px;">
                <strong>{t['current_route_lbl']}:</strong> {route_display_str}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ---- Dynamic point injection & routing ----
    temp_graph = copy.deepcopy(MULTI_CAD_GRAPH)
    temp_nodes = copy.deepcopy(MULTI_CAD_NODES)
    full_route_sequence = resolve_all_route_points(raw_sequence, 0, temp_graph, temp_nodes)

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

    # Only the start has been picked so far: show just the start marker
    if len(full_route_sequence) == 1:
        full_path = [full_route_sequence[0]]

    path = [] if route_failed else full_path

    if st.session_state.map_pick_mode:
        stop_ids = full_route_sequence[1:]
    else:
        stop_ids = full_route_sequence[1:-1]

    # ---- View mode and interactive-pick controls ----
    view_type = st.radio(t["view_mode"], options=[t["view_2d"], t["view_3d"]], horizontal=True)
    show_doors = st.checkbox(t["show_doors"], value=True)

    col_btn_pick, col_btn_clear = st.columns([0.7, 0.3])
    with col_btn_pick:
        if not st.session_state.map_pick_mode:
            if st.button(t["btn_interactive_pick"], use_container_width=True, type="primary"):
                st.session_state.map_pick_mode = True
                st.session_state.map_pick_step = "START"
                st.rerun()
        else:
            if st.button(t["btn_cancel_interactive"], use_container_width=True):
                st.session_state.map_pick_mode = False
                st.session_state.map_pick_step = "START"
                st.rerun()

    with col_btn_clear:
        if st.button(t["btn_reset_all"], use_container_width=True):
            st.session_state.waypoints = []
            st.session_state.map_pick_mode = False
            st.session_state.map_pick_step = "START"
            st.session_state.selected_start = "A_L0_Entrance"
            st.session_state.selected_dest = "A_L0_Lobby"
            st.rerun()

    if st.session_state.map_pick_mode:
        curr_start_label = format_location_label(st.session_state.selected_start, st.session_state.lang)
        curr_dest_label = format_location_label(st.session_state.selected_dest, st.session_state.lang)

        if st.session_state.map_pick_step == "START":
            col_msg, col_skip = st.columns([0.72, 0.28])
            with col_msg:
                st.info(f"{t['pick_step_1']} ({t['lbl_current']}: **{curr_start_label}**)")
            with col_skip:
                if st.button(t["btn_keep_start"], use_container_width=True):
                    st.session_state.map_pick_step = "WAYPOINT"
                    st.rerun()

        elif st.session_state.map_pick_step == "WAYPOINT":
            col_msg, col_done = st.columns([0.72, 0.28])
            with col_msg:
                st.warning(t["pick_step_2"])
            with col_done:
                if st.button(t["btn_done_adding_stops"], type="primary", use_container_width=True):
                    st.session_state.map_pick_step = "DEST"
                    st.rerun()

        elif st.session_state.map_pick_step == "DEST":
            col_msg, col_skip = st.columns([0.72, 0.28])
            with col_msg:
                st.success(f"{t['pick_step_3']} ({t['lbl_current']}: **{curr_dest_label}**)")
            with col_skip:
                if st.button(t["btn_keep_dest"], use_container_width=True):
                    st.session_state.map_pick_mode = False
                    st.session_state.map_pick_step = "START"
                    st.rerun()

        if view_type == t["view_3d"]:
            st.info(t["pick_3d_notice"])

    # ---- Render the selected map view ----
    if view_type == t["view_2d"]:
        floor_select = st.selectbox(
            t["active_floor"],
            options=[0, 1, 2, 3],
            format_func=lambda x: get_translated_floor_name(x, lang=st.session_state.lang)
        )

        folium_map = render_2d_folium_view(
            floor_select,
            route_path=path,
            node_coords_dict=temp_nodes,
            current_lang=st.session_state.lang,
            stop_ids=stop_ids,
            show_dest=not st.session_state.map_pick_mode,
            show_doors=show_doors,
        )
        map_data = st_folium(folium_map, height=550, width=1000, key="interactive_folium_map", returned_objects=["last_clicked"])

        if map_data and map_data.get("last_clicked"):
            click_lat = map_data["last_clicked"]["lat"]
            click_lng = map_data["last_clicked"]["lng"]
            click_sig = (click_lat, click_lng)

            if click_sig != st.session_state.last_processed_click:
                st.session_state.last_processed_click = click_sig
                raw_point = (click_lng, click_lat, floor_select)

                if st.session_state.map_pick_mode:
                    if st.session_state.map_pick_step == "START":
                        st.session_state.selected_start = raw_point
                        st.session_state.waypoints = []
                        st.session_state.map_pick_step = "WAYPOINT"
                        st.rerun()
                    elif st.session_state.map_pick_step == "WAYPOINT":
                        st.session_state.waypoint_counter += 1
                        st.session_state.waypoints.append({"id": st.session_state.waypoint_counter, "value": raw_point})
                        st.rerun()
                    elif st.session_state.map_pick_step == "DEST":
                        st.session_state.selected_dest = raw_point
                        st.session_state.map_pick_mode = False
                        st.session_state.map_pick_step = "START"
                        st.rerun()
                else:
                    st.session_state.selected_dest = raw_point
                    st.rerun()
    else:
        fig_3d = render_3d_isometric_view(route_path=path, node_coords=temp_nodes, current_lang=st.session_state.lang, show_doors=show_doors)
        st.plotly_chart(fig_3d, use_container_width=True)

# ------------------------------------------------------------------------------
# Directions Tab
# ------------------------------------------------------------------------------
with tab_dir:
    st.subheader(t["route_summary"])

    if path and len(path) > 1:
        summary = compute_route_summary(path, temp_nodes)
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric(t["total_dist"], f"{summary['total_distance']} m")
        m_col2.metric(t["floors_crossed"], summary["floors_crossed"])
        m_col3.metric(t["total_steps"], summary["steps"])

        st.markdown("---")
        st.subheader(t["turn_by_turn"])

        detailed_steps = generate_detailed_directions(path, temp_nodes, lang=st.session_state.lang)
        render_direction_steps(detailed_steps, t["step_lbl"])
    else:
        st.warning(t["no_route"])

# ------------------------------------------------------------------------------
# Smart Parking Tab
# ------------------------------------------------------------------------------
with tab_park:
    st.subheader(t["parking_sec"])

    curr_lang = st.session_state.lang
    availability_map = {slot_id: details["occupied"] for slot_id, details in PARKING_SLOTS.items()}

    assigned_slot, entry_path, exit_path = find_nearest_available_parking(
        "P_L3_Driveway_Entrance", MULTI_CAD_GRAPH, MULTI_CAD_NODES,
        availability_map=availability_map, accessible_only=accessible_flag
    )

    if assigned_slot:
        slot_icon = get_location_icon(assigned_slot)
        st.success(f"{t['nearest_spot_found']}: `{slot_icon} {assigned_slot}` ({t['rooftop_lot']})")

        tab_entry, tab_exit = st.tabs([t["tab_nav_drive_to_spot"], t["tab_nav_spot_to_exit"]])

        with tab_entry:
            st.markdown(f"### {t['header_driving_to_spot']}")
            entry_map = render_rooftop_folium_map(
                assigned_slot=assigned_slot, route_path=entry_path, current_lang=curr_lang, route_color="#2563EB"
            )
            st_folium(entry_map, height=450, width=900, key="park_entry_map", returned_objects=[])

            if entry_path:
                entry_summary = compute_route_summary(entry_path, MULTI_CAD_NODES)
                st.markdown("---")
                st.subheader(t["parking_route_summary"])

                p_col1, p_col2, p_col3 = st.columns(3)
                p_col1.metric(t["dist_to_spot"], f"{entry_summary['total_distance']} m")
                p_col2.metric(t["floors_to_ascend"], entry_summary["floors_crossed"])
                p_col3.metric(t["total_steps"], entry_summary["steps"])

                st.markdown("---")
                st.subheader(t["parking_turn_by_turn"])
                entry_steps = generate_detailed_directions(entry_path, MULTI_CAD_NODES, lang=curr_lang)
                render_direction_steps(entry_steps, t["step_lbl"])

        with tab_exit:
            st.markdown(f"### {t['header_leaving_spot']}")
            exit_map = render_rooftop_folium_map(
                assigned_slot=assigned_slot, route_path=exit_path, current_lang=curr_lang, route_color="#F97316"
            )
            st_folium(exit_map, height=450, width=900, key="park_exit_map", returned_objects=[])

            if exit_path:
                exit_summary = compute_route_summary(exit_path, MULTI_CAD_NODES)
                st.markdown("---")
                st.subheader(t["parking_route_summary"])

                e_col1, e_col2, e_col3 = st.columns(3)
                e_col1.metric(t["dist_to_spot"], f"{exit_summary['total_distance']} m")
                e_col2.metric(t["floors_to_ascend"], exit_summary["floors_crossed"])
                e_col3.metric(t["total_steps"], exit_summary["steps"])

                st.markdown("---")
                st.subheader(t["parking_turn_by_turn"])
                exit_steps = generate_detailed_directions(exit_path, MULTI_CAD_NODES, lang=curr_lang)
                render_direction_steps(exit_steps, t["step_lbl"])
    else:
        st.error(t["no_parking"])
        empty_map = render_rooftop_folium_map(assigned_slot=None, route_path=[], current_lang=curr_lang)
        st_folium(empty_map, height=450, width=900, key="park_empty_map", returned_objects=[])

# ==============================================================================
# 7. Footer
# ==============================================================================

def render_system_footer():
    st.markdown("---")
    foot_col1, foot_col2, foot_col3 = st.columns(3)
    lang_dict = LOCALIZATION.get(st.session_state.get("lang", "English"), LOCALIZATION["English"])

    with foot_col1:
        st.caption(lang_dict["footer_arch"])
    with foot_col2:
        st.caption(lang_dict["footer_vector"])
    with foot_col3:
        st.caption(lang_dict["footer_lang"])

render_system_footer()
