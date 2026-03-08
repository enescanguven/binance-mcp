# binance-mcp

Binance MCP server for Claude. Trade crypto, check balances, and monitor markets through natural language.

## Quick Start

```bash
npx binance-mcp
```

## Claude Desktop Configuration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "binance": {
      "command": "npx",
      "args": ["-y", "binance-mcp"],
      "env": {
        "BINANCE_API_KEY": "your_api_key",
        "BINANCE_API_SECRET": "your_api_secret"
      }
    }
  }
}
```

For testnet, add `"BINANCE_TESTNET": "true"` to env.

## Tools (21)

### Market Data (8 tools, no API key needed)

| Tool | Description |
|------|-------------|
| `get_ticker_price` | Current price for a trading pair |
| `get_ticker_24h` | 24-hour price change statistics |
| `get_order_book` | Order book depth |
| `get_recent_trades` | Recent trades |
| `get_klines` | Candlestick/kline data |
| `get_avg_price` | Current average price |
| `get_exchange_info` | Trading rules and symbol info |
| `get_symbol_ticker` | Best bid/ask price |

### Account (6 tools, API key required)

| Tool | Description |
|------|-------------|
| `get_account_info` | Account info with all balances |
| `get_asset_balance` | Balance for a specific asset |
| `get_account_trades` | Trade history for a pair |
| `get_account_status` | Account status |
| `get_trade_fee` | Trading fee rates |
| `get_asset_dividend_history` | Dividend/distribution history |

### Trading (7 tools, API key required)

| Tool | Description |
|------|-------------|
| `create_order` | Place a real order |
| `create_test_order` | Validate order without placing |
| `get_order` | Get order details |
| `cancel_order` | Cancel an order |
| `get_open_orders` | List open orders |
| `get_all_orders` | Full order history |
| `cancel_all_open_orders` | Cancel all open orders for a pair |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `BINANCE_API_KEY` | For account/trading | Binance API key |
| `BINANCE_API_SECRET` | For account/trading | Binance API secret |
| `BINANCE_TESTNET` | No | Set `true` for testnet |

## Development

```bash
npm install
npm run build
npm start
```

## License

MIT
