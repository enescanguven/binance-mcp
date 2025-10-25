"""Account management MCP tools for Binance."""

from typing import Any
from mcp.types import Tool
from binance.client import Client


def get_account_tools() -> list[Tool]:
    """Get list of account management tools."""
    return [
        Tool(
            name="get_account_info",
            description="Get current account information including balances",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_asset_balance",
            description="Get balance for a specific asset",
            inputSchema={
                "type": "object",
                "properties": {
                    "asset": {
                        "type": "string",
                        "description": "Asset symbol (e.g., 'BTC', 'USDT')"
                    }
                },
                "required": ["asset"]
            }
        ),
        Tool(
            name="get_account_trades",
            description="Get trades for a specific symbol",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Trading pair symbol (e.g., 'BTCUSDT')"
                    },
                    "limit": {
                        "type": "number",
                        "description": "Number of trades to retrieve (default: 500, max: 1000)",
                        "default": 500
                    },
                    "from_id": {
                        "type": "number",
                        "description": "Trade ID to fetch from"
                    }
                },
                "required": ["symbol"]
            }
        ),
        Tool(
            name="get_account_status",
            description="Get account status (normal, margin, futures)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_trade_fee",
            description="Get trade fee for a symbol",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Trading pair symbol (e.g., 'BTCUSDT')"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_asset_dividend_history",
            description="Get asset dividend history",
            inputSchema={
                "type": "object",
                "properties": {
                    "asset": {
                        "type": "string",
                        "description": "Asset symbol (e.g., 'BTC')"
                    },
                    "start_time": {
                        "type": "number",
                        "description": "Start time in milliseconds"
                    },
                    "end_time": {
                        "type": "number",
                        "description": "End time in milliseconds"
                    }
                },
                "required": []
            }
        ),
    ]


def handle_account_tool(client: Client, name: str, arguments: Any) -> Any:
    """Handle account tool execution."""
    if name == "get_account_info":
        return client.get_account()

    elif name == "get_asset_balance":
        return client.get_asset_balance(asset=arguments["asset"])

    elif name == "get_account_trades":
        return client.get_my_trades(
            symbol=arguments["symbol"],
            limit=arguments.get("limit", 500),
            fromId=arguments.get("from_id")
        )

    elif name == "get_account_status":
        return client.get_account_status()

    elif name == "get_trade_fee":
        symbol = arguments.get("symbol")
        if symbol:
            return client.get_trade_fee(symbol=symbol)
        return client.get_trade_fee()

    elif name == "get_asset_dividend_history":
        return client.get_asset_dividend_history(
            asset=arguments.get("asset"),
            startTime=arguments.get("start_time"),
            endTime=arguments.get("end_time")
        )

    return None
