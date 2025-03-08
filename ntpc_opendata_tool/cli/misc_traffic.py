"""
其他交通服務相關命令模組

提供查詢計程車服務、拖吊保管場、交通影響評估等功能。
"""
import typer
from typing import Optional
from ntpc_opendata_tool.api import MiscTrafficAPI
from ntpc_opendata_tool.cli.main import handle_api_error, format_output, console

# 初始化其他交通服務 API 客戶端
misc_traffic_api = MiscTrafficAPI()

# 創建子命令應用
app = typer.Typer(help="其他交通服務相關資訊查詢")


@app.command("taxi-services")
@handle_api_error
def get_taxi_services(
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """查詢計程車客運服務業者資訊"""
    console.print("查詢計程車客運服務業者資訊")
    
    data = misc_traffic_api.get_taxi_services()
    format_output(data, format, "計程車客運服務業者資訊列表")


@app.command("search-taxi")
@handle_api_error
def search_taxi_service(
    keyword: str = typer.Argument(..., help="搜尋關鍵字，可以是業者名稱或電話的一部分"),
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """關鍵字搜尋計程車服務"""
    console.print(f"以關鍵字 '{keyword}' 搜尋計程車服務")
    
    data = misc_traffic_api.search_taxi_service(keyword)
    format_output(data, format, f"關鍵字 '{keyword}' 搜尋結果")


@app.command("towing-storage")
@handle_api_error
def get_towing_storage_info(
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """查詢拖吊保管場資訊"""
    console.print("查詢拖吊保管場資訊")
    
    data = misc_traffic_api.get_towing_storage_info()
    format_output(data, format, "拖吊保管場資訊列表")


@app.command("nearest-towing")
@handle_api_error
def find_nearest_towing_storage(
    latitude: float = typer.Argument(..., help="緯度"),
    longitude: float = typer.Argument(..., help="經度"),
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """查詢最近的拖吊保管場"""
    console.print(f"搜尋座標 ({latitude}, {longitude}) 最近的拖吊保管場")
    
    data = misc_traffic_api.find_nearest_towing_storage(latitude, longitude)
    if data:
        format_output([data], format, "最近的拖吊保管場")
    else:
        console.print("找不到拖吊保管場資訊或無法計算距離")


@app.command("impact-assessment")
@handle_api_error
def get_traffic_impact_assessment(
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """查詢建築物交通影響評估資訊"""
    console.print("查詢建築物交通影響評估資訊")
    
    data = misc_traffic_api.get_traffic_impact_assessment()
    format_output(data, format, "建築物交通影響評估資訊列表")


if __name__ == "__main__":
    app() 