"""
交通相關資料模型

用於解析和格式化交通相關 API 的回應數據。
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class TrafficStatus(BaseModel):
    """交通狀況模型"""
    status_id: str = Field(..., alias="statusId")
    road: str
    area: str
    status: str  # 如「順暢」、「擁擠」、「壅塞」等
    avg_speed: Optional[float] = Field(None, alias="avgSpeed")
    congestion_level: Optional[int] = Field(None, alias="congestionLevel")  # 擁擠程度，1-5
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")
    
    class Config:
        populate_by_name = True


class ConstructionInfo(BaseModel):
    """道路施工資訊模型"""
    construction_id: str = Field(..., alias="constructionId")
    road: str
    area: str
    description: str
    start_date: datetime = Field(..., alias="startDate")
    end_date: datetime = Field(..., alias="endDate")
    status: str  # 如「施工中」、「已完成」
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    contact: Optional[str] = None
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")
    
    class Config:
        populate_by_name = True


class ParkingLot(BaseModel):
    """停車場資訊模型"""
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


class TrafficCamera(BaseModel):
    """交通攝影機模型"""
    camera_id: str = Field(..., alias="cameraId")
    road: str
    area: str
    direction: Optional[str] = None
    image_url: Optional[str] = Field(None, alias="imageUrl")
    video_url: Optional[str] = Field(None, alias="videoUrl")
    longitude: float
    latitude: float
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")
    
    class Config:
        populate_by_name = True


class TrafficIncident(BaseModel):
    """交通事件模型"""
    incident_id: str = Field(..., alias="incidentId")
    type: str  # 如「事故」、「拋錨」、「塞車」等
    road: str
    area: str
    description: str
    start_time: datetime = Field(..., alias="startTime")
    end_time: Optional[datetime] = Field(None, alias="endTime")
    status: str  # 如「處理中」、「已解決」
    severity: Optional[int] = None  # 嚴重程度，1-5
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")
    
    class Config:
        populate_by_name = True


def parse_traffic_status(data: List[Dict[str, Any]]) -> List[TrafficStatus]:
    """解析交通狀況資料
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的交通狀況物件列表
    """
    return [TrafficStatus.model_validate(item) for item in data]


def parse_construction_info(data: List[Dict[str, Any]]) -> List[ConstructionInfo]:
    """解析道路施工資訊
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的道路施工資訊物件列表
    """
    return [ConstructionInfo.model_validate(item) for item in data]


def parse_parking_lots(data: List[Dict[str, Any]]) -> List[ParkingLot]:
    """解析停車場資訊
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的停車場資訊物件列表
    """
    return [ParkingLot.model_validate(item) for item in data]


def parse_traffic_cameras(data: List[Dict[str, Any]]) -> List[TrafficCamera]:
    """解析交通攝影機資訊
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的交通攝影機資訊物件列表
    """
    return [TrafficCamera.model_validate(item) for item in data]


def parse_traffic_incidents(data: List[Dict[str, Any]]) -> List[TrafficIncident]:
    """解析交通事件資訊
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的交通事件資訊物件列表
    """
    return [TrafficIncident.model_validate(item) for item in data] 