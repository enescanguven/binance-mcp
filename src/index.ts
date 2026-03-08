#!/usr/bin/env node

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { BinanceClient } from "./client.js";
import { registerMarketTools } from "./tools/market.js";
import { registerAccountTools } from "./tools/account.js";
import { registerTradingTools } from "./tools/trading.js";

const client = new BinanceClient({
  apiKey: process.env.BINANCE_API_KEY,
  apiSecret: process.env.BINANCE_API_SECRET,
  testnet: process.env.BINANCE_TESTNET === "true",
});

const server = new McpServer({
  name: "binance-mcp",
  version: "1.0.0",
});

registerMarketTools(server, client);
registerAccountTools(server, client);
registerTradingTools(server, client);

const transport = new StdioServerTransport();
await server.connect(transport);
