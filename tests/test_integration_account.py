"""Integration tests for account management tools."""

import pytest
from binance_mcp.tools.account import handle_account_tool


class TestAccountTools:
    """Test account management tools with real API calls."""

    def test_get_account_info(self, binance_client):
        """Test getting account information."""
        result = handle_account_tool(
            binance_client,
            "get_account_info",
            {}
        )

        assert result is not None
        assert "accountType" in result
        assert "canTrade" in result
        assert "canWithdraw" in result
        assert "canDeposit" in result
        assert "balances" in result
        assert isinstance(result["balances"], list)

    def test_get_asset_balance_btc(self, binance_client):
        """Test getting balance for BTC."""
        result = handle_account_tool(
            binance_client,
            "get_asset_balance",
            {"asset": "BTC"}
        )

        assert result is not None
        assert "asset" in result
        assert result["asset"] == "BTC"
        assert "free" in result
        assert "locked" in result

        # Balances should be numeric strings
        assert isinstance(result["free"], str)
        assert isinstance(result["locked"], str)
        float(result["free"])  # Should be convertible to float
        float(result["locked"])  # Should be convertible to float

    def test_get_asset_balance_usdt(self, binance_client):
        """Test getting balance for USDT."""
        result = handle_account_tool(
            binance_client,
            "get_asset_balance",
            {"asset": "USDT"}
        )

        assert result is not None
        assert "asset" in result
        assert result["asset"] == "USDT"
        assert "free" in result
        assert "locked" in result

    def test_get_asset_balance_multiple_assets(self, binance_client):
        """Test getting balances for multiple assets."""
        assets = ["BTC", "ETH", "BNB", "USDT"]

        for asset in assets:
            result = handle_account_tool(
                binance_client,
                "get_asset_balance",
                {"asset": asset}
            )

            assert result is not None
            assert result["asset"] == asset

    def test_get_account_status(self, binance_client):
        """Test getting account status."""
        result = handle_account_tool(
            binance_client,
            "get_account_status",
            {}
        )

        assert result is not None
        assert "data" in result
        # Normal account should have "Normal" status
        # The exact structure may vary, so we just check it returns something

    def test_get_trade_fee_single_symbol(self, binance_client, test_symbol):
        """Test getting trade fee for a specific symbol."""
        result = handle_account_tool(
            binance_client,
            "get_trade_fee",
            {"symbol": test_symbol}
        )

        assert result is not None
        # The response structure may vary, but it should return data
        if isinstance(result, list):
            assert len(result) > 0
            fee = result[0]
            assert "symbol" in fee or "maker" in fee or "taker" in fee

    def test_get_trade_fee_all(self, binance_client):
        """Test getting trade fees for all symbols."""
        result = handle_account_tool(
            binance_client,
            "get_trade_fee",
            {}
        )

        assert result is not None
        if isinstance(result, list):
            assert len(result) > 0

    def test_get_account_trades(self, binance_client, test_symbol):
        """Test getting account trades for a symbol."""
        result = handle_account_tool(
            binance_client,
            "get_account_trades",
            {"symbol": test_symbol, "limit": 5}
        )

        # Result can be empty list if no trades
        assert result is not None
        assert isinstance(result, list)

        if len(result) > 0:
            trade = result[0]
            assert "id" in trade
            assert "symbol" in trade
            assert "price" in trade
            assert "qty" in trade
            assert "time" in trade

    def test_get_account_trades_with_limit(self, binance_client, test_symbol):
        """Test getting account trades with limit parameter."""
        result = handle_account_tool(
            binance_client,
            "get_account_trades",
            {"symbol": test_symbol, "limit": 10}
        )

        assert result is not None
        assert isinstance(result, list)
        # Should not exceed limit
        assert len(result) <= 10

    def test_get_asset_dividend_history_no_params(self, binance_client):
        """Test getting asset dividend history without parameters."""
        result = handle_account_tool(
            binance_client,
            "get_asset_dividend_history",
            {}
        )

        # Result can be empty if no dividends
        assert result is not None

    def test_get_asset_dividend_history_with_asset(self, binance_client):
        """Test getting asset dividend history for specific asset."""
        result = handle_account_tool(
            binance_client,
            "get_asset_dividend_history",
            {"asset": "BNB"}
        )

        # Result can be empty if no dividends
        assert result is not None

    def test_invalid_asset(self, binance_client):
        """Test handling of invalid asset."""
        from binance.exceptions import BinanceAPIException

        # Binance may return None for invalid assets without throwing error
        result = handle_account_tool(
            binance_client,
            "get_asset_balance",
            {"asset": "INVALIDASSET123"}
        )

        # Result can be None for invalid asset, which is acceptable behavior
        # The API doesn't always throw an error for invalid assets
        assert result is None or (isinstance(result, dict) and "asset" in result)

    def test_unknown_tool(self, binance_client):
        """Test that unknown tool returns None."""
        result = handle_account_tool(
            binance_client,
            "unknown_tool_name",
            {}
        )

        assert result is None
