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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
