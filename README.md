# MCP 工具：新北市交通局 OpenData 查詢

這是一個 MCP（Multi-Cloud Platform）工具，用於查詢新北市交通局的開放資料（OpenData）。該工具允許使用者直接在 Claude 中查詢新北市交通相關的開放資料應用，並獲取回應。

## 功能特點

- 整合新北市交通局 OpenData API
- 提供簡單的命令列介面
- 支援多種交通資料查詢（如公車路線、站點資訊、即時交通狀況等）
- 資料過濾與排序選項
- 錯誤處理與友善提示
- MCP 服務整合

## 安裝

### 使用虛擬環境

```bash
# 建立虛擬環境
python -m venv .venv

# 啟動虛擬環境
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate     # Windows

# 安裝依賴
pip install -e .
```

### 使用 MCP 安裝

```bash
mcp install ntpc_opendata_tool/server.py --name "新北市交通 OpenData 查詢" --with requests --with python-dotenv --with uvicorn --with typer --with pandas
```

## 使用方法

### 命令列工具

```bash
# 基本使用
ntpc-opendata --help

# 查詢公車路線
ntpc-opendata bus routes 307

# 查詢站點資訊
ntpc-opendata bus search-by-stop "捷運板橋站"

# 查詢即時交通狀況
ntpc-opendata traffic status --area "板橋區"

# 查詢 YouBike 站點
ntpc-opendata bike youbike --area "板橋區"

# 查詢停車場
ntpc-opendata parking list --area "板橋區"
```

### 作為 MCP 服務使用

在 Claude 中，可以直接調用此 MCP 服務：

```
我想查詢新北市307公車的路線資訊。
```

## API 模組資源

本工具提供了多個 API 模組，可以在您的 Python 程式中直接使用：

### 公車資訊 (BusAPI)

```python
from ntpc_opendata_tool.api.bus import BusAPI

bus_api = BusAPI()

# 查詢公車路線
routes = bus_api.get_routes(route_name="307")

# 查詢公車站點
stops = bus_api.get_stops(route_name="307")

# 查詢公車預計到站時間
estimated_times = bus_api.get_estimated_time(route_name="307", stop_name="捷運板橋站")

# 查詢所有站點
all_stops = bus_api.get_all_stops()

# 依站點名稱搜尋
stop_search = bus_api.search_by_stop(stop_name="捷運板橋站")

# 查詢公車即時位置
real_time = bus_api.get_real_time_by_route(route_name="307")

# 查詢公車業者資訊
operators = bus_api.get_bus_operators()

# 查詢公車轉乘優惠
discounts = bus_api.get_bus_transfer_discounts()

# 查詢路線資訊
route_info = bus_api.get_route_info(route_type="快速公車", route_name="307")
```

### 自行車資訊 (BikeAPI)

```python
from ntpc_opendata_tool.api.bike import BikeAPI

bike_api = BikeAPI()

# 查詢 YouBike 站點
youbike_stations = bike_api.get_youbike_stations(area="板橋區")

# 查詢可用 YouBike
available_bikes = bike_api.get_available_youbikes(min_bikes=5)

# 查詢附近 YouBike 站點
nearby_youbike = bike_api.find_nearby_youbike(lat=25.0132, lon=121.4670, radius=500)

# 查詢自行車架
bike_racks = bike_api.get_bike_racks(area="板橋區", near_mrt=True)

# 查詢自行車道
bike_lanes = bike_api.get_bike_lanes()
```

### 停車場資訊 (ParkingAPI)

```python
from ntpc_opendata_tool.api.parking import ParkingAPI

parking_api = ParkingAPI()

# 查詢停車場
parking_lots = parking_api.get_parking_lots(area="板橋區")

# 查詢特定類型停車場
type_parking = parking_api.get_parking_lots_by_type(lot_type="路邊停車")

# 查詢停車場詳情
parking_detail = parking_api.get_parking_lot_detail(parking_id="P-TY-0001")

# 查詢有空位的停車場
available_parking = parking_api.get_available_parking_lots(min_spaces=5, area="板橋區")

# 查詢路邊停車格
roadside_parking = parking_api.get_roadside_parking_spaces(area="板橋區")

# 查詢附近停車場
nearby_parking = parking_api.get_nearby_parking_lots(lat=25.0132, lon=121.4670, radius=500)

# 查詢機車停車場
motorcycle_parking = parking_api.get_motorcycle_parking(area="板橋區")

# 查詢婦幼停車位
women_children_parking = parking_api.get_women_children_parking(area="板橋區")

# 查詢身障停車位
disabled_parking = parking_api.get_disabled_parking(area="板橋區")

# 查詢颱風期間可停車路段
typhoon_parking = parking_api.get_typhoon_parking()

# 查詢路邊停車管理資訊
roadside_management = parking_api.get_roadside_parking_management()
```

### 交通資訊 (TrafficAPI)

```python
from ntpc_opendata_tool.api.traffic import TrafficAPI

traffic_api = TrafficAPI()

# 查詢交通監視器
cameras = traffic_api.get_traffic_cameras(district="板橋區")

# 查詢 ETag 位置
etag_locations = traffic_api.get_etag_locations(district="板橋區")

# 查詢限高資訊
height_limits = traffic_api.get_height_limit_info(area="板橋區", road="文化路")

# 查詢交通影響評估
impact_assessments = traffic_api.get_traffic_impact_assessment()

# 查詢附近交通監視器
nearby_cameras = traffic_api.get_nearby_traffic_cameras(lat=25.0132, lon=121.4670, radius=1000)
```

### 其他交通資訊 (MiscTrafficAPI)

```python
from ntpc_opendata_tool.api.misc_traffic import MiscTrafficAPI

misc_api = MiscTrafficAPI()

# 查詢計程車服務
taxi_services = misc_api.get_taxi_services()

# 查詢拖吊保管場資訊
towing_storage = misc_api.get_towing_storage_info()

# 查詢交通影響評估
impact_assessment = misc_api.get_traffic_impact_assessment()

# 查詢最近的拖吊保管場
nearest_towing = misc_api.find_nearest_towing_storage(lat=25.0132, lon=121.4670)

# 搜尋計程車服務
taxi_search = misc_api.search_taxi_service(keyword="大都會")
```

### 基礎 API 客戶端 (OpenDataClient)

```python
from ntpc_opendata_tool.api.client import OpenDataClient

client = OpenDataClient()

# 直接使用資源 ID 查詢
response = client.get_by_resource_id("382000000A-000187-001")

# 自訂 GET 請求
custom_response = client.get("/endpoint", params={"key": "value"})

# 自訂 POST 請求
post_response = client.post("/endpoint", data={"key": "value"})
```

## 開發

### 環境設置

```bash
# 安裝開發依賴
pip install -e ".[dev]"

# 運行測試
pytest
```

### 目錄結構

```
ntpc_opendata_tool/
├── ntpc_opendata_tool/
│   ├── __init__.py
│   ├── api/          # API 調用相關模組
│   ├── cli/          # 命令列介面
│   ├── models/       # 資料模型定義
│   ├── utils/        # 工具函數
│   └── server.py     # MCP 服務主入口
├── pyproject.toml    # 專案設定
├── README.md         # 專案說明
└── .env.example      # 環境變數範例
```

## 授權

本專案採用 MIT 授權。 