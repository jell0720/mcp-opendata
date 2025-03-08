"""
自行車相關資料模型

用於解析和格式化自行車相關 API 的回應數據。
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class YouBikeStation(BaseModel):
    """YouBike2.0 站點模型"""
    station_no: str = Field(..., alias="sno")
    station_name: str = Field(..., alias="sna")
    total_bikes: int = Field(..., alias="tot")
    available_bikes: int = Field(..., alias="sbi")
    area: str = Field(..., alias="sarea")
    updated_time: str = Field(..., alias="mday")
    latitude: float = Field(..., alias="lat")
    longitude: float = Field(..., alias="lng")
    address: str = Field(..., alias="ar")
    area_en: str = Field(..., alias="sareaen")
    station_name_en: str = Field(..., alias="snaen")
    address_en: str = Field(..., alias="aren")
    empty_spaces: int = Field(..., alias="bemp")
    is_active: bool = Field(..., alias="act")
    distance: Optional[int] = None  # 用於附近站點查詢
    
    class Config:
        populate_by_name = True


class BikeRackDistrict(BaseModel):
    """行政區自行車架模型"""
    item: str
    area: str = Field(..., alias="the_area_in_new_taipei_city")
    quantity: int
    
    class Config:
        populate_by_name = True


class BikeRackMRT(BaseModel):
    """捷運站週邊自行車架模型"""
    item: str
    station: str = Field(..., alias="the_mrt_stations_in_new_taipei_city")
    quantity: int
    
    class Config:
        populate_by_name = True


class BikeLane(BaseModel):
    """自行車道模型"""
    type: str
    countycode: str
    district: str
    bikeway: str
    route: str
    year_month: str = Field(..., alias="yyymmroc")
    length: float
    
    class Config:
        populate_by_name = True


def parse_youbike_stations(data: List[Dict[str, Any]]) -> List[YouBikeStation]:
    """解析 YouBike2.0 站點資料
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的 YouBike2.0 站點物件列表
    """
    return [YouBikeStation.model_validate(item) for item in data]


def parse_bike_rack_districts(data: List[Dict[str, Any]]) -> List[BikeRackDistrict]:
    """解析行政區自行車架資料
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的行政區自行車架物件列表
    """
    return [BikeRackDistrict.model_validate(item) for item in data]


def parse_bike_rack_mrt(data: List[Dict[str, Any]]) -> List[BikeRackMRT]:
    """解析捷運站週邊自行車架資料
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的捷運站週邊自行車架物件列表
    """
    return [BikeRackMRT.model_validate(item) for item in data]


def parse_bike_lanes(data: List[Dict[str, Any]]) -> List[BikeLane]:
    """解析自行車道資料
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的自行車道物件列表
    """
    return [BikeLane.model_validate(item) for item in data] 