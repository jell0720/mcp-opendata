"""
停車場相關資料模型

用於解析和格式化停車場相關 API 的回應數據。
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, time
from pydantic import BaseModel, Field


class ParkingLot(BaseModel):
    """停車場模型"""
    parking_id: str = Field(..., alias="parkingId")
    name: str
    area: str
    address: Optional[str] = None
    type: str  # 如「路邊停車」、「立體停車場」等
    total_spaces: int = Field(..., alias="totalSpaces")
    available_spaces: Optional[int] = Field(None, alias="availableSpaces")
    fee_description: Optional[str] = Field(None, alias="feeDescription")
    open_hours: Optional[str] = Field(None, alias="openHours")
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")
    
    class Config:
        populate_by_name = True


class ParkingFeeRate(BaseModel):
    """停車場收費標準模型"""
    fee_id: str = Field(..., alias="feeId")
    parking_id: str = Field(..., alias="parkingId")
    parking_name: str = Field(..., alias="parkingName")
    vehicle_type: str = Field(..., alias="vehicleType")  # 如「小型車」、「機車」等
    weekday_rate: Optional[float] = Field(None, alias="weekdayRate")
    weekend_rate: Optional[float] = Field(None, alias="weekendRate")
    holiday_rate: Optional[float] = Field(None, alias="holidayRate")
    hourly_rate: Optional[float] = Field(None, alias="hourlyRate")
    daily_maximum: Optional[float] = Field(None, alias="dailyMaximum")
    monthly_rate: Optional[float] = Field(None, alias="monthlyRate")
    description: Optional[str] = None
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")
    
    class Config:
        populate_by_name = True


class ParkingStatus(BaseModel):
    """停車場即時狀態模型"""
    status_id: str = Field(..., alias="statusId")
    parking_id: str = Field(..., alias="parkingId")
    parking_name: str = Field(..., alias="parkingName")
    area: str
    total_spaces: int = Field(..., alias="totalSpaces")
    available_spaces: int = Field(..., alias="availableSpaces")
    occupancy_rate: float = Field(..., alias="occupancyRate")  # 佔用率
    status: str  # 如「尚有空位」、「滿位」等
    updated_at: datetime = Field(..., alias="updatedAt")
    
    class Config:
        populate_by_name = True


class ParkingOpenHour(BaseModel):
    """停車場營業時間模型"""
    parking_id: str = Field(..., alias="parkingId")
    parking_name: str = Field(..., alias="parkingName")
    day_of_week: int = Field(..., alias="dayOfWeek")  # 1-7，1 表示週一
    open_time: time
    close_time: Optional[time] = None  # None 表示 24 小時營業
    is_24hours: bool = Field(..., alias="is24Hours")
    is_closed: bool = Field(..., alias="isClosed")
    description: Optional[str] = None
    
    class Config:
        populate_by_name = True


def parse_parking_lots(data: List[Dict[str, Any]]) -> List[ParkingLot]:
    """解析停車場資料
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的停車場物件列表
    """
    return [ParkingLot.model_validate(item) for item in data]


def parse_parking_fee_rates(data: List[Dict[str, Any]]) -> List[ParkingFeeRate]:
    """解析停車場收費標準資料
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的停車場收費標準物件列表
    """
    return [ParkingFeeRate.model_validate(item) for item in data]


def parse_parking_status(data: List[Dict[str, Any]]) -> List[ParkingStatus]:
    """解析停車場即時狀態資料
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的停車場即時狀態物件列表
    """
    return [ParkingStatus.model_validate(item) for item in data]


def parse_parking_open_hours(data: List[Dict[str, Any]]) -> List[ParkingOpenHour]:
    """解析停車場營業時間資料
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的停車場營業時間物件列表
    """
    return [ParkingOpenHour.model_validate(item) for item in data] 