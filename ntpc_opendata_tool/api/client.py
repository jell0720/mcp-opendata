"""
新北市交通局 OpenData API 客戶端模組

此模組提供基礎的 API 請求功能，包含錯誤處理、身份驗證等。
"""
import os
import logging
from typing import Dict, Any, Optional, Union
import requests
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 設置日誌
logger = logging.getLogger(__name__)


class APIError(Exception):
    """API 請求錯誤的自訂異常"""
    
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Any] = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class OpenDataClient:
    """新北市交通局 OpenData API 客戶端基礎類
    
    提供與 OpenData API 溝通的基本方法，包含 GET/POST 請求、
    錯誤處理、參數驗證等功能。
    """
    
    # 定義已知的資源 UUID
    RESOURCE_IDS = {
        "bus_stops": "34b402a8-53d9-483d-9406-24a682c2d6dc",  # 公車站位資訊
        "bus_routes": "0ee4e6bf-cee6-4ec8-8fe1-71f544015127",  # 公車路線清單
        "bus_estimated_time": "07f7ccb3-ed00-43c4-966d-08e9dab24e95",  # 公車預估到站時間
        "parking_realtime": "e09b35a5-a738-48cc-b0f5-570b67ad9c78",  # 公有路外停車場即時資訊
        "traffic_cameras": "157501bf-f1cd-4838-92a7-612770351e43",  # 交通局CCTV點位
        "traffic_etag": "357b88f7-947e-4f65-b966-c6a40d434fbe",  # 交通局etag點位
        "parking_lots": "b1464ef0-9c7c-4a6f-abf7-6bdf32847e68",  # 路外公共停車場資訊
        "roadside_parking": "54a507c4-c038-41b5-bf60-bbecb9d052c6",  # 路邊停車空位查詢
    }
    
    def __init__(self):
        """初始化 API 客戶端
        
        從環境變數中讀取設定，包含基礎 URL、API 金鑰等。
        """
        self.base_url = os.getenv("NTPC_OPENDATA_BASE_URL", "https://data.ntpc.gov.tw/api/datasets")
        self.api_key = os.getenv("NTPC_OPENDATA_API_KEY", "")
        self.timeout = int(os.getenv("REQUEST_TIMEOUT", "30"))
        
        logger.info(f"初始化 OpenDataClient，基礎 URL: {self.base_url}")
    
    def _build_headers(self) -> Dict[str, str]:
        """構建 HTTP 請求標頭
        
        Returns:
            Dict[str, str]: 包含認證資訊的標頭
        """
        headers = {"Accept": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers
    
    def _handle_response(self, response: requests.Response) -> Any:
        """處理 API 回應
        
        Args:
            response: requests.Response 物件
            
        Returns:
            解析後的 JSON 資料
            
        Raises:
            APIError: 當 API 回應含有錯誤時
        """
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP 錯誤: {e}"
            logger.error(error_msg)
            try:
                error_data = response.json()
                logger.error(f"API 錯誤詳情: {error_data}")
            except ValueError:
                error_data = response.text
            
            raise APIError(
                message=error_msg,
                status_code=response.status_code,
                response=error_data
            )
        except ValueError:
            error_msg = "無法解析 JSON 回應"
            logger.error(error_msg)
            raise APIError(message=error_msg, response=response.text)
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """發送 GET 請求至 API 端點
        
        Args:
            endpoint: API 端點路徑
            params: 查詢參數
            
        Returns:
            解析後的 API 回應
            
        Raises:
            APIError: 當請求失敗時
        """
        # 確保 endpoint 不含有多餘的空格
        endpoint = endpoint.strip()
        
        # 檢查是否為 UUID 格式的端點
        if endpoint in self.RESOURCE_IDS.values():
            url = f"{self.base_url}/{endpoint}/json"
        else:
            url = f"{self.base_url}/{endpoint}"
            
        headers = self._build_headers()
        
        # 處理 params 中可能含有的空格
        if params:
            processed_params = {}
            for key, value in params.items():
                if isinstance(value, str):
                    processed_params[key] = value.strip()
                else:
                    processed_params[key] = value
            params = processed_params
        
        logger.debug(f"發送 GET 請求至 {url}，參數: {params}")
        
        try:
            response = requests.get(
                url, 
                params=params, 
                headers=headers, 
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            error_msg = f"請求異常: {str(e)}"
            logger.error(error_msg)
            raise APIError(message=error_msg)
    
    def get_by_resource_id(self, resource_id: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """使用資源 ID 發送 GET 請求
        
        Args:
            resource_id: 資源 ID (UUID)
            params: 查詢參數
            
        Returns:
            解析後的 API 回應
            
        Raises:
            APIError: 當請求失敗時
            ValueError: 當資源 ID 無效時
        """
        if resource_id not in self.RESOURCE_IDS.values():
            raise ValueError(f"無效的資源 ID: {resource_id}")
        
        return self.get(f"{resource_id}/json", params)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, 
             json_data: Optional[Dict[str, Any]] = None) -> Any:
        """發送 POST 請求至 API 端點
        
        Args:
            endpoint: API 端點路徑
            data: 表單資料
            json_data: JSON 資料
            
        Returns:
            解析後的 API 回應
            
        Raises:
            APIError: 當請求失敗時
        """
        url = f"{self.base_url}/{endpoint}"
        headers = self._build_headers()
        
        logger.debug(f"發送 POST 請求至 {url}")
        
        try:
            response = requests.post(
                url, 
                data=data, 
                json=json_data,
                headers=headers, 
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            error_msg = f"請求異常: {str(e)}"
            logger.error(error_msg)
            raise APIError(message=error_msg) 