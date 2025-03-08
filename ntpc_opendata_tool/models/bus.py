"""
公車相關資料模型

用於解析和格式化公車相關 API 的回應數據。
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class BusRoute(BaseModel):
    """公車路線模型"""
    id: str = Field(..., alias="Id")
    provider_id: str = Field(..., alias="providerId")
    provider_name: str = Field(..., alias="providerName")
    name_zh: str = Field(..., alias="nameZh")
    name_en: str = Field(..., alias="nameEn")
    path_attribute_id: str = Field(..., alias="pathAttributeId")
    path_attribute_name: str = Field(..., alias="pathAttributeName")
    path_attribute_ename: str = Field(..., alias="pathAttributeEname")
    build_period: Optional[str] = Field(None, alias="buildPeriod")
    departure_zh: str = Field(..., alias="departureZh")
    departure_en: str = Field(..., alias="departureEn")
    destination_zh: str = Field(..., alias="destinationZh")
    destination_en: str = Field(..., alias="destinationEn")
    real_sequence: Optional[str] = Field(None, alias="realSequence")
    distance: Optional[str] = Field(None, alias="distance")
    go_first_bus_time: Optional[str] = Field(None, alias="goFirstBusTime")
    back_first_bus_time: Optional[str] = Field(None, alias="backFirstBusTime")
    go_last_bus_time: Optional[str] = Field(None, alias="goLastBusTime")
    back_last_bus_time: Optional[str] = Field(None, alias="backLastBusTime")
    peak_headway: Optional[str] = Field(None, alias="peakHeadway")
    holiday_headway_desc: Optional[str] = Field(None, alias="holidayHeadwayDesc")
    off_peak_headway: Optional[str] = Field(None, alias="offPeakHeadway")
    bus_time_desc: Optional[str] = Field(None, alias="busTimeDesc")
    holiday_go_first_bus_time: Optional[str] = Field(None, alias="holidayGoFirstBusTime")
    holiday_back_first_bus_time: Optional[str] = Field(None, alias="holidayBackFirstBusTime")
    holiday_go_last_bus_time: Optional[str] = Field(None, alias="holidayGoLastBusTime")
    holiday_back_last_bus_time: Optional[str] = Field(None, alias="holidayBackLastBusTime")
    holiday_bus_time_desc: Optional[str] = Field(None, alias="holidayBusTimeDesc")
    headway_desc: Optional[str] = Field(None, alias="headwayDesc")
    holiday_peak_headway: Optional[str] = Field(None, alias="holidayPeakHeadway")
    holiday_off_peak_headway: Optional[str] = Field(None, alias="holidayOffPeakHeadway")
    segment_buffer_zh: Optional[str] = Field(None, alias="segmentBufferZh")
    segment_buffer_en: Optional[str] = Field(None, alias="segmentBufferEn")
    ticket_price_description_zh: Optional[str] = Field(None, alias="ticketPriceDescriptionZh")
    ticket_price_description_en: Optional[str] = Field(None, alias="ticketPriceDescriptionEn")
    
    class Config:
        populate_by_name = True


class BusStop(BaseModel):
    """公車站點模型"""
    id: str = Field(..., alias="Id")
    route_id: str = Field(..., alias="routeId")
    name_zh: str = Field(..., alias="nameZh")
    name_en: str = Field(..., alias="nameEn")
    seq_no: str = Field(..., alias="seqNo")
    pgp: str = Field(..., alias="pgp")
    go_back: str = Field(..., alias="goBack")
    longitude: str = Field(..., alias="longitude")
    latitude: str = Field(..., alias="latitude")
    address: Optional[str] = Field(None, alias="address")
    stop_location_id: str = Field(..., alias="stopLocationId")
    show_lon: str = Field(..., alias="showLon")
    show_lat: str = Field(..., alias="showLat")
    vector: Optional[str] = Field(None, alias="vector")
    
    class Config:
        populate_by_name = True


class BusEstimatedTime(BaseModel):
    """公車預計到站時間模型"""
    route_id: str = Field(..., alias="RouteID")
    stop_id: str = Field(..., alias="StopID")
    estimate_time: str = Field(..., alias="EstimateTime")
    go_back: str = Field(..., alias="GoBack")
    
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


class BusOperator(BaseModel):
    """公車業者模型"""
    id: str = Field(..., alias="Id")
    name: str = Field(..., alias="name")
    phone: Optional[str] = Field(None, alias="phone")
    email: Optional[str] = Field(None, alias="email")
    website: Optional[str] = Field(None, alias="website")
    address: Optional[str] = Field(None, alias="address")
    
    class Config:
        populate_by_name = True


class BusRouteInfo(BaseModel):
    """公車路線說明模型"""
    id: str = Field(..., alias="Id")
    route_name: str = Field(..., alias="routeName")
    route_type: Optional[str] = Field(None, alias="routeType")
    route_map_url: Optional[str] = Field(None, alias="routeMapUrl")
    description: Optional[str] = Field(None, alias="description")
    
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


def parse_bus_operators(data: List[Dict[str, Any]]) -> List[BusOperator]:
    """解析公車業者資料
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的公車業者物件列表
    """
    return [BusOperator.model_validate(item) for item in data]


def parse_bus_route_info(data: List[Dict[str, Any]]) -> List[BusRouteInfo]:
    """解析公車路線說明資料
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的公車路線說明物件列表
    """
    return [BusRouteInfo.model_validate(item) for item in data] 