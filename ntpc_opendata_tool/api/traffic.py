"""
新北市交通狀況相關 API 功能模組

提供交通狀況、路況監控、事件通報等資訊查詢功能。
"""
import logging
from typing import Dict, List, Any, Optional
from ntpc_opendata_tool.api.client import OpenDataClient, APIError

logger = logging.getLogger(__name__)


class TrafficAPI:
    """新北市交通狀況 API 服務類
    
    提供交通相關資訊查詢功能，包括即時路況、交通事件、監視器畫面等。
    """
    
    def __init__(self, client: Optional[OpenDataClient] = None):
        """初始化交通狀況 API 服務
        
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
    
    def get_traffic_cameras(self, area: Optional[str] = None, road: Optional[str] = None) -> List[Dict[str, Any]]:
        """獲取交通監視器資訊
        
        Args:
            area: 行政區，可選
            road: 道路名稱，可選
            
        Returns:
            監視器資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            params = {}
            if area:
                params["area"] = area
            if road:
                params["road"] = road
            
            logger.info(f"查詢交通監視器: {area or ''} {road or ''}")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["traffic_cameras"],
                params=params
            )
            return self._process_response(response)
        except APIError as e:
            logger.error(f"查詢交通監視器失敗: {e.message}")
            raise
    
    def get_etag_locations(self, area: Optional[str] = None) -> List[Dict[str, Any]]:
        """獲取 ETag 設備位置資訊
        
        Args:
            area: 行政區，可選
            
        Returns:
            ETag 設備位置列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            params = {"area": area} if area else None
            logger.info(f"查詢 ETag 設備位置: {area if area else '所有區域'}")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["traffic_etag"],
                params=params
            )
            return self._process_response(response)
        except APIError as e:
            logger.error(f"查詢 ETag 設備位置失敗: {e.message}")
            raise
    
    def get_traffic_status(self, area: Optional[str] = None, road: Optional[str] = None) -> List[Dict[str, Any]]:
        """獲取即時交通狀況
        
        Args:
            area: 行政區，可選
            road: 道路名稱，可選
            
        Returns:
            交通狀況資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            params = {}
            if area:
                params["area"] = area
            if road:
                params["road"] = road
            
            logger.info(f"查詢即時交通狀況: {area or ''} {road or ''}")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["traffic_etag"],
                params=params
            )
            return self._process_response(response)
        except APIError as e:
            logger.error(f"查詢即時交通狀況失敗: {e.message}")
            raise
    
    def get_traffic_incidents(self, area: Optional[str] = None) -> List[Dict[str, Any]]:
        """獲取交通事件資訊
        
        Args:
            area: 行政區，可選
            
        Returns:
            交通事件列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            params = {"area": area} if area else None
            logger.info(f"查詢交通事件: {area if area else '所有區域'}")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["traffic_etag"],
                params=params
            )
            return self._process_response(response)
        except APIError as e:
            logger.error(f"查詢交通事件失敗: {e.message}")
            raise 