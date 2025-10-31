"""Pytest configuration and fixtures for Binance MCP tests."""

import os
import pytest
from dotenv import load_dotenv
from binance.client import Client

# Load environment variables from .env file
load_dotenv()


@pytest.fixture(scope="session")
def api_credentials():
    """Get API credentials from environment variables."""
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    testnet = os.getenv("BINANCE_TESTNET", "false").lower() == "true"

    if not api_key or not api_secret:
        pytest.skip(
            "BINANCE_API_KEY and BINANCE_API_SECRET environment variables are required. "
            "Please set them in .env file"
        )

    return {
        "api_key": api_key,
        "api_secret": api_secret,
        "testnet": testnet
    }


@pytest.fixture(scope="session")
def binance_client(api_credentials):
    """Create a Binance client instance for testing."""
    client = Client(
        api_key=api_credentials["api_key"],
        api_secret=api_credentials["api_secret"],
        testnet=api_credentials["testnet"]
    )
    return client


@pytest.fixture(scope="session")
def test_symbol():
    """Default test symbol for testing."""
    return "BTCUSDT"


@pytest.fixture(scope="session")
def test_symbols():
    """List of test symbols for testing."""
    return ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
