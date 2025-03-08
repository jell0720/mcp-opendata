"""
新北市其他交通服務相關 API 功能模組

提供計程車服務、拖吊保管場等資訊查詢功能。
"""
import logging
import math
from typing import Dict, List, Any, Optional
from ntpc_opendata_tool.api.client import OpenDataClient, APIError
from ntpc_opendata_tool.models.misc_traffic import (
    TaxiService, TowingStorage, TrafficImpactAssessment,
    parse_taxi_services, parse_towing_storage_info, parse_traffic_impact_assessment
)

logger = logging.getLogger(__name__)


class MiscTrafficAPI:
    """新北市其他交通服務 API 服務類
    
    提供計程車服務、拖吊保管場等資訊查詢功能。
    """
    
    def __init__(self, client: Optional[OpenDataClient] = None):
        """初始化其他交通服務 API 服務
        
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
    
    def get_taxi_services(self) -> List[TaxiService]:
        """獲取計程車客運服務業經營派遣業務業者資訊
        
        Returns:
            計程車客運服務業者資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            logger.info("查詢計程車客運服務業者資訊")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["taxi_service"]
            )
            data = self._process_response(response)
            return parse_taxi_services(data)
        except APIError as e:
            logger.error(f"查詢計程車客運服務業者資訊失敗: {e.message}")
            raise
    
    def get_towing_storage_info(self) -> List[TowingStorage]:
        """獲取拖吊保管場資訊
        
        Returns:
            拖吊保管場資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            logger.info("查詢拖吊保管場資訊")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["towing_storage"]
            )
            data = self._process_response(response)
            return parse_towing_storage_info(data)
        except APIError as e:
            logger.error(f"查詢拖吊保管場資訊失敗: {e.message}")
            raise
    
    def get_traffic_impact_assessment(self) -> List[TrafficImpactAssessment]:
        """獲取建築物交通影響評估資訊
        
        Returns:
            建築物交通影響評估資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            logger.info("查詢建築物交通影響評估資訊")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["traffic_impact_assessment"]
            )
            data = self._process_response(response)
            return parse_traffic_impact_assessment(data)
        except APIError as e:
            logger.error(f"查詢建築物交通影響評估資訊失敗: {e.message}")
            raise
            
    def find_nearest_towing_storage(self, lat: float, lon: float) -> Optional[TowingStorage]:
        """查詢最近的拖吊保管場
        
        Args:
            lat: 緯度
            lon: 經度
            
        Returns:
            最近的拖吊保管場資訊，如果找不到則返回 None
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            logger.info(f"查詢位置 ({lat}, {lon}) 最近的拖吊保管場")
            
            # 獲取所有拖吊保管場
            all_storage = self.get_towing_storage_info()
            
            # 計算距離並找出最近的
            nearest = None
            min_distance = float('inf')
            
            for storage in all_storage:
                try:
                    # 注意：目前資料中沒有經緯度資訊，這裡只是預留功能
                    # 實際應用時需要確認資料中是否有經緯度資訊
                    # 如果有，可以使用以下方法計算距離
                    # distance = self._calculate_distance(lat, lon, float(storage.latitude), float(storage.longitude))
                    # if distance < min_distance:
                    #     min_distance = distance
                    #     storage.distance = int(distance)
                    #     nearest = storage
                    pass
                except (ValueError, TypeError):
                    continue
            
            if nearest:
                return nearest
            else:
                logger.warning("找不到拖吊保管場資訊或無法計算距離")
                return None
            
        except APIError as e:
            logger.error(f"查詢最近拖吊保管場失敗: {e.message}")
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
            
    def search_taxi_service(self, keyword: str) -> List[TaxiService]:
        """關鍵字搜尋計程車服務
        
        Args:
            keyword: 搜尋關鍵字，可以是業者名稱或電話的一部分
            
        Returns:
            符合搜尋條件的計程車服務列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            logger.info(f"以關鍵字 '{keyword}' 搜尋計程車服務")
            
            all_services = self.get_taxi_services()
            
            # 過濾符合條件的服務
            result = []
            
            for service in all_services:
                if keyword.lower() in service.name.lower() or keyword in service.phone:
                    result.append(service)
            
            return result
            
        except APIError as e:
            logger.error(f"搜尋計程車服務失敗: {e.message}")
            raise 