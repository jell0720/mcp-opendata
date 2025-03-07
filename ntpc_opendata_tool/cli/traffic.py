"""
交通狀況相關命令模組

提供查詢即時交通狀況、道路施工資訊等功能。
"""
import typer
from typing import Optional
from ntpc_opendata_tool.api import TrafficAPI
from ntpc_opendata_tool.cli.main import handle_api_error, format_output, console

# 初始化交通 API 客戶端
traffic_api = TrafficAPI()

# 創建子命令應用
app = typer.Typer(help="交通狀況相關資訊查詢")


@app.command("status")
@handle_api_error
def get_traffic_status(
    area: Optional[str] = typer.Option(
        None, "--area", "-a", help="區域名稱，例如「板橋區」"
    ),
    road: Optional[str] = typer.Option(
        None, "--road", "-r", help="道路名稱，例如「文化路」"
    ),
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """查詢即時交通狀況"""
    msg = "查詢即時交通狀況"
    if area:
        msg += f"，區域：{area}"
    if road:
        msg += f"，道路：{road}"
    console.print(msg)
    
    data = traffic_api.get_traffic_status(area, road)
    format_output(data, format, "即時交通狀況")


@app.command("construction")
@handle_api_error
def get_construction_info(
    area: Optional[str] = typer.Option(
        None, "--area", "-a", help="區域名稱，例如「板橋區」"
    ),
    start_date: Optional[str] = typer.Option(
        None, "--start-date", help="開始日期，格式為 YYYY-MM-DD"
    ),
    end_date: Optional[str] = typer.Option(
        None, "--end-date", help="結束日期，格式為 YYYY-MM-DD"
    ),
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """查詢道路施工資訊"""
    msg = "查詢道路施工資訊"
    if area:
        msg += f"，區域：{area}"
    if start_date and end_date:
        msg += f"，期間：{start_date} 至 {end_date}"
    elif start_date:
        msg += f"，開始日期：{start_date}"
    elif end_date:
        msg += f"，結束日期：{end_date}"
    console.print(msg)
    
    data = traffic_api.get_construction_info(area, start_date, end_date)
    format_output(data, format, "道路施工資訊")


@app.command("cameras")
@handle_api_error
def get_traffic_cameras(
    area: Optional[str] = typer.Option(
        None, "--area", "-a", help="區域名稱，例如「板橋區」"
    ),
    road: Optional[str] = typer.Option(
        None, "--road", "-r", help="道路名稱，例如「文化路」"
    ),
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """查詢交通攝影機資訊"""
    msg = "查詢交通攝影機資訊"
    if area:
        msg += f"，區域：{area}"
    if road:
        msg += f"，道路：{road}"
    console.print(msg)
    
    data = traffic_api.get_traffic_cameras(area, road)
    format_output(data, format, "交通攝影機資訊")


@app.command("incidents")
@handle_api_error
def get_traffic_incidents(
    area: Optional[str] = typer.Option(
        None, "--area", "-a", help="區域名稱，例如「板橋區」"
    ),
    incident_type: Optional[str] = typer.Option(
        None, "--type", "-t", help="事件類型，例如「事故」、「塞車」"
    ),
    start_date: Optional[str] = typer.Option(
        None, "--start-date", help="開始日期，格式為 YYYY-MM-DD"
    ),
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
):
    """查詢交通事件資訊"""
    msg = "查詢交通事件資訊"
    if area:
        msg += f"，區域：{area}"
    if incident_type:
        msg += f"，類型：{incident_type}"
    if start_date:
        msg += f"，開始日期：{start_date}"
    console.print(msg)
    
    data = traffic_api.get_traffic_incidents(area, incident_type, start_date)
    format_output(data, format, "交通事件資訊")


if __name__ == "__main__":
    app() 