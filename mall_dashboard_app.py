import streamlit as st
import numpy as np
import plotly.graph_objects as go
import heapq
import math

# ==============================================================================
# 1. Page Configuration & Setup
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
        "home_title": "Welcome to the Smart Mall Navigation System",
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
        "pick_step_1": "👇 *Step 1:* Click any room on the map below to set as *Start Location*.",
        "pick_step_2": "👇 *Step 2:* Click any room on the map to add *Intermediate Stops* (or click button below when ready for Destination).",
        "pick_step_3": "👇 *Step 3:* Click any room on the map to set as *Destination*.",
        "btn_done_adding_stops": "➡️ Done Adding Stops (Next: Pick Destination)",
        "btn_add_as_stop": "➕ Add as Stop",
        "tab_parking_entry": "🚗 1. Entrance to Parking Spot",
        "tab_parking_exit": "🚪 2. Parking Spot to Exit",
        "drive_to_spot_title": "🚗 Driving to Parking Spot",
        "drive_to_exit_title": "🚪 Leaving Parking Spot to Driveway Exit",
        "btn_keep_start": "⏭️ Keep Current Start",
        "btn_keep_dest": "⏭️ Keep Current Destination",
        "lbl_current": "Current",
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
        "home_title": "欢迎使用智能商场导航与停车系统",
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
        "pick_step_1": "👇 *步骤 1：* 点击下方地图上的任意地点设为 *起点位置*。",
        "pick_step_2": "👇 *步骤 2：* 点击地图上的房间添加 *途经点*（若已添加完毕，请点击下方按钮选择终点）。",
        "pick_step_3": "👇 *步骤 3：* 点击地图上的任意房间设为 *终点位置*。",
        "btn_done_adding_stops": "➡️ 完成添加途经点 (下一步: 选择终点)",
        "btn_add_as_stop": "➕ 添加为途经点",
        "tab_parking_entry": "🚗 1. 入口至停车位",
        "tab_parking_exit": "🚪 2. 停车位至出口",
        "drive_to_spot_title": "🚗 驱动至停车位路线",
        "drive_to_exit_title": "🚪 从停车位前往车道出口",
        "btn_keep_start": "⏭️ 保留当前起点",
        "btn_keep_dest": "⏭️ 保留当前终点",
        "lbl_current": "当前",
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
        "home_title": "Selamat Datang ke Sistem Navigasi Pusat Beli-Belah Smart",
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
        "pick_step_1": "👇 *Langkah 1:* Klik mana-mana bilik pada peta di bawah untuk tetapkan *Lokasi Permulaan*.",
        "pick_step_2": "👇 *Langkah 2:* Klik bilik pada peta untuk tambah *Hentian Antara* (atau klik butang di bawah apabila sedia untuk Destinasi).",
        "pick_step_3": "👇 *Langkah 3:* Klik mana-mana bilik pada peta untuk tetapkan *Destinasi*.",
        "btn_done_adding_stops": "➡️ Selesai Menambah Hentian (Seterusnya: Pilih Destinasi)",
        "btn_add_as_stop": "➕ Tambah sebagai Hentian",
        "tab_parking_entry": "🚗 1. Pintu Masuk ke Ruang Letak Kereta",
        "tab_parking_exit": "🚪 2. Ruang Letak Kereta ke Pintu Keluar",
        "drive_to_spot_title": "🚗 Memandu ke Ruang Letak Kereta",
        "drive_to_exit_title": "🚪 Meninggalkan Ruang Letak Kereta ke Pintu Keluar",
        "btn_keep_start": "⏭️ Kekalkan Permulaan Semasa",
        "btn_keep_dest": "⏭️ Kekalkan Destinasi Semasa",
        "lbl_current": "Semasa",
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
        0: "底层 [GF]",
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
        "P_L3_Escalator": "🪜Escalator (R)",
        "P_L3_Driveway_Entrance": "🚪Entrance Ramp (R)",
        "P_L3_Driveway_Exit": "🚪Exit Ramp (R)",
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
        "P_L3_Escalator": "🪜楼顶自动扶梯",
        "P_L3_Driveway_Entrance": "🚪楼顶入口",
        "P_L3_Driveway_Exit": "🚪楼顶出口",
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
        "P_L3_Escalator": "🪜Eskalator (Bumbung)",
        "P_L3_Driveway_Entrance": "🚪Laluan Masuk Kenderaan (Bumbung)",
        "P_L3_Driveway_Exit": "🚪Laluan Keluar Kenderaan (Bumbung)",
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

# Session State Initialization
if "lang" not in st.session_state:
    st.session_state.lang = "English"
if "selected_start" not in st.session_state:
    st.session_state.selected_start = "A_L0_Entrance"
if "selected_dest" not in st.session_state:
    st.session_state.selected_dest = "A_L0_Lobby"
if "assigned_parking" not in st.session_state:
    st.session_state.assigned_parking = None
if "entry_path" not in st.session_state:
    st.session_state.entry_path = []
if "exit_path" not in st.session_state:
    st.session_state.exit_path = []
if "clicked_location" not in st.session_state:
    st.session_state.clicked_location = None
if "stops" not in st.session_state:
    st.session_state.stops = []
if "pick_mode" not in st.session_state:
    st.session_state.pick_mode = False
if "pick_step" not in st.session_state:
    st.session_state.pick_step = 1

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
    "Mega Supermarket": {
        "z": 0,
        "coords": [(-30, 20), (30, 20), (30, 44), (-30, 44)],
        "color": "#98FB98"
    },
    "A_L0_Lobby": {
        "z": 0,
        "coords": [(-30, -4), (30, -4), (30, 20), (-30, 20)],
        "color": "#B0C4DE"
    },
    "Fashion Hub": {
        "z": 0,
        "coords": [(-30, -28), (30, -28), (30, -4), (-30, -4)],
        "color": "#E6E6FA"
    },
    "A_L0_Info": {
        "z": 0,
        "coords": [(-50, 20), (-30, 20), (-30, 44), (-50, 44)],
        "color": "#ADD8E6"
    },
    "A_L0_Entrance": {
        "z": 0,
        "coords": [(-50, -4), (-30, -4), (-30, 20), (-50, 20)],
        "color": "#708090"
    },
    "A_L0_Restroom": {
        "z": 0,
        "coords": [(30, 20), (50, 20), (50, 44), (30, 44)],
        "color": "#E0FFFF"
    },
    "A_L0_Elevator": {
        "z": 0,
        "coords": [(30, 8), (50, 8), (50, 20), (30, 20)],
        "color": "#FFD700"
    },
    "A_L0_Escalator": {
        "z": 0,
        "coords": [(30, -4), (50, -4), (50, 8), (30, 8)],
        "color": "#FFA07A"
    },
    "A_L0_Stairs": {
        "z": 0,
        "coords": [(30, -28), (50, -28), (50, -4), (30, -4)],
        "color": "#FF8C00"
    },

    # 1st floor
    "Jewel Box": {
        "z": 1,
        "coords": [(-30, 20), (30, 20), (30, 44), (-30, 44)],
        "color": "#D8BFD8"
    },
    "A_L1_Hallway": {
        "z": 1,
        "coords": [(-30, -4), (30, -4), (30, 20), (-30, 20)],
        "color": "#87CEFA"
    },
    "Book Nook": {
        "z": 1,
        "coords": [(-30, -28), (0, -28), (0, -4), (-30, -4)],
        "color": "#F5DEB3"
    },
    "Tech Gadgets": {
        "z": 1,
        "coords": [(0, -28), (30, -28), (30, -4), (0, -4)],
        "color": "#9370DB"
    },
    "A_L1_Restroom": {
        "z": 1,
        "coords": [(30, 20), (50, 20), (50, 44), (30, 44)],
        "color": "#E0FFFF"
    },
    "A_L1_Elevator": {
        "z": 1,
        "coords": [(30, 8), (50, 8), (50, 20), (30, 20)],
        "color": "#FFD700"
    },
    "A_L1_Escalator": {
        "z": 1,
        "coords": [(30, -4), (50, -4), (50, 8), (30, 8)],
        "color": "#FFA07A"
    },
    "A_L1_Stairs": {
        "z": 1,
        "coords": [(30, -28), (50, -28), (50, -4), (30, -4)],
        "color": "#FF8C00"
    },

    # 2nd floor
    "Cineplex Theater": {
        "z": 2,
        "coords": [(-30, 20), (30, 20), (30, 44), (-30, 44)],
        "color": "#CD5C5C"
    },
    "VR World & Arcade": {
        "z": 2,
        "coords": [(-50, -4), (-30, -4), (-30, 20), (-50, 20)],
        "color": "#FF69B4"
    },
    "B_L2_Corridor": {
        "z": 2,
        "coords": [(-30, -4), (30, -4), (30, 20), (-30, 20)],
        "color": "#5F9EA0"
    },
    "Sky Food Court": {
        "z": 2,
        "coords": [(-30, -28), (0, -28), (0, -4), (-30, -4)],
        "color": "#FF7F50"
    },
    "Gourmet Bites": {
        "z": 2,
        "coords": [(0, -28), (30, -28), (30, -4), (0, -4)],
        "color": "#F4A460"
    },
    "B_L2_Restroom": {
        "z": 2,
        "coords": [(30, 20), (50, 20), (50, 44), (30, 44)],
        "color": "#E0FFFF"
    },
    "B_L2_Elevator": {
        "z": 2,
        "coords": [(30, 8), (50, 8), (50, 20), (30, 20)],
        "color": "#FFD700"
    },
    "B_L2_Escalator": {
        "z": 2,
        "coords": [(30, -4), (50, -4), (50, 8), (30, 8)],
        "color": "#FFA07A"
    },
    "B_L2_Stairs": {
        "z": 2,
        "coords": [(30, -28), (50, -28), (50, -4), (30, -4)],
        "color": "#FF8C00"
    },

    # Parking lot
    "P_L3_Aisle_Main": {
        "z": 3,
        "coords": [(-30, -4), (30, -4), (30, 20), (-30, 20)],
        "color": "#A9A9A9"
    },
    "P_L3_Driveway_Entrance": {
        "z": 3,
        "coords": [(-50, -4), (-30, -4), (-30, 8), (-50, 8)],
        "color": "#A9A9A9"
    },
    "P_L3_Driveway_Exit": {
        "z": 3,
        "coords": [(-50, 8), (-30, 8), (-30, 20), (-50, 20)],
        "color": "#708090"  
    },
    "P5": {
        "z": 3,
        "coords": [(-30, 20), (-15, 20), (-15, 44), (-30, 44)],
        "color": "#4682B4"
    },
    "P6": {
        "z": 3,
        "coords": [(-15, 20), (0, 20), (0, 44), (-15, 44)],
        "color": "#4682B4"
    },
    "P7": {
        "z": 3,
        "coords": [(0, 20), (15, 20), (15, 44), (0, 44)],
        "color": "#4682B4"
    },
    "P8": {
        "z": 3,
        "coords": [(15, 20), (30, 20), (30, 44), (15, 44)],
        "color": "#4682B4"
    },
    "P1": {
        "z": 3,
        "coords": [(-30, -28), (-15, -28), (-15, -4), (-30, -4)],
        "color": "#4682B4"
    },
    "P2": {
        "z": 3,
        "coords": [(-15, -28), (0, -28), (0, -4), (-15, -4)],
        "color": "#4682B4"
    },
    "P3": {
        "z": 3,
        "coords": [(0, -28), (15, -28), (15, -4), (0, -4)],
        "color": "#4682B4"
    },
    "P4": {
        "z": 3,
        "coords": [(15, -28), (30, -28), (30, -4), (15, -4)],
        "color": "#4682B4"
    },
    "P_L3_Elevator": {
        "z": 3,
        "coords": [(30, 8), (50, 8), (50, 20), (30, 20)],
        "color": "#FFD700"
    },
    "P_L3_Escalator": {
        "z": 3,
        "coords": [(30, -4), (50, -4), (50, 8), (30, 8)],
        "color": "#FFA07A"
    },
    "P_L3_Stairs": {
        "z": 3,
        "coords": [(30, -28), (50, -28), (50, -4), (30, -4)],
        "color": "#FF8C00"
    }
}

MULTI_CAD_NODES = {
    # Ground floor
    "Mega Supermarket": (0.0, 32.0, 0),
    "A_L0_Lobby": (0.0, 8.0, 0),
    "Fashion Hub": (0.0, -16.0, 0),
    "A_L0_Info": (-40.0, 32.0, 0),
    "A_L0_Entrance": (-40.0, 8.0, 0),
    "A_L0_Restroom": (40.0, 32.0, 0),
    "A_L0_Elevator": (40.0, 14.0, 0),
    "A_L0_Escalator": (40.0, 2.0, 0),
    "A_L0_Stairs": (40.0, -16.0, 0),

    # 1st floor
    "Jewel Box": (0.0, 32.0, 1),
    "A_L1_Hallway": (0.0, 8.0, 1),
    "Book Nook": (-15.0, -16.0, 1),
    "Tech Gadgets": (15.0, -16.0, 1),
    "A_L1_Restroom": (40.0, 32.0, 1),
    "A_L1_Elevator": (40.0, 14.0, 1),
    "A_L1_Escalator": (40.0, 2.0, 1),
    "A_L1_Stairs": (40.0, -16.0, 1),

    # 2nd floor
    "Cineplex Theater": (0.0, 32.0, 2),
    "VR World & Arcade": (-40.0, 8.0, 2),
    "B_L2_Corridor": (0.0, 8.0, 2),
    "Sky Food Court": (-15.0, -16.0, 2),
    "Gourmet Bites": (15.0, -16.0, 2),
    "B_L2_Restroom": (40.0, 32.0, 2),
    "B_L2_Elevator": (40.0, 14.0, 2),
    "B_L2_Escalator": (40.0, 2.0, 2),
    "B_L2_Stairs": (40.0, -16.0, 2),

    # Parking lot
    "P_L3_Aisle_Main": (0.0, 8.0, 3),
    "P_L3_Driveway_Entrance": (-40.0, 2.0, 3),  
    "P_L3_Driveway_Exit": (-40.0, 14.0, 3),
    "P1": (-22.5, -16.0, 3),
    "P2": (-7.5, -16.0, 3),
    "P3": (7.5, -16.0, 3),
    "P4": (22.5, -16.0, 3),
    "P5": (-22.5, 32.0, 3),
    "P6": (-7.5, 32.0, 3),
    "P7": (7.5, 32.0, 3),
    "P8": (22.5, 32.0, 3),
    "P_L3_Elevator": (40.0, 14.0, 3),
    "P_L3_Escalator": (40.0, 2.0, 3),
    "P_L3_Stairs": (40.0, -16.0, 3)
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
    "B_L2_Escalator":{"A_L1_Escalator": 12.0, "B_L2_Corridor": 33.0, "P_L3_Escalator": 12.0},
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
        "P_L3_Elevator": 40.0, "P_L3_Stairs": 40.0, 
        "P_L3_Escalator": 35.0, "P_L3_Driveway_Entrance": 25.0, "P_L3_Driveway_Exit": 25.0,
    },
    "P_L3_Driveway_Entrance": {"P_L3_Aisle_Main": 25.0},
    "P_L3_Elevator": {"P_L3_Aisle_Main": 40.0, "B_L2_Elevator": 15.0},
    "P_L3_Stairs":   {"P_L3_Aisle_Main": 40.0, "B_L2_Stairs": 15.0},
    "P_L3_Escalator": {"P_L3_Aisle_Main": 35.0, "B_L2_Escalator": 12.0},
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
        return (-60, 60, -40, 60)

    all_x = [pt[0] for room in floor_rooms for pt in room["coords"]]
    all_y = [pt[1] for room in floor_rooms for pt in room["coords"]]
    padding = 15
    return (min(all_x) - padding, max(all_x) + padding, min(all_y) - padding, max(all_y) + padding)

# Helper translation function
def tr(key):
    lang_dict = LOCALIZATION.get(st.session_state.lang, LOCALIZATION["English"])
    return lang_dict.get(key, key)

def get_poi_name(node_id):
    poi_dict = POI_TRANSLATIONS.get(st.session_state.lang, POI_TRANSLATIONS["English"])
    return poi_dict.get(node_id, node_id)

# ==============================================================================
# 3. Pathfinding Core Algorithms
# ==============================================================================
def find_shortest_path(start_node, dest_node, accessible_only=False):
    if start_node not in MULTI_CAD_GRAPH or dest_node not in MULTI_CAD_GRAPH:
        return None, 0.0

    distances = {node: float('inf') for node in MULTI_CAD_GRAPH}
    previous = {node: None for node in MULTI_CAD_GRAPH}
    distances[start_node] = 0.0
    
    pq = [(0.0, start_node)]
    
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        
        if current_dist > distances[current_node]:
            continue
            
        if current_node == dest_node:
            break

        for neighbor, weight in MULTI_CAD_GRAPH[current_node].items():
            # Check for accessibility restriction (Elevators only across floors)
            if accessible_only:
                if ("Stairs" in current_node and "Stairs" in neighbor) or \
                   ("Escalator" in current_node and "Escalator" in neighbor):
                    continue

            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    if distances[dest_node] == float('inf'):
        return None, 0.0

    path = []
    curr = dest_node
    while curr:
        path.append(curr)
        curr = previous[curr]
    path.reverse()
    
    return path, distances[dest_node]

def get_multi_stop_route(start, stops, destination, accessible_only=False):
    full_route = [start]
    total_dist = 0.0
    waypoints = [start] + [s for s in stops if s] + [destination]
    
    for i in range(len(waypoints) - 1):
        segment, seg_dist = find_shortest_path(waypoints[i], waypoints[i+1], accessible_only)
        if not segment:
            return None, 0.0
        full_route.extend(segment[1:])
        total_dist += seg_dist

    return full_route, total_dist

def calculate_bearing(pt1, pt2):
    dx = pt2[0] - pt1[0]
    dy = pt2[1] - pt1[1]
    angle = math.degrees(math.atan2(dy, dx))
    return (angle + 360) % 360

def generate_step_by_step_directions(path):
    if not path or len(path) < 2:
        return []

    directions = []
    lang = st.session_state.lang

    for i in range(len(path) - 1):
        curr_node = path[i]
        next_node = path[i+1]
        
        curr_name = get_poi_name(curr_node)
        next_name = get_poi_name(next_node)
        
        curr_pos = MULTI_CAD_NODES[curr_node]
        next_pos = MULTI_CAD_NODES[next_node]
        
        # Check floor change
        if curr_pos[2] != next_pos[2]:
            from_fl = get_translated_floor_name(curr_pos[2], lang)
            to_fl = get_translated_floor_name(next_pos[2], lang)
            
            if "Elevator" in curr_node:
                instruction = f" Take the elevator from **{from_fl}** to **{to_fl}**."
            elif "Escalator" in curr_node:
                instruction = f" Take the escalator from **{from_fl}** to **{to_fl}**."
            else:
                instruction = f" Take the stairs from **{from_fl}** to **{to_fl}**."
        else:
            dist = math.hypot(next_pos[0] - curr_pos[0], next_pos[1] - curr_pos[1])
            if dist == 0:
                dist = MULTI_CAD_GRAPH.get(curr_node, {}).get(next_node, 10.0)
                
            bearing = calculate_bearing(curr_pos, next_pos)
            
            if 45 <= bearing < 135:
                heading = "North" if lang == "English" else ("北" if lang == "Simplified Chinese" else "Utara")
            elif 135 <= bearing < 225:
                heading = "West" if lang == "English" else ("西" if lang == "Simplified Chinese" else "Barat")
            elif 225 <= bearing < 315:
                heading = "South" if lang == "English" else ("南" if lang == "Simplified Chinese" else "Selatan")
            else:
                heading = "East" if lang == "English" else ("东" if lang == "Simplified Chinese" else "Timur")
                
            instruction = f" Head {heading} from **{curr_name}** toward **{next_name}** (~{dist:.1f} m)."

        directions.append({"step": i + 1, "text": instruction, "from": curr_node, "to": next_node})

    return directions

# ==============================================================================
# 4. Visualization Utilities (Plotly Maps)
# ==============================================================================

def create_2d_floor_map(floor_z, route=None, interactive=False):
    fig = go.Figure()
    
    # Render Room Polygons
    for room_id, info in ROOM_POLYGONS.items():
        if info["z"] == floor_z:
            x_coords = [pt[0] for pt in info["coords"]] + [info["coords"][0][0]]
            y_coords = [pt[1] for pt in info["coords"]] + [info["coords"][0][1]]
            
            display_name = get_poi_name(room_id)
            
            fig.add_trace(go.Scatter(
                x=x_coords, y=y_coords,
                fill="toself",
                fillcolor=info["color"],
                line=dict(color="#333333", width=2),
                name=display_name,
                hoverinfo="text",
                hovertext=f"<b>{display_name}</b>",
                customdata=[room_id] * len(x_coords),
                showlegend=False
            ))

            # Room Title Text
            cx = sum([pt[0] for pt in info["coords"]]) / len(info["coords"])
            cy = sum([pt[1] for pt in info["coords"]]) / len(info["coords"])
            icon = get_location_icon(room_id)
            
            fig.add_trace(go.Scatter(
                x=[cx], y=[cy],
                mode="text",
                text=[f"{icon}<br><b>{display_name}</b>"],
                textposition="middle center",
                hoverinfo="none",
                showlegend=False
            ))

    # Render Route on Active Floor
    if route:
        floor_route = [node for node in route if MULTI_CAD_NODES[node][2] == floor_z]
        if len(floor_route) >= 2:
            rx = [MULTI_CAD_NODES[node][0] for node in floor_route]
            ry = [MULTI_CAD_NODES[node][1] for node in floor_route]
            
            fig.add_trace(go.Scatter(
                x=rx, y=ry,
                mode="lines+markers",
                line=dict(color="#FF0000", width=5, dash="dash"),
                marker=dict(size=10, color="#FF0000"),
                name="Route Path",
                showlegend=False
            ))

    # Render Active Selection Markers
    if st.session_state.selected_start in MULTI_CAD_NODES:
        sp = MULTI_CAD_NODES[st.session_state.selected_start]
        if sp[2] == floor_z:
            fig.add_trace(go.Scatter(
                x=[sp[0]], y=[sp[1]],
                mode="markers+text",
                marker=dict(size=18, color="green", symbol="triangle-up"),
                text=[f"🚩 {tr('marker_start')}"],
                textposition="top center",
                showlegend=False
            ))

    if st.session_state.selected_dest in MULTI_CAD_NODES:
        dp = MULTI_CAD_NODES[st.session_state.selected_dest]
        if dp[2] == floor_z:
            fig.add_trace(go.Scatter(
                x=[dp[0]], y=[dp[1]],
                mode="markers+text",
                marker=dict(size=18, color="red", symbol="square"),
                text=[f"🏁 {tr('marker_dest')}"],
                textposition="top center",
                showlegend=False
            ))

    min_x, max_x, min_y, max_y = get_floor_bounds(floor_z)
    
    fig.update_layout(
        xaxis=dict(range=[min_x, max_x], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[min_y, max_y], showgrid=False, zeroline=False, showticklabels=False, scaleanchor="x", scaleratio=1),
        margin=dict(l=10, r=10, t=30, b=10),
        height=550,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        clickmode="event+select" if interactive else "none"
    )

    return fig

def create_3d_isometric_map(route=None):
    fig = go.Figure()
    
    # Draw floor planes
    for floor_z in range(4):
        z_offset = floor_z * 40.0
        
        # Floor Plate outlines
        for room_id, info in ROOM_POLYGONS.items():
            if info["z"] == floor_z:
                x_coords = [pt[0] for pt in info["coords"]] + [info["coords"][0][0]]
                y_coords = [pt[1] for pt in info["coords"]] + [info["coords"][0][1]]
                z_coords = [z_offset] * len(x_coords)
                
                display_name = get_poi_name(room_id)
                
                fig.add_trace(go.Scatter3d(
                    x=x_coords, y=y_coords, z=z_coords,
                    mode="lines",
                    line=dict(color="#555555", width=3),
                    hoverinfo="text",
                    hovertext=f"<b>{display_name}</b> ({get_translated_floor_name(floor_z, st.session_state.lang)})",
                    showlegend=False
                ))

    # Draw Route in 3D Space
    if route and len(route) >= 2:
        rx = [MULTI_CAD_NODES[node][0] for node in route]
        ry = [MULTI_CAD_NODES[node][1] for node in route]
        rz = [MULTI_CAD_NODES[node][2] * 40.0 for node in route]
        
        fig.add_trace(go.Scatter3d(
            x=rx, y=ry, z=rz,
            mode="lines+markers",
            line=dict(color="#FF0000", width=8),
            marker=dict(size=5, color="#8B0000"),
            name="3D Path",
            showlegend=False
        ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(showbackground=False, showticklabels=False, title=""),
            yaxis=dict(showbackground=False, showticklabels=False, title=""),
            zaxis=dict(showbackground=False, showticklabels=False, title=""),
            camera=dict(
                eye=dict(x=1.6, y=-1.6, z=1.2)
            )
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=650
    )
    
    return fig

# ==============================================================================
# 5. Sidebar & Configuration Controls
# ==============================================================================

# Sidebar Header & Language Picker
st.sidebar.title(tr("config_header"))

curr_lang = st.session_state.lang
lang_options = list(LANG_OPTION_LABELS[curr_lang].keys())
selected_lang_label = st.sidebar.selectbox(
    tr("select_lang"),
    options=lang_options,
    format_func=lambda x: LANG_OPTION_LABELS[curr_lang][x]
)

if selected_lang_label != st.session_state.lang:
    st.session_state.lang = selected_lang_label
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader(tr("nav_controls"))

# POI Selection Dropdown Options
all_pois = list(MULTI_CAD_NODES.keys())
poi_options_formatted = {node: get_poi_name(node) for node in all_pois}

# Route Start and End controls
st.session_state.selected_start = st.sidebar.selectbox(
    tr("start_loc"),
    options=all_pois,
    index=all_pois.index(st.session_state.selected_start) if st.session_state.selected_start in all_pois else 0,
    format_func=lambda x: poi_options_formatted[x]
)

# Manage Intermediate Stops
st.sidebar.markdown(f"**{tr('intermediate_stops')}**")
stops_to_remove = []
for idx, stop_node in enumerate(st.session_state.stops):
    col_stop, col_del = st.sidebar.columns([4, 1])
    with col_stop:
        new_stop = st.selectbox(
            tr("stop_lbl").format(idx=idx+1),
            options=all_pois,
            index=all_pois.index(stop_node) if stop_node in all_pois else 0,
            format_func=lambda x: poi_options_formatted[x],
            key=f"stop_select_{idx}"
        )
        st.session_state.stops[idx] = new_stop
    with col_del:
        if st.button("❌", key=f"del_stop_{idx}"):
            stops_to_remove.append(idx)

for idx in reversed(stops_to_remove):
    st.session_state.stops.pop(idx)
    st.rerun()

if st.sidebar.button(tr("btn_add_stop_manual")):
    st.session_state.stops.append(all_pois[0])
    st.rerun()

st.session_state.selected_dest = st.sidebar.selectbox(
    tr("dest_loc"),
    options=all_pois,
    index=all_pois.index(st.session_state.selected_dest) if st.session_state.selected_dest in all_pois else 1,
    format_func=lambda x: poi_options_formatted[x]
)

# Route Preferences
accessible_pref = st.sidebar.checkbox(tr("accessible"), value=False)
route_type = "accessible" if accessible_pref else "shortest"

# Display Mode and Floor controls
view_mode = st.sidebar.radio(tr("view_mode"), [tr("view_2d"), tr("view_3d")])

active_floor_index = st.sidebar.slider(
    tr("active_floor"),
    min_value=0, max_value=3,
    value=MULTI_CAD_NODES[st.session_state.selected_start][2],
    format_func=lambda x: get_translated_floor_name(x, st.session_state.lang)
)

st.sidebar.markdown("---")
if st.sidebar.button(tr("btn_reset_all")):
    st.session_state.selected_start = "A_L0_Entrance"
    st.session_state.selected_dest = "A_L0_Lobby"
    st.session_state.stops = []
    st.session_state.assigned_parking = None
    st.session_state.pick_mode = False
    st.rerun()

# ==============================================================================
# 6. Main UI View & Layout
# ==============================================================================

# Title Section
st.title(tr("title"))
st.caption(tr("subtitle"))

# Interactive Picker Mode Alert Banner
if st.session_state.pick_mode:
    st.info(tr(f"pick_step_{st.session_state.pick_step}"))
    col_p1, col_p2 = st.columns([2, 1])
    with col_p1:
        if st.session_state.pick_step == 2 and st.button(tr("btn_done_adding_stops")):
            st.session_state.pick_step = 3
            st.rerun()
    with col_p2:
        if st.button(tr("btn_cancel_interactive")):
            st.session_state.pick_mode = False
            st.rerun()

# Compute Primary Route
route_nodes, total_distance = get_multi_stop_route(
    st.session_state.selected_start,
    st.session_state.stops,
    st.session_state.selected_dest,
    accessible_only=(route_type == "accessible")
)

# Top Metric Summary Cards
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric(tr("poi_metric"), len(MULTI_CAD_NODES))
col_m2.metric(tr("floors_metric"), 4)

avail_spots = sum(1 for slot in PARKING_SLOTS.values() if not slot["occupied"])
col_m3.metric(tr("spots_metric"), len(PARKING_SLOTS))
col_m4.metric(tr("available_metric"), avail_spots)

# Main Navigation Tabs
tab_nav_map, tab_directions, tab_parking = st.tabs([
    tr("tab_nav"), tr("tab_directions"), tr("tab_parking")
])

# ------------------------------------------------------------------------------
# TAB 1: MALL MAP (2D Vector Plan / 3D Isometric View)
# ------------------------------------------------------------------------------
with tab_nav_map:
    map_col, info_col = st.columns([3, 1])
    
    with map_col:
        if not st.session_state.pick_mode:
            if st.button(tr("btn_interactive_pick")):
                st.session_state.pick_mode = True
                st.session_state.pick_step = 1
                st.rerun()

        if view_mode == tr("view_2d"):
            fig_2d = create_2d_floor_map(active_floor_index, route=route_nodes, interactive=True)
            
            # Catch Map Click Events
            event_data = st.plotly_chart(fig_2d, use_container_width=True, on_select="rerun", selection_mode="points")
            
            if event_data and "selection" in event_data and event_data["selection"]["points"]:
                pts = event_data["selection"]["points"]
                if len(pts) > 0 and "customdata" in pts[0]:
                    clicked_node = pts[0]["customdata"][0]
                    
                    if st.session_state.pick_mode:
                        if st.session_state.pick_step == 1:
                            st.session_state.selected_start = clicked_node
                            st.session_state.pick_step = 2
                            st.rerun()
                        elif st.session_state.pick_step == 2:
                            st.session_state.stops.append(clicked_node)
                            st.rerun()
                        elif st.session_state.pick_step == 3:
                            st.session_state.selected_dest = clicked_node
                            st.session_state.pick_mode = False
                            st.rerun()
                    else:
                        st.session_state.clicked_location = clicked_node

        else: # 3D View
            fig_3d = create_3d_isometric_map(route=route_nodes)
            st.plotly_chart(fig_3d, use_container_width=True)

    with info_col:
        st.subheader(tr("route_summary"))
        
        if route_nodes:
            st.write(f"**{tr('from_lbl').capitalize()}:** {get_poi_name(st.session_state.selected_start)}")
            if st.session_state.stops:
                st.write(f"**{tr('intermediate_stops')}:** {len(st.session_state.stops)}")
            st.write(f"**{tr('dest_loc')}:** {get_poi_name(st.session_state.selected_dest)}")
            st.write(f"**{tr('total_dist')}:** {total_distance:.1f} meters")
            
            # Calculate floor changes
            floors_visited = set(MULTI_CAD_NODES[n][2] for n in route_nodes)
            st.write(f"**{tr('floors_crossed')}:** {len(floors_visited)}")
            st.write(f"**{tr('total_steps')}:** {len(route_nodes) - 1}")
        else:
            st.error(tr("no_route"))

        # Render Map Click Selection Dialog
        if st.session_state.clicked_location:
            st.markdown("---")
            loc_name = get_poi_name(st.session_state.clicked_location)
            st.markdown(tr("selected_on_map").format(location=loc_name))
            
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button(tr("btn_set_start")):
                    st.session_state.selected_start = st.session_state.clicked_location
                    st.session_state.clicked_location = None
                    st.rerun()
            with btn_col2:
                if st.button(tr("btn_set_dest")):
                    st.session_state.selected_dest = st.session_state.clicked_location
                    st.session_state.clicked_location = None
                    st.rerun()
            
            if st.button(tr("btn_add_as_stop")):
                st.session_state.stops.append(st.session_state.clicked_location)
                st.session_state.clicked_location = None
                st.rerun()

            if st.button(tr("btn_cancel")):
                st.session_state.clicked_location = None
                st.rerun()

# ------------------------------------------------------------------------------
# TAB 2: STEP-BY-STEP DIRECTIONS
# ------------------------------------------------------------------------------
with tab_directions:
    st.subheader(tr("turn_by_turn"))
    
    if route_nodes:
        directions = generate_step_by_step_directions(route_nodes)
        for d in directions:
            with st.container():
                st.markdown(f"**{tr('step_lbl')} {d['step']}:** {d['text']}")
                st.markdown("---")
    else:
        st.warning(tr("no_route"))

# ------------------------------------------------------------------------------
# TAB 3: SMART PARKING ALLOCATION
# ------------------------------------------------------------------------------
with tab_parking:
    st.subheader(tr("parking_sec"))
    
    # Auto-assign nearest parking spot if not assigned
    if not st.session_state.assigned_parking:
        avail_parking = [spot for spot, info in PARKING_SLOTS.items() if not info["occupied"]]
        if avail_parking:
            # Pick parking spot closest to Main Driveway Entrance
            entry_node = "P_L3_Driveway_Entrance"
            best_spot = None
            min_d = float('inf')
            for spot in avail_parking:
                _, d = find_shortest_path(entry_node, spot)
                if d < min_d:
                    min_d = d
                    best_spot = spot
            st.session_state.assigned_parking = best_spot

    assigned = st.session_state.assigned_parking
    
    if assigned:
        st.success(f"**{tr('nearest_spot_found')}:** {get_poi_name(assigned)} ({tr('rooftop_lot')})")
        
        parking_sub_tab1, parking_sub_tab2 = st.tabs([
            tr("tab_parking_entry"), tr("tab_parking_exit")
        ])

        with parking_sub_tab1:
            st.markdown(f"### {tr('drive_to_spot_title')}")
            entry_path, entry_dist = find_shortest_path("P_L3_Driveway_Entrance", assigned)
            
            if entry_path:
                st.write(f"**{tr('total_dist')}:** {entry_dist:.1f} meters")
                fig_park = create_2d_floor_map(3, route=entry_path)
                st.plotly_chart(fig_park, use_container_width=True)
                
                p_dirs = generate_step_by_step_directions(entry_path)
                st.markdown(f"#### {tr('parking_turn_by_turn')}")
                for pd in p_dirs:
                    st.markdown(f"**{tr('step_lbl')} {pd['step']}:** {pd['text']}")

        with parking_sub_tab2:
            st.markdown(f"### {tr('drive_to_exit_title')}")
            exit_path, exit_dist = find_shortest_path(assigned, "P_L3_Driveway_Exit")
            
            if exit_path:
                st.write(f"**{tr('total_dist')}:** {exit_dist:.1f} meters")
                fig_park_exit = create_2d_floor_map(3, route=exit_path)
                st.plotly_chart(fig_park_exit, use_container_width=True)
                
                pe_dirs = generate_step_by_step_directions(exit_path)
                st.markdown(f"#### {tr('parking_turn_by_turn')}")
                for ped in pe_dirs:
                    st.markdown(f"**{tr('step_lbl')} {ped['step']}:** {ped['text']}")
    else:
        st.error("No parking spots currently available.")
