"""
新北市自行車相關 API 功能模組

提供 YouBike2.0、自行車架、自行車道等資訊查詢功能。
"""
import logging
import math
from typing import Dict, List, Any, Optional, Union
from ntpc_opendata_tool.api.client import OpenDataClient, APIError
from ntpc_opendata_tool.models.bike import (
    YouBikeStation, BikeRackDistrict, BikeRackMRT, BikeLane,
    parse_youbike_stations, parse_bike_rack_districts, parse_bike_rack_mrt, parse_bike_lanes
)

logger = logging.getLogger(__name__)


class BikeAPI:
    """新北市自行車 API 服務類
    
    提供自行車相關資訊查詢功能，包括 YouBike2.0 站點、自行車架、自行車道等。
    """
    
    def __init__(self, client: Optional[OpenDataClient] = None):
        """初始化自行車 API 服務
        
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
    
    def get_youbike_stations(self, area: Optional[str] = None) -> List[YouBikeStation]:
        """獲取 YouBike2.0 站點資訊
        
        Args:
            area: 行政區，可選
            
        Returns:
            YouBike 站點資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            params = {"area": area} if area else None
            logger.info(f"查詢 YouBike2.0 站點資訊: {area if area else '所有區域'}")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["youbike"],
                params=params
            )
            data = self._process_response(response)
            return parse_youbike_stations(data)
        except APIError as e:
            logger.error(f"查詢 YouBike 站點資訊失敗: {e.message}")
            raise
    
    def get_bike_racks(self, area: Optional[str] = None, near_mrt: bool = False) -> List[Union[BikeRackDistrict, BikeRackMRT]]:
        """獲取自行車架資訊
        
        Args:
            area: 行政區，可選
            near_mrt: 是否只查詢捷運站週邊的自行車架，預設 False
            
        Returns:
            自行車架資訊列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            params = {"area": area} if area else None
            
            resource_id = self.client.RESOURCE_IDS["bike_racks_mrt"] if near_mrt else self.client.RESOURCE_IDS["bike_racks_districts"]
            
            logger.info(f"查詢{'捷運站週邊' if near_mrt else ''}自行車架資訊: {area if area else '所有區域'}")
            
            response = self.client.get_by_resource_id(
                resource_id,
                params=params
            )
            data = self._process_response(response)
            
            if near_mrt:
                return parse_bike_rack_mrt(data)
            else:
                return parse_bike_rack_districts(data)
        except APIError as e:
            logger.error(f"查詢自行車架資訊失敗: {e.message}")
            raise
    
    def get_bike_lanes(self) -> List[BikeLane]:
        """獲取自行車道建設統計資料
        
        Returns:
            自行車道建設統計資料列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            logger.info("查詢自行車道建設統計資料")
            
            response = self.client.get_by_resource_id(
                self.client.RESOURCE_IDS["bike_lanes"]
            )
            data = self._process_response(response)
            return parse_bike_lanes(data)
        except APIError as e:
            logger.error(f"查詢自行車道建設統計資料失敗: {e.message}")
            raise
            
    def find_nearby_youbike(self, lat: float, lon: float, radius: int = 500) -> List[YouBikeStation]:
        """查詢附近的 YouBike 站點
        
        Args:
            lat: 緯度
            lon: 經度
            radius: 搜尋半徑（公尺），預設 500 公尺
            
        Returns:
            附近 YouBike 站點列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            logger.info(f"查詢位置 ({lat}, {lon}) 半徑 {radius}m 內的 YouBike 站點")
            
            # 獲取所有站點
            all_stations = self.get_youbike_stations()
            
            # 計算距離並篩選
            nearby_stations = []
            
            for station in all_stations:
                try:
                    station_lat = station.latitude
                    station_lon = station.longitude
                    
                    if station_lat and station_lon:
                        # 計算距離
                        distance = self._calculate_distance(lat, lon, station_lat, station_lon)
                        
                        if distance <= radius:
                            # 設置距離屬性
                            station.distance = int(distance)
                            nearby_stations.append(station)
                except (ValueError, TypeError):
                    continue
            
            # 按距離排序
            return sorted(nearby_stations, key=lambda x: x.distance or 999999)
            
        except APIError as e:
            logger.error(f"查詢附近 YouBike 站點失敗: {e.message}")
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
            
    def get_available_youbikes(self, min_bikes: int = 1) -> List[YouBikeStation]:
        """獲取有可借車輛的 YouBike 站點
        
        Args:
            min_bikes: 最少可借車輛數，預設為 1
            
        Returns:
            有可借車輛的 YouBike 站點列表
            
        Raises:
            APIError: 當 API 請求失敗時
        """
        try:
            logger.info(f"查詢至少有 {min_bikes} 輛可借車輛的 YouBike 站點")
            
            all_stations = self.get_youbike_stations()
            
            # 篩選有足夠可借車輛的站點
            available_stations = [
                station for station in all_stations 
                if station.available_bikes >= min_bikes
            ]
            
            # 按可借車輛數排序
            return sorted(available_stations, key=lambda x: x.available_bikes, reverse=True)
            
        except APIError as e:
            logger.error(f"查詢有可借車輛的 YouBike 站點失敗: {e.message}")
            raise 