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
        """獲取路外公共停車場資訊
        
        Args:
            area: 行政區，可選。如未提供則返回所有停車場
            
        Returns:
            停車場資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            params = {"AREA": area} if area else None
            logger.info(f"查詢路外公共停車場資訊: {area if area else '所有區域'}")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["parking_lots"],
                params=params
            )
            return self._process_response(response)
        except APIError as e:
            logger.error(f"查詢路外公共停車場資訊失敗: {e.message}")
            raise
    
    def get_parking_lots_by_type(self, lot_type: str) -> List[Dict[str, Any]]:
        """依類型獲取路外公共停車場資訊
        
        Args:
            lot_type: 停車場類型
            
        Returns:
            停車場資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            logger.info(f"查詢類型為 {lot_type} 的路外公共停車場")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["parking_lots"],
                params={"TYPE": lot_type}
            )
            return self._process_response(response)
        except APIError as e:
            logger.error(f"查詢路外公共停車場類型失敗: {e.message}")
            raise
    
    def get_parking_lot_detail(self, parking_id: str) -> Dict[str, Any]:
        """獲取特定路外公共停車場詳細資訊
        
        Args:
            parking_id: 停車場 ID
            
        Returns:
            停車場詳細資訊
            
        Raises:
            APIError: 當 API 請求失敗時或找不到停車場時
        """
        try:
            logger.info(f"查詢停車場 {parking_id} 的詳細資訊")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["parking_lots"],
                params={"ID": parking_id}
            )
            data = self._process_response(response)
            
            if not data:
                raise APIError(f"找不到停車場: {parking_id}")
            
            return data[0]
        except APIError as e:
            logger.error(f"查詢停車場詳細資訊失敗: {e.message}")
            raise
    
    def get_available_parking_lots(self, min_spaces: int = 1, area: Optional[str] = None) -> List[Dict[str, Any]]:
        """獲取有空位的路外公共停車場
        
        Args:
            min_spaces: 最少空位數，預設為 1
            area: 行政區，可選
            
        Returns:
            有空位的停車場列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            logger.info(f"查詢有至少 {min_spaces} 個空位的停車場 {f'(區域: {area})' if area else ''}")
            
            # 獲取即時空位資訊
            availability_response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["parking_realtime"]
            )
            availability_data = self._process_response(availability_response)
            
            # 篩選有足夠空位的停車場 ID
            available_ids = [
                item["ID"] for item in availability_data 
                if item.get("AVAILABLECAR", "0").isdigit() and int(item["AVAILABLECAR"]) >= min_spaces
            ]
            
            if not available_ids:
                return []
            
            # 獲取停車場基本資訊
            params = {}
            if area:
                params["AREA"] = area
            
            lots_response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["parking_lots"],
                params=params
            )
            lots_data = self._process_response(lots_response)
            
            # 合併資訊
            result = []
            availability_dict = {item["ID"]: item["AVAILABLECAR"] for item in availability_data}
            
            for lot in lots_data:
                if lot["ID"] in available_ids:
                    lot_copy = lot.copy()
                    lot_copy["AVAILABLECAR"] = availability_dict.get(lot["ID"], "0")
                    result.append(lot_copy)
            
            return result
        except APIError as e:
            logger.error(f"查詢有空位的停車場失敗: {e.message}")
            raise
    
    def get_roadside_parking_spaces(self, area: Optional[str] = None) -> List[Dict[str, Any]]:
        """獲取路邊停車空位資訊
        
        Args:
            area: 行政區代碼，可選。如未提供則返回所有路邊停車空位
            
        Returns:
            路邊停車空位資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            params = {"AreaCode": area} if area else None
            logger.info(f"查詢路邊停車空位資訊: {area if area else '所有區域'}")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["roadside_parking"],
                params=params
            )
            return self._process_response(response)
        except APIError as e:
            logger.error(f"查詢路邊停車空位資訊失敗: {e.message}")
            raise
    
    def get_nearby_parking_lots(self, lat: float, lon: float, radius: int = 500) -> List[Dict[str, Any]]:
        """獲取指定位置附近的路外公共停車場
        
        Args:
            lat: 緯度
            lon: 經度
            radius: 搜尋半徑（公尺），預設為 500 公尺
            
        Returns:
            附近的停車場列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            logger.info(f"查詢位置 ({lat}, {lon}) 附近 {radius} 公尺內的停車場")
            
            # 獲取所有停車場
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["parking_lots"]
            )
            lots_data = self._process_response(response)
            
            # 計算距離並篩選
            import math
            
            def calculate_distance(lat1: float, lon1: float, lat2: str, lon2: str) -> float:
                """計算兩點間的距離（公尺）"""
                try:
                    lat2_float = float(lat2)
                    lon2_float = float(lon2)
                    
                    # 使用簡化版的 Haversine 公式計算距離
                    R = 6371000  # 地球半徑（公尺）
                    dlat = math.radians(lat2_float - lat1)
                    dlon = math.radians(lon2_float - lon1)
                    a = (math.sin(dlat/2) * math.sin(dlat/2) +
                         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2_float)) *
                         math.sin(dlon/2) * math.sin(dlon/2))
                    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
                    distance = R * c
                    
                    return distance
                except (ValueError, TypeError):
                    return float('inf')  # 無法計算距離時返回無限大
            
            result = []
            for lot in lots_data:
                # 使用 TW97 座標系統的座標
                if "TW97X" in lot and "TW97Y" in lot and lot["TW97X"] and lot["TW97Y"]:
                    # 這裡需要將 TW97 座標轉換為 WGS84 座標
                    # 由於轉換較複雜，這裡僅使用近似值進行示範
                    # 實際應用中應使用專業的座標轉換庫
                    
                    # 簡化處理：直接使用 TW97 座標計算距離
                    distance = calculate_distance(lat, lon, lot["TW97Y"], lot["TW97X"])
                    
                    if distance <= radius:
                        lot_copy = lot.copy()
                        lot_copy["distance"] = distance
                        result.append(lot_copy)
            
            # 按距離排序
            result.sort(key=lambda x: x.get("distance", float('inf')))
            
            return result
        except APIError as e:
            logger.error(f"查詢附近停車場失敗: {e.message}")
            raise
    
    def get_motorcycle_parking(self, area: Optional[str] = None) -> List[Dict[str, Any]]:
        """獲取機車停車彎資訊
        
        Args:
            area: 行政區，可選。如未提供則返回所有機車停車彎
            
        Returns:
            機車停車彎資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            params = {"area": area} if area else None
            logger.info(f"查詢機車停車彎資訊: {area if area else '所有區域'}")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["motorcycle_parking"],
                params=params
            )
            return self._process_response(response)
        except APIError as e:
            logger.error(f"查詢機車停車彎資訊失敗: {e.message}")
            raise
    
    def get_women_children_parking(self, area: Optional[str] = None) -> List[Dict[str, Any]]:
        """獲取婦幼停車位資訊
        
        Args:
            area: 行政區，可選。如未提供則返回所有婦幼停車位
            
        Returns:
            婦幼停車位資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            params = {"area": area} if area else None
            logger.info(f"查詢婦幼停車位資訊: {area if area else '所有區域'}")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["women_children_parking"],
                params=params
            )
            return self._process_response(response)
        except APIError as e:
            logger.error(f"查詢婦幼停車位資訊失敗: {e.message}")
            raise
    
    def get_disabled_parking(self, area: Optional[str] = None) -> List[Dict[str, Any]]:
        """獲取身心障礙停車格資訊
        
        Args:
            area: 行政區，可選。如未提供則返回所有身心障礙停車格
            
        Returns:
            身心障礙停車格資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            params = {"zone": area} if area else None
            logger.info(f"查詢身心障礙停車格資訊: {area if area else '所有區域'}")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["disabled_parking"],
                params=params
            )
            return self._process_response(response)
        except APIError as e:
            logger.error(f"查詢身心障礙停車格資訊失敗: {e.message}")
            raise
    
    def get_typhoon_parking(self) -> List[Dict[str, Any]]:
        """獲取颱風期間可供停車路段資訊
        
        Returns:
            颱風期間可供停車路段資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            logger.info("查詢颱風期間可供停車路段資訊")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["typhoon_parking"]
            )
            return self._process_response(response)
        except APIError as e:
            logger.error(f"查詢颱風期間可供停車路段資訊失敗: {e.message}")
            raise
    
    def get_roadside_parking_management(self) -> List[Dict[str, Any]]:
        """獲取路邊收費停管場資訊
        
        Returns:
            路邊收費停管場資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            logger.info("查詢路邊收費停管場資訊")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["roadside_parking_management"]
            )
            return self._process_response(response)
        except APIError as e:
            logger.error(f"查詢路邊收費停管場資訊失敗: {e.message}")
            raise 