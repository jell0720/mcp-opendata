import re
import json
import logging
import sys
import uuid
from typing import Dict, Any, List, Optional, Union
import os

# 將目錄加入 Python 路徑
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

# 生成唯一的 UUID，用於服務器實例標識
SERVER_UUID = str(uuid.uuid4())

class NTPCOpenDataMCP(FastMCP):
    """新北市交通局 OpenData MCP 服務器"""
    
    def __init__(self):
        """初始化 MCP 服務器"""
        super().__init__(
            name="ntpc_opendata_mcp",
            description="新北市交通局開放資料查詢助手",
            version="0.1.0",
            uuid=str(uuid.uuid4())
        )
        
        # 初始化 logger
        self.logger = logging.getLogger("ntpc_opendata_mcp")
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        self.logger.info("初始化新北市交通局 OpenData MCP 服務器")
        
        # 初始化 API 客戶端
        self.bus_api = BusAPI()
        self.traffic_api = TrafficAPI()
        self.parking_api = ParkingAPI()
        self.bike_api = BikeAPI()
        self.misc_traffic_api = MiscTrafficAPI()
        
        # 註冊查詢處理函數
        @self.tool(name="ntpc-query", description="處理交通相關查詢")
        async def handle_query(query: str) -> str:
            """處理用戶查詢
            
            Args:
                query: 用戶查詢內容
                
            Returns:
                MCP 回應
            """
            self.logger.info(f"收到查詢: {query}")
            print(f"收到查詢: {query}", file=sys.stderr)
            
            try:
                # 檢查是否為幫助請求
                if self._is_help_query(query):
                    return self._get_help_message()
                
                # 檢查查詢類型並分發到相應處理函數
                if self._is_bus_query(query):
                    return await self._handle_bus_query(query)
                elif self._is_traffic_query(query):
                    return await self._handle_traffic_query(query)
                elif self._is_parking_query(query):
                    return await self._handle_parking_query(query)
                elif self._is_bike_query(query):
                    return await self._handle_bike_query(query)
                elif self._is_misc_traffic_query(query):
                    return await self._handle_misc_traffic_query(query)
                else:
                    # 一般性查詢，提供幫助信息
                    return f"抱歉，我無法理解您的查詢。以下是我可以提供的服務：\n\n{self._get_help_message()}"
            except APIError as e:
                self.logger.error(f"API 錯誤: {e.message}")
                print(f"API 錯誤: {e.message}", file=sys.stderr)
                return f"抱歉，查詢過程中發生錯誤: {e.message}"
            except Exception as e:
                self.logger.exception(f"未預期錯誤: {str(e)}")
                print(f"未預期錯誤: {str(e)}", file=sys.stderr)
                return f"抱歉，查詢處理過程中發生未預期錯誤: {str(e)}"
    
    def _is_bus_query(self, query: str) -> bool:
        """判斷是否為公車相關查詢"""
        bus_keywords = [
            "公車", "巴士", "路線", "站牌", "站點", "幾分鐘", "到站", "幾號公車",
            "公車路線", "哪些公車", "班次", "公車時刻"
        ]
        return any(keyword in query for keyword in bus_keywords)
    
    def _is_traffic_query(self, query: str) -> bool:
        """判斷是否為交通狀況相關查詢"""
        traffic_keywords = [
            "交通", "路況", "塞車", "施工", "道路", "車流", "車速", "交通狀況",
            "壅塞", "事故", "交通事件", "交通攝影機", "監視器"
        ]
        return any(keyword in query for keyword in traffic_keywords)
    
    def _is_parking_query(self, query: str) -> bool:
        """判斷是否為停車場相關查詢"""
        parking_keywords = [
            "停車", "停車場", "車位", "停車費", "收費標準", "停車資訊",
            "有位子", "有空位", "找車位", "泊車"
        ]
        return any(keyword in query for keyword in parking_keywords)
    
    def _is_bike_query(self, query: str) -> bool:
        """判斷是否為自行車相關查詢"""
        bike_keywords = [
            "自行車", "腳踏車", "單車", "單車路線", "單車站點", "單車時刻",
            "youbike", "ubike", "YouBike", "UBike", "自行車道", "腳踏車道",
            "自行車架", "腳踏車架", "單車架", "自行車站", "腳踏車站", "單車站"
        ]
        return any(keyword in query for keyword in bike_keywords)
    
    def _is_misc_traffic_query(self, query: str) -> bool:
        """判斷是否為其他交通服務相關查詢"""
        misc_traffic_keywords = [
            "其他交通服務", "交通資訊", "交通規劃", "交通管理", "交通諮詢",
            "計程車", "taxi", "Taxi", "TAXI", "拖吊", "保管場", "拖吊保管場",
            "交通影響評估", "交評", "交通服務", "交通局", "運輸局"
        ]
        return any(keyword in query for keyword in misc_traffic_keywords)
    
    def _is_help_query(self, query: str) -> bool:
        """判斷是否為幫助請求"""
        help_keywords = [
            "幫助", "help", "Help", "HELP", "說明", "使用說明", "指南", "使用指南",
            "怎麼用", "如何使用", "功能", "有什麼功能", "能做什麼", "可以做什麼"
        ]
        return any(keyword in query for keyword in help_keywords)
    
    async def _handle_bus_query(self, query: str) -> str:
        """處理公車相關查詢"""
        self.logger.info("處理公車相關查詢")
        print("處理公車相關查詢", file=sys.stderr)
        
        # 嘗試提取公車路線號碼
        route_match = re.search(r'(\d+[a-zA-Z]?|[a-zA-Z]\d+|紅\d+|藍\d+|綠\d+)(?:號|線|路|公車)', query)
        route_name = route_match.group(1) if route_match else None
        
        # 嘗試提取站點名稱
        stop_match = re.search(r'(?:站牌|站點|車站|站)「?([\w\s]+?)」?(?:的|有|到|站|$)', query)
        stop_name = stop_match.group(1) if stop_match else None
        
        try:
            if route_name and "到站" in query:
                # 查詢到站時間
                data = self.bus_api.get_estimated_time(route_name, stop_name)
                return self._format_bus_estimated_time(data, route_name, stop_name)
            elif route_name and ("站牌" in query or "站點" in query):
                # 查詢路線站牌
                data = self.bus_api.get_stops(route_name)
                return self._format_bus_stops(data, route_name)
            elif route_name:
                # 查詢路線資訊
                data = self.bus_api.get_routes(route_name)
                return self._format_bus_routes(data, route_name)
            elif stop_name:
                # 查詢站點經過的公車
                data = self.bus_api.search_by_stop(stop_name)
                return self._format_bus_search_by_stop(data, stop_name)
            else:
                # 一般公車查詢
                return "您似乎在查詢公車資訊，請提供更具體的資訊，例如公車路線號碼或站牌名稱。例如「307公車的路線」或「捷運板橋站有哪些公車」。"
        except APIError as e:
            return f"查詢公車資訊時發生錯誤: {e.message}"
    
    async def _handle_traffic_query(self, query: str) -> str:
        """處理交通狀況相關查詢"""
        self.logger.info("處理交通狀況相關查詢")
        print("處理交通狀況相關查詢", file=sys.stderr)
        
        # 嘗試提取區域
        area_match = re.search(r'([\w]+區)', query)
        area = area_match.group(1) if area_match else None
        
        # 嘗試提取道路名稱
        road_match = re.search(r'([^\s]+(?:路|街|大道|橋))', query)
        road = road_match.group(1) if road_match else None
        
        try:
            if "施工" in query:
                # 查詢道路施工資訊
                data = self.traffic_api.get_construction_info(area)
                return self._format_traffic_construction(data, area)
            elif "攝影機" in query or "監視器" in query or "即時影像" in query:
                # 查詢交通攝影機
                data = self.traffic_api.get_traffic_cameras(area, road)
                return self._format_traffic_cameras(data, area, road)
            elif "事件" in query or "事故" in query:
                # 查詢交通事件
                data = self.traffic_api.get_traffic_incidents(area)
                return self._format_traffic_incidents(data, area)
            else:
                # 查詢交通狀況
                data = self.traffic_api.get_traffic_status(area, road)
                return self._format_traffic_status(data, area, road)
        except APIError as e:
            return f"查詢交通資訊時發生錯誤: {e.message}"
    
    async def _handle_parking_query(self, query: str) -> str:
        """處理停車場相關查詢"""
        self.logger.info("處理停車場相關查詢")
        print("處理停車場相關查詢", file=sys.stderr)
        
        # 嘗試提取區域
        area_match = re.search(r'([\w]+區)', query)
        area = area_match.group(1) if area_match else None
        
        # 嘗試提取停車場類型
        type_match = re.search(r'(路邊停車|立體停車場|地下停車場)', query)
        type_name = type_match.group(1) if type_match else None
        
        try:
            if "收費" in query or "費率" in query or "費用" in query:
                # 查詢停車場收費標準
                data = self.parking_api.get_parking_lots()
                return self._format_parking_fee_rates(data)
            elif "有空位" in query or "有位子" in query or "可以停" in query:
                # 查詢有空位的停車場
                min_spaces = 1
                data = self.parking_api.get_available_parking_lots(min_spaces, area)
                return self._format_parking_available(data, area)
            elif area and type_name:
                # 查詢特定區域和類型的停車場
                data = self.parking_api.get_parking_lots_by_type(type_name)
                # 手動過濾區域
                data = [item for item in data if area in item.get("area", "")]
                return self._format_parking_lots(data, area, type_name)
            elif area:
                # 查詢特定區域的停車場
                data = self.parking_api.get_parking_lots(area)
                return self._format_parking_lots(data, area)
            elif type_name:
                # 查詢特定類型的停車場
                data = self.parking_api.get_parking_lots_by_type(type_name)
                return self._format_parking_lots(data, type_name=type_name)
            else:
                # 一般停車場查詢
                return "您似乎在查詢停車場資訊，請提供更具體的資訊，例如區域或停車場類型。例如「板橋區有哪些停車場」或「新莊區有空位的停車場」。"
        except APIError as e:
            return f"查詢停車場資訊時發生錯誤: {e.message}"
    
    async def _handle_bike_query(self, query: str) -> str:
        """處理自行車相關查詢"""
        try:
            # 嘗試提取路線編號
            route_match = re.search(r'([A-Za-z0-9]+)\s*(?:路線|自行車|腳踏車|單車)', query)
            route_name = route_match.group(1) if route_match else None
            
            # 嘗試提取站點名稱
            stop_match = re.search(r'到\s*([^\s]+)\s*(?:站|站點)', query)
            stop_name = stop_match.group(1) if stop_match else None
            
            # 嘗試提取行政區
            district_match = re.search(r'([^\s]+(?:區|鎮|市))', query)
            district = district_match.group(1) if district_match else None
            
            # 判斷查詢類型
            if "youbike" in query.lower() or "ubike" in query.lower():
                # YouBike 站點查詢
                if district:
                    youbike_stations = self.bike_api.get_youbike_stations(area=district)
                    return self._format_traffic_service_info(youbike_stations, "YouBike 站點")
                else:
                    youbike_stations = self.bike_api.get_youbike_stations()
                    return self._format_traffic_service_info(youbike_stations, "YouBike 站點")
            
            elif "自行車架" in query or "腳踏車架" in query or "單車架" in query:
                # 自行車架查詢
                near_mrt = "捷運" in query or "mrt" in query.lower() or "MRT" in query
                
                if district:
                    bike_racks = self.bike_api.get_bike_racks(area=district, near_mrt=near_mrt)
                    return self._format_traffic_service_info(bike_racks, "自行車架")
                else:
                    bike_racks = self.bike_api.get_bike_racks(near_mrt=near_mrt)
                    return self._format_traffic_service_info(bike_racks, "自行車架")
            
            elif "自行車道" in query or "腳踏車道" in query or "單車道" in query:
                # 自行車道查詢
                bike_lanes = self.bike_api.get_bike_lanes()
                return self._format_traffic_service_info(bike_lanes, "自行車道")
            
            elif "附近" in query or "最近" in query:
                # 查詢附近的 YouBike 站點
                coord_match = re.search(r'座標\s*(\d+\.\d+)\s*,\s*(\d+\.\d+)', query)
                if coord_match:
                    lat = float(coord_match.group(1))
                    lng = float(coord_match.group(2))
                    radius = 500  # 預設搜尋半徑 500 公尺
                    
                    # 嘗試提取搜尋半徑
                    radius_match = re.search(r'(\d+)\s*(?:公尺|米|m)', query)
                    if radius_match:
                        radius = int(radius_match.group(1))
                    
                    nearby_stations = self.bike_api.find_nearby_youbike(lat, lng, radius)
                    return self._format_traffic_service_info(nearby_stations, f"附近 {radius} 公尺內的 YouBike 站點")
                else:
                    return "請提供座標以查詢附近的 YouBike 站點，例如「座標25.0330, 121.5654附近的 YouBike 站點」。"
            
            elif "可借" in query or "有車" in query:
                # 查詢有可借車輛的 YouBike 站點
                min_bikes = 1  # 預設至少有 1 輛可借車輛
                
                # 嘗試提取最少可借車輛數
                min_bikes_match = re.search(r'至少\s*(\d+)\s*(?:輛|台|臺)', query)
                if min_bikes_match:
                    min_bikes = int(min_bikes_match.group(1))
                
                available_stations = self.bike_api.get_available_youbikes(min_bikes)
                return self._format_traffic_service_info(available_stations, f"有至少 {min_bikes} 輛可借車輛的 YouBike 站點")
            
            else:
                # 默認返回所有 YouBike 站點
                youbike_stations = self.bike_api.get_youbike_stations()
                return self._format_traffic_service_info(youbike_stations, "YouBike 站點")
        
        except Exception as e:
            self.logger.error(f"處理自行車查詢時出錯: {str(e)}")
            return f"抱歉，處理您的自行車查詢時出現錯誤: {str(e)}"
    
    async def _handle_misc_traffic_query(self, query: str) -> str:
        """處理其他交通服務相關查詢"""
        try:
            # 嘗試提取服務類型
            service_type = None
            if "計程車" in query or "taxi" in query.lower():
                service_type = "計程車"
                keyword_match = re.search(r'(?:搜尋|查詢)\s*([^\s]+)\s*(?:計程車|的計程車)', query)
                keyword = keyword_match.group(1) if keyword_match else None
                
                if keyword:
                    taxi_services = self.misc_traffic_api.search_taxi_service(keyword)
                    return self._format_traffic_service_info(taxi_services, "計程車服務")
                else:
                    taxi_services = self.misc_traffic_api.get_taxi_services()
                    return self._format_traffic_service_info(taxi_services, "計程車服務")
            
            elif "拖吊" in query or "保管場" in query:
                service_type = "拖吊保管場"
                district_match = re.search(r'([^\s]+(?:區|鎮|市))', query)
                district = district_match.group(1) if district_match else None
                
                if "最近" in query or "附近" in query:
                    # 尋找最近的拖吊保管場
                    # 注意：這裡需要提取座標，但通常用戶不會直接提供座標
                    # 這裡僅作為示例，實際應用可能需要地址轉座標的功能
                    coord_match = re.search(r'座標\s*(\d+\.\d+)\s*,\s*(\d+\.\d+)', query)
                    if coord_match:
                        lat = float(coord_match.group(1))
                        lng = float(coord_match.group(2))
                        nearest = self.misc_traffic_api.find_nearest_towing_storage(lat, lng)
                        if nearest:
                            # 將 Pydantic 模型轉換為字典
                            if hasattr(nearest, 'model_dump'):
                                nearest = nearest.model_dump()
                            return self._format_traffic_service_info([nearest], "最近的拖吊保管場")
                        else:
                            return "找不到附近的拖吊保管場。"
                    else:
                        return "請提供座標以查詢最近的拖吊保管場，例如「座標25.0330, 121.5654附近的拖吊保管場」。"
                
                elif district:
                    # 按區域查詢拖吊保管場
                    towing_storages = self.misc_traffic_api.get_towing_storage_info()
                    # 將 Pydantic 模型轉換為字典
                    if towing_storages and hasattr(towing_storages[0], 'model_dump'):
                        towing_storages_dict = [item.model_dump() for item in towing_storages]
                    else:
                        towing_storages_dict = towing_storages
                    # 過濾特定區域的拖吊保管場
                    filtered_storages = [
                        storage for storage in towing_storages_dict 
                        if district in storage.get("address", "")
                    ]
                    return self._format_traffic_service_info(filtered_storages, "拖吊保管場")
                else:
                    towing_storages = self.misc_traffic_api.get_towing_storage_info()
                    return self._format_traffic_service_info(towing_storages, "拖吊保管場")
            
            elif "交通影響評估" in query or "交評" in query:
                service_type = "交通影響評估"
                assessments = self.misc_traffic_api.get_traffic_impact_assessment()
                return self._format_traffic_service_info(assessments, "交通影響評估")
            
            else:
                # 默認返回計程車服務資訊
                taxi_services = self.misc_traffic_api.get_taxi_services()
                return self._format_traffic_service_info(taxi_services, "計程車服務")
        
        except Exception as e:
            self.logger.error(f"處理其他交通服務查詢時出錯: {str(e)}")
            return f"抱歉，處理您的交通服務查詢時出現錯誤: {str(e)}"
    
    def _format_bus_routes(self, data: List[Dict[str, Any]], route_name: Optional[str] = None) -> str:
        """格式化公車路線資訊"""
        if not data:
            return f"找不到公車路線 {route_name} 的資訊。"
        
        if len(data) == 1:
            route = data[0]
            result = f"### 公車 {route.get('nameZh', '無編號')} 路線資訊\n\n"
            result += f"- **路線 ID**: {route.get('Id', '無資料')}\n"
            result += f"- **營運業者**: {route.get('providerName', '無資料')}\n"
            result += f"- **路線類型**: {route.get('pathAttributeName', '無資料')}\n"
            result += f"- **起點站**: {route.get('departureZh', '無資料')}\n"
            result += f"- **終點站**: {route.get('destinationZh', '無資料')}\n"
            result += f"- **建置期間**: {route.get('buildPeriod', '無資料')}\n"
            
            # 如果有英文資訊，加入雙語顯示
            if route.get('nameEn'):
                result += f"\n**英文路線資訊**:\n"
                result += f"- **Route Name**: {route.get('nameEn', 'N/A')}\n"
                result += f"- **Departure**: {route.get('departureEn', 'N/A')}\n"
                result += f"- **Destination**: {route.get('destinationEn', 'N/A')}\n"
            
            return result
        else:
            if route_name:
                result = f"### 與 {route_name} 相關的公車路線:\n\n"
            else:
                result = "### 公車路線列表:\n\n"
            
            for route in data[:10]:  # 限制顯示數量避免太長
                result += f"- **{route.get('nameZh', '無編號')}**: {route.get('departureZh', '無起點')} - {route.get('destinationZh', '無終點')}\n"
            
            if len(data) > 10:
                result += f"\n*共有 {len(data)} 條路線，僅顯示前 10 條。*"
            
            return result
    
    def _format_bus_stops(self, data: List[Dict[str, Any]], route_name: str) -> str:
        """格式化公車站點資訊"""
        if not data:
            return f"找不到公車路線 {route_name} 的站點資訊。"
        
        # 預設為不分方向的合併列表
        result = f"### 公車 {route_name} 的站點資訊\n\n"
        
        # 根據方向分組
        directions = {}
        for stop in data:
            direction = stop.get('direction', 0)
            if direction not in directions:
                directions[direction] = []
            directions[direction].append(stop)
        
        # 如果有多個方向，就分開顯示
        if len(directions) > 1:
            for direction, stops in directions.items():
                dir_name = "去程" if direction == 0 else "返程"
                result += f"#### {dir_name}方向\n\n"
                
                for i, stop in enumerate(stops, 1):
                    result += f"{i}. **{stop.get('stopName', '無名稱')}**\n"
                
                result += "\n"
        else:
            # 只有一個方向
            stops = list(directions.values())[0]
            for i, stop in enumerate(stops, 1):
                result += f"{i}. **{stop.get('stopName', '無名稱')}**\n"
        
        return result
    
    def _format_bus_estimated_time(self, data: List[Dict[str, Any]], route_name: str, stop_name: Optional[str] = None) -> str:
        """格式化公車預計到站時間"""
        if not data:
            msg = f"找不到公車路線 {route_name}"
            if stop_name:
                msg += f" 在站點 {stop_name}"
            msg += " 的到站時間資訊。"
            return msg
        
        if stop_name:
            result = f"### 公車 {route_name} 在站點 {stop_name} 的到站時間\n\n"
            filtered_data = [item for item in data if item.get('stopName') == stop_name]
            
            if not filtered_data:
                return f"找不到公車路線 {route_name} 在站點 {stop_name} 的到站時間資訊。"
            
            for item in filtered_data:
                direction = "去程" if item.get('direction') == 0 else "返程"
                time = item.get('estimatedTime')
                status = item.get('status', '無資料')
                
                if time is not None:
                    minutes = time // 60
                    result += f"- **{direction}**: {minutes} 分鐘後到站\n"
                else:
                    result += f"- **{direction}**: {status}\n"
        else:
            result = f"### 公車 {route_name} 的到站時間\n\n"
            
            # 根據方向和站點分組
            grouped_data = {}
            for item in data:
                direction = item.get('direction', 0)
                stop_name = item.get('stopName', '未知站點')
                if direction not in grouped_data:
                    grouped_data[direction] = []
                grouped_data[direction].append(item)
            
            for direction, items in grouped_data.items():
                dir_name = "去程" if direction == 0 else "返程"
                result += f"#### {dir_name}方向\n\n"
                
                for item in items:
                    stop = item.get('stopName', '未知站點')
                    time = item.get('estimatedTime')
                    status = item.get('status', '無資料')
                    
                    if time is not None:
                        minutes = time // 60
                        result += f"- **{stop}**: {minutes} 分鐘後到站\n"
                    else:
                        result += f"- **{stop}**: {status}\n"
                
                result += "\n"
        
        return result
    
    def _format_bus_search_by_stop(self, data: List[Dict[str, Any]], stop_name: str) -> str:
        """格式化依站點查詢的公車資訊"""
        if not data:
            return f"找不到站點 {stop_name} 的公車資訊。"
        
        result = f"### 站點 {stop_name} 的公車資訊\n\n"
        
        # 依路線分組
        routes = {}
        for item in data:
            route_name = item.get('routeName', '未知路線')
            if route_name not in routes:
                routes[route_name] = []
            routes[route_name].append(item)
        
        for route_name, items in routes.items():
            result += f"#### 路線 {route_name}\n\n"
            
            for item in items:
                direction = "去程" if item.get('direction') == 0 else "返程"
                time = item.get('estimatedTime')
                status = item.get('status', '無資料')
                
                if time is not None:
                    minutes = time // 60
                    result += f"- **{direction}**: {minutes} 分鐘後到站\n"
                else:
                    result += f"- **{direction}**: {status}\n"
            
            result += "\n"
        
        return result
    
    def _format_traffic_status(self, data: List[Dict[str, Any]], area: Optional[str] = None, road: Optional[str] = None) -> str:
        """格式化交通狀況資訊"""
        if not data:
            msg = "找不到交通狀況資訊"
            if area:
                msg += f"，區域: {area}"
            if road:
                msg += f"，道路: {road}"
            msg += "。"
            return msg
        
        title = "### 交通狀況資訊"
        if area:
            title += f" - {area}"
        if road:
            title += f" {road}"
        
        result = f"{title}\n\n"
        
        for item in data[:15]:  # 限制顯示數量
            road_name = item.get('road', '未知道路')
            area_name = item.get('area', '未知區域')
            status = item.get('status', '無資料')
            speed = item.get('avgSpeed')
            
            result += f"- **{area_name} {road_name}**: {status}"
            if speed is not None:
                result += f", 平均車速 {speed} km/h"
            result += "\n"
        
        if len(data) > 15:
            result += f"\n*共有 {len(data)} 筆資料，僅顯示前 15 筆。*"
        
        return result
    
    def _format_traffic_construction(self, data: List[Dict[str, Any]], area: Optional[str] = None) -> str:
        """格式化道路施工資訊"""
        if not data:
            msg = "找不到道路施工資訊"
            if area:
                msg += f"，區域: {area}"
            msg += "。"
            return msg
        
        title = "### 道路施工資訊"
        if area:
            title += f" - {area}"
        
        result = f"{title}\n\n"
        
        for item in data[:10]:  # 限制顯示數量
            road = item.get('road', '未知道路')
            area_name = item.get('area', '未知區域')
            desc = item.get('description', '無說明')
            start_date = item.get('startDate', '未知')
            end_date = item.get('endDate', '未知')
            status = item.get('status', '無資料')
            
            result += f"- **{area_name} {road}**\n"
            result += f"  - 說明: {desc}\n"
            result += f"  - 期間: {start_date} 至 {end_date}\n"
            result += f"  - 狀態: {status}\n\n"
        
        if len(data) > 10:
            result += f"\n*共有 {len(data)} 筆資料，僅顯示前 10 筆。*"
        
        return result
    
    def _format_traffic_cameras(self, data: List[Dict[str, Any]], area: Optional[str] = None, road: Optional[str] = None) -> str:
        """格式化交通攝影機資訊"""
        if not data:
            msg = "找不到交通攝影機資訊"
            if area:
                msg += f"，區域: {area}"
            if road:
                msg += f"，道路: {road}"
            msg += "。"
            return msg
        
        title = "### 交通攝影機資訊"
        if area:
            title += f" - {area}"
        if road:
            title += f" {road}"
        
        result = f"{title}\n\n"
        
        for item in data[:10]:  # 限制顯示數量
            road_name = item.get('road', '未知道路')
            area_name = item.get('area', '未知區域')
            direction = item.get('direction', '未知方向')
            image_url = item.get('imageUrl')
            
            result += f"- **{area_name} {road_name}** ({direction})\n"
            if image_url:
                result += f"  - 影像連結: {image_url}\n"
            result += "\n"
        
        if len(data) > 10:
            result += f"\n*共有 {len(data)} 個攝影機，僅顯示前 10 個。*"
        
        return result
    
    def _format_traffic_incidents(self, data: List[Dict[str, Any]], area: Optional[str] = None) -> str:
        """格式化交通事件資訊"""
        if not data:
            msg = "找不到交通事件資訊"
            if area:
                msg += f"，區域: {area}"
            msg += "。"
            return msg
        
        title = "### 交通事件資訊"
        if area:
            title += f" - {area}"
        
        result = f"{title}\n\n"
        
        for item in data[:10]:  # 限制顯示數量
            road = item.get('road', '未知道路')
            area_name = item.get('area', '未知區域')
            incident_type = item.get('type', '未知類型')
            desc = item.get('description', '無說明')
            start_time = item.get('startTime', '未知')
            status = item.get('status', '無資料')
            
            result += f"- **{area_name} {road}** ({incident_type})\n"
            result += f"  - 說明: {desc}\n"
            result += f"  - 開始時間: {start_time}\n"
            result += f"  - 狀態: {status}\n\n"
        
        if len(data) > 10:
            result += f"\n*共有 {len(data)} 筆事件，僅顯示前 10 筆。*"
        
        return result
    
    def _format_parking_lots(self, data: List[Dict[str, Any]], area: Optional[str] = None, type_name: Optional[str] = None) -> str:
        """格式化停車場資訊"""
        if not data:
            msg = "找不到停車場資訊"
            if area:
                msg += f"，區域: {area}"
            if type_name:
                msg += f"，類型: {type_name}"
            msg += "。"
            return msg
        
        title = "### 停車場資訊"
        if area:
            title += f" - {area}"
        if type_name:
            title += f" {type_name}"
        
        result = f"{title}\n\n"
        
        for item in data[:15]:  # 限制顯示數量
            name = item.get('name', '未知停車場')
            area_name = item.get('area', '未知區域')
            address = item.get('address', '無地址')
            total = item.get('totalSpaces', '未知')
            available = item.get('availableSpaces')
            
            result += f"- **{name}** ({area_name})\n"
            result += f"  - 地址: {address}\n"
            result += f"  - 總車位: {total}\n"
            if available is not None:
                result += f"  - 可用車位: {available}\n"
            result += "\n"
        
        if len(data) > 15:
            result += f"\n*共有 {len(data)} 個停車場，僅顯示前 15 個。*"
        
        return result
    
    def _format_parking_available(self, data: List[Dict[str, Any]], area: Optional[str] = None) -> str:
        """格式化有空位的停車場資訊"""
        if not data:
            msg = "找不到有空位的停車場資訊"
            if area:
                msg += f"，區域: {area}"
            msg += "。"
            return msg
        
        # 如果有指定區域，過濾資料
        if area:
            data = [item for item in data if area in item.get('area', '')]
        
        title = "### 有空位的停車場"
        if area:
            title += f" - {area}"
        
        result = f"{title}\n\n"
        
        for item in data[:15]:  # 限制顯示數量
            name = item.get('name', '未知停車場')
            area_name = item.get('area', '未知區域')
            address = item.get('address', '無地址')
            total = item.get('totalSpaces', '未知')
            available = item.get('availableSpaces', '未知')
            
            result += f"- **{name}** ({area_name})\n"
            result += f"  - 地址: {address}\n"
            result += f"  - 總車位: {total}\n"
            result += f"  - 可用車位: {available}\n\n"
        
        if len(data) > 15:
            result += f"\n*共有 {len(data)} 個有空位的停車場，僅顯示前 15 個。*"
        
        return result
    
    def _format_parking_fee_rates(self, data: List[Dict[str, Any]]) -> str:
        """格式化停車場收費標準"""
        if not data:
            return "找不到停車場收費標準資訊。"
        
        result = "### 停車場收費標準\n\n"
        
        # 根據停車場分組
        parking_rates = {}
        for item in data:
            parking_id = item.get('parkingId')
            parking_name = item.get('parkingName', '未知停車場')
            if parking_id not in parking_rates:
                parking_rates[parking_id] = {
                    'name': parking_name,
                    'rates': []
                }
            parking_rates[parking_id]['rates'].append(item)
        
        # 顯示前10個停車場的收費標準
        count = 0
        for parking_id, info in parking_rates.items():
            if count >= 10:
                break
            
            result += f"#### {info['name']}\n\n"
            
            for rate in info['rates']:
                vehicle_type = rate.get('vehicleType', '未知')
                hourly_rate = rate.get('hourlyRate')
                daily_max = rate.get('dailyMaximum')
                monthly_rate = rate.get('monthlyRate')
                desc = rate.get('description', '無')
                
                result += f"- **{vehicle_type}**:\n"
                if hourly_rate is not None:
                    result += f"  - 小時費率: {hourly_rate} 元\n"
                if daily_max is not None:
                    result += f"  - 每日上限: {daily_max} 元\n"
                if monthly_rate is not None:
                    result += f"  - 月租費率: {monthly_rate} 元\n"
                if desc != '無':
                    result += f"  - 說明: {desc}\n"
                result += "\n"
            
            count += 1
        
        if len(parking_rates) > 10:
            result += f"\n*共有 {len(parking_rates)} 個停車場的收費標準，僅顯示前 10 個。*"
        
        return result
    
    def _get_help_message(self) -> str:
        """獲取幫助信息"""
        return """### 新北市交通局開放資料查詢助手

我可以幫您查詢新北市的交通相關資訊，包括：

1. **公車資訊**：
   - 公車路線查詢，例如「307公車的路線」
   - 站牌查詢，例如「307公車的站牌」
   - 到站時間查詢，例如「307公車到板橋站的時間」
   - 站點公車查詢，例如「板橋站有哪些公車」

2. **交通狀況**：
   - 道路交通狀況，例如「板橋區的交通狀況」
   - 道路施工資訊，例如「板橋區有哪些道路施工」
   - 交通攝影機，例如「板橋區的交通攝影機」
   - 交通事件，例如「板橋區有哪些交通事件」

3. **停車場資訊**：
   - 停車場查詢，例如「板橋區有哪些停車場」
   - 停車場空位查詢，例如「板橋區有空位的停車場」
   - 停車場收費標準，例如「板橋區停車場的收費標準」

4. **自行車資訊**：
   - YouBike 站點查詢，例如「板橋區的 YouBike 站點」
   - 自行車架查詢，例如「板橋區的自行車架」
   - 自行車道查詢，例如「板橋區的自行車道」

5. **其他交通服務**：
   - 計程車服務查詢，例如「新北市的計程車服務」
   - 拖吊保管場查詢，例如「板橋區的拖吊保管場」
   - 交通影響評估查詢，例如「新北市的交通影響評估」

請告訴我您想查詢的資訊，我會盡力協助您。
"""

    def _format_traffic_service_info(self, data: List[Dict[str, Any]], service_type: Optional[str] = None) -> str:
        """格式化交通服務資訊"""
        if not data:
            return f"找不到{service_type or ''}交通服務資訊。"
        
        if service_type:
            result = f"### {service_type}資訊\n\n"
        else:
            result = "### 交通服務資訊\n\n"
        
        # 檢查是否為 Pydantic 模型對象列表
        if data and hasattr(data[0], 'model_dump'):
            # 將 Pydantic 模型轉換為字典
            data = [item.model_dump() for item in data]
        
        for service in data[:10]:  # 限制顯示數量避免太長
            # 根據不同類型的服務處理不同的字段
            if "taxi_transportation_service" in service:
                # 計程車服務（舊格式）
                name = service.get("taxi_transportation_service", service.get("name", "無名稱"))
                phone = service.get("phone_number", service.get("phone", "無電話"))
                
                result += f"- **{name}**\n"
                if phone:
                    result += f"  電話: {phone}\n"
                result += "\n"
            elif "title" in service:
                # 拖吊保管場
                name = service.get("title", service.get("name", "無名稱"))
                address = service.get("address", "無地址")
                tel = service.get("tel", "無電話")
                distance = service.get("distance")
                
                result += f"- **{name}**\n"
                if address:
                    result += f"  地址: {address}\n"
                if tel:
                    result += f"  電話: {tel}\n"
                if distance:
                    result += f"  距離: {distance} 公尺\n"
                result += "\n"
            elif "url" in service:
                # 交通影響評估
                name = service.get("name", "無名稱")
                category = service.get("category", "無類別")
                url = service.get("url", "")
                
                result += f"- **{name}**"
                if category:
                    result += f" ({category})"
                result += "\n"
                if url:
                    result += f"  連結: {url}\n"
                result += "\n"
            elif "countycode" in service and "phone" in service:
                # 計程車服務（新格式）
                name = service.get("name", "無名稱")
                phone = service.get("phone", "無電話")
                
                result += f"- **{name}**\n"
                if phone:
                    result += f"  電話: {phone}\n"
                result += "\n"
            elif "station_name" in service or "sna" in service:
                # YouBike 站點
                name = service.get("station_name", service.get("sna", "無名稱"))
                address = service.get("address", service.get("ar", "無地址"))
                available_bikes = service.get("available_bikes", service.get("sbi", 0))
                empty_spaces = service.get("empty_spaces", service.get("bemp", 0))
                total_bikes = service.get("total_bikes", service.get("tot", 0))
                distance = service.get("distance")
                
                result += f"- **{name}**\n"
                if address:
                    result += f"  地址: {address}\n"
                result += f"  可借車輛: {available_bikes} 輛\n"
                result += f"  可還空位: {empty_spaces} 個\n"
                result += f"  總車位數: {total_bikes} 個\n"
                if distance:
                    result += f"  距離: {distance} 公尺\n"
                result += "\n"
            elif "area" in service and "quantity" in service:
                # 自行車架
                if "station" in service:
                    # 捷運站週邊自行車架
                    station = service.get("station", "無站名")
                    item = service.get("item", "無項目")
                    quantity = service.get("quantity", 0)
                    
                    result += f"- **{station}**\n"
                    result += f"  項目: {item}\n"
                    result += f"  數量: {quantity} 個\n"
                    result += "\n"
                else:
                    # 行政區自行車架
                    area = service.get("area", "無區域")
                    item = service.get("item", "無項目")
                    quantity = service.get("quantity", 0)
                    
                    result += f"- **{area}**\n"
                    result += f"  項目: {item}\n"
                    result += f"  數量: {quantity} 個\n"
                    result += "\n"
            elif "type" in service and "bikeway" in service:
                # 自行車道
                district = service.get("district", "無區域")
                bikeway = service.get("bikeway", "無名稱")
                route = service.get("route", "無路線")
                length = service.get("length", 0)
                
                result += f"- **{bikeway}**\n"
                result += f"  行政區: {district}\n"
                result += f"  路線: {route}\n"
                result += f"  長度: {length} 公里\n"
                result += "\n"
            else:
                # 一般服務
                name = service.get("name", "無名稱")
                category = service.get("category", "無類別")
                address = service.get("address", "無地址")
                tel = service.get("tel", "無電話")
                phone = service.get("phone", "")  # 計程車服務可能有 phone 而非 tel
                url = service.get("url", "")  # 交通影響評估可能有 url
                
                result += f"- **{name}**"
                if category:
                    result += f" ({category})"
                result += "\n"
                
                if address:
                    result += f"  地址: {address}\n"
                if tel:
                    result += f"  電話: {tel}\n"
                if phone and not tel:  # 如果有 phone 但沒有 tel，則顯示 phone
                    result += f"  電話: {phone}\n"
                if url:
                    result += f"  連結: {url}\n"
                result += "\n"
        
        if len(data) > 10:
            result += f"\n*共有 {len(data)} 筆資料，僅顯示前 10 筆。*"
        
        return result

    def _format_bike_routes(self, data: List[Dict[str, Any]], route_name: Optional[str] = None) -> str:
        """格式化自行車路線資訊"""
        if not data:
            return f"找不到自行車路線 {route_name} 的資訊。"
        
        # 檢查是否為 Pydantic 模型對象列表
        if data and hasattr(data[0], 'model_dump'):
            # 將 Pydantic 模型轉換為字典
            data = [item.model_dump() for item in data]
        
        if len(data) == 1:
            route = data[0]
            result = f"### 自行車路線 {route.get('name', '無編號')} 資訊\n\n"
            result += f"- **路線類型**: {route.get('type', '無資料')}\n"
            result += f"- **縣市代碼**: {route.get('countycode', '無資料')}\n"
            result += f"- **行政區**: {route.get('district', '無資料')}\n"
            result += f"- **路線**: {route.get('route', '無資料')}\n"
            result += f"- **建置年月**: {route.get('year_month', '無資料')}\n"
            result += f"- **長度(公里)**: {route.get('length', '無資料')}\n"
            
            return result
        else:
            if route_name:
                result = f"### 與 {route_name} 相關的自行車路線:\n\n"
            else:
                result = "### 自行車路線列表:\n\n"
            
            for route in data[:10]:  # 限制顯示數量避免太長
                result += f"- **{route.get('name', '無編號')}**: {route.get('district', '無區域')} - {route.get('route', '無路線')}, 長度: {route.get('length', '無資料')}公里\n"
            
            if len(data) > 10:
                result += f"\n*共有 {len(data)} 條路線，僅顯示前 10 條。*"
            
            return result

    def _format_bike_stops(self, data: List[Dict[str, Any]], route_name: str) -> str:
        """格式化自行車站點資訊"""
        if not data:
            return f"找不到自行車路線 {route_name} 的站點資訊。"
        
        # 檢查是否為 Pydantic 模型對象列表
        if data and hasattr(data[0], 'model_dump'):
            # 將 Pydantic 模型轉換為字典
            data = [item.model_dump() for item in data]
        
        result = f"### 自行車路線 {route_name} 的站點資訊\n\n"
        
        # 分為去程和回程
        go_stops = [stop for stop in data if stop.get("direction") == 0]
        back_stops = [stop for stop in data if stop.get("direction") == 1]
        
        if go_stops:
            result += "#### 去程站點\n\n"
            for i, stop in enumerate(go_stops, 1):
                result += f"{i}. **{stop.get('name', '無名稱')}**"
                if stop.get("address"):
                    result += f" ({stop.get('address')})"
                result += "\n"
        
        if back_stops:
            result += "\n#### 回程站點\n\n"
            for i, stop in enumerate(back_stops, 1):
                result += f"{i}. **{stop.get('name', '無名稱')}**"
                if stop.get("address"):
                    result += f" ({stop.get('address')})"
                result += "\n"
        
        return result

    def _format_bike_estimated_time(self, data: List[Dict[str, Any]], route_name: str, stop_name: Optional[str] = None) -> str:
        """格式化自行車預計到站時間"""
        if not data:
            return f"找不到自行車路線 {route_name} 的到站時間資訊。"
        
        # 檢查是否為 Pydantic 模型對象列表
        if data and hasattr(data[0], 'model_dump'):
            # 將 Pydantic 模型轉換為字典
            data = [item.model_dump() for item in data]
        
        if stop_name:
            # 過濾特定站點
            filtered_data = [item for item in data if stop_name in item.get("name", "")]
            if not filtered_data:
                return f"找不到自行車路線 {route_name} 在站點 {stop_name} 的到站時間資訊。"
            data = filtered_data
        
        result = f"### 自行車路線 {route_name} 的到站時間\n\n"
        
        # 分為去程和回程
        go_stops = [stop for stop in data if stop.get("direction") == 0]
        back_stops = [stop for stop in data if stop.get("direction") == 1]
        
        if go_stops:
            result += "#### 去程\n\n"
            for stop in go_stops:
                name = stop.get("name", "無名稱")
                eta = stop.get("eta", "無資料")
                status = stop.get("status", "無狀態")
                
                result += f"- **{name}**: "
                if eta == -1:
                    result += "尚未發車"
                elif eta == 0:
                    result += "進站中"
                else:
                    result += f"預計 {eta} 分鐘到站"
                
                if status:
                    result += f" ({status})"
                result += "\n"
        
        if back_stops:
            result += "\n#### 回程\n\n"
            for stop in back_stops:
                name = stop.get("name", "無名稱")
                eta = stop.get("eta", "無資料")
                status = stop.get("status", "無狀態")
                
                result += f"- **{name}**: "
                if eta == -1:
                    result += "尚未發車"
                elif eta == 0:
                    result += "進站中"
                else:
                    result += f"預計 {eta} 分鐘到站"
                
                if status:
                    result += f" ({status})"
                result += "\n"
        
        return result

    def _format_bike_search_by_stop(self, data: List[Dict[str, Any]], stop_name: str) -> str:
        """格式化站點經過的自行車路線"""
        if not data:
            return f"找不到經過站點 {stop_name} 的自行車路線。"
        
        # 檢查是否為 Pydantic 模型對象列表
        if data and hasattr(data[0], 'model_dump'):
            # 將 Pydantic 模型轉換為字典
            data = [item.model_dump() for item in data]
        
        result = f"### 經過站點 {stop_name} 的自行車路線\n\n"
        
        for route in data:
            route_name = route.get("name", "無編號")
            direction = "去程" if route.get("direction") == 0 else "回程"
            eta = route.get("eta", "無資料")
            
            result += f"- **{route_name}** ({direction}): "
            if eta == -1:
                result += "尚未發車"
            elif eta == 0:
                result += "進站中"
            else:
                result += f"預計 {eta} 分鐘到站"
            result += "\n"
        
        return result


# 初始化 MCP 服務器的實例
mcp = NTPCOpenDataMCP()

# 確保 MCP 運行時有可識別的 ID
if __name__ == "__main__":
    print(f"MCP 服務器 UUID: {SERVER_UUID}", file=sys.stderr)
    mcp.run()
