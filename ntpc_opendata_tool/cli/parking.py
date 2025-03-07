"""
停車場相關命令模組

提供查詢停車場資訊、收費標準、即時狀態等功能。
"""
import typer
from typing import Optional
from ntpc_opendata_tool.api import ParkingAPI
from ntpc_opendata_tool.cli.main import handle_api_error, format_output, console

# 初始化停車場 API 客戶端
parking_api = ParkingAPI()

# 創建子命令應用
app = typer.Typer(help="停車場相關資訊查詢")


@app.command("list")
@handle_api_error
def list_parking_lots(
    area: Optional[str] = typer.Option(
        None, "--area", "-a", help="區域名稱，例如「板橋區」、「新莊區」"
    ),
    type_name: Optional[str] = typer.Option(
        None, "--type", "-t", help="停車場類型，例如「路邊停車」、「立體停車場」"
    ),
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """列出停車場資訊"""
    if area:
        console.print(f"查詢 {area} 的停車場資訊")
        data = parking_api.get_parking_lots_by_area(area)
    elif type_name:
        console.print(f"查詢類型為 {type_name} 的停車場資訊")
        data = parking_api.get_parking_lots_by_type(type_name)
    else:
        console.print("查詢所有停車場資訊")
        data = parking_api.get_all_parking_lots()
    
    format_output(data, format, "停車場資訊列表")


@app.command("info")
@handle_api_error
def get_parking_lot_info(
    parking_id: str = typer.Argument(..., help="停車場 ID"),
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """查詢特定停車場詳細資訊"""
    console.print(f"查詢停車場 ID {parking_id} 的詳細資訊")
    
    data = parking_api.get_parking_lot_by_id(parking_id)
    format_output(data, format, f"停車場 {parking_id} 詳細資訊")


@app.command("available")
@handle_api_error
def get_available_parking_lots(
    min_spaces: Optional[int] = typer.Option(
        None, "--min-spaces", "-m", help="最小空位數量"
    ),
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """查詢有空位的停車場"""
    if min_spaces is not None:
        console.print(f"查詢至少有 {min_spaces} 個空位的停車場")
    else:
        console.print("查詢有空位的停車場")
    
    data = parking_api.get_available_parking_lots(min_spaces)
    format_output(data, format, "有空位的停車場列表")


@app.command("fee-rates")
@handle_api_error
def get_parking_fee_rates(
    parking_id: Optional[str] = typer.Option(
        None, "--id", help="停車場 ID，如未提供則返回所有停車場的收費標準"
    ),
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """查詢停車場收費標準"""
    if parking_id:
        console.print(f"查詢停車場 ID {parking_id} 的收費標準")
    else:
        console.print("查詢所有停車場的收費標準")
    
    data = parking_api.get_parking_fee_rates(parking_id)
    format_output(data, format, "停車場收費標準")


@app.command("nearby")
@handle_api_error
def find_nearby_parking(
    longitude: float = typer.Argument(..., help="經度"),
    latitude: float = typer.Argument(..., help="緯度"),
    radius: Optional[int] = typer.Option(
        None, "--radius", "-r", help="搜尋半徑（公尺）"
    ),
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """查詢附近的停車場"""
    if radius:
        console.print(f"搜尋座標 ({longitude}, {latitude}) 半徑 {radius} 公尺內的停車場")
    else:
        console.print(f"搜尋座標 ({longitude}, {latitude}) 附近的停車場")
    
    data = parking_api.find_nearby_parking(longitude, latitude, radius)
    format_output(data, format, "附近的停車場")


@app.command("status")
@handle_api_error
def get_real_time_status(
    parking_id: Optional[str] = typer.Option(
        None, "--id", help="停車場 ID，如未提供則返回所有停車場的即時狀態"
    ),
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """查詢停車場即時狀態"""
    if parking_id:
        console.print(f"查詢停車場 ID {parking_id} 的即時狀態")
    else:
        console.print("查詢所有停車場的即時狀態")
    
    data = parking_api.get_real_time_parking_status(parking_id)
    format_output(data, format, "停車場即時狀態")


if __name__ == "__main__":
    app() 