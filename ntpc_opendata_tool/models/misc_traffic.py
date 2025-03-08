"""
其他交通服務相關資料模型

用於解析和格式化其他交通服務相關 API 的回應數據，包括計程車服務、拖吊保管場、交通影響評估等。
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class TaxiService(BaseModel):
    """計程車客運服務業經營派遣業務業者模型"""
    countycode: str
    name: str = Field(..., alias="taxi_transportation_service")
    phone: str = Field(..., alias="phone_number")
    
    class Config:
        populate_by_name = True


class TowingStorage(BaseModel):
    """拖吊保管場模型"""
    title: str
    address: str
    tel: str
    distance: Optional[int] = None  # 用於最近拖吊保管場查詢
    
    class Config:
        populate_by_name = True


class TrafficImpactAssessment(BaseModel):
    """交通影響評估模型"""
    name: str
    category: str
    url: str
    
    class Config:
        populate_by_name = True


def parse_taxi_services(data: List[Dict[str, Any]]) -> List[TaxiService]:
    """解析計程車客運服務業經營派遣業務業者資料
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的計程車客運服務業者物件列表
    """
    return [TaxiService.model_validate(item) for item in data]


def parse_towing_storage_info(data: List[Dict[str, Any]]) -> List[TowingStorage]:
    """解析拖吊保管場資料
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的拖吊保管場物件列表
    """
    return [TowingStorage.model_validate(item) for item in data]


def parse_traffic_impact_assessment(data: List[Dict[str, Any]]) -> List[TrafficImpactAssessment]:
    """解析交通影響評估資料
    
    Args:
        data: API 回應的原始資料
        
    Returns:
        解析後的交通影響評估物件列表
    """
    return [TrafficImpactAssessment.model_validate(item) for item in data] 