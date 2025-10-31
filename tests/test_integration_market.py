"""Integration tests for market data tools."""

import pytest
from binance_mcp.tools.market import handle_market_tool


class TestMarketTools:
    """Test market data tools with real API calls."""

    def test_get_ticker_price_single_symbol(self, binance_client, test_symbol):
        """Test getting price for a single symbol."""
        result = handle_market_tool(
            binance_client,
            "get_ticker_price",
            {"symbol": test_symbol}
        )

        assert result is not None
        assert "symbol" in result
        assert result["symbol"] == test_symbol
        assert "price" in result
        assert float(result["price"]) > 0

    def test_get_ticker_price_all_symbols(self, binance_client):
        """Test getting prices for all symbols."""
        result = handle_market_tool(
            binance_client,
            "get_ticker_price",
            {}
        )

        assert result is not None
        assert isinstance(result, list)
        assert len(result) > 0
        assert "symbol" in result[0]
        assert "price" in result[0]

    def test_get_ticker_24h_single_symbol(self, binance_client, test_symbol):
        """Test getting 24h ticker for a single symbol."""
        result = handle_market_tool(
            binance_client,
            "get_ticker_24h",
            {"symbol": test_symbol}
        )

        assert result is not None
        assert "symbol" in result
        assert result["symbol"] == test_symbol
        assert "priceChange" in result
        assert "priceChangePercent" in result
        assert "lastPrice" in result
        assert "volume" in result

    def test_get_ticker_24h_all_symbols(self, binance_client):
        """Test getting 24h ticker for all symbols."""
        result = handle_market_tool(
            binance_client,
            "get_ticker_24h",
            {}
        )

        assert result is not None
        assert isinstance(result, list)
        assert len(result) > 0
        assert "symbol" in result[0]

    def test_get_order_book(self, binance_client, test_symbol):
        """Test getting order book for a symbol."""
        result = handle_market_tool(
            binance_client,
            "get_order_book",
            {"symbol": test_symbol, "limit": 10}
        )

        assert result is not None
        assert "bids" in result
        assert "asks" in result
        assert len(result["bids"]) > 0
        assert len(result["asks"]) > 0
        assert len(result["bids"]) <= 10

        # Check bid format
        bid = result["bids"][0]
        assert len(bid) == 2  # [price, quantity]
        assert float(bid[0]) > 0  # price
        assert float(bid[1]) > 0  # quantity

    def test_get_recent_trades(self, binance_client, test_symbol):
        """Test getting recent trades for a symbol."""
        result = handle_market_tool(
            binance_client,
            "get_recent_trades",
            {"symbol": test_symbol, "limit": 5}
        )

        assert result is not None
        assert isinstance(result, list)
        assert len(result) > 0
        assert len(result) <= 5

        trade = result[0]
        assert "id" in trade
        assert "price" in trade
        assert "qty" in trade
        assert "time" in trade

    def test_get_klines(self, binance_client, test_symbol):
        """Test getting klines/candlestick data."""
        result = handle_market_tool(
            binance_client,
            "get_klines",
            {
                "symbol": test_symbol,
                "interval": "1h",
                "limit": 10
            }
        )

        assert result is not None
        assert isinstance(result, list)
        assert len(result) > 0
        assert len(result) <= 10

        # Check kline format
        kline = result[0]
        assert len(kline) >= 11
        # [open_time, open, high, low, close, volume, close_time, ...]
        assert int(kline[0]) > 0  # open_time
        assert float(kline[1]) > 0  # open
        assert float(kline[2]) > 0  # high
        assert float(kline[3]) > 0  # low
        assert float(kline[4]) > 0  # close
        assert float(kline[5]) >= 0  # volume

    def test_get_klines_different_intervals(self, binance_client, test_symbol):
        """Test getting klines with different intervals."""
        intervals = ["1m", "5m", "1h", "1d"]

        for interval in intervals:
            result = handle_market_tool(
                binance_client,
                "get_klines",
                {
                    "symbol": test_symbol,
                    "interval": interval,
                    "limit": 5
                }
            )

            assert result is not None
            assert isinstance(result, list)
            assert len(result) > 0

    def test_get_avg_price(self, binance_client, test_symbol):
        """Test getting average price for a symbol."""
        result = handle_market_tool(
            binance_client,
            "get_avg_price",
            {"symbol": test_symbol}
        )

        assert result is not None
        assert "mins" in result
        assert "price" in result
        assert float(result["price"]) > 0

    def test_get_exchange_info_single_symbol(self, binance_client, test_symbol):
        """Test getting exchange info for a single symbol."""
        result = handle_market_tool(
            binance_client,
            "get_exchange_info",
            {"symbol": test_symbol}
        )

        assert result is not None
        assert "symbol" in result
        assert result["symbol"] == test_symbol
        assert "status" in result
        assert "baseAsset" in result
        assert "quoteAsset" in result

    def test_get_exchange_info_all(self, binance_client):
        """Test getting exchange info for all symbols."""
        result = handle_market_tool(
            binance_client,
            "get_exchange_info",
            {}
        )

        assert result is not None
        assert "symbols" in result
        assert isinstance(result["symbols"], list)
        assert len(result["symbols"]) > 0

    def test_get_symbol_ticker_single(self, binance_client, test_symbol):
        """Test getting symbol ticker for single symbol."""
        result = handle_market_tool(
            binance_client,
            "get_symbol_ticker",
            {"symbol": test_symbol}
        )

        assert result is not None
        assert "symbol" in result
        assert result["symbol"] == test_symbol
        assert "price" in result or "bidPrice" in result

    def test_get_symbol_ticker_all(self, binance_client):
        """Test getting symbol ticker for all symbols."""
        result = handle_market_tool(
            binance_client,
            "get_symbol_ticker",
            {}
        )

        assert result is not None
        assert isinstance(result, list)
        assert len(result) > 0

    def test_invalid_symbol(self, binance_client):
        """Test handling of invalid symbol."""
        from binance.exceptions import BinanceAPIException

        with pytest.raises(BinanceAPIException):
            handle_market_tool(
                binance_client,
                "get_ticker_price",
                {"symbol": "INVALIDSYMBOL123"}
            )

    def test_unknown_tool(self, binance_client):
        """Test that unknown tool returns None."""
        result = handle_market_tool(
            binance_client,
            "unknown_tool_name",
            {}
        )

        assert result is None
