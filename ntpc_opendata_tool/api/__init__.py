"""
新北市交通局 OpenData API 模組

提供與新北市交通局 OpenData API 通信的功能。
"""

from .client import OpenDataClient, APIError
from .bus import BusAPI
from .traffic import TrafficAPI
from .parking import ParkingAPI

__all__ = ["OpenDataClient", "APIError", "BusAPI", "TrafficAPI", "ParkingAPI"] 