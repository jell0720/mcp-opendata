"""
新北市交通局 OpenData 命令列工具

提供簡便的命令列介面，讓使用者可以查詢新北市交通相關資訊。
"""
import json
import sys
from typing import Optional, Any, Dict, List

import typer
from rich.console import Console
from rich.table import Table

from ntpc_opendata_tool.utils import setup_logger
from ntpc_opendata_tool.api import APIError

# 初始化日誌
logger = setup_logger()

# 初始化 Typer 應用
app = typer.Typer(
    name="ntpc-opendata",
    help="新北市交通局開放資料查詢工具",
    add_completion=False
)

# 初始化 Rich 控制台
console = Console()


def version_callback(value: bool):
    """返回版本信息的回調函數"""
    if value:
        console.print("新北市交通局 OpenData 命令列工具 v0.1.0")
        raise typer.Exit()


# 定義全局選項
@app.callback()
def main(
    version: bool = typer.Option(
        False, "--version", "-v", help="顯示版本信息", callback=version_callback
    ),
    format: str = typer.Option(
        "table", "--format", "-f", help="輸出格式: table, json, text"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", help="顯示詳細日誌信息"
    ),
):
    """新北市交通局開放資料命令列工具
    
    提供便捷的方式查詢新北市的公車、交通和停車場資訊。
    """
    # 設置日誌級別
    if verbose:
        setup_logger(level="DEBUG")
        logger.debug("啟用詳細日誌")


def format_output(data: Any, format_type: str = "table", table_title: Optional[str] = None):
    """格式化輸出結果
    
    Args:
        data: 要輸出的資料
        format_type: 輸出格式（table、json 或 text）
        table_title: 表格標題（僅在 format_type 為 table 時有效）
    """
    if format_type == "json":
        if isinstance(data, (dict, list)):
            return console.print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            return console.print(str(data))
    
    if format_type == "text":
        if isinstance(data, list):
            for item in data:
                console.print(item)
        else:
            console.print(data)
        return
    
    # 預設以表格形式輸出
    if isinstance(data, list) and len(data) > 0:
        table = Table(title=table_title)
        
        # 動態添加列
        sample = data[0]
        for key in sample.keys():
            table.add_column(key)
        
        # 添加行
        for item in data:
            row = [str(value) for value in item.values()]
            table.add_row(*row)
        
        console.print(table)
    elif isinstance(data, dict):
        table = Table(title=table_title)
        table.add_column("屬性")
        table.add_column("值")
        
        for key, value in data.items():
            table.add_row(key, str(value))
        
        console.print(table)
    else:
        console.print(data)


def handle_api_error(func):
    """處理 API 錯誤的裝飾器"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except APIError as e:
            console.print(f"[bold red]錯誤: {e.message}[/bold red]")
            if e.status_code:
                console.print(f"狀態碼: {e.status_code}")
            sys.exit(1)
        except Exception as e:
            console.print(f"[bold red]未預期錯誤: {str(e)}[/bold red]")
            logger.exception("執行時發生未預期錯誤")
            sys.exit(1)
    
    return wrapper


def register_commands():
    """註冊所有子命令"""
    from ntpc_opendata_tool.cli import bus, traffic, parking
    
    # 添加子命令
    app.add_typer(bus.app, name="bus", help="公車相關資訊查詢")
    app.add_typer(traffic.app, name="traffic", help="交通狀況相關資訊查詢")
    app.add_typer(parking.app, name="parking", help="停車場相關資訊查詢")


# 為了與 pyproject.toml 中的設定相符，命令列入口點需命名為 cli
def cli():
    """命令列入口點"""
    register_commands()
    app()


if __name__ == "__main__":
    cli() 