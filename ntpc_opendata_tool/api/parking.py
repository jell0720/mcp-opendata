"""
新北市停車場相關 API 功能模組

提供停車場資訊、即時車位數等查詢功能。
"""
import logging
from typing import Dict, List, Any, Optional, Union
from ntpc_opendata_tool.api.client import OpenDataClient, APIError

logger = logging.getLogger(__name__)


class ParkingAPI:
    """新北市停車場 API 服務類
    
    提供停車場相關資訊查詢功能，包括停車場基本資訊、即時車位數等。
    """
    
    def __init__(self, client: Optional[OpenDataClient] = None):
        """初始化停車場 API 服務
        
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
    
    def get_parking_lots(self, area: Optional[str] = None) -> List[Dict[str, Any]]:
        """獲取停車場基本資訊
        
        Args:
            area: 行政區，可選。如未提供則返回所有停車場
            
        Returns:
            停車場資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            params = {"area": area} if area else None
            logger.info(f"查詢停車場資訊: {area if area else '所有區域'}")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["parking_lots"],
                params=params
            )
            return self._process_response(response)
        except APIError as e:
            logger.error(f"查詢停車場資訊失敗: {e.message}")
            raise
    
    def get_parking_lots_by_type(self, lot_type: str) -> List[Dict[str, Any]]:
        """依類型獲取停車場資訊
        
        Args:
            lot_type: 停車場類型
            
        Returns:
            停車場資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            logger.info(f"查詢類型為 {lot_type} 的停車場")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["parking_lots"],
                params={"type": lot_type}
            )
            return self._process_response(response)
        except APIError as e:
            logger.error(f"查詢停車場類型失敗: {e.message}")
            raise
    
    def get_parking_lot_detail(self, parking_id: str) -> Dict[str, Any]:
        """獲取特定停車場詳細資訊
        
        Args:
            parking_id: 停車場 ID
            
        Returns:
            停車場詳細資訊
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            logger.info(f"查詢停車場 {parking_id} 的詳細資訊")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["parking_lots"],
                params={"id": parking_id}
            )
            data = self._process_response(response)
            return data[0] if data else {}
        except APIError as e:
            logger.error(f"查詢停車場詳細資訊失敗: {e.message}")
            raise
    
    def get_available_parking_lots(self, min_spaces: int = 1, area: Optional[str] = None) -> List[Dict[str, Any]]:
        """獲取有空位的停車場資訊
        
        Args:
            min_spaces: 最少空位數，預設為 1
            area: 行政區，可選。如提供則只返回指定區域的停車場
            
        Returns:
            有空位的停車場列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            params = {"minSpaces": min_spaces}
            if area:
                params["area"] = area
            
            logger.info(f"查詢{area+'的' if area else ''}至少有 {min_spaces} 個空位的停車場")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["parking_realtime"],
                params=params
            )
            
            data = self._process_response(response)
            
            # 如果指定了區域，過濾結果
            if area and data:
                data = [lot for lot in data if area in lot.get("area", "")]
            
            return data
        except APIError as e:
            logger.error(f"查詢停車場空位失敗: {e.message}")
            raise
    
    def get_roadside_parking_spaces(self, area: Optional[str] = None) -> List[Dict[str, Any]]:
        """獲取路邊停車格資訊
        
        Args:
            area: 行政區，可選
            
        Returns:
            路邊停車格資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            params = {"area": area} if area else None
            logger.info(f"查詢路邊停車格資訊: {area if area else '所有區域'}")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["roadside_parking"],
                params=params
            )
            return self._process_response(response)
        except APIError as e:
            logger.error(f"查詢路邊停車格資訊失敗: {e.message}")
            raise
    
    def get_nearby_parking_lots(self, lat: float, lon: float, radius: int = 500) -> List[Dict[str, Any]]:
        """查詢附近的停車場
        
        Args:
            lat: 緯度
            lon: 經度
            radius: 搜尋半徑（公尺），預設 500 公尺
            
        Returns:
            附近停車場列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            logger.info(f"查詢位置 ({lat}, {lon}) 半徑 {radius}m 內的停車場")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["parking_lots"],
                params={
                    "lat": lat,
                    "lon": lon,
                    "radius": radius
                }
            )
            return self._process_response(response)
        except APIError as e:
            logger.error(f"查詢附近停車場失敗: {e.message}")
            raise 