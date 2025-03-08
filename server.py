import re
import json
import logging
import sys
from typing import Dict, Any, List, Optional, Union

from mcp.server.fastmcp import FastMCP

# 使用絕對導入
from ntpc_opendata_tool.utils.logger import setup_logger
from ntpc_opendata_tool.api.bus import BusAPI
from ntpc_opendata_tool.api.traffic import TrafficAPI
from ntpc_opendata_tool.api.parking import ParkingAPI
from ntpc_opendata_tool.api.bike import BikeAPI
from ntpc_opendata_tool.api.misc_traffic import MiscTrafficAPI
from ntpc_opendata_tool.api.client import APIError

# 設置日誌
logger = setup_logger("ntpc_opendata_mcp")

# 初始化 API 客戶端
bus_api = BusAPI()
traffic_api = TrafficAPI() 
parking_api = ParkingAPI()
bike_api = BikeAPI()
misc_traffic_api = MiscTrafficAPI()

app = FastMCP()

@app.get("/")
def root():
    return {"message": "新北市交通局開放資料 API"}

# 公車相關 API
@app.get("/bus/routes")
def get_bus_routes(route_name: Optional[str] = None, page: int = 0, size: int = 100):
    try:
        return bus_api.get_routes(route_name, page, size)
    except APIError as e:
        logger.error(f"獲取公車路線失敗: {e.message}")
        return {"error": e.message, "status_code": e.status_code}

@app.get("/bus/stops")
def get_bus_stops(route_name: str):
    try:
        return bus_api.get_stops(route_name)
    except APIError as e:
        logger.error(f"獲取公車站點失敗: {e.message}")
        return {"error": e.message, "status_code": e.status_code}

@app.get("/bus/arrival")
def get_bus_arrival(route_name: str, stop_name: Optional[str] = None):
    try:
        return bus_api.get_estimated_time(route_name, stop_name)
    except APIError as e:
        logger.error(f"獲取公車到站時間失敗: {e.message}")
        return {"error": e.message, "status_code": e.status_code}

@app.get("/bus/all-stops")
def get_all_bus_stops():
    try:
        return bus_api.get_all_stops()
    except APIError as e:
        logger.error(f"獲取所有公車站點失敗: {e.message}")
        return {"error": e.message, "status_code": e.status_code}

@app.get("/bus/search-by-stop")
def search_bus_by_stop(stop_name: str):
    try:
        return bus_api.search_by_stop(stop_name)
    except APIError as e:
        logger.error(f"根據站點搜尋公車失敗: {e.message}")
        return {"error": e.message, "status_code": e.status_code}

@app.get("/bus/real-time")
def get_bus_real_time(route_name: str):
    try:
        return bus_api.get_real_time_by_route(route_name)
    except APIError as e:
        logger.error(f"獲取公車即時位置失敗: {e.message}")
        return {"error": e.message, "status_code": e.status_code}

# 交通相關 API
@app.get("/traffic/status")
def get_traffic_status(area: Optional[str] = None, road: Optional[str] = None):
    try:
        return traffic_api.get_traffic_status(area, road)
    except APIError as e:
        logger.error(f"獲取交通狀況失敗: {e.message}")
        return {"error": e.message, "status_code": e.status_code}

@app.get("/traffic/construction")
def get_construction_info(area: Optional[str] = None, road: Optional[str] = None):
    try:
        return traffic_api.get_construction_info(area, road)
    except APIError as e:
        logger.error(f"獲取施工資訊失敗: {e.message}")
        return {"error": e.message, "status_code": e.status_code}

@app.get("/traffic/cameras")
def get_traffic_cameras(area: Optional[str] = None):
    try:
        return traffic_api.get_traffic_cameras(area)
    except APIError as e:
        logger.error(f"獲取交通攝影機失敗: {e.message}")
        return {"error": e.message, "status_code": e.status_code}

@app.get("/traffic/incidents")
def get_traffic_incidents(area: Optional[str] = None):
    try:
        return traffic_api.get_traffic_incidents(area)
    except APIError as e:
        logger.error(f"獲取交通事件失敗: {e.message}")
        return {"error": e.message, "status_code": e.status_code}

# 停車場相關 API
@app.get("/parking/lots")
def get_parking_lots(area: Optional[str] = None, type_name: Optional[str] = None):
    try:
        if area:
            return parking_api.get_parking_lots_by_area(area)
        elif type_name:
            return parking_api.get_parking_lots_by_type(type_name)
        else:
            return parking_api.get_all_parking_lots()
    except APIError as e:
        logger.error(f"獲取停車場資訊失敗: {e.message}")
        return {"error": e.message, "status_code": e.status_code}

@app.get("/parking/lot/{parking_id}")
def get_parking_lot_by_id(parking_id: str):
    try:
        return parking_api.get_parking_lot_by_id(parking_id)
    except APIError as e:
        logger.error(f"獲取停車場詳細資訊失敗: {e.message}")
        return {"error": e.message, "status_code": e.status_code}

@app.get("/parking/available")
def get_available_parking_lots(min_spaces: Optional[int] = None):
    try:
        return parking_api.get_available_parking_lots(min_spaces)
    except APIError as e:
        logger.error(f"獲取有空位的停車場失敗: {e.message}")
        return {"error": e.message, "status_code": e.status_code}

@app.get("/parking/nearby")
def find_nearby_parking(longitude: float, latitude: float, radius: Optional[int] = None):
    try:
        return parking_api.find_nearby_parking(longitude, latitude, radius)
    except APIError as e:
        logger.error(f"搜尋附近停車場失敗: {e.message}")
        return {"error": e.message, "status_code": e.status_code}

# 自行車相關 API
@app.get("/bike/youbike")
def get_youbike_stations(area: Optional[str] = None):
    try:
        return bike_api.get_youbike_stations(area)
    except APIError as e:
        logger.error(f"獲取 YouBike 站點資訊失敗: {e.message}")
        return {"error": e.message, "status_code": e.status_code}

@app.get("/bike/available-bikes")
def get_available_youbikes(min_bikes: int = 1):
    try:
        return bike_api.get_available_youbikes(min_bikes)
    except APIError as e:
        logger.error(f"獲取有可借車輛的 YouBike 站點失敗: {e.message}")
        return {"error": e.message, "status_code": e.status_code}

@app.get("/bike/nearby-youbike")
def find_nearby_youbike(latitude: float, longitude: float, radius: int = 500):
    try:
        return bike_api.find_nearby_youbike(latitude, longitude, radius)
    except APIError as e:
        logger.error(f"搜尋附近 YouBike 站點失敗: {e.message}")
        return {"error": e.message, "status_code": e.status_code}

@app.get("/bike/bike-racks")
def get_bike_racks(area: Optional[str] = None, near_mrt: bool = False):
    try:
        return bike_api.get_bike_racks(area, near_mrt)
    except APIError as e:
        logger.error(f"獲取自行車架資訊失敗: {e.message}")
        return {"error": e.message, "status_code": e.status_code}

@app.get("/bike/bike-lanes")
def get_bike_lanes():
    try:
        return bike_api.get_bike_lanes()
    except APIError as e:
        logger.error(f"獲取自行車道建設統計資料失敗: {e.message}")
        return {"error": e.message, "status_code": e.status_code}

# 其他交通服務相關 API
@app.get("/misc-traffic/taxi-services")
def get_taxi_services():
    try:
        return misc_traffic_api.get_taxi_services()
    except APIError as e:
        logger.error(f"獲取計程車客運服務業者資訊失敗: {e.message}")
        return {"error": e.message, "status_code": e.status_code}

@app.get("/misc-traffic/search-taxi")
def search_taxi_service(keyword: str):
    try:
        return misc_traffic_api.search_taxi_service(keyword)
    except APIError as e:
        logger.error(f"關鍵字搜尋計程車服務失敗: {e.message}")
        return {"error": e.message, "status_code": e.status_code}

@app.get("/misc-traffic/towing-storage")
def get_towing_storage_info():
    try:
        return misc_traffic_api.get_towing_storage_info()
    except APIError as e:
        logger.error(f"獲取拖吊保管場資訊失敗: {e.message}")
        return {"error": e.message, "status_code": e.status_code}

@app.get("/misc-traffic/nearest-towing")
def find_nearest_towing_storage(latitude: float, longitude: float):
    try:
        return misc_traffic_api.find_nearest_towing_storage(latitude, longitude)
    except APIError as e:
        logger.error(f"搜尋最近的拖吊保管場失敗: {e.message}")
        return {"error": e.message, "status_code": e.status_code}

@app.get("/misc-traffic/impact-assessment")
def get_traffic_impact_assessment():
    try:
        return misc_traffic_api.get_traffic_impact_assessment()
    except APIError as e:
        logger.error(f"獲取建築物交通影響評估資訊失敗: {e.message}")
        return {"error": e.message, "status_code": e.status_code}

def _is_bus_query(self, query: str) -> bool:
    """判斷是否為公車相關查詢"""
    bus_keywords = {
        "路線": ["公車", "巴士", "路線", "幾號", "班次", "路線圖", "路線時刻"],
        "站點": ["站牌", "站點", "車站", "站", "下車", "上車"],
        "到站": ["幾分鐘", "到站", "進站", "抵達", "還要多久", "什麼時候到"],
        "時刻": ["發車", "末班", "首班", "班次", "時刻表", "幾點"],
        "業者": ["公車處", "客運", "業者", "哪家"],
        "優惠": ["轉乘", "優惠", "票價", "多少錢", "費用"]
    }
    
    # 檢查是否包含路線號碼
    route_patterns = [
        r'\d+[a-zA-Z]?(?:路|線|公車|號)',  # 一般路線，如 307, 307A
        r'[藍紅綠橘棕]\d+',                # 藍線等，如 藍1
        r'F\d+',                          # F開頭路線，如 F501
    ]
    
    # 檢查關鍵字
    for category, keywords in bus_keywords.items():
        if any(keyword in query for keyword in keywords):
            return True
            
    # 檢查路線號碼
    for pattern in route_patterns:
        if re.search(pattern, query):
            return True
            
    return False

def _is_bike_query(self, query: str) -> bool:
    """判斷是否為自行車相關查詢"""
    bike_keywords = {
        "系統": ["youbike", "ubike", "微笑單車", "共享單車"],
        "設施": ["自行車道", "腳踏車道", "單車道", "自行車架", "單車架", "停車架"],
        "狀態": ["可以借", "有車", "可借", "可還", "車位", "空位"],
        "位置": ["在哪", "附近", "哪裡有", "距離", "多遠"]
    }
    
    # 檢查自行車相關詞
    base_terms = ["自行車", "腳踏車", "單車", "bike"]
    if any(term in query.lower() for term in base_terms):
        return True
        
    # 檢查關鍵字組合
    for category, keywords in bike_keywords.items():
        if any(keyword.lower() in query.lower() for keyword in keywords):
            return True
            
    return False

def _is_parking_query(self, query: str) -> bool:
    """判斷是否為停車場相關查詢"""
    parking_keywords = {
        "一般": ["停車場", "停車", "泊車", "車位", "停車格"],
        "費用": ["收費", "費率", "計費", "票價", "多少錢"],
        "狀態": ["有位子", "有空位", "滿了", "客滿", "可以停"],
        "特殊": ["婦幼", "身障", "殘障", "機車", "汽車"],
        "緊急": ["颱風", "防災", "臨時", "緊急"]
    }
    
    # 檢查關鍵字組合
    for category, keywords in parking_keywords.items():
        if any(keyword in query for keyword in keywords):
            return True
            
    # 檢查問句模式
    parking_patterns = [
        r'停車.*在哪',
        r'哪裡.*停車',
        r'可以停.*車',
        r'車.*停在哪'
    ]
    
    for pattern in parking_patterns:
        if re.search(pattern, query):
            return True
            
    return False

def _is_traffic_query(self, query: str) -> bool:
    """判斷是否為交通狀況相關查詢"""
    traffic_keywords = {
        "路況": ["塞車", "壅塞", "順暢", "車多", "車流", "車速"],
        "監控": ["監視器", "攝影機", "即時影像", "路況", "etag"],
        "施工": ["施工", "封路", "改道", "維修", "工程"],
        "事件": ["事故", "車禍", "故障", "拋錨", "事件"],
        "限制": ["限高", "限重", "禁行", "單行"]
    }
    
    # 檢查關鍵字組合
    for category, keywords in traffic_keywords.items():
        if any(keyword in query for keyword in keywords):
            return True
            
    # 檢查問句模式
    traffic_patterns = [
        r'路況.*如何',
        r'交通.*狀況',
        r'好不好走',
        r'塞不塞'
    ]
    
    for pattern in traffic_patterns:
        if re.search(pattern, query):
            return True
            
    return False

def _is_misc_traffic_query(self, query: str) -> bool:
    """判斷是否為其他交通服務相關查詢"""
    misc_keywords = {
        "計程車": ["計程車", "taxi", "叫車", "車行"],
        "拖吊": ["拖吊", "保管場", "被拖", "領車"],
        "評估": ["交通影響", "評估", "交評", "影響評估"]
    }
    
    # 檢查關鍵字組合
    for category, keywords in misc_keywords.items():
        if any(keyword.lower() in query.lower() for keyword in keywords):
            return True
            
    return False

def _get_help_message(self) -> str:
    """獲取幫助信息"""
    return """### 新北市交通局開放資料查詢助手

我可以協助您查詢以下交通相關資訊：

🚌 公車資訊
- 路線查詢：「307公車怎麼走？」
- 到站時間：「307公車什麼時候到捷運板橋站？」
- 站點查詢：「捷運板橋站有哪些公車？」
- 路線類型：「板橋有哪些快速公車？」
- 轉乘優惠：「哪些公車有轉乘優惠？」

🚲 自行車資訊
- YouBike站點：「板橋火車站附近有YouBike嗎？」
- 即時車位：「哪些YouBike站還有車可以借？」
- 自行車道：「板橋區的自行車道在哪裡？」
- 停車架：「捷運站附近有自行車架嗎？」

🅿️ 停車資訊
- 停車場查詢：「板橋車站附近有停車場嗎？」
- 即時空位：「板橋哪些停車場還有空位？」
- 收費標準：「板橋停車場要收多少錢？」
- 特殊車位：「板橋區有哪些婦幼停車位？」

🚦 交通狀況
- 即時路況：「板橋往台北現在塞車嗎？」
- 施工資訊：「板橋區最近有哪裡在施工？」
- 交通事件：「板橋區有發生車禍嗎？」
- 監視器：「板橋區有哪些交通監視器？」

🚕 其他服務
- 計程車：「板橋區有哪些合法計程車行？」
- 拖吊服務：「我的車被拖吊了要去哪裡領？」
- 交通評估：「新板特區的交通影響評估如何？」

您可以用自然的方式詢問，我會協助您找到需要的資訊。
需要範例可以輸入「範例」或「使用說明」。"""

def _format_no_result_message(self, query_type: str, area: Optional[str] = None) -> str:
    """格式化無結果時的提示訊息"""
    messages = {
        "bus": f"抱歉，找不到相關的公車資訊。您可以：\n"
              f"1. 確認路線號碼是否正確\n"
              f"2. 使用較寬鬆的搜尋條件\n"
              f"3. 改用站點名稱搜尋\n"
              f"4. 查詢附近的其他站點",
        
        "bike": f"抱歉，找不到相關的自行車資訊。您可以：\n"
               f"1. 擴大搜尋範圍\n"
               f"2. 查詢附近的其他站點\n"
               f"3. 使用座標搜尋附近站點",
        
        "parking": f"抱歉，找不到相關的停車場資訊。您可以：\n"
                  f"1. 查詢附近的其他停車場\n"
                  f"2. 嘗試不同類型的停車場\n"
                  f"3. 查詢路邊停車格",
        
        "traffic": f"抱歉，找不到相關的交通狀況資訊。您可以：\n"
                  f"1. 查詢主要道路的狀況\n"
                  f"2. 使用交通監視器查看即時狀況\n"
                  f"3. 查詢特定路段的施工資訊",
        
        "misc": f"抱歉，找不到相關的交通服務資訊。您可以：\n"
               f"1. 使用其他關鍵字搜尋\n"
               f"2. 查詢鄰近區域的服務\n"
               f"3. 聯繫交通局詢問更多資訊"
    }
    
    base_message = messages.get(query_type, "抱歉，找不到相關資訊。")
    if area:
        base_message = f"{area}地區：{base_message}"
        
    return base_message

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
