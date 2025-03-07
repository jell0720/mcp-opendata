# MCP Langflow 文檔問答工具開發規劃

## 一、目標說明
- 建立一個 MCP 服務器，利用 FastMCP 類整合 Langflow 文檔問答功能。
- 提供一個簡單介面，接收使用者查詢後調用 Langflow API 進行檢索。
- 加入提示模板、狀態查詢與錯誤處理，確保系統穩定運作。
- 利用 Typer 與 uvicorn 建立命令列工具與服務端，方便操作與管理。

---

## 二、環境與專案設置
### 1. 建立虛擬環境
- 使用 `uv` 建立虛擬環境。
- 指令：

  ```sh
  uv add "mcp[cli]"
  ```

- 啟動虛擬環境：

  ```sh
  source .venv/bin/activate
  ```

### 2. 依賴管理
- 使用 `pyproject.toml` 定義專案依賴。
- 依賴包含：`requests`、`python-dotenv`、`mcp[cli]`、`typer`、`uvicorn` 等。

### 3. 專案目錄結構
- 建立專案資料夾：

  ```sh
  mkdir -p langflow_mcp_tool
  ```

- 程式碼皆置於 `langflow_mcp_tool` 目錄中，方便管理與打包。

---

## 三、功能設計與流程
### 1. 使用者輸入與查詢格式化
- 提供使用者介面接收查詢提示詞。
- 製作提示模板，協助使用者規範查詢內容。

### 2. 調用 Langflow API
- 利用 `requests` 模組發送 HTTP POST 請求。
- 根據使用者輸入，組合 `payload` 並呼叫 API。
- 處理返回結果，並進行錯誤與異常管理。

### 3. MCP 服務整合
- 使用 `FastMCP` 類建立服務器。
- 整合資源查詢功能，提供 Langflow 服務狀態資訊。
- 設計接口，讓查詢結果能夠以統一格式返回。

---

## 四、命令列工具與 MCP 安裝
### 1. 建立命令列工具
- 利用 `Typer` 建立命令列工具。
- 設定命令入口：在 `pyproject.toml` 的 `[project.scripts]` 中指定：

  ```toml
  [project.scripts]
  langflow-mcp = "langflow_mcp_tool.cli:cli"
  ```

- 實作 `CLI` 模組，包含基本的命令參數與幫助說明。

### 2. MCP 安裝與部署
- 安裝 MCP 工具，將 `server.py` 部署到 MCP 系統中：

  ```sh
  source .venv/bin/activate && mcp install langflow_mcp_tool/server.py --name "Langflow 文檔問答" --with requests --with python-dotenv --with uvicorn --with typer
  ```

---

## 五、測試與資源 URI 修正
### 1. API 測試
- 撰寫單元測試 (`pytest`) 測試 API 調用與回傳格式。
- 確認各功能模組正常運作，避免意外錯誤。

### 2. 資源 URI 格式修正
- 檢查所有資源 `URI` 是否符合 `URL` 格式。
- 如有錯誤，立即修正為正確的 `URL` 格式。

---

## 六、Cloud Desktop 套件整合
### 1. 安裝 Cloud Desktop 所需套件
- 根據 `Cloud Desktop` 需求，確認並安裝所有相關依賴。
- 測試整合後系統能夠正常運作，確保用戶體驗良好。

---

## 七、錯誤處理與日誌管理
### 1. 例外處理
- 增加 `try-except` 機制，捕捉 API 調用及其他錯誤。
- 提供友善錯誤訊息，方便使用者了解發生了什麼問題。

### 2. 日誌記錄
- 建議加入 `日誌模組`，記錄關鍵操作與錯誤資訊。
- 方便後續追蹤與除錯。

---

## 八、文件與說明文件
### 1. README 文件
- 撰寫詳細 `README`，說明專案背景、環境設置、使用方法與開發注意事項。
- 包含部署指令與常見問題解答，方便其他開發者與使用者參考。

### 2. 程式碼註解
- 在程式碼中加入清晰註解，便於維護與後續擴展。

---

## 九、後續規劃與功能擴充
### 1. 功能擴充
- 未來可增加更多資源查詢、智能提示與多語言支持等功能。
- 持續更新與優化系統，提升使用者體驗。

### 2. 使用者反饋
- 收集使用者反饋，定期檢視並改善工具功能。
- 建立 `FAQ` 與線上支援，方便用戶交流與疑難排解。

---

請依照上述更新後的規劃步驟逐步執行，並密切注意各環節細節。若在開發過程中遇到任何問題，請隨時進一步討論或查詢相關文件。

