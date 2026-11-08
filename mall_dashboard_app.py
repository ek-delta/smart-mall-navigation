import math
import heapq
import copy
import functools
import json
import streamlit as st
import streamlit.components.v1 as components
import folium
import plotly.graph_objects as go
from streamlit_folium import st_folium
from folium.plugins import AntPath, PolyLineTextPath
from branca.element import MacroElement
from jinja2 import Template

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
        "view_2d": "2D Plotly Map",
        "view_2d_folium": "2D Folium Map",
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
        "edit_hint": "👆 Click the start, a stop or the destination marker on the map, then click a new location to move it.",
        "editing_start": "✏️ Moving **Start** – click its new location on the map (click the marker again to cancel).",
        "editing_stop": "✏️ Moving **Stop {idx}** – click its new location on the map (click the marker again to cancel).",
        "editing_dest": "✏️ Moving **Destination** – click its new location on the map (click the marker again to cancel).",
        "btn_cancel_edit": "❌ Cancel moving",
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
        "map_nav_hint_folium": "🖱️ Drag to pan · scroll to zoom · click anywhere to choose a point (exact position).",
        "map_nav_hint_parking": "🖱️ Drag to pan · scroll to zoom · double-click to reset the view · use the toolbar's Autoscale button to fit the whole floor.",
        "map_nav_hint": "🖱️ Drag to pan · scroll to zoom · double-click to reset the view · click to choose a point (snaps to the nearest 1 m).",
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
        "view_2d": "2D Plotly 地图",
        "view_2d_folium": "2D Folium 地图",
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
        "edit_hint": "👆 点击地图上的起点、途经点或终点标记，再点击新位置即可移动。",
        "editing_start": "✏️ 正在移动 **起点** – 请在地图上点击新位置（再次点击该标记可取消）。",
        "editing_stop": "✏️ 正在移动 **途经点 {idx}** – 请在地图上点击新位置（再次点击该标记可取消）。",
        "editing_dest": "✏️ 正在移动 **终点** – 请在地图上点击新位置（再次点击该标记可取消）。",
        "btn_cancel_edit": "❌ 取消移动",
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
        "map_nav_hint_folium": "🖱️ 拖动平移 · 滚轮缩放 · 点击地图任意位置选点（精确位置）。",
        "map_nav_hint_parking": "🖱️ 拖动平移 · 滚轮缩放 · 双击重置视图 · 使用工具栏的“自动缩放”按钮适配整层平面图。",
        "map_nav_hint": "🖱️ 拖动平移 · 滚轮缩放 · 双击重置视图 · 点击选点（吸附到最近的 1 米）。",
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
        "view_2d": "Peta Plotly 2D",
        "view_2d_folium": "Peta Folium 2D",
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
        "edit_hint": "👆 Klik penanda permulaan, hentian atau destinasi pada peta, kemudian klik lokasi baharu untuk mengalihkannya.",
        "editing_start": "✏️ Mengalihkan **Permulaan** – klik lokasi baharunya pada peta (klik penanda sekali lagi untuk batal).",
        "editing_stop": "✏️ Mengalihkan **Hentian {idx}** – klik lokasi baharunya pada peta (klik penanda sekali lagi untuk batal).",
        "editing_dest": "✏️ Mengalihkan **Destinasi** – klik lokasi baharunya pada peta (klik penanda sekali lagi untuk batal).",
        "btn_cancel_edit": "❌ Batal alih",
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
        "map_nav_hint_folium": "🖱️ Seret untuk alih · skrol untuk zum · klik di mana-mana untuk pilih titik (kedudukan tepat).",
        "map_nav_hint_parking": "🖱️ Seret untuk alih · skrol untuk zum · klik dua kali untuk set semula paparan · guna butang Autoscale pada bar alat untuk muatkan seluruh tingkat.",
        "map_nav_hint": "🖱️ Seret untuk alih · skrol untuk zum · klik dua kali untuk set semula paparan · klik untuk pilih titik (dipadankan ke 1 m terdekat).",
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
# Main corridor/hub room of each floor (used to name the junction nodes along it)
FLOOR_CORRIDOR = {0: "A_L0_Lobby", 1: "A_L1_Hallway", 2: "B_L2_Corridor", 3: "P_L3_Aisle_Main"}
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
if "last_folium_clicks" not in st.session_state: st.session_state.last_folium_clicks = {}
if "edit_target" not in st.session_state: st.session_state.edit_target = None

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
    "A_L0_Lobby": {"z": 0, "coords": [(-30, -4), (50, -4), (50, 20), (-30, 20)], "color": "#B0C4DE"},
    "Fashion Hub": {"z": 0, "coords": [(-30, -28), (30, -28), (30, -4), (-30, -4)], "color": "#E6E6FA"},
    "A_L0_Info": {"z": 0, "coords": [(-50, 20), (-30, 20), (-30, 44), (-50, 44)], "color": "#ADD8E6"},
    "A_L0_Entrance": {"z": 0, "coords": [(-50, -4), (-30, -4), (-30, 20), (-50, 20)], "color": "#708090"},
    "A_L0_Restroom": {"z": 0, "coords": [(36, 20), (46, 20), (46, 28), (36, 28)], "color": "#E0FFFF"},
    "A_L0_Elevator": {"z": 0, "coords": [(50, 14), (56, 14), (56, 20), (50, 20)], "color": "#FFD700"},
    "A_L0_Escalator": {"z": 0, "coords": [(50, 1), (62, 1), (62, 6), (50, 6)], "color": "#FFA07A"},
    "A_L0_Stairs": {"z": 0, "coords": [(37, -12), (45, -12), (45, -4), (37, -4)], "color": "#FF8C00"},

    "Jewel Box": {"z": 1, "coords": [(-30, 20), (30, 20), (30, 44), (-30, 44)], "color": "#D8BFD8"},
    "A_L1_Hallway": {"z": 1, "coords": [(-30, -4), (50, -4), (50, 20), (-30, 20)], "color": "#87CEFA"},
    "Book Nook": {"z": 1, "coords": [(-30, -28), (0, -28), (0, -4), (-30, -4)], "color": "#F5DEB3"},
    "Tech Gadgets": {"z": 1, "coords": [(0, -28), (30, -28), (30, -4), (0, -4)], "color": "#9370DB"},
    "A_L1_Restroom": {"z": 1, "coords": [(36, 20), (46, 20), (46, 28), (36, 28)], "color": "#E0FFFF"},
    "A_L1_Elevator": {"z": 1, "coords": [(50, 14), (56, 14), (56, 20), (50, 20)], "color": "#FFD700"},
    "A_L1_Escalator": {"z": 1, "coords": [(50, 1), (62, 1), (62, 6), (50, 6)], "color": "#FFA07A"},
    "A_L1_Stairs": {"z": 1, "coords": [(37, -12), (45, -12), (45, -4), (37, -4)], "color": "#FF8C00"},

    "Cineplex Theater": {"z": 2, "coords": [(-30, 20), (30, 20), (30, 44), (-30, 44)], "color": "#CD5C5C"},
    "VR World & Arcade": {"z": 2, "coords": [(-50, -4), (-30, -4), (-30, 20), (-50, 20)], "color": "#FF69B4"},
    "B_L2_Corridor": {"z": 2, "coords": [(-30, -4), (50, -4), (50, 20), (-30, 20)], "color": "#5F9EA0"},
    "Sky Food Court": {"z": 2, "coords": [(-30, -28), (0, -28), (0, -4), (-30, -4)], "color": "#FF7F50"},
    "Gourmet Bites": {"z": 2, "coords": [(0, -28), (30, -28), (30, -4), (0, -4)], "color": "#F4A460"},
    "B_L2_Restroom": {"z": 2, "coords": [(36, 20), (46, 20), (46, 28), (36, 28)], "color": "#E0FFFF"},
    "B_L2_Elevator": {"z": 2, "coords": [(50, 14), (56, 14), (56, 20), (50, 20)], "color": "#FFD700"},
    "B_L2_Escalator": {"z": 2, "coords": [(50, 1), (62, 1), (62, 6), (50, 6)], "color": "#FFA07A"},
    "B_L2_Stairs": {"z": 2, "coords": [(37, -12), (45, -12), (45, -4), (37, -4)], "color": "#FF8C00"},

    "P_L3_Aisle_Main": {"z": 3, "coords": [(-30, -4), (50, -4), (50, 20), (-30, 20)], "color": "#A9A9A9"},
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
    "P_L3_Elevator": {"z": 3, "coords": [(50, 14), (56, 14), (56, 20), (50, 20)], "color": "#FFD700"},
    "P_L3_Escalator": {"z": 3, "coords": [(50, 1), (62, 1), (62, 6), (50, 6)], "color": "#FFA07A"},
    "P_L3_Stairs": {"z": 3, "coords": [(37, -12), (45, -12), (45, -4), (37, -4)], "color": "#FF8C00"}
}

MULTI_CAD_NODES = {
    # Ground Floor
    "A_L0_Entrance": (-40.0, 8.0, 0), "A_L0_Info": (-40.0, 32.0, 0), "A_L0_Lobby": (0.0, 8.0, 0),
    "Fashion Hub": (0.0, -16.0, 0), "Mega Supermarket": (0.0, 32.0, 0), "A_L0_Restroom": (41.0, 24.0, 0),
    "A_L0_Elevator": (53.0, 17.0, 0), "A_L0_Escalator": (56.0, 3.5, 0), "A_L0_Stairs": (41.0, -8.0, 0),
    "H_L0_West": (-20.0, 8.0, 0), "H_L0_East": (20.0, 8.0, 0), "H_L0_North": (0.0, 20.0, 0), "H_L0_South": (0.0, -4.0, 0),

    # 1st Floor
    "A_L1_Hallway": (0.0, 8.0, 1), "Book Nook": (-15.0, -16.0, 1), "Tech Gadgets": (15.0, -16.0, 1),
    "Jewel Box": (0.0, 32.0, 1), "A_L1_Restroom": (41.0, 24.0, 1), "A_L1_Elevator": (53.0, 17.0, 1),
    "A_L1_Escalator": (56.0, 3.5, 1), "A_L1_Stairs": (41.0, -8.0, 1),
    "H_L1_West": (-20.0, 8.0, 1), "H_L1_East": (20.0, 8.0, 1), "H_L1_South_West": (-15.0, -4.0, 1), "H_L1_South_East": (15.0, -4.0, 1),

    # 2nd Floor
    "B_L2_Corridor": (0.0, 8.0, 2), "VR World & Arcade": (-40.0, 8.0, 2), "Cineplex Theater": (0.0, 32.0, 2),
    "Sky Food Court": (-15.0, -16.0, 2), "Gourmet Bites": (15.0, -16.0, 2), "B_L2_Restroom": (41.0, 24.0, 2),
    "B_L2_Elevator": (53.0, 17.0, 2), "B_L2_Escalator": (56.0, 3.5, 2), "B_L2_Stairs": (41.0, -8.0, 2),
    "H_L2_West": (-20.0, 8.0, 2), "H_L2_East": (20.0, 8.0, 2), "H_L2_South_West": (-15.0, -4.0, 2), "H_L2_South_East": (15.0, -4.0, 2),

    # Rooftop Parking
    "P_L3_Aisle_Main": (0.0, 8.0, 3), "P_L3_Driveway_Entrance": (-40.0, 2.0, 3), "P_L3_Driveway_Exit": (-40.0, 14.0, 3),
    "P1": (-22.5, -16.0, 3), "P2": (-7.5, -16.0, 3), "P3": (7.5, -16.0, 3), "P4": (22.5, -16.0, 3),
    "P5": (-22.5, 32.0, 3), "P6": (-7.5, 32.0, 3), "P7": (7.5, 32.0, 3), "P8": (22.5, 32.0, 3),
    "P_L3_Elevator": (53.0, 17.0, 3), "P_L3_Escalator": (56.0, 3.5, 3), "P_L3_Stairs": (41.0, -8.0, 3)
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
# boundary. Each corridor runs on to x=50, so the restrooms and stairwells sit
# alongside it like the stores (doors on the corridor-facing wall). The elevator
# and escalator are at the east end of the corridor; the restroom, stairwell,
# elevator and escalator are all drawn at a realistic (small) size.
# ------------------------------------------------------------------------------
DOORS = {
    # Ground Floor
    "Fashion Hub": (0.0, -4.0, "H_L0_South"),
    "Mega Supermarket": (0.0, 20.0, "H_L0_North"),
    "A_L0_Entrance": (-30.0, 8.0, "H_L0_West"),
    "A_L0_Info": (-40.0, 20.0, "A_L0_Entrance"),
    "A_L0_Elevator": (50.0, 17.0, "H_L0_End"),
    "A_L0_Escalator": (50.0, 3.5, "H_L0_End"),
    "A_L0_Stairs": (41.0, -4.0, "H_L0_End"),
    "A_L0_Restroom": (41.0, 20.0, "H_L0_End"),

    # 1st Floor
    "Jewel Box": (0.0, 20.0, "A_L1_Hallway"),
    "Book Nook": (-15.0, -4.0, "H_L1_South_West"),
    "Tech Gadgets": (15.0, -4.0, "H_L1_South_East"),
    "A_L1_Elevator": (50.0, 17.0, "H_L1_End"),
    "A_L1_Escalator": (50.0, 3.5, "H_L1_End"),
    "A_L1_Stairs": (41.0, -4.0, "H_L1_End"),
    "A_L1_Restroom": (41.0, 20.0, "H_L1_End"),

    # 2nd Floor
    "Cineplex Theater": (0.0, 20.0, "B_L2_Corridor"),
    "VR World & Arcade": (-30.0, 8.0, "H_L2_West"),
    "Sky Food Court": (-15.0, -4.0, "H_L2_South_West"),
    "Gourmet Bites": (15.0, -4.0, "H_L2_South_East"),
    "B_L2_Elevator": (50.0, 17.0, "H_L2_End"),
    "B_L2_Escalator": (50.0, 3.5, "H_L2_End"),
    "B_L2_Stairs": (41.0, -4.0, "H_L2_End"),
    "B_L2_Restroom": (41.0, 20.0, "H_L2_End"),

    # Rooftop Parking
    "P_L3_Driveway_Entrance": (-30.0, 2.0, "P_L3_Aisle_Main"),
    "P_L3_Driveway_Exit": (-30.0, 14.0, "P_L3_Aisle_Main"),
    "P1": (-22.5, -4.0, "P_L3_Aisle_Main"), "P2": (-7.5, -4.0, "P_L3_Aisle_Main"),
    "P3": (7.5, -4.0, "P_L3_Aisle_Main"), "P4": (22.5, -4.0, "P_L3_Aisle_Main"),
    "P5": (-22.5, 20.0, "P_L3_Aisle_Main"), "P6": (-7.5, 20.0, "P_L3_Aisle_Main"),
    "P7": (7.5, 20.0, "P_L3_Aisle_Main"), "P8": (22.5, 20.0, "P_L3_Aisle_Main"),
    "P_L3_Elevator": (50.0, 17.0, "H_L3_End"),
    "P_L3_Escalator": (50.0, 3.5, "H_L3_End"),
    "P_L3_Stairs": (41.0, -4.0, "H_L3_End"),
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

# Hubs at the east end of each corridor (where restroom/stairwell/lift doors meet it)
END_HUBS = {
    "H_L0_End": ((40.0, 8.0, 0), "H_L0_East"),
    "H_L1_End": ((40.0, 8.0, 1), "H_L1_East"),
    "H_L2_End": ((40.0, 8.0, 2), "H_L2_East"),
    "H_L3_End": ((40.0, 8.0, 3), "P_L3_Aisle_Main"),
}
for _hub, (_xyz, _anchor) in END_HUBS.items():
    MULTI_CAD_NODES[_hub] = _xyz
    _d = math.hypot(_xyz[0] - MULTI_CAD_NODES[_anchor][0], _xyz[1] - MULTI_CAD_NODES[_anchor][1])
    MULTI_CAD_GRAPH.setdefault(_hub, {})[_anchor] = _d
    MULTI_CAD_GRAPH.setdefault(_anchor, {})[_hub] = _d

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

            if not graph_copy[temp_id]:
                # Degenerate click (e.g. exactly on a wall): attach to the nearest node on this floor
                same_floor = [n for n, c in nodes_copy.items()
                              if n != temp_id and not n.startswith(DYNAMIC_PREFIX) and int(c[2]) == int(pz)]
                if same_floor:
                    link(min(same_floor, key=lambda n: math.hypot(px - nodes_copy[n][0], py - nodes_copy[n][1])))

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

def room_label(room_id, lang):
    """Room name with exactly one emoji (names usually carry their own; add one only if missing)."""
    name = POI_TRANSLATIONS.get(lang, {}).get(room_id, room_id)
    has_emoji = bool(name) and ord(name[0]) >= 0x1F000
    return name if has_emoji else f"{get_location_icon(room_id)}{name}"

def hex_to_rgba(hex_color, alpha=0.75):
    h = hex_color.lstrip("#")
    return f"rgba({int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)},{alpha})"

CLICK_GRID_STEP = 1.0  # metres between invisible click targets

@functools.lru_cache(maxsize=8)
def build_click_grid(floor_z, step=CLICK_GRID_STEP):
    """Invisible grid of points over the floor plan. Plotly only reports clicks on
    points, so a dense grid lets a click land (almost) anywhere inside the building."""
    rects = []
    for info in ROOM_POLYGONS.values():
        if int(info["z"]) != int(floor_z):
            continue
        xs = [pt[0] for pt in info["coords"]]
        ys = [pt[1] for pt in info["coords"]]
        rects.append((min(xs), max(xs), min(ys), max(ys)))
    if not rects:
        return (), ()

    min_x = min(r[0] for r in rects)
    max_x = max(r[1] for r in rects)
    min_y = min(r[2] for r in rects)
    max_y = max(r[3] for r in rects)

    # Cell centres (offset by half a step) so no point sits exactly on a wall
    gx, gy = [], []
    for i in range(int(round((max_x - min_x) / step))):
        x = min_x + (i + 0.5) * step
        for j in range(int(round((max_y - min_y) / step))):
            y = min_y + (j + 0.5) * step
            if any(r[0] <= x <= r[1] and r[2] <= y <= r[3] for r in rects):
                gx.append(x)
                gy.append(y)
    return tuple(gx), tuple(gy)

ROUTE_FLOW_COLOR = "#FFFEFD"  # looks white; its odd value lets the CSS below find this one line

# Streamlit draws Plotly in the page itself (not an iframe), so this CSS reaches the route's
# overlay line and makes its dashes flow from the start towards the destination.
ROUTE_FLOW_CSS = """
<style>
@keyframes route-flow { from { stroke-dashoffset: 0; } to { stroke-dashoffset: -34; } }
.js-plotly-plot .scatterlayer path.js-line[style*="rgb(255, 254, 253)"],
.js-plotly-plot .scatterlayer path.js-line[style*="rgb(255,254,253)"] {
    stroke-dasharray: 10 24;
    animation: route-flow 0.7s linear infinite;
    pointer-events: none;
}
</style>
"""

# ---- Animated arrows -------------------------------------------------------------
# The arrowheads are split into ARROW_PHASES traces (arrow i goes to trace i % ARROW_PHASES).
# Each trace gets its own fill colour rgb(255, 255, 240+phase), which the CSS keyframes below
# use to find it. Every phase runs the same "light up" keyframes, delayed a bit more than the
# one before, so a bright wave of arrows travels from the start towards the destination.
ARROW_PHASES = 8
ARROW_CYCLE_S = 1.6

def arrow_phase_color(phase):
    return f"rgb(255,255,{240 + phase})"

def build_arrow_css():
    step = ARROW_CYCLE_S / ARROW_PHASES
    rules = []
    for k in range(ARROW_PHASES):
        b = 240 + k
        delay = k * step - ARROW_CYCLE_S   # negative: the wave is already running on first paint
        rules.append(
            f'.js-plotly-plot .scatterlayer path.js-fill[style*="rgb(255, 255, {b})"],\n'
            f'.js-plotly-plot .scatterlayer path.js-fill[style*="rgb(255,255,{b})"] '
            f'{{ animation-delay: {delay:.3f}s; }}'
        )
    selectors = ",\n".join(
        f'.js-plotly-plot .scatterlayer path.js-fill[style*="rgb(255, 255, {240 + k})"],\n'
        f'.js-plotly-plot .scatterlayer path.js-fill[style*="rgb(255,255,{240 + k})"]'
        for k in range(ARROW_PHASES)
    )
    reduced = selectors.replace("{", "{{")
    return f"""
<style>
@keyframes route-arrow-wave {{
    0%, 100% {{ fill-opacity: 0.12; }}
    30%      {{ fill-opacity: 1; }}
    60%      {{ fill-opacity: 0.12; }}
}}
{selectors} {{
    animation: route-arrow-wave {ARROW_CYCLE_S}s ease-in-out infinite;
    pointer-events: none;
}}
{chr(10).join(rules)}
</style>
"""

ROUTE_ARROW_CSS = build_arrow_css()

def route_arrow_polygons(points, spacing=9.0, length=3.2, half_width=1.4):
    """Arrowheads (closed triangles, None-separated) every `spacing` metres along a polyline,
    each pointing in the direction of travel. Returns (xs, ys)."""
    pts = []
    for pt in points:
        if not pts or math.hypot(pt[0] - pts[-1][0], pt[1] - pts[-1][1]) > 1e-9:
            pts.append(pt)
    if len(pts) < 2:
        return [], []

    seg_len = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]
    total = sum(seg_len)
    if total < length * 1.5:
        return [], []

    n_arrows = max(1, int(total // spacing))
    offsets = [(i + 0.5) * total / n_arrows for i in range(n_arrows)]

    xs, ys = [], []
    for dist in offsets:
        # find the segment that holds this distance along the route
        run = 0.0
        for (a, b), ln in zip(zip(pts, pts[1:]), seg_len):
            if run + ln >= dist:
                t = (dist - run) / ln
                cx, cy = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
                ux, uy = (b[0] - a[0]) / ln, (b[1] - a[1]) / ln
                break
            run += ln
        nx, ny = -uy, ux
        tip = (cx + ux * length / 2, cy + uy * length / 2)
        bx, by = cx - ux * length / 2, cy - uy * length / 2
        xs += [tip[0], bx + nx * half_width, bx - nx * half_width, tip[0], None]
        ys += [tip[1], by + ny * half_width, by - ny * half_width, tip[1], None]
    return xs, ys

PLAY_LABELS = {
    "English": ("▶ Play arrows", "⏸ Pause"),
    "Simplified Chinese": ("▶ 播放箭头", "⏸ 暂停"),
    "Malay": ("▶ Mainkan anak panah", "⏸ Jeda"),
}
HOVER_MARKER_PX_3D = 22    # same for the 3D map
ARROW_FRAME_CYCLE = 18     # frames for an arrow to travel one arrow-spacing
ARROW_FRAME_MS = 50        # milliseconds per frame
ARROW_LOOPS = 40           # Plotly can't loop an animation, so the cycle is queued this many times

def build_arrow_frames(points, spacing, n_frames=ARROW_FRAME_CYCLE):
    """Arrow positions along a polyline for each frame of a looping animation.
    Returns a list (one entry per frame) of [(position, unit_direction), ...], or None when
    the route is too short. `points` are equal-length coordinate tuples (2D or 3D)."""
    pts = []
    for p in points:
        if not pts or math.dist(p, pts[-1]) > 1e-9:
            pts.append(tuple(p))
    if len(pts) < 2:
        return None
    seg = [math.dist(a, b) for a, b in zip(pts, pts[1:])]
    cum = [0.0]
    for s in seg:
        cum.append(cum[-1] + s)
    total = cum[-1]
    n_arrows = int(total // spacing)
    if n_arrows < 1:
        return None

    frames = []
    for f in range(n_frames):
        offset = spacing * f / n_frames
        arrows = []
        for i in range(n_arrows):
            d = offset + i * spacing
            k = 0
            while k < len(seg) - 1 and cum[k + 1] < d:
                k += 1
            t = min(1.0, max(0.0, (d - cum[k]) / seg[k]))
            a, b = pts[k], pts[k + 1]
            pos = tuple(a[j] + (b[j] - a[j]) * t for j in range(len(a)))
            direction = tuple((b[j] - a[j]) / seg[k] for j in range(len(a)))
            arrows.append((pos, direction))
        frames.append(arrows)
    return frames

def play_menu(lang, frame_names, x=0.01, y=0.99, redraw=True):
    """Play / Pause buttons that run the queued arrow frames.
    redraw=False updates only the moving trace (fast); 3D scenes need redraw=True."""
    play_lbl, pause_lbl = PLAY_LABELS.get(lang, PLAY_LABELS["English"])
    return dict(
        type="buttons", direction="left", showactive=False,
        x=x, y=y, xanchor="left", yanchor="top", pad=dict(l=4, t=4, r=4, b=4),
        bgcolor="#FFFFFF", bordercolor="#CBD5E1", font=dict(size=12, color="#0f172a"),
        buttons=[
            dict(label=play_lbl, method="animate",
                 args=[list(frame_names) * ARROW_LOOPS,
                       dict(frame=dict(duration=ARROW_FRAME_MS, redraw=redraw),
                            transition=dict(duration=0), fromcurrent=True, mode="immediate")]),
            dict(label=pause_lbl, method="animate",
                 args=[[None], dict(frame=dict(duration=0, redraw=False),
                                    transition=dict(duration=0), mode="immediate")]),
        ],
    )

def hover_text_lines(samples, hover):
    """Plotly hover strings for build_route_hover samples."""
    import html as _html
    loc_lbl, rem_lbl = hover["loc_label"], hover["rem_label"]
    texts = []
    for _lat, _lng, name, rem in samples:
        line = f"<b>{_html.escape(loc_lbl)}:</b> {_html.escape(name)}"
        if rem_lbl:
            line += f"<br>{_html.escape(rem_lbl)}: <b>{rem:.1f} m</b>"
        texts.append(line)
    return texts

HOVER_BAND_M = 3.0   # 2D Plotly: the route shows its annotation within this many metres of the line

def route_hover_band(gx, gy, samples, band_m):
    """For every click-grid point: is it within `band_m` metres of the route, and which route
    sample is nearest to it? Returns (in_band boolean array, nearest sample index array)."""
    import numpy as np
    gxa, gya = np.asarray(gx, dtype=float), np.asarray(gy, dtype=float)
    sx = np.array([s[1] for s in samples], dtype=float)
    sy = np.array([s[0] for s in samples], dtype=float)
    if gxa.size == 0 or sx.size == 0:
        return None, None
    nearest = np.empty(gxa.size, dtype=int)
    dist = np.empty(gxa.size)
    for a in range(0, gxa.size, 2000):               # chunks keep memory small
        b = a + 2000
        d2 = (gxa[a:b, None] - sx[None, :]) ** 2 + (gya[a:b, None] - sy[None, :]) ** 2
        k = d2.argmin(axis=1)
        nearest[a:b] = k
        dist[a:b] = np.sqrt(d2[np.arange(k.size), k])
    return dist <= band_m, nearest

def render_2d_plotly_view(active_floor_z, route_path=None, node_coords_dict=MULTI_CAD_NODES, current_lang="English",
                          stop_ids=None, show_dest=True, show_doors=True,
                          show_slots=False, assigned_slot=None, route_color="#EF4444", highlight=None):
    """2D floor plan. The view (pan/zoom) is kept across reruns via `uirevision`,
    so clicking a point no longer moves the map."""
    fig = go.Figure()
    lang_dict = LOCALIZATION.get(current_lang, LOCALIZATION["English"])
    floor_z = int(active_floor_z)
    LABEL_COLOR = "#0f172a"

    floor_rooms = {r_id: info for r_id, info in ROOM_POLYGONS.items() if int(info["z"]) == floor_z}

    # Room outlines + fills (not clickable, so clicks fall through to the grid)
    for room_id, info in floor_rooms.items():
        coords = info["coords"]
        fig.add_trace(go.Scatter(
            x=[pt[0] for pt in coords] + [coords[0][0]],
            y=[pt[1] for pt in coords] + [coords[0][1]],
            mode="lines", fill="toself",
            fillcolor=hex_to_rgba(info.get("color", "#CBD5E1")),
            line=dict(color="#334155", width=1.5),
            hoverinfo="skip", showlegend=False,
        ))

    # Room labels
    lab_x, lab_y, lab_text = [], [], []
    for room_id, info in floor_rooms.items():
        if show_slots and room_id in PARKING_SLOTS:
            continue   # drawn as a coloured slot with its own label below
        coords = info["coords"]
        lab_x.append(sum(pt[0] for pt in coords) / len(coords))
        lab_y.append(sum(pt[1] for pt in coords) / len(coords))
        lab_text.append(room_label(room_id, current_lang))
    fig.add_trace(go.Scatter(
        x=lab_x, y=lab_y, mode="text", text=lab_text, textposition="middle center",
        textfont=dict(size=10, color=LABEL_COLOR),
        hoverinfo="skip", showlegend=False,
        unselected=dict(textfont=dict(color=LABEL_COLOR)),
    ))

    # Parking slots: green = free, red = taken, blue = assigned to the driver
    if show_slots:
        s_lx, s_ly, s_txt = [], [], []
        for slot_id, details in PARKING_SLOTS.items():
            if slot_id not in node_coords_dict or int(node_coords_dict[slot_id][2]) != floor_z:
                continue
            cx, cy, _ = node_coords_dict[slot_id]
            col = "#2563EB" if slot_id == assigned_slot else ("#DC2626" if details["occupied"] else "#16A34A")
            hw, hh = 1.75, 3.0
            fig.add_trace(go.Scatter(
                x=[cx - hw, cx + hw, cx + hw, cx - hw, cx - hw],
                y=[cy - hh, cy - hh, cy + hh, cy + hh, cy - hh],
                mode="lines", fill="toself", fillcolor=hex_to_rgba(col, 0.8),
                line=dict(color=col, width=1.5), hoverinfo="skip", showlegend=False,
            ))
            s_lx.append(cx); s_ly.append(cy); s_txt.append(slot_id)
        if s_lx:
            fig.add_trace(go.Scatter(
                x=s_lx, y=s_ly, mode="text", text=s_txt, textposition="middle center",
                textfont=dict(size=11, color="#FFFFFF"), hoverinfo="skip", showlegend=False,
                unselected=dict(textfont=dict(color="#FFFFFF")),
            ))

    # Entry/exit points
    if show_doors:
        door_lbl = DOOR_LABELS.get(current_lang, DOOR_LABELS["English"])
        d_x, d_y, d_text = [], [], []
        for room_id, (dx, dy, _link) in DOORS.items():
            if int(ROOM_POLYGONS[room_id]["z"]) != floor_z:
                continue
            name = POI_TRANSLATIONS.get(current_lang, {}).get(room_id, room_id).split("(")[0].strip()
            d_x.append(dx)
            d_y.append(dy)
            d_text.append(f"{name} – {door_lbl}")
        if d_x:
            fig.add_trace(go.Scatter(
                x=d_x, y=d_y, mode="markers", text=d_text, hoverinfo="text",
                marker=dict(size=9, color="#34D399", line=dict(color="#065F46", width=2)),
                showlegend=False,
            ))

    # Parking infrastructure labels (ramps, stairwell, elevator, escalator) as boxed tags
    if show_slots:
        for node_id, key in (("P_L3_Driveway_Entrance", "lbl_entrance_ramp"), ("P_L3_Driveway_Exit", "lbl_exit_ramp"),
                             ("P_L3_Stairs", "lbl_stairwell"), ("P_L3_Elevator", "lbl_elevator"),
                             ("P_L3_Escalator", "lbl_escalator")):
            if node_id in node_coords_dict and int(node_coords_dict[node_id][2]) == floor_z:
                nx_, ny_, _ = node_coords_dict[node_id]
                fig.add_annotation(
                    x=nx_, y=ny_, xref="x", yref="y", text=f"<b>{lang_dict.get(key, node_id)}</b>",
                    showarrow=False, font=dict(size=11, color="#000000"),
                    bgcolor="rgba(255,255,255,0.95)", bordercolor="#1976D2", borderwidth=2, borderpad=3,
                )

    # Route, stops, start, destination
    arrow_frames = []
    if route_path:
        on_floor = lambda n: n in node_coords_dict and int(node_coords_dict[n][2]) == floor_z
        floor_path = [n for n in route_path if on_floor(n)]

        if len(floor_path) > 1:
            route_x = [node_coords_dict[n][0] for n in floor_path]
            route_y = [node_coords_dict[n][1] for n in floor_path]
            fig.add_trace(go.Scatter(
                x=route_x, y=route_y,
                mode="lines", line=dict(color=route_color, width=5),
                hoverinfo="skip", showlegend=False,
            ))
            # Arrowheads that travel along the route (frames are played by the Play button)
            arrow_anim = build_arrow_frames(list(zip(route_x, route_y)), 9.0)
            if arrow_anim:
                def arrow_polys(arrows, length=3.2, half_width=1.4):
                    # Arrowheads as filled triangles (None-separated). The direction is part of the
                    # shape, so a frame only changes x/y and Plotly can animate it without a full redraw.
                    xs, ys = [], []
                    for (cx, cy), (ux, uy) in arrows:
                        nx, ny = -uy, ux
                        tx, ty = cx + ux * length / 2, cy + uy * length / 2
                        bx, by = cx - ux * length / 2, cy - uy * length / 2
                        xs += [tx, bx + nx * half_width, bx - nx * half_width, tx, None]
                        ys += [ty, by + ny * half_width, by - ny * half_width, ty, None]
                    return xs, ys
                arrow_trace_idx = len(fig.data)
                ax0, ay0 = arrow_polys(arrow_anim[0])
                fig.add_trace(go.Scatter(
                    x=ax0, y=ay0, mode="lines", fill="toself",
                    fillcolor="#FFFFFF", line=dict(color="#B91C1C", width=1.5),
                    hoverinfo="skip", showlegend=False,
                ))
                for k, arrows in enumerate(arrow_anim):
                    fx, fy = arrow_polys(arrows)
                    arrow_frames.append(go.Frame(
                        name=f"arrow{k}", traces=[arrow_trace_idx],
                        data=[go.Scatter(x=fx, y=fy)],
                    ))

        stop_nodes = [(i, n) for i, n in enumerate(stop_ids or [], start=1) if on_floor(n)]
        if stop_nodes:
            fig.add_trace(go.Scatter(
                x=[node_coords_dict[n][0] for _, n in stop_nodes],
                y=[node_coords_dict[n][1] for _, n in stop_nodes],
                mode="markers+text", text=[str(i) for i, _ in stop_nodes], textposition="top center",
                textfont=dict(size=12, color="#C2410C"),
                marker=dict(size=13, symbol="diamond", color="#F97316", line=dict(color="#FFFFFF", width=2)),
                hoverinfo="skip", showlegend=False,
                unselected=dict(textfont=dict(color="#C2410C")),
            ))

        if on_floor(route_path[0]):
            sx, sy, _ = node_coords_dict[route_path[0]]
            fig.add_trace(go.Scatter(
                x=[sx], y=[sy], mode="markers+text", text=[lang_dict["marker_start"].strip()],
                textposition="top center", textfont=dict(size=12, color="#B91C1C"),
                marker=dict(size=15, symbol="circle", color="#EF4444", line=dict(color="#FFFFFF", width=2)),
                hoverinfo="skip", showlegend=False,
                unselected=dict(textfont=dict(color="#B91C1C")),
            ))

        if show_dest and len(route_path) > 1 and on_floor(route_path[-1]):
            dx, dy, _ = node_coords_dict[route_path[-1]]
            fig.add_trace(go.Scatter(
                x=[dx], y=[dy], mode="markers+text", text=[lang_dict["marker_dest"].strip()],
                textposition="top center", textfont=dict(size=12, color="#15803D"),
                marker=dict(size=17, symbol="star", color="#22C55E", line=dict(color="#FFFFFF", width=2)),
                hoverinfo="skip", showlegend=False,
                unselected=dict(textfont=dict(color="#15803D")),
            ))

    # Ring around the start / stop / destination that is being moved
    if highlight and int(highlight[2]) == floor_z:
        fig.add_trace(go.Scatter(
            x=[highlight[0]], y=[highlight[1]], mode="markers",
            marker=dict(size=30, symbol="circle-open", color="#F97316", line=dict(width=4, color="#F97316")),
            hoverinfo="skip", showlegend=False,
        ))

    # Invisible click targets (added last)
    gx, gy = build_click_grid(floor_z)
    hover = None
    if route_path:
        hover = build_route_hover(route_path, node_coords_dict, floor_z, current_lang, include_remaining=show_dest)

    # The click grid doubles as the hover layer. Grid points within HOVER_BAND_M metres of the route
    # form a second trace that shows the route annotation; every other grid point stays a silent
    # click target. The two sets never overlap, so no point can win the "closest point" contest
    # and hide the tooltip (that contest made it flicker and leave gaps), and the hover area is
    # an even band along the whole route.
    in_band, nearest = (None, None)
    if hover:
        in_band, nearest = route_hover_band(gx, gy, hover["samples"], HOVER_BAND_M)
    if in_band is not None and in_band.any():
        texts = hover_text_lines(hover["samples"], hover)
        plain = [i for i in range(len(gx)) if not in_band[i]]
        band = [i for i in range(len(gx)) if in_band[i]]
        fig.add_trace(go.Scatter(
            x=[gx[i] for i in plain], y=[gy[i] for i in plain], mode="markers",
            marker=dict(size=12, color="rgba(0,0,0,0)"),
            hoverinfo="none", showlegend=False,
        ))
        fig.add_trace(go.Scatter(
            x=[gx[i] for i in band], y=[gy[i] for i in band], mode="markers",
            marker=dict(size=12, color="rgba(0,0,0,0)"),
            hovertext=[texts[int(nearest[i])] for i in band], hoverinfo="text",
            hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="#EF4444", font=dict(size=12, color="#0f172a")),
            showlegend=False,
        ))
    else:
        fig.add_trace(go.Scatter(
            x=list(gx), y=list(gy), mode="markers",
            marker=dict(size=12, color="rgba(0,0,0,0)"),
            hoverinfo="none", showlegend=False,
        ))

    # Keep markers at full strength when a point is selected
    fig.update_traces(selected=dict(marker=dict(opacity=1)), unselected=dict(marker=dict(opacity=1)))

    all_pts = [pt for info in floor_rooms.values() for pt in info["coords"]]
    if all_pts:
        x_rng = [min(p[0] for p in all_pts) - 5, max(p[0] for p in all_pts) + 5]
        y_rng = [min(p[1] for p in all_pts) - 5, max(p[1] for p in all_pts) + 5]
    else:
        x_rng, y_rng = [-60, 60], [-35, 55]

    # Numbered axes: Plotly re-spaces the tick intervals automatically as you zoom
    axis_style = dict(
        showgrid=True, gridcolor="rgba(100,116,139,0.18)", gridwidth=1,
        zeroline=False,
        showline=True, linecolor="#64748B", linewidth=1,
        showticklabels=True, ticks="outside", ticklen=4, tickcolor="#64748B",
        tickfont=dict(size=11, color="#64748B"),
        automargin=True,
    )
    fig.update_layout(
        height=640,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
        plot_bgcolor="#F8FAFC",
        dragmode="pan",
        clickmode="event+select",
        hovermode="closest",
        hoverdistance=60,     # look this many pixels around the mouse for a hover point (default 20)
        uirevision=f"floor_{floor_z}",   # same value every rerun -> pan/zoom is kept
        xaxis=dict(range=x_rng, title=dict(text="X (m)", font=dict(size=12, color="#64748B")), **axis_style),
        yaxis=dict(range=y_rng, scaleanchor="x", scaleratio=1,
                   title=dict(text="Y (m)", font=dict(size=12, color="#64748B")), **axis_style),
    )
    if arrow_frames:
        fig.frames = arrow_frames
        fig.update_layout(updatemenus=[play_menu(current_lang, [f.name for f in arrow_frames], redraw=False)])
    return fig

FOLIUM_BASE_CSS = """
<style>
.leaflet-container { background: #F8FAFC; }
@keyframes route-flow { from { stroke-dashoffset: 0; } to { stroke-dashoffset: -34; } }
.route-flow, path.leaflet-interactive[stroke="#FFFEFD"] {
    animation: route-flow 0.7s linear infinite;
    pointer-events: none;
}
/* Arrowheads light up one after another, so a wave runs start -> destination */
@keyframes route-arrow-wave {
    0%, 100% { fill-opacity: 0.12; stroke-opacity: 0.35; }
    30%      { fill-opacity: 1;    stroke-opacity: 1; }
    60%      { fill-opacity: 0.12; stroke-opacity: 0.35; }
}
.route-arrow {
    animation: route-arrow-wave __CYCLE__s ease-in-out infinite;
    pointer-events: none;
}
__PHASE_RULES__
</style>
"""
FOLIUM_BASE_CSS = (FOLIUM_BASE_CSS
    .replace("__CYCLE__", str(ARROW_CYCLE_S))
    .replace("__PHASE_RULES__", "\n".join(
        f".route-arrow.arrow-phase-{k} {{ animation-delay: {k * ARROW_CYCLE_S / ARROW_PHASES - ARROW_CYCLE_S:.3f}s; }}"
        for k in range(ARROW_PHASES))))

def build_axis_grid_js(map_var, x_title="X (m)", y_title="Y (m)"):
    """Leaflet script that draws numbered X/Y axes and grid lines on a CRS.Simple map.
    The spacing is re-chosen (1, 2, 5, 10, 20, 50 ...) every time the map is zoomed or panned."""
    js = """
(function () {
    var map = __MAP__;
    var container = map.getContainer();
    var X_TITLE = __X_TITLE__;
    var Y_TITLE = __Y_TITLE__;
    var TARGET_PX = 90;   // aim for about this many pixels between grid lines

    function makeCanvas(z) {
        var c = document.createElement('canvas');
        c.style.cssText = 'position:absolute;left:0;top:0;pointer-events:none;z-index:' + z + ';';
        container.appendChild(c);
        return c;
    }
    var gridCanvas = makeCanvas(399);    // grid lines sit under the map layers
    var labelCanvas = makeCanvas(450);   // numbers and titles sit on top

    function niceStep(raw) {
        var p = Math.pow(10, Math.floor(Math.log10(raw)));
        var f = raw / p;
        return (f <= 1 ? 1 : f <= 2 ? 2 : f <= 5 ? 5 : 10) * p;
    }
    function decimals(step) { return step >= 1 ? 0 : Math.ceil(-Math.log10(step) - 1e-9); }
    function prepare(canvas, size) {
        var dpr = window.devicePixelRatio || 1;
        var w = Math.round(size.x * dpr), h = Math.round(size.y * dpr);
        if (canvas.width !== w || canvas.height !== h) {
            canvas.width = w;
            canvas.height = h;
            canvas.style.width = size.x + 'px';
            canvas.style.height = size.y + 'px';
        }
        var ctx = canvas.getContext('2d');
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        ctx.clearRect(0, 0, size.x, size.y);
        return ctx;
    }
    function tag(ctx, text, x, y, align) {
        ctx.textAlign = align;
        ctx.textBaseline = 'middle';
        var w = ctx.measureText(text).width;
        var left = align === 'center' ? x - w / 2 : (align === 'left' ? x : x - w);
        ctx.fillStyle = 'rgba(248,250,252,0.85)';
        ctx.fillRect(left - 2, y - 7, w + 4, 14);
        ctx.fillStyle = '#475569';
        ctx.fillText(text, x, y);
    }
    function draw() {
        var size, zoom, bounds;
        try { size = map.getSize(); zoom = map.getZoom(); bounds = map.getBounds(); } catch (e) { return; }
        if (zoom === undefined || !isFinite(zoom)) return;

        var g = prepare(gridCanvas, size);
        var l = prepare(labelCanvas, size);
        var step = niceStep(TARGET_PX / map.options.crs.scale(zoom));
        var dec = decimals(step);

        g.strokeStyle = 'rgba(100,116,139,0.28)';
        g.lineWidth = 1;
        l.font = '11px sans-serif';

        var i0 = Math.ceil(bounds.getWest() / step - 1e-9), i1 = Math.floor(bounds.getEast() / step + 1e-9);
        if (i1 - i0 <= 400) {
            for (var i = i0; i <= i1; i++) {
                var px = Math.round(map.latLngToContainerPoint([bounds.getSouth(), i * step]).x) + 0.5;
                g.beginPath(); g.moveTo(px, 0); g.lineTo(px, size.y); g.stroke();
                if (px > 30 && px < size.x - 60) tag(l, (i * step).toFixed(dec), px, size.y - 11, 'center');
            }
        }
        var j0 = Math.ceil(bounds.getSouth() / step - 1e-9), j1 = Math.floor(bounds.getNorth() / step + 1e-9);
        if (j1 - j0 <= 400) {
            for (var j = j0; j <= j1; j++) {
                var py = Math.round(map.latLngToContainerPoint([j * step, bounds.getWest()]).y) + 0.5;
                g.beginPath(); g.moveTo(0, py); g.lineTo(size.x, py); g.stroke();
                if (py > 30 && py < size.y - 30) tag(l, (j * step).toFixed(dec), 6, py, 'left');
            }
        }
        l.font = 'bold 12px sans-serif';
        tag(l, X_TITLE, size.x - 8, size.y - 29, 'right');
        tag(l, Y_TITLE, 8, 14, 'left');
    }
    map.on('move zoom viewreset resize', draw);
    draw();
})();
"""
    return (js.replace("__MAP__", map_var)
              .replace("__X_TITLE__", json.dumps(x_title))
              .replace("__Y_TITLE__", json.dumps(y_title)))

class AxisGrid(MacroElement):
    """Adds numbered X/Y axes + grid lines to a folium map (see build_axis_grid_js)."""
    _template = Template("{% macro script(this, kwargs) %}{{ this.build_js() }}{% endmacro %}")

    def __init__(self, x_title="X (m)", y_title="Y (m)"):
        super().__init__()
        self._name = "AxisGrid"
        self.x_title = x_title
        self.y_title = y_title

    def build_js(self):
        return build_axis_grid_js(self._parent.get_name(), self.x_title, self.y_title)

AUTOSCALE_LABELS = {
    "English": "Autoscale (reset view)",
    "Simplified Chinese": "自动缩放（重置视图）",
    "Malay": "Skala automatik (set semula paparan)",
}

class AutoscaleControl(MacroElement):
    """Button under the zoom controls that fits the whole floor plan back into view
    (like the autoscale button in the Plotly toolbar)."""
    _template = Template("{% macro script(this, kwargs) %}{{ this.build_js() }}{% endmacro %}")

    def __init__(self, bounds, label="Autoscale"):
        super().__init__()
        self._name = "AutoscaleControl"
        self.bounds = bounds
        self.label = label

    def build_js(self):
        js = """
(function () {
    var map = __MAP__;
    var BOUNDS = __BOUNDS__;
    var LABEL = __LABEL__;
    var Ctl = L.Control.extend({
        options: {position: 'topleft'},
        onAdd: function () {
            var box = L.DomUtil.create('div', 'leaflet-bar leaflet-control');
            var a = L.DomUtil.create('a', '', box);
            a.href = '#';
            a.title = LABEL;
            a.setAttribute('role', 'button');
            a.setAttribute('aria-label', LABEL);
            a.style.cssText = 'display:flex;align-items:center;justify-content:center;width:30px;height:30px;';
            a.innerHTML = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="#334155" ' +
                          'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">' +
                          '<path d="M2 6V2h4M10 2h4v4M14 10v4h-4M6 14H2v-4"/></svg>';
            L.DomEvent.disableClickPropagation(box);
            L.DomEvent.on(a, 'click', function (e) {
                L.DomEvent.preventDefault(e);
                map.fitBounds(BOUNDS);
            });
            return box;
        }
    });
    new Ctl().addTo(map);
})();
"""
        return (js.replace("__MAP__", self._parent.get_name())
                  .replace("__BOUNDS__", json.dumps(self.bounds))
                  .replace("__LABEL__", json.dumps(self.label)))

def render_2d_folium_view(active_floor_z, route_path=None, node_coords_dict=MULTI_CAD_NODES, current_lang="English",
                          stop_ids=None, show_dest=True, show_doors=True, highlight=None):
    """Returns (base_map, route_layer).

    base_map only holds what does not change while you pick points (rooms, labels, doors, axes),
    so its HTML is the same on every rerun and streamlit-folium keeps the map (pan/zoom) as it is.
    Everything that changes with the route lives in route_layer, which streamlit-folium swaps in
    place through `feature_group_to_add`.
    """
    floor_z = int(active_floor_z)
    floor_rooms = {r_id: info for r_id, info in ROOM_POLYGONS.items() if int(info["z"]) == floor_z}

    all_pts = [pt for info in floor_rooms.values() for pt in info["coords"]]
    if all_pts:
        bounds = [[min(p[1] for p in all_pts) - 5, min(p[0] for p in all_pts) - 5],
                  [max(p[1] for p in all_pts) + 5, max(p[0] for p in all_pts) + 5]]
    else:
        bounds = [[-35, -60], [55, 60]]

    # ---- static base map ----
    m = folium.Map(crs="Simple", tiles=None, zoom_control=True, scroll_wheel_zoom=True,
                   zoomSnap=0.25, zoomDelta=0.5, attribution_control=False)
    m.get_root().header.add_child(folium.Element(FOLIUM_BASE_CSS))

    for room_id, info in floor_rooms.items():
        coords = info["coords"]
        label = room_label(room_id, current_lang)
        folium.Polygon(
            locations=[[pt[1], pt[0]] for pt in coords],
            color="#334155", weight=2, fill=True,
            fill_color=info.get("color", "#CBD5E1"), fill_opacity=0.7,
            tooltip=label,
        ).add_to(m)

        cx = sum(pt[0] for pt in coords) / len(coords)
        cy = sum(pt[1] for pt in coords) / len(coords)
        folium.Marker(
            location=[cy, cx], interactive=False,   # labels must not swallow clicks
            icon=folium.DivIcon(html=(
                '<div style="font-size: 10px; font-weight: bold; color: #0f172a; white-space: nowrap; '
                f'pointer-events: none; transform: translate(-50%, -50%);">{label}</div>'
            )),
        ).add_to(m)

    if show_doors:
        add_door_markers_2d(m, floor_z, current_lang)

    AxisGrid().add_to(m)
    m.fit_bounds(bounds)
    AutoscaleControl(bounds, AUTOSCALE_LABELS.get(current_lang, AUTOSCALE_LABELS["English"])).add_to(m)

    # ---- route layer (changes with every click) ----
    route_layer = folium.FeatureGroup(name="route")
    if route_path:
        on_floor = lambda n: n in node_coords_dict and int(node_coords_dict[n][2]) == floor_z
        floor_path = [n for n in route_path if on_floor(n)]

        if len(floor_path) > 1:
            xy = [(node_coords_dict[n][0], node_coords_dict[n][1]) for n in floor_path]
            line_pts = [[y, x] for x, y in xy]
            # Exactly the Smart Parking method: moving ► arrowheads + flowing dashes
            hover = build_route_hover(route_path, node_coords_dict, floor_z, current_lang,
                                      include_remaining=show_dest)
            add_animated_route(route_layer, line_pts, "#EF4444", hover=hover)

        for idx, stop_id in enumerate(stop_ids or [], start=1):
            if on_floor(stop_id):
                stx, sty, _ = node_coords_dict[stop_id]
                folium.Marker(
                    location=[sty, stx], interactive=False,
                    icon=folium.DivIcon(html=(
                        '<div style="width: 22px; height: 22px; border-radius: 50%; background: #F97316; color: #fff; '
                        'border: 2px solid #fff; font: bold 12px/18px sans-serif; text-align: center; '
                        f'transform: translate(-50%, -50%);">{idx}</div>'
                    )),
                ).add_to(route_layer)

        if on_floor(route_path[0]):
            sx, sy, _ = node_coords_dict[route_path[0]]
            folium.Marker(location=[sy, sx], interactive=False,
                          icon=folium.Icon(color="red", icon="play")).add_to(route_layer)

        if show_dest and len(route_path) > 1 and on_floor(route_path[-1]):
            dx, dy, _ = node_coords_dict[route_path[-1]]
            folium.Marker(location=[dy, dx], interactive=False,
                          icon=folium.Icon(color="green", icon="flag")).add_to(route_layer)

    if highlight and int(highlight[2]) == floor_z:
        folium.CircleMarker(location=[highlight[1], highlight[0]], radius=18, color="#F97316", weight=4,
                            fill=False, interactive=False).add_to(route_layer)

    return m, route_layer

# Soft, translucent grid for the 3D scene (same tone as the 2D map grid)
GRID3D = dict(gridcolor="rgba(100,116,139,0.18)", zerolinecolor="rgba(100,116,139,0.18)",
              linecolor="rgba(100,116,139,0.35)", showgrid=True, gridwidth=1)

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

    arrow3d_payload = None   # arrow positions per frame, played by JS (see render_3d_html)
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

        # Arrows that travel along the route (frames are played by the Play button).
        # Each arrow is drawn from line segments (shaft + two barbs) of a fixed size in metres.
        # (go.Cone is not used: Plotly rescales cones from their spacing on every frame, so
        # they pulsed in size while moving.)
        ARROW3D_LEN, ARROW3D_BARB, ARROW3D_WING = 7.0, 2.6, 2.0
        arrow3d_anim = build_arrow_frames(list(zip(rx, ry, rz)), 20.0)
        if arrow3d_anim:
            def arrow3d_lines(arrows):
                xs, ys, zs = [], [], []
                for pos, d in arrows:
                    # a sideways vector perpendicular to the direction of travel
                    side = (-d[1], d[0], 0.0)
                    norm = math.hypot(side[0], side[1])
                    side = (side[0] / norm, side[1] / norm, 0.0) if norm > 1e-6 else (1.0, 0.0, 0.0)
                    tip = [pos[j] + d[j] * ARROW3D_LEN / 2 for j in range(3)]
                    tail = [pos[j] - d[j] * ARROW3D_LEN / 2 for j in range(3)]
                    back = [tip[j] - d[j] * ARROW3D_BARB for j in range(3)]
                    left = [back[j] + side[j] * ARROW3D_WING for j in range(3)]
                    right = [back[j] - side[j] * ARROW3D_WING for j in range(3)]
                    for seg in ((tail, tip), (left, tip, right)):
                        for p in seg:
                            xs.append(p[0]); ys.append(p[1]); zs.append(p[2])
                        xs.append(None); ys.append(None); zs.append(None)
                return xs, ys, zs
            arrow3d_idx = len(fig.data)
            ax0, ay0, az0 = arrow3d_lines(arrow3d_anim[0])
            fig.add_trace(go.Scatter3d(
                x=ax0, y=ay0, z=az0, mode="lines",
                line=dict(color="#CC0000", width=7), hoverinfo="skip", showlegend=False,
            ))
            arrow3d_payload = {"trace": arrow3d_idx,
                               "frames": [list(arrow3d_lines(arrows)) for arrows in arrow3d_anim]}

        # Hover annotation along the route, floor by floor (place + distance left to the destination)
        h_x, h_y, h_z, h_text = [], [], [], []
        for fz in range(4):
            hov = build_route_hover(route_path, node_coords, fz, current_lang, step=2.0)
            if hov:
                h_x += [s[1] for s in hov["samples"]]
                h_y += [s[0] for s in hov["samples"]]
                h_z += [fz * 40] * len(hov["samples"])
                h_text += hover_text_lines(hov["samples"], hov)
        if h_x:
            fig.add_trace(go.Scatter3d(
                x=h_x, y=h_y, z=h_z, mode="markers",
                # Practically invisible: many overlapping translucent markers used to add up
                # to a red glow along the route.
                marker=dict(size=HOVER_MARKER_PX_3D, color="#EF4444", opacity=0.003),
                hovertext=h_text, hoverinfo="text",
                hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="#EF4444", font=dict(size=12, color="#0f172a")),
                showlegend=False,
            ))

    # Fixed axis ranges: while the arrows animate, auto-ranging would re-fit the scene on every
    # frame and make the whole map zoom in and out. The proportions match aspectmode="data".
    all_xy = [pt for info in ROOM_POLYGONS.values() for pt in info["coords"]]
    x_rng = [min(p[0] for p in all_xy) - 5, max(p[0] for p in all_xy) + 5]
    y_rng = [min(p[1] for p in all_xy) - 5, max(p[1] for p in all_xy) + 5]
    z_max = max(info["z"] for info in ROOM_POLYGONS.values()) * 40
    z_rng = [-10, z_max + 10]
    spans = [x_rng[1] - x_rng[0], y_rng[1] - y_rng[0], z_rng[1] - z_rng[0]]
    longest = max(spans)
    fig.update_layout(
        scene=dict(
            xaxis=dict(title="X (m)", backgroundcolor="#F8FAFC", **GRID3D, range=x_rng, autorange=False),
            yaxis=dict(title="Y (m)", backgroundcolor="#F8FAFC", **GRID3D, range=y_rng, autorange=False),
            zaxis=dict(title="Floor Level", backgroundcolor="#F8FAFC", **GRID3D, range=z_rng, autorange=False),
            aspectmode="manual",
            aspectratio=dict(x=spans[0] / longest, y=spans[1] / longest, z=spans[2] / longest),
        ),
        hoverdistance=60,
        uirevision="iso3d",   # keep the camera as the user left it across reruns
        height=680,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return fig, arrow3d_payload

def render_3d_html(fig, payload, lang="English", height=680):
    """3D map as standalone HTML (for st.components.v1.html) with the arrow animation driven by JS.

    Plotly's own frame animation redraws the whole 3D scene on every frame, which resets the
    camera (the map zoomed out and could not be rotated/zoomed while playing). Here the arrows are
    updated with Plotly.restyle on one trace only, so the camera is never touched."""
    play_lbl, pause_lbl = PLAY_LABELS.get(lang, PLAY_LABELS["English"])
    js = """
(function () {
    var gd = document.getElementById('{plot_id}');
    var P = __PAYLOAD__, MS = __MS__;
    var i = 0, timer = null, busy = false, interacting = false, idleT = null;
    // Plotly re-applies the last committed camera whenever the trace is updated, which fights a
    // drag in progress. So the arrows hold still while the user is rotating / zooming.
    function hold(ms) {
        interacting = true;
        clearTimeout(idleT);
        idleT = setTimeout(function () { interacting = false; }, ms);
    }
    gd.addEventListener('pointerdown', function () { interacting = true; clearTimeout(idleT); }, true);
    window.addEventListener('pointerup', function () { hold(250); }, true);
    window.addEventListener('pointercancel', function () { hold(250); }, true);
    gd.addEventListener('wheel', function () { hold(450); }, {capture: true, passive: true});
    function step() {
        if (busy || interacting) return;
        busy = true;
        i = (i + 1) % P.frames.length;
        var f = P.frames[i];
        Plotly.restyle(gd, {x: [f[0]], y: [f[1]], z: [f[2]]}, [P.trace])
            .then(function () { busy = false; }, function () { busy = false; });
    }
    document.getElementById('arrow-play').onclick = function () { if (!timer) timer = setInterval(step, MS); };
    document.getElementById('arrow-pause').onclick = function () { clearInterval(timer); timer = null; };
})();
""".replace("__PAYLOAD__", json.dumps(payload)).replace("__MS__", str(ARROW_FRAME_MS)) if payload else None

    bar = ""
    if payload:
        btn = ("font:12px sans-serif;color:#0f172a;background:#fff;border:1px solid #CBD5E1;"
               "border-radius:4px;padding:4px 10px;margin-right:6px;cursor:pointer;")
        bar = (f'<div style="margin:2px 0 4px 4px;">'
               f'<button id="arrow-play" style="{btn}">{play_lbl}</button>'
               f'<button id="arrow-pause" style="{btn}">{pause_lbl}</button></div>')
    # Streamlit's chart theme normally styles the axes/grid; outside it Plotly falls back to its own
    # defaults (white grid on grey walls), so the grid is styled explicitly here.
    grid_axis = dict(showgrid=True, gridcolor="rgba(100,116,139,0.15)", gridwidth=1,
                     zeroline=False, showline=True, linecolor="rgba(100,116,139,0.45)",
                     showbackground=False, backgroundcolor="rgba(0,0,0,0)",
                     tickfont=dict(size=11, color="#64748B"),
                     title_font=dict(size=12, color="#64748B"))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(family="Source Sans Pro, sans-serif"),
                      scene=dict(bgcolor="rgba(0,0,0,0)", xaxis=grid_axis, yaxis=grid_axis, zaxis=grid_axis))
    body = fig.to_html(full_html=False, include_plotlyjs="cdn", default_height=f"{height}px",
                       config={"displaylogo": False}, post_script=js)
    return '<style>html,body{background:transparent !important;margin:0;}</style>' + bar + body

def show_parking_map(assigned_slot, route_path, lang, route_color, key):
    """Rooftop parking map drawn with the 2D Plotly map (pan, scroll-zoom, numbered axes,
    animated arrows, route hover and the toolbar's Autoscale / Reset axes buttons)."""
    fig = render_2d_plotly_view(
        3, route_path=route_path or None, node_coords_dict=MULTI_CAD_NODES, current_lang=lang,
        show_dest=True, show_doors=True, show_slots=True, assigned_slot=assigned_slot,
        route_color=route_color,
    )
    st.caption(LOCALIZATION.get(lang, LOCALIZATION["English"])["map_nav_hint_parking"])
    st.plotly_chart(
        fig, use_container_width=True, key=key,
        config={"scrollZoom": True, "displaylogo": False, "modeBarButtonsToRemove": ["select2d", "lasso2d"]},
    )

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

class MovingArrows(MacroElement):
    """Arrowheads that glide along a route (in the direction of travel) and loop.

    Each arrow is a small Leaflet marker that a requestAnimationFrame loop moves along the
    polyline and turns to face the way it is heading. Map units are metres (CRS.Simple),
    so SPACING and SPEED are in metres / metres per second."""
    _template = Template("{% macro script(this, kwargs) %}{{ this.build_js() }}{% endmacro %}")

    SPACING = 9.0
    SPEED = 11.0

    def __init__(self, line_pts, color="#EF4444"):
        super().__init__()
        self._name = "MovingArrows"
        self.line_pts = [[float(p[0]), float(p[1])] for p in line_pts]
        self.color = color

    def build_js(self):
        node = self._parent
        while node is not None and not isinstance(node, folium.Map):
            node = getattr(node, "_parent", None)
        map_var = node.get_name() if node is not None else self._parent.get_name()
        js = """
(function () {
    var map = __MAP__;
    var pts = __PTS__;            // [lat, lng] = [y, x]
    var COLOR = __COLOR__;
    var SPACING = __SPACING__, SPEED = __SPEED__;

    // cumulative length along the route
    var cum = [0];
    for (var i = 1; i < pts.length; i++) {
        cum.push(cum[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
    }
    var total = cum[cum.length - 1];
    if (!(total > 1)) return;

    function at(d) {                // position + heading at distance d along the route
        d = ((d % total) + total) % total;
        var k = 1;
        while (k < cum.length - 1 && cum[k] < d) k++;
        var seg = cum[k] - cum[k - 1] || 1e-9, t = (d - cum[k - 1]) / seg;
        var a = pts[k - 1], b = pts[k];
        return {
            lat: a[0] + (b[0] - a[0]) * t,
            lng: a[1] + (b[1] - a[1]) * t,
            deg: Math.atan2(b[0] - a[0], b[1] - a[1]) * 180 / Math.PI   // east = 0, north = 90
        };
    }

    var svg = '<svg width="22" height="22" viewBox="-11 -11 22 22" style="display:block;overflow:visible">' +
              '<polygon points="9,0 -6,-7 -3,0 -6,7" fill="' + COLOR + '" stroke="#FFFFFF" stroke-width="1.6" ' +
              'stroke-linejoin="round"/></svg>';
    var n = Math.max(1, Math.floor(total / SPACING));
    var gap = total / n;
    var arrows = [];
    for (var j = 0; j < n; j++) {
        var m = L.marker([pts[0][0], pts[0][1]], {
            interactive: false, keyboard: false,
            icon: L.divIcon({
                className: '',
                html: '<div class="mv-arrow" style="width:22px;height:22px;pointer-events:none;">' + svg + '</div>',
                iconSize: [22, 22], iconAnchor: [11, 11]
            })
        }).addTo(map);
        arrows.push(m);
    }

    function place(offset) {
        for (var j = 0; j < arrows.length; j++) {
            var p = at(offset + j * gap);
            arrows[j].setLatLng([p.lat, p.lng]);
            var el = arrows[j]._icon && arrows[j]._icon.firstChild;
            if (el) el.style.transform = 'rotate(' + (-p.deg) + 'deg)';   // screen y points down
        }
    }

    // Note: deliberately NOT disabled by the OS "reduce motion" setting. That setting is easy to
    // have switched on without knowing, and it made the arrows look frozen.
    var t0 = null;
    function frame(ts) {
        if (!map.getContainer().isConnected) return;     // map was replaced: stop
        if (t0 === null) t0 = ts;
        place(((ts - t0) / 1000) * SPEED);
        requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
})();
"""
        return (js.replace("__MAP__", map_var)
                  .replace("__PTS__", json.dumps(self.line_pts))
                  .replace("__COLOR__", json.dumps(self.color))
                  .replace("__SPACING__", str(self.SPACING))
                  .replace("__SPEED__", str(self.SPEED)))

HOVER_LABELS = {
    "English": ("Location", "Remaining to destination"),
    "Simplified Chinese": ("当前位置", "距终点剩余"),
    "Malay": ("Lokasi", "Baki jarak ke destinasi"),
}

def build_route_hover(path, node_coords, floor_z, lang="English", include_remaining=True, step=1.0):
    """Samples along the part of the route on `floor_z`, one about every `step` metres:
    [lat, lng, place name, metres still to walk to the end of the whole route].
    The remaining distance counts the entire route (other floors too), measured the same
    way as the route summary (15 m for each floor change)."""
    path = dedupe_path(path, node_coords)
    if len(path) < 2:
        return None

    seg = []
    for a, b in zip(path, path[1:]):
        (ax, ay, az), (bx, by, bz) = node_coords[a], node_coords[b]
        seg.append(math.hypot(ax - bx, ay - by) if az == bz else 15.0)
    cum = [0.0]
    for d in seg:
        cum.append(cum[-1] + d)
    total = cum[-1]

    def place_name(x, y, a, b):
        room_id = find_room_at(x, y, floor_z)
        if room_id:
            return POI_TRANSLATIONS.get(lang, {}).get(room_id, room_id).split("(")[0].strip()
        # not inside any room polygon: use the nearer end of this leg
        near = a if math.hypot(x - node_coords[a][0], y - node_coords[a][1]) <= \
                    math.hypot(x - node_coords[b][0], y - node_coords[b][1]) else b
        return get_node_display_name(near, lang, node_coords)

    samples = []
    for i, (a, b) in enumerate(zip(path, path[1:])):
        ax, ay, az = node_coords[a]
        bx, by, bz = node_coords[b]
        if az != bz or int(az) != int(floor_z):
            continue
        length = seg[i]
        if length < 1e-9:
            continue
        n = max(1, int(math.ceil(length / step)))
        for k in range(n + 1):
            t = k / n
            x, y = ax + (bx - ax) * t, ay + (by - ay) * t
            remaining = max(0.0, total - (cum[i] + length * t))
            samples.append([round(y, 2), round(x, 2), place_name(x, y, a, b), round(remaining, 1)])

    if not samples:
        return None
    loc_lbl, rem_lbl = HOVER_LABELS.get(lang, HOVER_LABELS["English"])
    return {"samples": samples, "loc_label": loc_lbl, "rem_label": rem_lbl if include_remaining else None}

class RouteHover(MacroElement):
    """Hovering the route shows a tooltip with the place under the mouse and the distance
    still to walk to the destination, and a dot marks the spot on the route."""
    _template = Template("{% macro script(this, kwargs) %}{{ this.build_js() }}{% endmacro %}")

    def __init__(self, line_pts, color, hover):
        super().__init__()
        self._name = "RouteHover"
        self.line_pts = [[float(p[0]), float(p[1])] for p in line_pts]
        self.color = color
        self.hover = hover

    def build_js(self):
        node = self._parent
        while node is not None and not isinstance(node, folium.Map):
            node = getattr(node, "_parent", None)
        map_var = node.get_name() if node is not None else self._parent.get_name()
        js = """
(function () {
    var map = __MAP__;
    var S = __SAMPLES__;                 // [lat, lng, name, metres remaining]
    var LOC = __LOC__, REM = __REM__, COLOR = __COLOR__;
    if (!S.length) return;

    function esc(s) {
        return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }
    var HIT_PX = 28;     // how close (in screen pixels) the mouse must be to the route
    var tip = L.tooltip({direction: 'top', offset: [0, -12], opacity: 0.96, className: 'route-hover-tip'});
    var dot = L.circleMarker([0, 0], {radius: 6, color: '#FFFFFF', weight: 2, fillColor: COLOR,
                                       fillOpacity: 1, interactive: false});

    // Closest point on the route to the mouse, measured in screen pixels. This does not rely on
    // the browser hit-testing a thin SVG line, so the hover area is centred on the route.
    function closest(cp) {
        var best = null, bd = Infinity;
        var prev = map.latLngToContainerPoint([S[0][0], S[0][1]]);
        for (var i = 1; i < S.length; i++) {
            var cur = map.latLngToContainerPoint([S[i][0], S[i][1]]);
            if (Math.abs(S[i][0] - S[i - 1][0]) + Math.abs(S[i][1] - S[i - 1][1]) < 3) {   // same leg
                var dx = cur.x - prev.x, dy = cur.y - prev.y, len2 = dx * dx + dy * dy;
                var t = len2 > 0 ? ((cp.x - prev.x) * dx + (cp.y - prev.y) * dy) / len2 : 0;
                t = Math.max(0, Math.min(1, t));
                var px = prev.x + dx * t, py = prev.y + dy * t;
                var d = Math.hypot(cp.x - px, cp.y - py);
                if (d < bd) {
                    bd = d;
                    var a = S[i - 1], b = S[i];
                    best = {
                        lat: a[0] + (b[0] - a[0]) * t, lng: a[1] + (b[1] - a[1]) * t,
                        name: (t < 0.5 ? a : b)[2], rem: a[3] + (b[3] - a[3]) * t
                    };
                }
            }
            prev = cur;
        }
        return bd <= HIT_PX ? best : null;
    }
    function hide() {
        map.closeTooltip(tip);
        if (map.hasLayer(dot)) map.removeLayer(dot);
    }
    map.on('mousemove', function (e) {
        var s = closest(e.containerPoint);
        if (!s) { hide(); return; }
        var ll = L.latLng(s.lat, s.lng);
        var html = '<div style="font:12px/1.35 sans-serif;"><b>' + esc(LOC) + ':</b> ' + esc(s.name) + '</div>';
        if (REM) html += '<div style="font:12px/1.35 sans-serif;">' + esc(REM) + ': <b>' + s.rem.toFixed(1) + ' m</b></div>';
        tip.setLatLng(ll).setContent(html);
        dot.setLatLng(ll);
        if (!map.hasLayer(dot)) dot.addTo(map);
        if (!map.hasLayer(tip)) map.openTooltip(tip);
    });
    map.on('mouseout', hide);
})();
"""
        return (js.replace("__MAP__", map_var)
                  .replace("__SAMPLES__", json.dumps(self.hover["samples"]))
                  .replace("__LOC__", json.dumps(self.hover["loc_label"]))
                  .replace("__REM__", json.dumps(self.hover["rem_label"]))
                  .replace("__COLOR__", json.dumps(self.color))
                  .replace("__PTS__", json.dumps(self.line_pts)))

def add_animated_route(m, line_pts, color, hover=None):
    """Route line with arrowheads that travel along it from the start to the end.
    `hover` (from build_route_hover) adds the hover annotation."""
    # One solid line (no soft glow underneath); the arrows move on top of it
    folium.PolyLine(locations=line_pts, color=color, weight=4, opacity=1.0).add_to(m)
    if hover:
        RouteHover(line_pts, color, hover).add_to(m)
    MovingArrows(line_pts, color).add_to(m)

def render_rooftop_folium_map(assigned_slot=None, route_path=None, current_lang="English", route_color="#2563EB"):
    rooftop_rooms = {r_id: poly["coords"] for r_id, poly in ROOM_POLYGONS.items() if poly["z"] == 3}
    all_pts = [pt for coords in rooftop_rooms.values() for pt in coords]
    min_x, max_x = min(p[0] for p in all_pts) - 5, max(p[0] for p in all_pts) + 5
    min_y, max_y = min(p[1] for p in all_pts) - 5, max(p[1] for p in all_pts) + 5
    bounds = [[min_y, min_x], [max_y, max_x]]

    # Same map setup as the 2D Folium floor map (zoom behaviour, background, axes, autoscale)
    m = folium.Map(crs="Simple", tiles=None, zoom_control=True, scroll_wheel_zoom=True,
                   zoomSnap=0.25, zoomDelta=0.5, attribution_control=False)
    m.get_root().header.add_child(folium.Element(FOLIUM_BASE_CSS))

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
            hover = build_route_hover(route_path, MULTI_CAD_NODES, 3, current_lang)
            add_animated_route(m, line_pts, route_color, hover=hover)

    add_door_markers_2d(m, 3, current_lang, radius=3)
    add_parking_infrastructure_markers(m, current_lang)

    AxisGrid().add_to(m)
    m.fit_bounds(bounds)
    AutoscaleControl(bounds, AUTOSCALE_LABELS.get(current_lang, AUTOSCALE_LABELS["English"])).add_to(m)
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

def describe_point(x, y, z, lang):
    """Name of the POI/room that a clicked map point falls in, or None."""
    room_id = find_room_at(x, y, z)
    if not room_id:
        return None
    return POI_TRANSLATIONS.get(lang, {}).get(room_id, room_id).split("(")[0].strip()

def format_location_label(loc, lang):
    if isinstance(loc, tuple):
        point_lbl = POINT_LABELS.get(lang, "Point")
        poi_name = describe_point(loc[0], loc[1], loc[2], lang)
        coords_txt = f"{point_lbl} ({loc[0]:.1f}, {loc[1]:.1f})"
        prefix = f"[{floor_code_for(loc[2])}]"
        return f"{prefix} {poi_name} – {coords_txt}" if poi_name else f"{prefix} {coords_txt}"

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
        coords_txt = f"{POINT_LABELS.get(lang, 'Point')} ({x:.1f}, {y:.1f})"
        poi_name = describe_point(x, y, z, lang)
        return f"{poi_name} – {coords_txt}" if poi_name else f"📍{coords_txt}"
    if node_id.startswith(DOOR_PREFIX):
        room_id = node_id[len(DOOR_PREFIX):]
        room_name = POI_TRANSLATIONS.get(lang, {}).get(room_id, room_id).split("(")[0].strip()
        return f"{room_name} ({DOOR_LABELS.get(lang, DOOR_LABELS['English'])})"
    if node_id.startswith("H_L"):
        # Corridor junctions are named after the main corridor of their floor
        corridor_id = FLOOR_CORRIDOR.get(int(node_coords[node_id][2]))
        if corridor_id:
            return POI_TRANSLATIONS.get(lang, {}).get(corridor_id, corridor_id)
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

    # Build a list of items first so that consecutive walking steps toward the same
    # place can be merged into one (distances are added together).
    items = []

    start_poi = get_node_display_name(path[0], lang, node_coords)
    first_dest_poi = get_node_display_name(path[1], lang, node_coords)
    items.append({
        "kind": "start", "poi": start_poi, "target": first_dest_poi,
        "dist": euclidean_distance_3d(path[0], path[1], node_coords),
    })

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

            items.append({"kind": "transit", "icon": icon, "text": trans_text.get(lang, trans_text["English"])})
            continue

        step_dist = euclidean_distance_3d(curr_node, next_node, node_coords)

        # Same place as the previous walking step: extend that step instead of adding a new one
        if items[-1]["kind"] in ("start", "walk") and items[-1]["target"] == next_poi:
            items[-1]["dist"] += step_dist
            continue

        next_heading = calculate_heading_angle(curr_node, next_node, node_coords)
        if node_coords[prev_node][2] != node_coords[curr_node][2]:
            # Just arrived from another floor: there is no meaningful incoming heading
            prev_heading = next_heading
        else:
            prev_heading = calculate_heading_angle(prev_node, curr_node, node_coords)

        items.append({"kind": "walk", "target": next_poi, "dist": step_dist, "angle": next_heading - prev_heading})

    # Render the items into numbered steps
    directions = []
    for item in items:
        if item["kind"] == "start":
            start_text = {
                "English": f"Start at **{item['poi']}** and head towards **{item['target']}** ({item['dist']:.1f}m).",
                "Simplified Chinese": f"从 **{item['poi']}** 出发，前往 **{item['target']}**（{item['dist']:.1f} 米）。",
                "Malay": f"Mula di **{item['poi']}** dan menuju ke **{item['target']}** ({item['dist']:.1f}m)."
            }
            directions.append({"step": len(directions) + 1, "text": start_text.get(lang, start_text["English"]), "icon": "🛫"})
        elif item["kind"] == "transit":
            directions.append({"step": len(directions) + 1, "text": item["text"], "icon": item["icon"]})
        else:
            instruction_str = format_turn_instruction(item["angle"], item["dist"], f"**{item['target']}**", lang=lang)
            angle_norm = (item["angle"] + 180) % 360 - 180
            icon = "↪️" if angle_norm < -22.5 else ("↩️" if angle_norm > 22.5 else "⬆️")
            directions.append({"step": len(directions) + 1, "text": instruction_str, "icon": icon})

    final_poi = get_node_display_name(path[-1], lang, node_coords)
    arrival_text = {
        "English": f"You have arrived at your destination: **{final_poi}**.",
        "Simplified Chinese": f"您已到达目的地：**{final_poi}**。",
        "Malay": f"Anda telah tiba di destinasi: **{final_poi}**."
    }
    directions.append({"step": len(directions) + 1, "text": arrival_text.get(lang, arrival_text["English"]), "icon": "🏁"})

    return directions

def compute_route_summary(path, node_coords, lang="English"):
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
        # Number of steps in the written directions (after merging repeated steps)
        "steps": len(generate_detailed_directions(path, node_coords, lang=lang))
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

def _point_xyz(value):
    """(x, y, floor) of a route item: a clicked point or a room (its centre node)."""
    if isinstance(value, tuple):
        return value
    return MULTI_CAD_NODES[value] if value in MULTI_CAD_NODES else None

def editable_targets():
    """Start, every stop and the destination as [(target, (x, y, floor)), ...].
    A target is ("start", None), ("wp", waypoint_id) or ("dest", None)."""
    items = [(("start", None), _point_xyz(st.session_state.selected_start))]
    for wp in st.session_state.waypoints:
        if isinstance(wp, dict):
            items.append((("wp", wp["id"]), _point_xyz(wp["value"])))
    items.append((("dest", None), _point_xyz(st.session_state.selected_dest)))
    return [(tg, xyz) for tg, xyz in items if xyz is not None]

def find_marker_at(raw_point, radius=4.0, pin_offset=0.0):
    """Start/stop/destination marker closest to a clicked point on the same floor (within `radius`
    metres), or None. `pin_offset` also accepts clicks that far above the marker's position
    (Folium pins are drawn above the spot they point at)."""
    px, py, pz = raw_point
    best, best_d = None, radius
    for target, (x, y, z) in editable_targets():
        if int(z) != int(pz):
            continue
        d = min(math.hypot(px - x, py - y), math.hypot(px - x, py - (y + pin_offset)))
        if d <= best_d:
            best, best_d = target, d
    return best

def current_edit_target():
    """The marker being moved, or None (also None if it no longer exists)."""
    target = st.session_state.edit_target
    if target is not None and target not in [tg for tg, _ in editable_targets()]:
        st.session_state.edit_target = target = None
    return target

def apply_edit(target, raw_point):
    kind, wp_id = target
    if kind == "start":
        st.session_state.selected_start = raw_point
    elif kind == "dest":
        st.session_state.selected_dest = raw_point
    else:
        for wp in st.session_state.waypoints:
            if wp["id"] == wp_id:
                wp["value"] = raw_point
                break

def handle_map_click(raw_point, pin_offset=0.0):
    """Apply a clicked map point (x, y, floor).
    While picking a route on the map it follows the pick step. Otherwise clicking the start, a stop
    or the destination selects it, and the next click on the map moves it there."""
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
        return

    target = current_edit_target()
    hit = find_marker_at(raw_point, pin_offset=pin_offset)
    if target is None:
        if hit is not None:                      # pick a marker to move
            st.session_state.edit_target = hit
            st.rerun()
        return                                   # a click on empty map changes nothing
    if hit is not None:                          # click on a marker: switch to it, or cancel on the same one
        st.session_state.edit_target = None if hit == target else hit
        st.rerun()
    apply_edit(target, raw_point)
    st.session_state.edit_target = None
    st.rerun()

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
    view_type = st.radio(t["view_mode"], options=[t["view_2d_folium"], t["view_2d"], t["view_3d"]], horizontal=True)
    show_doors = st.checkbox(t["show_doors"], value=True)

    col_btn_pick, col_btn_clear = st.columns([0.7, 0.3])
    with col_btn_pick:
        if not st.session_state.map_pick_mode:
            if st.button(t["btn_interactive_pick"], use_container_width=True, type="primary"):
                st.session_state.map_pick_mode = True
                st.session_state.map_pick_step = "START"
                st.session_state.edit_target = None
                st.rerun()
        else:
            if st.button(t["btn_cancel_interactive"], use_container_width=True):
                st.session_state.map_pick_mode = False
                st.session_state.map_pick_step = "START"
                st.rerun()

    with col_btn_clear:
        if st.button(t["btn_reset_all"], use_container_width=True):
            st.session_state.waypoints = []
            st.session_state.edit_target = None
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

    # ---- Moving an existing start / stop / destination ----
    edit_target = None if st.session_state.map_pick_mode else current_edit_target()
    highlight_xyz = None
    if edit_target is not None:
        highlight_xyz = dict(editable_targets())[edit_target]
        kind, wp_id = edit_target
        if kind == "start":
            edit_msg = t["editing_start"]
        elif kind == "dest":
            edit_msg = t["editing_dest"]
        else:
            idx = [wp["id"] for wp in st.session_state.waypoints].index(wp_id) + 1
            edit_msg = t["editing_stop"].format(idx=idx)
        col_edit_msg, col_edit_cancel = st.columns([0.72, 0.28])
        with col_edit_msg:
            st.warning(edit_msg)
        with col_edit_cancel:
            if st.button(t["btn_cancel_edit"], use_container_width=True):
                st.session_state.edit_target = None
                st.rerun()
    elif not st.session_state.map_pick_mode and view_type != t["view_3d"]:
        st.caption(t["edit_hint"])

    # ---- Render the selected map view ----
    if view_type in (t["view_2d_folium"], t["view_2d"]):
        floor_select = st.selectbox(
            t["active_floor"],
            options=[0, 1, 2, 3],
            format_func=lambda x: get_translated_floor_name(x, lang=st.session_state.lang)
        )

        if view_type == t["view_2d_folium"]:
            base_map, route_layer = render_2d_folium_view(
                floor_select,
                route_path=path,
                node_coords_dict=temp_nodes,
                current_lang=st.session_state.lang,
                stop_ids=stop_ids,
                show_dest=not st.session_state.map_pick_mode,
                show_doors=show_doors,
                highlight=highlight_xyz,
            )
            st.caption(t["map_nav_hint_folium"])
            folium_kwargs = dict(
                height=620, use_container_width=True, key=f"map2d_folium_{floor_select}",
                returned_objects=["last_clicked"],   # no pan/zoom reruns
            )
            # Same as the Smart Parking map: the route is part of the map itself, so the
            # moving-arrow script runs normally (the map is rebuilt on each new click).
            base_map.add_child(route_layer)
            map_data = st_folium(base_map, **folium_kwargs)

            if map_data and map_data.get("last_clicked"):
                click = map_data["last_clicked"]
                raw_point = (round(click["lng"], 2), round(click["lat"], 2), floor_select)
                click_key = f"folium_{floor_select}"
                # The component remembers its last click, so only act on a new one
                if raw_point != st.session_state.last_folium_clicks.get(click_key):
                    st.session_state.last_folium_clicks[click_key] = raw_point
                    handle_map_click(raw_point, pin_offset=3.0)

        else:
            fig_2d = render_2d_plotly_view(
                floor_select,
                route_path=path,
                node_coords_dict=temp_nodes,
                current_lang=st.session_state.lang,
                stop_ids=stop_ids,
                show_dest=not st.session_state.map_pick_mode,
                show_doors=show_doors,
                highlight=highlight_xyz,
            )
            st.caption(t["map_nav_hint"])
            map_event = st.plotly_chart(
                fig_2d,
                use_container_width=True,
                key=f"map2d_floor_{floor_select}",
                on_select="rerun",
                selection_mode="points",
                config={"scrollZoom": True, "displaylogo": False, "modeBarButtonsToRemove": ["select2d", "lasso2d"]},
            )

            clicked_points = []
            if map_event and "selection" in map_event and "points" in map_event["selection"]:
                clicked_points = map_event["selection"]["points"]

            if clicked_points:
                pt = clicked_points[0]
                raw_point = (round(float(pt["x"]), 2), round(float(pt["y"]), 2), floor_select)

                # The selection persists across reruns, so only act on a new click
                if raw_point != st.session_state.last_processed_click:
                    st.session_state.last_processed_click = raw_point
                    handle_map_click(raw_point)
            else:
                st.session_state.last_processed_click = None
    else:
        fig_3d, arrow3d_payload = render_3d_isometric_view(route_path=path, node_coords=temp_nodes, current_lang=st.session_state.lang, show_doors=show_doors)
        components.html(render_3d_html(fig_3d, arrow3d_payload, st.session_state.lang, height=680),
                        height=730, scrolling=False)

# ------------------------------------------------------------------------------
# Directions Tab
# ------------------------------------------------------------------------------
with tab_dir:
    st.subheader(t["route_summary"])

    if path and len(path) > 1:
        summary = compute_route_summary(path, temp_nodes, lang=st.session_state.lang)
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
            show_parking_map(assigned_slot, entry_path, curr_lang, "#2563EB", "park_entry_map")

            if entry_path:
                entry_summary = compute_route_summary(entry_path, MULTI_CAD_NODES, lang=curr_lang)
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
            show_parking_map(assigned_slot, exit_path, curr_lang, "#F97316", "park_exit_map")

            if exit_path:
                exit_summary = compute_route_summary(exit_path, MULTI_CAD_NODES, lang=curr_lang)
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
        show_parking_map(None, [], curr_lang, "#2563EB", "park_empty_map")

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
