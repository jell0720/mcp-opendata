"""
資料模型模組

提供各種資料模型類和解析函數。
"""

from .bus import (
    BusRoute, BusStop, BusEstimatedTime, BusRealTime,
    parse_bus_routes, parse_bus_stops, parse_bus_estimated_times, parse_bus_real_times
)
from .traffic import (
    TrafficStatus, ConstructionInfo, TrafficCamera, TrafficIncident,
    ETagLocation, HeightLimit, TrafficImpactAssessment as TrafficImpactAssessmentTraffic,
    parse_traffic_status, parse_construction_info, parse_traffic_cameras, 
    parse_traffic_incidents, parse_etag_locations, parse_height_limits,
    parse_traffic_impact_assessments as parse_traffic_impact_assessments_traffic
)
from .parking import (
    ParkingLot, ParkingAvailability, RoadsideParking, MotorcycleParking,
    WomenChildrenParking, DisabledParking, TyphoonParking, RoadsideParkingManagement,
    parse_parking_lots, parse_parking_availability, parse_roadside_parking,
    parse_motorcycle_parking, parse_women_children_parking, parse_disabled_parking,
    parse_typhoon_parking, parse_roadside_parking_management
)
from .bike import (
    YouBikeStation, BikeRackDistrict, BikeRackMRT, BikeLane,
    parse_youbike_stations, parse_bike_rack_districts, parse_bike_rack_mrt, parse_bike_lanes
)
from .misc_traffic import (
    TaxiService, TowingStorage, TrafficImpactAssessment,
    parse_taxi_services, parse_towing_storage_info, parse_traffic_impact_assessment
)

__all__ = [
    # 公車相關模型
    "BusRoute", "BusStop", "BusEstimatedTime", "BusRealTime",
    "parse_bus_routes", "parse_bus_stops", "parse_bus_estimated_times", "parse_bus_real_times",
    
    # 交通相關模型
    "TrafficStatus", "ConstructionInfo", "TrafficCamera", "TrafficIncident",
    "ETagLocation", "HeightLimit", "TrafficImpactAssessmentTraffic",
    "parse_traffic_status", "parse_construction_info", "parse_traffic_cameras", 
    "parse_traffic_incidents", "parse_etag_locations", "parse_height_limits",
    "parse_traffic_impact_assessments_traffic",
    
    # 停車場相關模型
    "ParkingLot", "ParkingAvailability", "RoadsideParking", "MotorcycleParking",
    "WomenChildrenParking", "DisabledParking", "TyphoonParking", "RoadsideParkingManagement",
    "parse_parking_lots", "parse_parking_availability", "parse_roadside_parking",
    "parse_motorcycle_parking", "parse_women_children_parking", "parse_disabled_parking",
    "parse_typhoon_parking", "parse_roadside_parking_management",
    
    # 自行車相關模型
    "YouBikeStation", "BikeRackDistrict", "BikeRackMRT", "BikeLane",
    "parse_youbike_stations", "parse_bike_rack_districts", "parse_bike_rack_mrt", "parse_bike_lanes",
    
    # 其他交通服務相關模型
    "TaxiService", "TowingStorage", "TrafficImpactAssessment",
    "parse_taxi_services", "parse_towing_storage_info", "parse_traffic_impact_assessment"
] 