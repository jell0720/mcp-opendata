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
from ntpc_opendata_tool.api.client import APIError

# 設置日誌
logger = setup_logger("ntpc_opendata_mcp")

# 初始化 API 客戶端
bus_api = BusAPI()
traffic_api = TrafficAPI() 
parking_api = ParkingAPI()

# 生成唯一的 UUID，用於服務器實例標識
SERVER_UUID = str(uuid.uuid4())

class NTPCOpenDataMCP(FastMCP):
    """新北市交通局 OpenData MCP 服務器"""
    
    def __init__(self):
        """初始化 MCP 服務器"""
        super().__init__(
            name="新北市交通局 OpenData",
            description="查詢新北市交通局開放資料的工具，包括公車、交通狀況和停車場資訊。",
            id=SERVER_UUID  # 添加唯一識別碼
        )
        logger.info("初始化新北市交通局 OpenData MCP 服務器")
        
        # 註冊查詢處理函數
        @self.tool(name="ntpc-query", description="處理交通相關查詢")
        async def handle_query(query: str) -> str:
            """處理用戶查詢
            
            Args:
                query: 用戶查詢內容
                
            Returns:
                MCP 回應
            """
            logger.info(f"收到查詢: {query}")
            print(f"收到查詢: {query}", file=sys.stderr)
            
            try:
                # 檢查查詢類型並分發到相應處理函數
                if self._is_bus_query(query):
                    return await self._handle_bus_query(query)
                elif self._is_traffic_query(query):
                    return await self._handle_traffic_query(query)
                elif self._is_parking_query(query):
                    return await self._handle_parking_query(query)
                else:
                    # 一般性查詢，提供幫助信息
                    return self._get_help_message()
            except APIError as e:
                logger.error(f"API 錯誤: {e.message}")
                print(f"API 錯誤: {e.message}", file=sys.stderr)
                return f"抱歉，查詢過程中發生錯誤: {e.message}"
            except Exception as e:
                logger.exception(f"未預期錯誤: {str(e)}")
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
    
    async def _handle_bus_query(self, query: str) -> str:
        """處理公車相關查詢"""
        logger.info("處理公車相關查詢")
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
                data = bus_api.get_estimated_time(route_name, stop_name)
                return self._format_bus_estimated_time(data, route_name, stop_name)
            elif route_name and ("站牌" in query or "站點" in query):
                # 查詢路線站牌
                data = bus_api.get_stops(route_name)
                return self._format_bus_stops(data, route_name)
            elif route_name:
                # 查詢路線資訊
                data = bus_api.get_routes(route_name)
                return self._format_bus_routes(data, route_name)
            elif stop_name:
                # 查詢站點經過的公車
                data = bus_api.search_by_stop(stop_name)
                return self._format_bus_search_by_stop(data, stop_name)
            else:
                # 一般公車查詢
                return "您似乎在查詢公車資訊，請提供更具體的資訊，例如公車路線號碼或站牌名稱。例如「307公車的路線」或「捷運板橋站有哪些公車」。"
        except APIError as e:
            return f"查詢公車資訊時發生錯誤: {e.message}"
    
    async def _handle_traffic_query(self, query: str) -> str:
        """處理交通狀況相關查詢"""
        logger.info("處理交通狀況相關查詢")
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
                data = traffic_api.get_construction_info(area)
                return self._format_traffic_construction(data, area)
            elif "攝影機" in query or "監視器" in query or "即時影像" in query:
                # 查詢交通攝影機
                data = traffic_api.get_traffic_cameras(area, road)
                return self._format_traffic_cameras(data, area, road)
            elif "事件" in query or "事故" in query:
                # 查詢交通事件
                data = traffic_api.get_traffic_incidents(area)
                return self._format_traffic_incidents(data, area)
            else:
                # 查詢交通狀況
                data = traffic_api.get_traffic_status(area, road)
                return self._format_traffic_status(data, area, road)
        except APIError as e:
            return f"查詢交通資訊時發生錯誤: {e.message}"
    
    async def _handle_parking_query(self, query: str) -> str:
        """處理停車場相關查詢"""
        logger.info("處理停車場相關查詢")
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
                data = parking_api.get_parking_lots()
                return self._format_parking_fee_rates(data)
            elif "有空位" in query or "有位子" in query or "可以停" in query:
                # 查詢有空位的停車場
                min_spaces = 1
                data = parking_api.get_available_parking_lots(min_spaces, area)
                return self._format_parking_available(data, area)
            elif area and type_name:
                # 查詢特定區域和類型的停車場
                data = parking_api.get_parking_lots_by_type(type_name)
                # 手動過濾區域
                data = [item for item in data if area in item.get("area", "")]
                return self._format_parking_lots(data, area, type_name)
            elif area:
                # 查詢特定區域的停車場
                data = parking_api.get_parking_lots(area)
                return self._format_parking_lots(data, area)
            elif type_name:
                # 查詢特定類型的停車場
                data = parking_api.get_parking_lots_by_type(type_name)
                return self._format_parking_lots(data, type_name=type_name)
            else:
                # 一般停車場查詢
                return "您似乎在查詢停車場資訊，請提供更具體的資訊，例如區域或停車場類型。例如「板橋區有哪些停車場」或「新莊區有空位的停車場」。"
        except APIError as e:
            return f"查詢停車場資訊時發生錯誤: {e.message}"
    
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
        return """
## 新北市交通局 OpenData 查詢工具

您可以查詢以下資訊：

### 1. 公車資訊
- 公車路線查詢，例如：「307公車的路線」
- 站點查詢，例如：「307公車的站牌」
- 到站時間查詢，例如：「307公車幾分鐘到站」
- 站點經過的公車，例如：「捷運板橋站有哪些公車」

### 2. 交通狀況
- 即時路況查詢，例如：「板橋區交通狀況」
- 道路施工資訊，例如：「新莊區道路施工」
- 交通攝影機資訊，例如：「板橋區交通監視器」
- 交通事件資訊，例如：「新莊區交通事故」

### 3. 停車場資訊
- 停車場查詢，例如：「板橋區停車場」
- 有空位的停車場，例如：「板橋區有空位的停車場」
- 停車場收費標準，例如：「停車場收費標準」

請提供更具體的資訊，以幫助我提供更準確的查詢結果。
        """


# 初始化 MCP 服務器的實例
mcp = NTPCOpenDataMCP()

# 確保 MCP 運行時有可識別的 ID
if __name__ == "__main__":
    print(f"MCP 服務器 UUID: {SERVER_UUID}", file=sys.stderr)
    mcp.run()
