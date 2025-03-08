"""
公車相關命令模組

提供查詢公車路線、站牌與預計到站時間等功能。
"""
import typer
from typing import Optional
from ntpc_opendata_tool.api import BusAPI
from ntpc_opendata_tool.cli.main import handle_api_error, format_output, console

# 初始化公車 API 客戶端
bus_api = BusAPI()

# 創建子命令應用
app = typer.Typer(help="公車相關資訊查詢")


@app.command("routes")
@handle_api_error
def get_routes(
    route_name: Optional[str] = typer.Argument(
        None, help="路線名稱或編號，如未提供則返回所有路線"
    ),
    page: int = typer.Option(0, "--page", "-p", help="頁碼(0..N)"),
    size: int = typer.Option(100, "--size", "-s", help="每頁筆數"),
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """查詢公車路線資訊"""
    if route_name:
        console.print(f"查詢路線: {route_name}")
    else:
        console.print(f"查詢所有路線 (頁碼: {page}, 每頁筆數: {size})")
    
    data = bus_api.get_routes(route_name, page, size)
    format_output(data, format, f"路線資訊: {route_name if route_name else '所有路線'}")


@app.command("stops")
@handle_api_error
def get_stops(
    route_name: str = typer.Argument(..., help="路線名稱或編號"),
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """查詢公車路線站點資訊"""
    console.print(f"查詢路線 {route_name} 的站點資訊")
    
    data = bus_api.get_stops(route_name)
    format_output(data, format, f"路線 {route_name} 的站點資訊")


@app.command("arrival")
@handle_api_error
def get_estimated_time(
    route_name: str = typer.Argument(..., help="路線名稱或編號"),
    stop_name: Optional[str] = typer.Option(
        None, "--stop", "-s", help="站點名稱，如未提供則返回該路線所有站點的到站時間"
    ),
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """查詢公車預計到站時間"""
    if stop_name:
        console.print(f"查詢路線 {route_name} 在站點 {stop_name} 的到站時間")
    else:
        console.print(f"查詢路線 {route_name} 的所有站點到站時間")
    
    data = bus_api.get_estimated_time(route_name, stop_name)
    format_output(data, format, f"路線 {route_name} 的預計到站時間")


@app.command("all-stops")
@handle_api_error
def get_all_stops(
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """查詢所有公車站點資訊"""
    console.print("查詢所有公車站點資訊")
    
    data = bus_api.get_all_stops()
    format_output(data, format, "所有公車站點資訊")


@app.command("search-by-stop")
@handle_api_error
def search_by_stop(
    stop_name: str = typer.Argument(..., help="站點名稱"),
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """根據站點名稱搜尋路線"""
    console.print(f"搜尋經過站點 {stop_name} 的路線")
    
    data = bus_api.search_by_stop(stop_name)
    format_output(data, format, f"經過站點 {stop_name} 的路線資訊")


@app.command("real-time")
@handle_api_error
def get_real_time(
    route_name: str = typer.Argument(..., help="路線名稱或編號"),
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """查詢公車即時位置資訊"""
    console.print(f"查詢路線 {route_name} 的公車即時位置")
    
    data = bus_api.get_real_time_by_route(route_name)
    format_output(data, format, f"路線 {route_name} 的即時公車位置")


@app.command("operators")
@handle_api_error
def get_bus_operators(
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """查詢公車業者資訊"""
    console.print("查詢公車業者資訊")
    
    data = bus_api.get_bus_operators()
    format_output(data, format, "公車業者資訊")


@app.command("transfer-discounts")
@handle_api_error
def get_bus_transfer_discounts(
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """查詢公車轉乘優惠資訊"""
    console.print("查詢公車轉乘優惠資訊")
    
    data = bus_api.get_bus_transfer_discounts()
    format_output(data, format, "公車轉乘優惠資訊")


@app.command("route-info")
@handle_api_error
def get_route_info(
    route_name: Optional[str] = typer.Argument(
        None, help="路線名稱或編號，如未提供則返回所有路線說明"
    ),
    route_type: Optional[str] = typer.Option(
        None, "--type", "-t", help="路線類型，如：一般路線、快速公車、跳蛙路線、捷運接駁、捷運先導、幸福巴士、新巴士、輕軌公車"
    ),
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """查詢公車路線說明及示意圖"""
    if route_name and route_type:
        console.print(f"查詢類型為 {route_type} 的路線 {route_name} 的說明及示意圖")
    elif route_name:
        console.print(f"查詢路線 {route_name} 的說明及示意圖")
    elif route_type:
        console.print(f"查詢類型為 {route_type} 的所有路線說明及示意圖")
    else:
        console.print("查詢所有路線說明及示意圖")
    
    data = bus_api.get_route_info(route_type, route_name)
    format_output(data, format, "公車路線說明及示意圖")


if __name__ == "__main__":
    app() 