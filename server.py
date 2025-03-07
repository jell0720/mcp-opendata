import re
import json
import logging
import sys
from typing import Dict, Any, List, Optional, Union

from mcp.server.fastmcp import FastMCP

# 使用相對導入
from .ntpc_opendata_tool.utils.logger import setup_logger
from .ntpc_opendata_tool.api.bus import BusAPI
from .ntpc_opendata_tool.api.traffic import TrafficAPI
from .ntpc_opendata_tool.api.parking import ParkingAPI
from .ntpc_opendata_tool.api.client import APIError

# 設置日誌
logger = setup_logger("ntpc_opendata_mcp")

# 初始化 API 客戶端
bus_api = BusAPI()
traffic_api = TrafficAPI() 
parking_api = ParkingAPI()

# ... existing code ...
