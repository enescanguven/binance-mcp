# Binance MCP Server

A Model Context Protocol (MCP) server for Binance cryptocurrency exchange. This server enables Claude to access real-time crypto market data, account information, and execute trades through the Binance API.

## Features

### Market Data Tools
- Get current price for symbols
- Get 24-hour price change statistics
- Get order book (market depth)
- Get recent trades
- Get candlestick/kline data
- Get average price
- Get exchange information
- Get best bid/ask prices

### Account Management Tools
- Get account information and balances
- Get balance for specific assets
- Get account trade history
- Get account status
- Get trading fees
- Get asset dividend history

### Trading Tools
- Create new orders (market, limit, stop-loss, etc.)
- Test order creation without execution
- Get order details
- Cancel orders
- Get open orders
- Get all orders history
- Cancel all open orders for a symbol

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd binance-mcp
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package:
```bash
pip install -e .
```

## Configuration

1. Get your Binance API keys:
   - Go to [Binance API Management](https://www.binance.com/en/my/settings/api-management)
   - Create a new API key
   - **Important**: For security, restrict your API key to only the permissions you need
   - **Never share your API keys or commit them to version control**

2. Create a `.env` file in the project root:
```bash
cp .env.example .env
```

3. Edit `.env` and add your API credentials:
```
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
BINANCE_TESTNET=false
```

**Security Notes:**
- Use testnet (`BINANCE_TESTNET=true`) for development and testing
- Enable IP restrictions on your API keys
- Never use API keys with withdrawal permissions unless absolutely necessary
- Regularly rotate your API keys

## Usage with Claude Desktop

Add this to your Claude Desktop configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "binance": {
      "command": "python",
      "args": ["-m", "binance_mcp"],
      "env": {
        "BINANCE_API_KEY": "your_api_key_here",
        "BINANCE_API_SECRET": "your_api_secret_here",
        "BINANCE_TESTNET": "false"
      }
    }
  }
}
```

Or if you want to use the .env file:

```json
{
  "mcpServers": {
    "binance": {
      "command": "/path/to/your/venv/bin/python",
      "args": ["-m", "binance_mcp"],
      "cwd": "/path/to/binance-mcp"
    }
  }
}
```

## Running the Server

You can run the server directly:

```bash
python -m binance_mcp
```

Or use it as a module:

```python
from binance_mcp.server import main
import asyncio

asyncio.run(main())
```

## Example Queries with Claude

Once configured, you can ask Claude:

- "What's the current price of Bitcoin?"
- "Show me the order book for ETHUSDT"
- "Get my account balance"
- "What are my open orders?"
- "Show me the 1-hour candlestick data for BTCUSDT from the last 24 hours"
- "Create a test limit buy order for 0.001 BTC at $50,000"

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Format code:

```bash
black src/
ruff check src/
```

## API Rate Limits

Be aware of Binance API rate limits:
- Weight-based rate limits (1200 per minute for most endpoints)
- Order rate limits (10 orders per second, 100,000 per 24 hours)
- WebSocket connection limits

The server will handle rate limit errors gracefully and return appropriate error messages.

## Security Best Practices

1. **Never commit API keys** - Use environment variables or .env files (add .env to .gitignore)
2. **Use IP restrictions** - Restrict your API key to specific IP addresses
3. **Limit permissions** - Only enable the API key permissions you need
4. **Use testnet** - Test your integration on Binance testnet before using real funds
5. **Monitor usage** - Regularly check your API key usage and trade history
6. **Rotate keys** - Periodically generate new API keys

## Troubleshooting

### API Key Errors
- Make sure your API key is active and not expired
- Check that your API key has the required permissions
- Verify your IP is whitelisted if you have IP restrictions

### Connection Errors
- Check your internet connection
- Verify Binance is not under maintenance
- Try using testnet to isolate the issue

### Rate Limit Errors
- Reduce the frequency of your requests
- Implement exponential backoff for retries
- Use WebSocket connections for real-time data instead of REST polling

## License

MIT License - See LICENSE file for details

## Disclaimer

This software is for educational purposes only. Use at your own risk. Trading cryptocurrencies carries significant risk. Always test thoroughly on testnet before using real funds.
