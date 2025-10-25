"""Trading MCP tools for Binance."""

from typing import Any
from mcp.types import Tool
from binance.client import Client


def get_trading_tools() -> list[Tool]:
    """Get list of trading tools."""
    return [
        Tool(
            name="create_order",
            description="Create a new order (market, limit, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Trading pair symbol (e.g., 'BTCUSDT')"
                    },
                    "side": {
                        "type": "string",
                        "description": "Order side: BUY or SELL",
                        "enum": ["BUY", "SELL"]
                    },
                    "type": {
                        "type": "string",
                        "description": "Order type: LIMIT, MARKET, STOP_LOSS, STOP_LOSS_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT, LIMIT_MAKER",
                        "enum": ["LIMIT", "MARKET", "STOP_LOSS", "STOP_LOSS_LIMIT", "TAKE_PROFIT", "TAKE_PROFIT_LIMIT", "LIMIT_MAKER"]
                    },
                    "quantity": {
                        "type": "number",
                        "description": "Order quantity"
                    },
                    "price": {
                        "type": "number",
                        "description": "Order price (required for LIMIT orders)"
                    },
                    "time_in_force": {
                        "type": "string",
                        "description": "Time in force: GTC (Good Till Cancel), IOC (Immediate or Cancel), FOK (Fill or Kill)",
                        "enum": ["GTC", "IOC", "FOK"],
                        "default": "GTC"
                    },
                    "stop_price": {
                        "type": "number",
                        "description": "Stop price (for STOP_LOSS and TAKE_PROFIT orders)"
                    }
                },
                "required": ["symbol", "side", "type", "quantity"]
            }
        ),
        Tool(
            name="create_test_order",
            description="Test new order creation without actually placing it",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Trading pair symbol (e.g., 'BTCUSDT')"
                    },
                    "side": {
                        "type": "string",
                        "description": "Order side: BUY or SELL",
                        "enum": ["BUY", "SELL"]
                    },
                    "type": {
                        "type": "string",
                        "description": "Order type: LIMIT, MARKET, etc.",
                        "enum": ["LIMIT", "MARKET", "STOP_LOSS", "STOP_LOSS_LIMIT", "TAKE_PROFIT", "TAKE_PROFIT_LIMIT", "LIMIT_MAKER"]
                    },
                    "quantity": {
                        "type": "number",
                        "description": "Order quantity"
                    },
                    "price": {
                        "type": "number",
                        "description": "Order price (required for LIMIT orders)"
                    },
                    "time_in_force": {
                        "type": "string",
                        "description": "Time in force",
                        "enum": ["GTC", "IOC", "FOK"],
                        "default": "GTC"
                    }
                },
                "required": ["symbol", "side", "type", "quantity"]
            }
        ),
        Tool(
            name="get_order",
            description="Get details of a specific order",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Trading pair symbol (e.g., 'BTCUSDT')"
                    },
                    "order_id": {
                        "type": "number",
                        "description": "Order ID"
                    },
                    "orig_client_order_id": {
                        "type": "string",
                        "description": "Original client order ID"
                    }
                },
                "required": ["symbol"]
            }
        ),
        Tool(
            name="cancel_order",
            description="Cancel an active order",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Trading pair symbol (e.g., 'BTCUSDT')"
                    },
                    "order_id": {
                        "type": "number",
                        "description": "Order ID"
                    },
                    "orig_client_order_id": {
                        "type": "string",
                        "description": "Original client order ID"
                    }
                },
                "required": ["symbol"]
            }
        ),
        Tool(
            name="get_open_orders",
            description="Get all open orders for a symbol or all symbols",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Trading pair symbol (e.g., 'BTCUSDT'). If not provided, returns all open orders"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_all_orders",
            description="Get all orders (active, canceled, or filled) for a symbol",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Trading pair symbol (e.g., 'BTCUSDT')"
                    },
                    "order_id": {
                        "type": "number",
                        "description": "Order ID to start from"
                    },
                    "limit": {
                        "type": "number",
                        "description": "Number of orders to retrieve (default: 500, max: 1000)",
                        "default": 500
                    }
                },
                "required": ["symbol"]
            }
        ),
        Tool(
            name="cancel_all_open_orders",
            description="Cancel all open orders for a symbol",
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
    ]


def handle_trading_tool(client: Client, name: str, arguments: Any) -> Any:
    """Handle trading tool execution."""
    if name == "create_order":
        params = {
            "symbol": arguments["symbol"],
            "side": arguments["side"],
            "type": arguments["type"],
            "quantity": arguments["quantity"]
        }

        if "price" in arguments:
            params["price"] = arguments["price"]
        if "time_in_force" in arguments:
            params["timeInForce"] = arguments["time_in_force"]
        if "stop_price" in arguments:
            params["stopPrice"] = arguments["stop_price"]

        return client.create_order(**params)

    elif name == "create_test_order":
        params = {
            "symbol": arguments["symbol"],
            "side": arguments["side"],
            "type": arguments["type"],
            "quantity": arguments["quantity"]
        }

        if "price" in arguments:
            params["price"] = arguments["price"]
        if "time_in_force" in arguments:
            params["timeInForce"] = arguments["time_in_force"]

        return client.create_test_order(**params)

    elif name == "get_order":
        params = {"symbol": arguments["symbol"]}
        if "order_id" in arguments:
            params["orderId"] = arguments["order_id"]
        if "orig_client_order_id" in arguments:
            params["origClientOrderId"] = arguments["orig_client_order_id"]

        return client.get_order(**params)

    elif name == "cancel_order":
        params = {"symbol": arguments["symbol"]}
        if "order_id" in arguments:
            params["orderId"] = arguments["order_id"]
        if "orig_client_order_id" in arguments:
            params["origClientOrderId"] = arguments["orig_client_order_id"]

        return client.cancel_order(**params)

    elif name == "get_open_orders":
        symbol = arguments.get("symbol")
        if symbol:
            return client.get_open_orders(symbol=symbol)
        return client.get_open_orders()

    elif name == "get_all_orders":
        params = {"symbol": arguments["symbol"]}
        if "order_id" in arguments:
            params["orderId"] = arguments["order_id"]
        if "limit" in arguments:
            params["limit"] = arguments["limit"]

        return client.get_all_orders(**params)

    elif name == "cancel_all_open_orders":
        return client.cancel_open_orders(symbol=arguments["symbol"])

    return None
