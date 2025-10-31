"""Integration tests for trading tools."""

import pytest
from binance_mcp.tools.trading import handle_trading_tool


class TestTradingTools:
    """Test trading tools with real API calls (using test orders)."""

    def test_create_test_order_market_buy(self, binance_client, test_symbol):
        """Test creating a market buy test order."""
        result = handle_trading_tool(
            binance_client,
            "create_test_order",
            {
                "symbol": test_symbol,
                "side": "BUY",
                "type": "MARKET",
                "quantity": 0.001
            }
        )

        # Test orders return empty dict on success
        assert result is not None

    def test_create_test_order_market_sell(self, binance_client, test_symbol):
        """Test creating a market sell test order."""
        result = handle_trading_tool(
            binance_client,
            "create_test_order",
            {
                "symbol": test_symbol,
                "side": "SELL",
                "type": "MARKET",
                "quantity": 0.001
            }
        )

        assert result is not None

    def test_create_test_order_limit_buy(self, binance_client, test_symbol):
        """Test creating a limit buy test order."""
        # Get current price to create a reasonable limit order
        from binance_mcp.tools.market import handle_market_tool
        price_data = handle_market_tool(
            binance_client,
            "get_ticker_price",
            {"symbol": test_symbol}
        )
        current_price = float(price_data["price"])
        limit_price = round(current_price * 0.95, 2)  # 5% below current price

        result = handle_trading_tool(
            binance_client,
            "create_test_order",
            {
                "symbol": test_symbol,
                "side": "BUY",
                "type": "LIMIT",
                "quantity": 0.001,
                "price": limit_price,
                "time_in_force": "GTC"
            }
        )

        assert result is not None

    def test_create_test_order_limit_sell(self, binance_client, test_symbol):
        """Test creating a limit sell test order."""
        from binance_mcp.tools.market import handle_market_tool
        price_data = handle_market_tool(
            binance_client,
            "get_ticker_price",
            {"symbol": test_symbol}
        )
        current_price = float(price_data["price"])
        limit_price = round(current_price * 1.05, 2)  # 5% above current price

        result = handle_trading_tool(
            binance_client,
            "create_test_order",
            {
                "symbol": test_symbol,
                "side": "SELL",
                "type": "LIMIT",
                "quantity": 0.001,
                "price": limit_price,
                "time_in_force": "GTC"
            }
        )

        assert result is not None

    def test_create_test_order_different_time_in_force(self, binance_client, test_symbol):
        """Test creating test orders with different time in force options."""
        from binance_mcp.tools.market import handle_market_tool
        price_data = handle_market_tool(
            binance_client,
            "get_ticker_price",
            {"symbol": test_symbol}
        )
        current_price = float(price_data["price"])
        limit_price = round(current_price * 0.95, 2)

        time_in_force_options = ["GTC", "IOC", "FOK"]

        for tif in time_in_force_options:
            result = handle_trading_tool(
                binance_client,
                "create_test_order",
                {
                    "symbol": test_symbol,
                    "side": "BUY",
                    "type": "LIMIT",
                    "quantity": 0.001,
                    "price": limit_price,
                    "time_in_force": tif
                }
            )

            assert result is not None

    def test_get_open_orders_all(self, binance_client):
        """Test getting all open orders."""
        result = handle_trading_tool(
            binance_client,
            "get_open_orders",
            {}
        )

        assert result is not None
        assert isinstance(result, list)
        # Can be empty if no open orders

    def test_get_open_orders_single_symbol(self, binance_client, test_symbol):
        """Test getting open orders for a specific symbol."""
        result = handle_trading_tool(
            binance_client,
            "get_open_orders",
            {"symbol": test_symbol}
        )

        assert result is not None
        assert isinstance(result, list)
        # Can be empty if no open orders for this symbol

    def test_get_all_orders(self, binance_client, test_symbol):
        """Test getting all orders (history) for a symbol."""
        result = handle_trading_tool(
            binance_client,
            "get_all_orders",
            {"symbol": test_symbol, "limit": 5}
        )

        assert result is not None
        assert isinstance(result, list)
        assert len(result) <= 5

        if len(result) > 0:
            order = result[0]
            assert "symbol" in order
            assert "orderId" in order
            assert "price" in order
            assert "origQty" in order
            assert "status" in order

    def test_get_all_orders_with_different_limits(self, binance_client, test_symbol):
        """Test getting order history with different limit values."""
        limits = [5, 10, 20]

        for limit in limits:
            result = handle_trading_tool(
                binance_client,
                "get_all_orders",
                {"symbol": test_symbol, "limit": limit}
            )

            assert result is not None
            assert isinstance(result, list)
            assert len(result) <= limit

    def test_create_test_order_invalid_quantity(self, binance_client, test_symbol):
        """Test that invalid quantity raises an error."""
        from binance.exceptions import BinanceAPIException

        with pytest.raises(BinanceAPIException):
            handle_trading_tool(
                binance_client,
                "create_test_order",
                {
                    "symbol": test_symbol,
                    "side": "BUY",
                    "type": "MARKET",
                    "quantity": 0.00000001  # Too small
                }
            )

    def test_create_test_order_invalid_symbol(self, binance_client):
        """Test that invalid symbol raises an error."""
        from binance.exceptions import BinanceAPIException

        with pytest.raises(BinanceAPIException):
            handle_trading_tool(
                binance_client,
                "create_test_order",
                {
                    "symbol": "INVALIDSYMBOL123",
                    "side": "BUY",
                    "type": "MARKET",
                    "quantity": 0.001
                }
            )

    def test_get_order_invalid_symbol(self, binance_client):
        """Test getting order with invalid symbol."""
        from binance.exceptions import BinanceAPIException

        with pytest.raises(BinanceAPIException):
            handle_trading_tool(
                binance_client,
                "get_order",
                {
                    "symbol": "INVALIDSYMBOL123",
                    "order_id": 12345
                }
            )

    def test_cancel_order_nonexistent(self, binance_client, test_symbol):
        """Test canceling a non-existent order."""
        from binance.exceptions import BinanceAPIException

        with pytest.raises(BinanceAPIException):
            handle_trading_tool(
                binance_client,
                "cancel_order",
                {
                    "symbol": test_symbol,
                    "order_id": 999999999999  # Non-existent order ID
                }
            )

    def test_unknown_tool(self, binance_client):
        """Test that unknown tool returns None."""
        result = handle_trading_tool(
            binance_client,
            "unknown_tool_name",
            {}
        )

        assert result is None

    @pytest.mark.skip(reason="Only test real orders if you explicitly want to - requires real funds")
    def test_create_real_order_limit(self, binance_client, test_symbol):
        """Test creating a real limit order (SKIPPED by default)."""
        # This test is skipped by default to avoid real trading
        # Remove @pytest.mark.skip to test real order creation
        from binance_mcp.tools.market import handle_market_tool
        price_data = handle_market_tool(
            binance_client,
            "get_ticker_price",
            {"symbol": test_symbol}
        )
        current_price = float(price_data["price"])
        # Set price very low so it won't execute
        limit_price = round(current_price * 0.5, 2)

        result = handle_trading_tool(
            binance_client,
            "create_order",
            {
                "symbol": test_symbol,
                "side": "BUY",
                "type": "LIMIT",
                "quantity": 0.001,
                "price": limit_price,
                "time_in_force": "GTC"
            }
        )

        assert result is not None
        assert "orderId" in result

        # Clean up - cancel the order
        if "orderId" in result:
            handle_trading_tool(
                binance_client,
                "cancel_order",
                {
                    "symbol": test_symbol,
                    "order_id": result["orderId"]
                }
            )
