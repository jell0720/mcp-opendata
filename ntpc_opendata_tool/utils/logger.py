"""
日誌工具模組

提供統一的日誌設定與管理功能。
"""
import os
import logging
from typing import Optional
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()


def setup_logger(name: Optional[str] = None, level: Optional[str] = None) -> logging.Logger:
    """設置並返回日誌器
    
    Args:
        name: 日誌器名稱，如未提供則使用 'ntpc_opendata_tool'
        level: 日誌級別，如未提供則從環境變數讀取，預設為 INFO
        
    Returns:
        已設置的日誌器
    """
    name = name or "ntpc_opendata_tool"
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # 從環境變數獲取日誌級別，預設為 INFO
    if level is None:
        level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    numeric_level = getattr(logging, level, logging.INFO)
    
    # 檢查是否已存在該名稱的日誌器
    logger = logging.getLogger(name)
    
    # 避免重複設置處理器
    if not logger.handlers:
        # 創建控制台處理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(numeric_level)
        
        # 設置格式
        formatter = logging.Formatter(log_format, date_format)
        console_handler.setFormatter(formatter)
        
        # 添加處理器到日誌器
        logger.addHandler(console_handler)
    
    # 設置日誌器級別
    logger.setLevel(numeric_level)
    
    return logger 