"""Market data MCP tools for Binance."""

from typing import Any
from mcp.types import Tool
from binance.client import Client


def get_market_tools() -> list[Tool]:
    """Get list of market data tools."""
    return [
        Tool(
            name="get_ticker_price",
            description="Get current price for a symbol or all symbols",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Trading pair symbol (e.g., 'BTCUSDT'). If not provided, returns all symbols"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_ticker_24h",
            description="Get 24-hour price change statistics for a symbol or all symbols",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Trading pair symbol (e.g., 'BTCUSDT'). If not provided, returns all symbols"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_order_book",
            description="Get order book (market depth) for a symbol",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Trading pair symbol (e.g., 'BTCUSDT')"
                    },
                    "limit": {
                        "type": "number",
                        "description": "Number of orders to retrieve (default: 100, max: 5000)",
                        "default": 100
                    }
                },
                "required": ["symbol"]
            }
        ),
        Tool(
            name="get_recent_trades",
            description="Get recent trades for a symbol",
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
                    }
                },
                "required": ["symbol"]
            }
        ),
        Tool(
            name="get_klines",
            description="Get candlestick/kline data for a symbol",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Trading pair symbol (e.g., 'BTCUSDT')"
                    },
                    "interval": {
                        "type": "string",
                        "description": "Kline interval: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M",
                        "default": "1h"
                    },
                    "limit": {
                        "type": "number",
                        "description": "Number of klines to retrieve (default: 500, max: 1000)",
                        "default": 500
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
                "required": ["symbol"]
            }
        ),
        Tool(
            name="get_avg_price",
            description="Get current average price for a symbol",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Trading pair symbol (e.g., 'BTCUSDT')"
                    }
                },
                "required": ["symbol"]
            }
        ),
        Tool(
            name="get_exchange_info",
            description="Get exchange trading rules and symbol information",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Trading pair symbol (e.g., 'BTCUSDT'). If not provided, returns all symbols"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_symbol_ticker",
            description="Get best price/quantity on the order book for a symbol or all symbols",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Trading pair symbol (e.g., 'BTCUSDT'). If not provided, returns all symbols"
                    }
                },
                "required": []
            }
        ),
    ]


def handle_market_tool(client: Client, name: str, arguments: Any) -> Any:
    """Handle market tool execution."""
    if name == "get_ticker_price":
        symbol = arguments.get("symbol")
        if symbol:
            return client.get_symbol_ticker(symbol=symbol)
        return client.get_all_tickers()

    elif name == "get_ticker_24h":
        symbol = arguments.get("symbol")
        if symbol:
            return client.get_ticker(symbol=symbol)
        return client.get_ticker()

    elif name == "get_order_book":
        return client.get_order_book(
            symbol=arguments["symbol"],
            limit=arguments.get("limit", 100)
        )

    elif name == "get_recent_trades":
        return client.get_recent_trades(
            symbol=arguments["symbol"],
            limit=arguments.get("limit", 500)
        )

    elif name == "get_klines":
        return client.get_klines(
            symbol=arguments["symbol"],
            interval=arguments.get("interval", "1h"),
            limit=arguments.get("limit", 500),
            startTime=arguments.get("start_time"),
            endTime=arguments.get("end_time")
        )

    elif name == "get_avg_price":
        return client.get_avg_price(symbol=arguments["symbol"])

    elif name == "get_exchange_info":
        symbol = arguments.get("symbol")
        if symbol:
            return client.get_symbol_info(symbol=symbol)
        return client.get_exchange_info()

    elif name == "get_symbol_ticker":
        symbol = arguments.get("symbol")
        if symbol:
            return client.get_symbol_ticker(symbol=symbol)
        return client.get_orderbook_tickers()

    return None
