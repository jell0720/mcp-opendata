# MCP 工具：新北市交通局 OpenData 查詢

這是一個 MCP（Multi-Cloud Platform）工具，用於查詢新北市交通局的開放資料（OpenData）。該工具允許使用者直接在 Claude 中查詢新北市交通相關的開放資料應用，並獲取回應。

## 功能特點

- 整合新北市交通局 OpenData API
- 提供簡單的命令列介面
- 支援多種交通資料查詢（如公車路線、站點資訊、即時交通狀況等）
- 資料過濾與排序選項
- 錯誤處理與友善提示
- MCP 服務整合

## 安裝

### 使用虛擬環境

```bash
# 建立虛擬環境
python -m venv .venv

# 啟動虛擬環境
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate     # Windows

# 安裝依賴
pip install -e .
```

### 使用 MCP 安裝

```bash
mcp install ntpc_opendata_tool/server.py --name "新北市交通 OpenData 查詢" --with requests --with python-dotenv --with uvicorn --with typer --with pandas
```

## 使用方法

### 命令列工具

```bash
# 基本使用
ntpc-opendata --help

# 查詢公車路線
ntpc-opendata bus-route 307

# 查詢站點資訊
ntpc-opendata bus-stop "捷運板橋站"

# 查詢即時交通狀況
ntpc-opendata traffic-status --area "板橋區"
```

### 作為 MCP 服務使用

在 Claude 中，可以直接調用此 MCP 服務：

```
我想查詢新北市307公車的路線資訊。
```

## 開發

### 環境設置

```bash
# 安裝開發依賴
pip install -e ".[dev]"

# 運行測試
pytest
```

### 目錄結構

```
ntpc_opendata_tool/
├── ntpc_opendata_tool/
│   ├── __init__.py
│   ├── api/          # API 調用相關模組
│   ├── cli/          # 命令列介面
│   ├── models/       # 資料模型定義
│   ├── utils/        # 工具函數
│   └── server.py     # MCP 服務主入口
├── pyproject.toml    # 專案設定
├── README.md         # 專案說明
└── .env.example      # 環境變數範例
```

## 授權

本專案採用 MIT 授權。 