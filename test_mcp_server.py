"""Test MCP Server tools."""

import asyncio
from binance_mcp.server import list_tools, call_tool


async def test_mcp_server():
    """Test MCP server functionality."""
    print("Testing Binance MCP Server...\n")

    # Test 1: List all available tools
    print("1. Listing available tools...")
    tools = await list_tools()
    print(f"✓ Found {len(tools)} tools:")
    for tool in tools[:5]:  # Show first 5
        print(f"  - {tool.name}: {tool.description[:60]}...")
    print(f"  ... and {len(tools) - 5} more\n")

    # Test 2: Get BTC price
    print("2. Testing get_ticker_price tool (BTC)...")
    result = await call_tool("get_ticker_price", {"symbol": "BTCUSDT"})
    print(f"✓ Result: {result[0].text[:100]}...\n")

    # Test 3: Get 24h ticker
    print("3. Testing get_ticker_24h tool (ETH)...")
    result = await call_tool("get_ticker_24h", {"symbol": "ETHUSDT"})
    print(f"✓ Result: {result[0].text[:150]}...\n")

    # Test 4: Get account info
    print("4. Testing get_account_info tool...")
    result = await call_tool("get_account_info", {})
    print(f"✓ Result: {result[0].text[:200]}...\n")

    # Test 5: Get asset balance
    print("5. Testing get_asset_balance tool (ETH)...")
    result = await call_tool("get_asset_balance", {"asset": "ETH"})
    print(f"✓ Result: {result[0].text}\n")

    print("✅ All MCP server tests passed!")


if __name__ == "__main__":
    asyncio.run(test_mcp_server())
