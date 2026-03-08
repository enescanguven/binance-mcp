import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { BinanceClient } from "../client.js";
import { success, error } from "../utils.js";

export function registerMarketTools(server: McpServer, client: BinanceClient) {
  server.tool(
    "get_ticker_price",
    "Get current price for a trading pair. Returns all tickers if no symbol provided.",
    { symbol: z.string().optional().describe("Trading pair (e.g. BTCUSDT)") },
    async ({ symbol }) => {
      try {
        return success(await client.getTickerPrice(symbol));
      } catch (err) {
        return error(err);
      }
    },
  );

  server.tool(
    "get_ticker_24h",
    "Get 24-hour price change statistics for a trading pair",
    { symbol: z.string().optional().describe("Trading pair (e.g. BTCUSDT)") },
    async ({ symbol }) => {
      try {
        return success(await client.getTicker24h(symbol));
      } catch (err) {
        return error(err);
      }
    },
  );

  server.tool(
    "get_order_book",
    "Get order book depth for a trading pair",
    {
      symbol: z.string().describe("Trading pair (e.g. BTCUSDT)"),
      limit: z
        .number()
        .optional()
        .describe("Number of price levels (default: 100, max: 5000)"),
    },
    async ({ symbol, limit }) => {
      try {
        return success(await client.getOrderBook(symbol, limit));
      } catch (err) {
        return error(err);
      }
    },
  );

  server.tool(
    "get_recent_trades",
    "Get recent trades for a trading pair",
    {
      symbol: z.string().describe("Trading pair (e.g. BTCUSDT)"),
      limit: z
        .number()
        .optional()
        .describe("Number of trades to return (default: 500, max: 1000)"),
    },
    async ({ symbol, limit }) => {
      try {
        return success(await client.getRecentTrades(symbol, limit));
      } catch (err) {
        return error(err);
      }
    },
  );

  server.tool(
    "get_klines",
    "Get candlestick/kline data for a trading pair",
    {
      symbol: z.string().describe("Trading pair (e.g. BTCUSDT)"),
      interval: z
        .enum([
          "1m", "3m", "5m", "15m", "30m",
          "1h", "2h", "4h", "6h", "8h", "12h",
          "1d", "3d", "1w", "1M",
        ])
        .optional()
        .describe("Kline interval (default: 1h)"),
      limit: z
        .number()
        .optional()
        .describe("Number of klines (default: 500, max: 1000)"),
      start_time: z
        .number()
        .optional()
        .describe("Start time in milliseconds"),
      end_time: z.number().optional().describe("End time in milliseconds"),
    },
    async ({ symbol, interval, limit, start_time, end_time }) => {
      try {
        return success(
          await client.getKlines(
            symbol,
            interval ?? "1h",
            limit,
            start_time,
            end_time,
          ),
        );
      } catch (err) {
        return error(err);
      }
    },
  );

  server.tool(
    "get_avg_price",
    "Get current average price for a trading pair",
    { symbol: z.string().describe("Trading pair (e.g. BTCUSDT)") },
    async ({ symbol }) => {
      try {
        return success(await client.getAvgPrice(symbol));
      } catch (err) {
        return error(err);
      }
    },
  );

  server.tool(
    "get_exchange_info",
    "Get exchange trading rules and symbol information",
    {
      symbol: z
        .string()
        .optional()
        .describe(
          "Trading pair for specific info, omit for all symbols",
        ),
    },
    async ({ symbol }) => {
      try {
        return success(await client.getExchangeInfo(symbol));
      } catch (err) {
        return error(err);
      }
    },
  );

  server.tool(
    "get_symbol_ticker",
    "Get best bid/ask price on the order book",
    {
      symbol: z
        .string()
        .optional()
        .describe("Trading pair (e.g. BTCUSDT)"),
    },
    async ({ symbol }) => {
      try {
        return success(await client.getBookTicker(symbol));
      } catch (err) {
        return error(err);
      }
    },
  );
}
