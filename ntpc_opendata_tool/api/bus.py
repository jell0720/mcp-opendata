"""
新北市公車相關 API 功能模組

提供公車路線、站點、到站時間等資訊查詢功能。
"""
import logging
from typing import Dict, List, Any, Optional
from ntpc_opendata_tool.api.client import OpenDataClient, APIError

logger = logging.getLogger(__name__)


class BusAPI:
    """新北市公車 API 服務類
    
    提供公車相關資訊查詢功能，包括路線、站點、到站時間等。
    """
    
    def __init__(self, client: Optional[OpenDataClient] = None):
        """初始化公車 API 服務
        
        Args:
            client: OpenDataClient 實例，如未提供則自動創建
        """
        self.client = client or OpenDataClient()
    
    def _process_response(self, response: Any) -> List[Dict[str, Any]]:
        """處理 API 回應
        
        Args:
            response: API 回應
            
        Returns:
            處理後的資料列表
        """
        if isinstance(response, dict):
            return response.get("data", [])
        elif isinstance(response, list):
            return response
        return []
    
    def get_routes(self, route_name: Optional[str] = None, page: int = 0, size: int = 100) -> List[Dict[str, Any]]:
        """獲取公車路線資訊
        
        Args:
            route_name: 路線名稱或編號，可選。如未提供則返回所有路線
            page: 頁碼(0..N)，預設為 0
            size: 每頁筆數，預設為 100
            
        Returns:
            公車路線資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            params = {
                "page": page,
                "size": size
            }
            if route_name:
                params["nameZh"] = route_name
                
            logger.info(f"查詢公車路線: {route_name if route_name else '所有路線'} (頁碼: {page}, 每頁筆數: {size})")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["bus_routes"],
                params=params
            )
            return self._process_response(response)
        except APIError as e:
            logger.error(f"查詢公車路線失敗: {e.message}")
            raise
    
    def get_stops(self, route_name: str) -> List[Dict[str, Any]]:
        """獲取指定路線的站點資訊
        
        Args:
            route_name: 路線名稱或編號
            
        Returns:
            站點資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            logger.info(f"查詢路線 {route_name} 的站點資訊")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["bus_stops"],
                params={"routeId": self._get_route_id(route_name)}
            )
            return self._process_response(response)
        except APIError as e:
            logger.error(f"查詢站點資訊失敗: {e.message}")
            raise
    
    def _get_route_id(self, route_name: str) -> str:
        """根據路線名稱獲取路線ID
        
        Args:
            route_name: 路線名稱或編號
            
        Returns:
            路線ID
            
        Raises:
            APIError: 當 API 請求失敗或找不到路線時
        """
        routes = self.get_routes(route_name)
        if not routes:
            raise APIError(f"找不到路線: {route_name}")
        return routes[0]["Id"]
    
    def get_estimated_time(self, route_name: str, stop_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """獲取公車預計到站時間
        
        Args:
            route_name: 路線名稱或編號
            stop_name: 站點名稱，可選。如未提供則返回該路線所有站點的到站時間
            
        Returns:
            預計到站時間資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            logger.info(f"查詢路線 {route_name} 的預計到站時間 {f'(站點: {stop_name})' if stop_name else ''}")
            
            route_id = self._get_route_id(route_name)
            params = {"RouteID": route_id}
            
            if stop_name:
                # 先獲取站點ID
                stops = self.get_stops(route_name)
                stop_ids = [stop["Id"] for stop in stops if stop["nameZh"] == stop_name]
                if not stop_ids:
                    raise APIError(f"找不到站點: {stop_name}")
                params["StopID"] = stop_ids[0]
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["bus_estimated_time"],
                params=params
            )
            return self._process_response(response)
        except APIError as e:
            logger.error(f"查詢預計到站時間失敗: {e.message}")
            raise
    
    def get_all_stops(self) -> List[Dict[str, Any]]:
        """獲取所有公車站點資訊
        
        Returns:
            所有站點資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            logger.info("查詢所有公車站點資訊")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["bus_stops"]
            )
            return self._process_response(response)
        except APIError as e:
            logger.error(f"查詢所有站點資訊失敗: {e.message}")
            raise
    
    def search_by_stop(self, stop_name: str) -> List[Dict[str, Any]]:
        """根據站點名稱搜尋路線
        
        Args:
            stop_name: 站點名稱
            
        Returns:
            經過該站點的路線資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            logger.info(f"搜尋經過站點 {stop_name} 的路線")
            
            all_stops = self.get_all_stops()
            matching_stops = [stop for stop in all_stops if stop_name in stop["nameZh"]]
            
            if not matching_stops:
                return []
            
            # 獲取經過這些站點的路線
            route_ids = set(stop["routeId"] for stop in matching_stops)
            routes = []
            
            for route_id in route_ids:
                route_info = self.client.get_by_resource_id(
                    self.client.RESOURCE_IDS["bus_routes"],
                    params={"Id": route_id}
                )
                routes.extend(self._process_response(route_info))
            
            return routes
        except APIError as e:
            logger.error(f"搜尋站點路線失敗: {e.message}")
            raise
    
    def get_real_time_by_route(self, route_name: str) -> List[Dict[str, Any]]:
        """獲取指定路線的公車即時位置
        
        Args:
            route_name: 路線名稱或編號
            
        Returns:
            公車即時位置資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            logger.info(f"查詢路線 {route_name} 的公車即時位置")
            
            route_id = self._get_route_id(route_name)
            
            # 注意：此處假設有即時位置的 API 資源，實際上可能需要調整
            # 由於原始 JSON 中沒有看到即時位置的資料，這裡僅作為示例
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS.get("bus_real_time", ""),
                params={"routeId": route_id}
            )
            return self._process_response(response)
        except APIError as e:
            logger.error(f"查詢公車即時位置失敗: {e.message}")
            raise
    
    def get_bus_operators(self) -> List[Dict[str, Any]]:
        """獲取公車業者資訊
        
        Returns:
            公車業者資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            logger.info("查詢公車業者資訊")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["bus_operators"]
            )
            return self._process_response(response)
        except APIError as e:
            logger.error(f"查詢公車業者資訊失敗: {e.message}")
            raise
    
    def get_bus_transfer_discounts(self) -> List[Dict[str, Any]]:
        """獲取公車轉乘優惠資訊
        
        Returns:
            公車轉乘優惠資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            logger.info("查詢公車轉乘優惠資訊")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["bus_transfer_discount"]
            )
            return self._process_response(response)
        except APIError as e:
            logger.error(f"查詢公車轉乘優惠資訊失敗: {e.message}")
            raise
    
    def get_route_info(self, route_type: Optional[str] = None, route_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """獲取公車路線說明及示意圖
        
        Args:
            route_type: 路線類型，可選。如：一般路線、快速公車等
            route_name: 路線名稱或編號，可選
            
        Returns:
            公車路線說明及示意圖資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            logger.info(f"查詢公車路線說明及示意圖 {f'(類型: {route_type})' if route_type else ''} {f'(路線: {route_name})' if route_name else ''}")
            
            resource_id = self.client.RESOURCE_IDS["bus_route_info"]
            
            # 根據路線類型選擇不同的資源
            if route_type:
                type_mapping = {
                    "一般路線": "bus_route_info_general",
                    "快速公車": "bus_route_info_express",
                    "跳蛙路線": "bus_route_info_jump",
                    "捷運接駁": "bus_route_info_mrt_shuttle",
                    "捷運先導": "bus_route_info_mrt_pilot",
                    "幸福巴士": "bus_route_info_happy",
                    "新巴士": "bus_route_info_new_bus",
                    "輕軌公車": "bus_route_info_light_rail"
                }
                if route_type in type_mapping and type_mapping[route_type] in self.client.RESOURCE_IDS:
                    resource_id = self.client.RESOURCE_IDS[type_mapping[route_type]]
            
            params = {}
            if route_name:
                params["routeName"] = route_name
                
            response = self.client.get_by_resource_id(
                resource_id,
                params=params
            )
            return self._process_response(response)
        except APIError as e:
            logger.error(f"查詢公車路線說明及示意圖失敗: {e.message}")
            raise 