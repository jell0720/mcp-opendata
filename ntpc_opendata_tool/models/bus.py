"""
公車相關資料模型

用於解析和格式化公車相關 API 的回應數據。
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class BusRoute(BaseModel):
    """公車路線模型"""
    route_id: str = Field(..., alias="routeId")
    route_name: str = Field(..., alias="routeName")
    route_type: Optional[str] = Field(None, alias="routeType")
    operator: Optional[str] = None
    start_stop: Optional[str] = Field(None, alias="startStop")
    end_stop: Optional[str] = Field(None, alias="endStop")
    frequency: Optional[str] = None
    fare: Optional[str] = None
    description: Optional[str] = None
    
    class Config:
        populate_by_name = True


class BusStop(BaseModel):
    """公車站點模型"""
    stop_id: str = Field(..., alias="stopId")
    stop_name: str = Field(..., alias="stopName")
    stop_sequence: int = Field(..., alias="stopSequence")
    route_id: str = Field(..., alias="routeId")
    route_name: str = Field(..., alias="routeName")
    direction: Optional[int] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    address: Optional[str] = None
    
    class Config:
        populate_by_name = True


class BusEstimatedTime(BaseModel):
    """公車預計到站時間模型"""
    route_id: str = Field(..., alias="routeId")
    route_name: str = Field(..., alias="routeName")
    stop_id: str = Field(..., alias="stopId")
    stop_name: str = Field(..., alias="stopName")
    direction: int
    estimated_time: Optional[int] = Field(None, alias="estimatedTime")  # 秒數
    status: Optional[str] = None  # 狀態說明，如「即將進站」、「未發車」等
    plate_number: Optional[str] = Field(None, alias="plateNumber")  # 車牌號碼
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")
    
    class Config:
        populate_by_name = True


class BusRealTime(BaseModel):
    """公車即時位置模型"""
    plate_number: str = Field(..., alias="plateNumber")
    route_id: str = Field(..., alias="routeId")
    route_name: str = Field(..., alias="routeName")
    direction: int
    longitude: float
    latitude: float
    speed: Optional[float] = None
    azimuth: Optional[float] = None  # 方位角
    status: Optional[str] = None  # 狀態，如「行駛中」、「停靠站」等
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")
    
    class Config:
        populate_by_name = True


def parse_bus_routes(data: List[Dict[str, Any]]) -> List[BusRoute]:
    """解析公車路線資料
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的公車路線物件列表
    """
    return [BusRoute.model_validate(item) for item in data]


def parse_bus_stops(data: List[Dict[str, Any]]) -> List[BusStop]:
    """解析公車站點資料
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的公車站點物件列表
    """
    return [BusStop.model_validate(item) for item in data]


def parse_bus_estimated_times(data: List[Dict[str, Any]]) -> List[BusEstimatedTime]:
    """解析公車預計到站時間資料
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的公車預計到站時間物件列表
    """
    return [BusEstimatedTime.model_validate(item) for item in data]


def parse_bus_real_times(data: List[Dict[str, Any]]) -> List[BusRealTime]:
    """解析公車即時位置資料
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的公車即時位置物件列表
    """
    return [BusRealTime.model_validate(item) for item in data] 