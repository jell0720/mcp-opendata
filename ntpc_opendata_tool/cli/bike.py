"""
自行車相關命令模組

提供查詢 YouBike2.0 站點、自行車架、自行車道等功能。
"""
import typer
from typing import Optional
from ntpc_opendata_tool.api import BikeAPI
from ntpc_opendata_tool.cli.main import handle_api_error, format_output, console

# 初始化自行車 API 客戶端
bike_api = BikeAPI()

# 創建子命令應用
app = typer.Typer(help="自行車相關資訊查詢")


@app.command("youbike")
@handle_api_error
def get_youbike_stations(
    area: Optional[str] = typer.Option(
        None, "--area", "-a", help="行政區名稱，例如「板橋區」、「新莊區」"
    ),
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """查詢 YouBike2.0 站點資訊"""
    if area:
        console.print(f"查詢 {area} 的 YouBike2.0 站點資訊")
    else:
        console.print("查詢所有 YouBike2.0 站點資訊")
    
    data = bike_api.get_youbike_stations(area)
    format_output(data, format, "YouBike2.0 站點資訊列表")


@app.command("available-bikes")
@handle_api_error
def get_available_youbikes(
    min_bikes: int = typer.Option(
        1, "--min-bikes", "-m", help="最少可借車輛數"
    ),
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """查詢有可借車輛的 YouBike 站點"""
    console.print(f"查詢至少有 {min_bikes} 輛可借車輛的 YouBike 站點")
    
    data = bike_api.get_available_youbikes(min_bikes)
    format_output(data, format, "有可借車輛的 YouBike 站點列表")


@app.command("nearby-youbike")
@handle_api_error
def find_nearby_youbike(
    latitude: float = typer.Argument(..., help="緯度"),
    longitude: float = typer.Argument(..., help="經度"),
    radius: int = typer.Option(
        500, "--radius", "-r", help="搜尋半徑（公尺）"
    ),
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """查詢附近的 YouBike 站點"""
    console.print(f"搜尋座標 ({latitude}, {longitude}) 半徑 {radius} 公尺內的 YouBike 站點")
    
    data = bike_api.find_nearby_youbike(latitude, longitude, radius)
    format_output(data, format, "附近的 YouBike 站點")


@app.command("bike-racks")
@handle_api_error
def get_bike_racks(
    area: Optional[str] = typer.Option(
        None, "--area", "-a", help="行政區名稱，例如「板橋區」、「新莊區」"
    ),
    near_mrt: bool = typer.Option(
        False, "--near-mrt", help="是否只查詢捷運站週邊的自行車架"
    ),
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """查詢自行車架資訊"""
    if area:
        console.print(f"查詢 {area} 的{'捷運站週邊' if near_mrt else ''}自行車架資訊")
    else:
        console.print(f"查詢所有{'捷運站週邊' if near_mrt else ''}自行車架資訊")
    
    data = bike_api.get_bike_racks(area, near_mrt)
    format_output(data, format, "自行車架資訊列表")


@app.command("bike-lanes")
@handle_api_error
def get_bike_lanes(
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """查詢自行車道建設統計資料"""
    console.print("查詢自行車道建設統計資料")
    
    data = bike_api.get_bike_lanes()
    format_output(data, format, "自行車道建設統計資料")


if __name__ == "__main__":
    app() 