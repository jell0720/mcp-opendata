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
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """查詢公車路線資訊"""
    if route_name:
        console.print(f"查詢路線: {route_name}")
    else:
        console.print("查詢所有路線")
    
    data = bus_api.get_routes(route_name)
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


@app.command("search-by-stop")
@handle_api_error
def search_by_stop(
    stop_name: str = typer.Argument(..., help="站點名稱"),
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """依站點名稱查詢公車資訊"""
    console.print(f"依站點名稱 {stop_name} 查詢公車資訊")
    
    data = bus_api.search_by_stop(stop_name)
    format_output(data, format, f"站點 {stop_name} 的公車資訊")


@app.command("real-time")
@handle_api_error
def get_real_time(
    route_name: str = typer.Argument(..., help="路線名稱或編號"),
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """查詢公車即時位置資訊"""
    console.print(f"查詢路線 {route_name} 的實時公車位置")
    
    data = bus_api.get_real_time_by_route(route_name)
    format_output(data, format, f"路線 {route_name} 的即時公車位置")


if __name__ == "__main__":
    app() 