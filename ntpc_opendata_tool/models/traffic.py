"""
交通相關資料模型

用於解析和格式化交通相關 API 的回應數據。
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class TrafficCamera(BaseModel):
    """交通監視器模型"""
    cctv_id: str
    district: str
    areacode: str
    address: str
    
    class Config:
        populate_by_name = True


class ETagLocation(BaseModel):
    """ETag 設備位置模型"""
    etag_id: str
    district: str
    areacode: str
    address: str
    
    class Config:
        populate_by_name = True


class HeightLimit(BaseModel):
    """交通限高資訊模型"""
    county: str
    countycode: Optional[str] = None
    area: str
    areacode: Optional[str] = None
    road1: str
    road2: Optional[str] = None
    latitude: str
    longitude: str
    sign_number: str
    sign_name: str
    master_name: str
    second_name: Optional[str] = None
    
    class Config:
        populate_by_name = True


class TrafficImpactAssessment(BaseModel):
    """交通影響評估模型"""
    name: str
    category: str
    url: str
    
    class Config:
        populate_by_name = True


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


def parse_traffic_cameras(data: List[Dict[str, Any]]) -> List[TrafficCamera]:
    """解析交通監視器資料
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的交通監視器物件列表
    """
    return [TrafficCamera.model_validate(item) for item in data]


def parse_etag_locations(data: List[Dict[str, Any]]) -> List[ETagLocation]:
    """解析 ETag 設備位置資料
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的 ETag 設備位置物件列表
    """
    return [ETagLocation.model_validate(item) for item in data]


def parse_height_limits(data: List[Dict[str, Any]]) -> List[HeightLimit]:
    """解析交通限高資訊
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的交通限高資訊物件列表
    """
    return [HeightLimit.model_validate(item) for item in data]


def parse_traffic_impact_assessments(data: List[Dict[str, Any]]) -> List[TrafficImpactAssessment]:
    """解析交通影響評估資料
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的交通影響評估物件列表
    """
    return [TrafficImpactAssessment.model_validate(item) for item in data]


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


def parse_traffic_incidents(data: List[Dict[str, Any]]) -> List[TrafficIncident]:
    """解析交通事件資訊
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的交通事件資訊物件列表
    """
    return [TrafficIncident.model_validate(item) for item in data] 