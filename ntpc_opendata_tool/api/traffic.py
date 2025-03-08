"""
新北市交通狀況相關 API 功能模組

提供交通狀況、路況監控、事件通報等資訊查詢功能。
"""
import logging
import math
from typing import Dict, List, Any, Optional, Tuple
from ntpc_opendata_tool.api.client import OpenDataClient, APIError
from ntpc_opendata_tool.models.traffic import (
    TrafficCamera, ETagLocation, HeightLimit, TrafficImpactAssessment,
    parse_traffic_cameras, parse_etag_locations, parse_height_limits,
    parse_traffic_impact_assessments
)

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
    
    def get_traffic_cameras(self, district: Optional[str] = None) -> List[TrafficCamera]:
        """獲取交通監視器資訊
        
        Args:
            district: 行政區，可選
            
        Returns:
            監視器資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            params = {"district": district} if district else None
            
            logger.info(f"查詢交通監視器: {district or '所有區域'}")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["traffic_cameras"],
                params=params
            )
            data = self._process_response(response)
            return parse_traffic_cameras(data)
        except APIError as e:
            logger.error(f"查詢交通監視器失敗: {e.message}")
            raise
    
    def get_etag_locations(self, district: Optional[str] = None) -> List[ETagLocation]:
        """獲取 ETag 設備位置資訊
        
        Args:
            district: 行政區，可選
            
        Returns:
            ETag 設備位置列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            params = {"district": district} if district else None
            logger.info(f"查詢 ETag 設備位置: {district if district else '所有區域'}")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["traffic_etag"],
                params=params
            )
            data = self._process_response(response)
            return parse_etag_locations(data)
        except APIError as e:
            logger.error(f"查詢 ETag 設備位置失敗: {e.message}")
            raise
    
    def get_height_limit_info(self, area: Optional[str] = None, road: Optional[str] = None) -> List[HeightLimit]:
        """獲取交通限高資訊
        
        Args:
            area: 行政區，可選
            road: 道路名稱，可選
            
        Returns:
            交通限高資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            params = {}
            if area:
                params["area"] = area
            if road:
                params["road1"] = road
            
            logger.info(f"查詢交通限高資訊: {area or ''} {road or ''}")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["traffic_height_limit"],
                params=params
            )
            data = self._process_response(response)
            return parse_height_limits(data)
        except APIError as e:
            logger.error(f"查詢交通限高資訊失敗: {e.message}")
            raise
    
    def get_traffic_impact_assessment(self) -> List[TrafficImpactAssessment]:
        """獲取交通影響評估資訊
        
        Returns:
            交通影響評估資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            logger.info("查詢交通影響評估資訊")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["traffic_impact_assessment"]
            )
            data = self._process_response(response)
            return parse_traffic_impact_assessments(data)
        except APIError as e:
            logger.error(f"查詢交通影響評估資訊失敗: {e.message}")
            raise
    
    def get_nearby_traffic_cameras(self, lat: float, lon: float, radius: int = 1000) -> List[TrafficCamera]:
        """獲取指定位置附近的交通監視器
        
        Args:
            lat: 緯度
            lon: 經度
            radius: 搜尋半徑（公尺），預設 1000 公尺
            
        Returns:
            附近的交通監視器列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            logger.info(f"查詢位置 ({lat}, {lon}) 附近 {radius}m 內的交通監視器")
            
            # 獲取所有交通監視器
            all_cameras = self.get_traffic_cameras()
            
            # 篩選出在指定半徑內的監視器
            nearby_cameras = []
            for camera in all_cameras:
                # 目前資料中沒有經緯度資訊，這裡只是預留功能
                # 實際應用時需要確認資料中是否有經緯度資訊
                # 如果有，可以使用以下方法計算距離
                # distance = self._calculate_distance(lat, lon, float(camera.latitude), float(camera.longitude))
                # if distance <= radius:
                #     nearby_cameras.append(camera)
                pass
            
            return nearby_cameras
        except APIError as e:
            logger.error(f"查詢附近交通監視器失敗: {e.message}")
            raise
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """計算兩點間的距離（使用 Haversine 公式）
        
        Args:
            lat1: 第一點緯度
            lon1: 第一點經度
            lat2: 第二點緯度
            lon2: 第二點經度
            
        Returns:
            兩點間的距離（公尺）
        """
        # 地球半徑（公尺）
        R = 6371000
        
        # 將經緯度轉換為弧度
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        # Haversine 公式
        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        
        return distance 