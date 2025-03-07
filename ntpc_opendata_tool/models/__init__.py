"""
資料模型模組

提供各種資料模型類和解析函數。
"""

from .bus import (
    BusRoute, BusStop, BusEstimatedTime, BusRealTime,
    parse_bus_routes, parse_bus_stops, parse_bus_estimated_times, parse_bus_real_times
)
from .traffic import (
    TrafficStatus, ConstructionInfo, ParkingLot as TrafficParkingLot, TrafficCamera, TrafficIncident,
    parse_traffic_status, parse_construction_info, parse_parking_lots as parse_traffic_parking_lots,
    parse_traffic_cameras, parse_traffic_incidents
)
from .parking import (
    ParkingLot, ParkingFeeRate, ParkingStatus, ParkingOpenHour,
    parse_parking_lots, parse_parking_fee_rates, parse_parking_status, parse_parking_open_hours
)

__all__ = [
    # 公車相關模型
    "BusRoute", "BusStop", "BusEstimatedTime", "BusRealTime",
    "parse_bus_routes", "parse_bus_stops", "parse_bus_estimated_times", "parse_bus_real_times",
    
    # 交通相關模型
    "TrafficStatus", "ConstructionInfo", "TrafficParkingLot", "TrafficCamera", "TrafficIncident",
    "parse_traffic_status", "parse_construction_info", "parse_traffic_parking_lots",
    "parse_traffic_cameras", "parse_traffic_incidents",
    
    # 停車場相關模型
    "ParkingLot", "ParkingFeeRate", "ParkingStatus", "ParkingOpenHour",
    "parse_parking_lots", "parse_parking_fee_rates", "parse_parking_status", "parse_parking_open_hours"
] 