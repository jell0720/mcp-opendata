"""
新北市交通局 OpenData API 模組

提供訪問新北市交通局 OpenData 資料庫的 API 功能
"""

from ntpc_opendata_tool.api.client import OpenDataClient, APIError
from ntpc_opendata_tool.api.bus import BusAPI
from ntpc_opendata_tool.api.parking import ParkingAPI
from ntpc_opendata_tool.api.traffic import TrafficAPI
from ntpc_opendata_tool.api.bike import BikeAPI
from ntpc_opendata_tool.api.misc_traffic import MiscTrafficAPI

__all__ = [
    'OpenDataClient',
    'APIError',
    'BusAPI',
    'ParkingAPI',
    'TrafficAPI',
    'BikeAPI',
    'MiscTrafficAPI'
] 