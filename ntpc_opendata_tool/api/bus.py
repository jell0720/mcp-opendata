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
                params["routeName"] = route_name
                
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
                params={"routeName": route_name}
            )
            return self._process_response(response)
        except APIError as e:
            logger.error(f"查詢站點資訊失敗: {e.message}")
            raise
    
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
            params = {"routeName": route_name}
            if stop_name:
                params["stopName"] = stop_name
                logger.info(f"查詢路線 {route_name} 在站點 {stop_name} 的到站時間")
            else:
                logger.info(f"查詢路線 {route_name} 的所有到站時間")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["bus_estimated_time"],
                params=params
            )
            return self._process_response(response)
        except APIError as e:
            logger.error(f"查詢到站時間失敗: {e.message}")
            raise
    
    def get_all_stops(self) -> List[Dict[str, Any]]:
        """獲取所有公車站位資訊
        
        Returns:
            所有站位資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            logger.info("查詢所有公車站位資訊")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["bus_stops"]
            )
            return self._process_response(response)
        except APIError as e:
            logger.error(f"查詢所有站位資訊失敗: {e.message}")
            raise
    
    def search_by_stop(self, stop_name: str) -> List[Dict[str, Any]]:
        """依站點名稱查詢公車資訊
        
        Args:
            stop_name: 站點名稱
            
        Returns:
            符合該站點的公車資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            logger.info(f"依站點名稱 {stop_name} 查詢公車資訊")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["bus_stops"],
                params={"stopName": stop_name}
            )
            return self._process_response(response)
        except APIError as e:
            logger.error(f"依站點查詢失敗: {e.message}")
            raise
    
    def get_real_time_by_route(self, route_name: str) -> List[Dict[str, Any]]:
        """獲取指定路線的實時公車位置
        
        Args:
            route_name: 路線名稱或編號
            
        Returns:
            實時公車位置資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            logger.info(f"查詢路線 {route_name} 的實時公車位置")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["bus_estimated_time"],
                params={"routeName": route_name}
            )
            return self._process_response(response)
        except APIError as e:
            logger.error(f"查詢實時公車位置失敗: {e.message}")
            raise 