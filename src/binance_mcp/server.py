"""MCP Server for Binance API."""

import os
import json
from typing import Any
from dotenv import load_dotenv

from mcp.server import Server
from mcp.types import Tool, TextContent
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

from .tools import (
    get_market_tools,
    handle_market_tool,
    get_account_tools,
    handle_account_tool,
    get_trading_tools,
    handle_trading_tool,
)

# Load environment variables
load_dotenv()

# Initialize MCP server
app = Server("binance-mcp")

# Global Binance client instance
binance_client: Client | None = None


def get_binance_client() -> Client:
    """Get or create Binance client instance."""
    global binance_client

    if binance_client is None:
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")
        testnet = os.getenv("BINANCE_TESTNET", "false").lower() == "true"

        if not api_key or not api_secret:
            raise ValueError(
                "BINANCE_API_KEY and BINANCE_API_SECRET environment variables are required. "
                "Get your API keys from: https://www.binance.com/en/my/settings/api-management"
            )

        binance_client = Client(
            api_key=api_key,
            api_secret=api_secret,
            testnet=testnet
        )

    return binance_client


def format_response(data: Any) -> str:
    """Format API response data as JSON string."""
    return json.dumps(data, indent=2, default=str)


def handle_binance_error(error: Exception) -> str:
    """Convert Binance exceptions to error messages."""
    if isinstance(error, BinanceAPIException):
        return f"Binance API Error [{error.code}]: {error.message}"
    elif isinstance(error, BinanceRequestException):
        return f"Binance Request Error: {str(error)}"
    elif isinstance(error, ValueError):
        return f"Configuration Error: {str(error)}"
    else:
        return f"Error: {str(error)}"


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available Binance API tools."""
    tools = []
    tools.extend(get_market_tools())
    tools.extend(get_account_tools())
    tools.extend(get_trading_tools())
    return tools


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool execution requests."""
    try:
        client = get_binance_client()
        result = None

        # Try market tools
        result = handle_market_tool(client, name, arguments)
        if result is not None:
            return [TextContent(type="text", text=format_response(result))]

        # Try account tools
        result = handle_account_tool(client, name, arguments)
        if result is not None:
            return [TextContent(type="text", text=format_response(result))]

        # Try trading tools
        result = handle_trading_tool(client, name, arguments)
        if result is not None:
            return [TextContent(type="text", text=format_response(result))]

        # Unknown tool
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]

    except Exception as e:
        error_msg = handle_binance_error(e)
        return [TextContent(type="text", text=error_msg)]


async def main():
    """Run the MCP server."""
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
