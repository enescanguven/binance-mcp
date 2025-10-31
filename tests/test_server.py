"""Tests for Binance MCP server."""

import pytest
from unittest.mock import Mock, patch
from binance_mcp.server import (
    get_binance_client,
    format_response,
    handle_binance_error
)
from binance.exceptions import BinanceAPIException, BinanceRequestException


def test_format_response_dict():
    """Test formatting dictionary response."""
    data = {"price": "50000.00", "symbol": "BTCUSDT"}
    result = format_response(data)
    assert "price" in result
    assert "50000.00" in result


def test_format_response_list():
    """Test formatting list response."""
    data = [{"price": "50000.00"}, {"price": "3000.00"}]
    result = format_response(data)
    assert "50000.00" in result
    assert "3000.00" in result


def test_handle_binance_api_exception():
    """Test handling Binance API exceptions."""
    # Create a mock response with proper attributes
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.text = '{"code": -1121, "msg": "Invalid symbol"}'

    error = BinanceAPIException(mock_response, 400, '{"code": -1121, "msg": "Invalid symbol"}')
    result = handle_binance_error(error)
    assert "Binance API Error" in result
    assert "-1121" in result


def test_handle_binance_request_exception():
    """Test handling Binance request exceptions."""
    error = BinanceRequestException("Connection error")
    result = handle_binance_error(error)
    assert "Binance Request Error" in result


def test_handle_value_error():
    """Test handling configuration errors."""
    error = ValueError("API key not found")
    result = handle_binance_error(error)
    assert "Configuration Error" in result


@patch.dict('os.environ', {}, clear=True)
def test_get_binance_client_missing_keys():
    """Test that missing API keys raise an error."""
    # Reset the global client
    import binance_mcp.server as server_module
    server_module.binance_client = None

    with pytest.raises(ValueError) as exc_info:
        get_binance_client()

    assert "BINANCE_API_KEY" in str(exc_info.value)


@patch.dict('os.environ', {
    'BINANCE_API_KEY': 'test_key',
    'BINANCE_API_SECRET': 'test_secret'
}, clear=False)
@patch('binance_mcp.server.Client')
def test_get_binance_client_success(mock_client):
    """Test successful client creation."""
    # Reset the global client
    import binance_mcp.server as server_module
    server_module.binance_client = None

    client = get_binance_client()
    assert client is not None
    mock_client.assert_called_once()
