"""
停車場相關資料模型

用於解析和格式化停車場相關 API 的回應數據。
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, time
from pydantic import BaseModel, Field


class ParkingLot(BaseModel):
    """路外公共停車場模型"""
    id: str = Field(..., alias="ID")
    area: str = Field(..., alias="AREA")
    name: str = Field(..., alias="NAME")
    type: str = Field(..., alias="TYPE")
    summary: str = Field(..., alias="SUMMARY")
    address: str = Field(..., alias="ADDRESS")
    tel: Optional[str] = Field(None, alias="TEL")
    payex: Optional[str] = Field(None, alias="PAYEX")
    service_time: Optional[str] = Field(None, alias="SERVICETIME")
    tw97x: Optional[str] = Field(None, alias="TW97X")
    tw97y: Optional[str] = Field(None, alias="TW97Y")
    total_car: Optional[str] = Field(None, alias="TOTALCAR")
    total_motor: Optional[str] = Field(None, alias="TOTALMOTOR")
    total_bike: Optional[str] = Field(None, alias="TOTALBIKE")
    
    class Config:
        populate_by_name = True


class ParkingAvailability(BaseModel):
    """停車場即時空位模型"""
    id: str = Field(..., alias="ID")
    available_car: str = Field(..., alias="AVAILABLECAR")
    
    class Config:
        populate_by_name = True


class RoadsideParking(BaseModel):
    """路邊停車空位模型"""
    id: str = Field(..., alias="ID")
    cell_id: str = Field(..., alias="CELLID")
    name: str = Field(..., alias="NAME")
    day: str = Field(..., alias="DAY")
    hour: str = Field(..., alias="HOUR")
    pay: str = Field(..., alias="PAY")
    pay_cash: str = Field(..., alias="PAYCASH")
    memo: Optional[str] = Field(None, alias="MEMO")
    road_id: str = Field(..., alias="ROADID")
    road_name: str = Field(..., alias="ROADNAME")
    cell_status: str = Field(..., alias="CELLSTATUS")
    is_now_cash: str = Field(..., alias="ISNOWCASH")
    parking_status: str = Field(..., alias="ParkingStatus")
    latitude: str = Field(..., alias="latitude")
    longitude: str = Field(..., alias="longitude")
    county_code: str = Field(..., alias="CountyCode")
    area_code: str = Field(..., alias="AreaCode")
    
    class Config:
        populate_by_name = True


class MotorcycleParking(BaseModel):
    """機車停車彎模型"""
    area: str
    areacode: str
    address: str
    motorcycle_parking_bay_length: str
    parking_lots: str
    
    class Config:
        populate_by_name = True


class WomenChildrenParking(BaseModel):
    """婦幼停車位模型"""
    area: str
    areacode: str
    address: str
    quantity: str
    
    class Config:
        populate_by_name = True


class DisabledParking(BaseModel):
    """身心障礙停車格模型"""
    zone: str
    areacode: str
    address: str
    quantity: str
    vehicle_classification: str
    charged: str
    disabled_parking_sign: str
    disabled_parking_lot: str
    
    class Config:
        populate_by_name = True


class TyphoonParking(BaseModel):
    """颱風期間可供停車路段模型"""
    area: str
    areacode: str
    road_section: str
    road_direction: str
    road_length: str
    parking_capacity: str
    
    class Config:
        populate_by_name = True


class RoadsideParkingManagement(BaseModel):
    """路邊收費停管場模型"""
    area: str
    areacode: str
    name: str
    address: str
    
    class Config:
        populate_by_name = True


def parse_parking_lots(data: List[Dict[str, Any]]) -> List[ParkingLot]:
    """解析路外公共停車場資料
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的路外公共停車場物件列表
    """
    return [ParkingLot.model_validate(item) for item in data]


def parse_parking_availability(data: List[Dict[str, Any]]) -> List[ParkingAvailability]:
    """解析停車場即時空位資料
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的停車場即時空位物件列表
    """
    return [ParkingAvailability.model_validate(item) for item in data]


def parse_roadside_parking(data: List[Dict[str, Any]]) -> List[RoadsideParking]:
    """解析路邊停車空位資料
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的路邊停車空位物件列表
    """
    return [RoadsideParking.model_validate(item) for item in data]


def parse_motorcycle_parking(data: List[Dict[str, Any]]) -> List[MotorcycleParking]:
    """解析機車停車彎資料
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的機車停車彎物件列表
    """
    return [MotorcycleParking.model_validate(item) for item in data]


def parse_women_children_parking(data: List[Dict[str, Any]]) -> List[WomenChildrenParking]:
    """解析婦幼停車位資料
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的婦幼停車位物件列表
    """
    return [WomenChildrenParking.model_validate(item) for item in data]


def parse_disabled_parking(data: List[Dict[str, Any]]) -> List[DisabledParking]:
    """解析身心障礙停車格資料
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的身心障礙停車格物件列表
    """
    return [DisabledParking.model_validate(item) for item in data]


def parse_typhoon_parking(data: List[Dict[str, Any]]) -> List[TyphoonParking]:
    """解析颱風期間可供停車路段資料
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的颱風期間可供停車路段物件列表
    """
    return [TyphoonParking.model_validate(item) for item in data]


def parse_roadside_parking_management(data: List[Dict[str, Any]]) -> List[RoadsideParkingManagement]:
    """解析路邊收費停管場資料
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的路邊收費停管場物件列表
    """
    return [RoadsideParkingManagement.model_validate(item) for item in data] 