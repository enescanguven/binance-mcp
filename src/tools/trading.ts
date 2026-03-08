import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { BinanceClient } from "../client.js";
import { success, error } from "../utils.js";

export function registerTradingTools(server: McpServer, client: BinanceClient) {
  server.tool(
    "create_order",
    "Create a new order. WARNING: This places a REAL order on Binance.",
    {
      symbol: z.string().describe("Trading pair (e.g. BTCUSDT)"),
      side: z.enum(["BUY", "SELL"]).describe("Order side"),
      type: z
        .enum([
          "LIMIT",
          "MARKET",
          "STOP_LOSS",
          "STOP_LOSS_LIMIT",
          "TAKE_PROFIT",
          "TAKE_PROFIT_LIMIT",
          "LIMIT_MAKER",
        ])
        .describe("Order type"),
      quantity: z.string().describe("Order quantity"),
      price: z.string().optional().describe("Order price (required for LIMIT orders)"),
      time_in_force: z
        .enum(["GTC", "IOC", "FOK"])
        .optional()
        .describe("Time in force (default: GTC for LIMIT orders)"),
      stop_price: z
        .string()
        .optional()
        .describe("Stop price (for STOP_LOSS and TAKE_PROFIT orders)"),
    },
    async ({ symbol, side, type, quantity, price, time_in_force, stop_price }) => {
      try {
        return success(
          await client.createOrder({
            symbol,
            side,
            type,
            quantity,
            price,
            timeInForce: time_in_force,
            stopPrice: stop_price,
          }),
        );
      } catch (err) {
        return error(err);
      }
    },
  );

  server.tool(
    "create_test_order",
    "Test order creation without actually placing it. Use this to validate order parameters.",
    {
      symbol: z.string().describe("Trading pair (e.g. BTCUSDT)"),
      side: z.enum(["BUY", "SELL"]).describe("Order side"),
      type: z
        .enum([
          "LIMIT",
          "MARKET",
          "STOP_LOSS",
          "STOP_LOSS_LIMIT",
          "TAKE_PROFIT",
          "TAKE_PROFIT_LIMIT",
          "LIMIT_MAKER",
        ])
        .describe("Order type"),
      quantity: z.string().describe("Order quantity"),
      price: z.string().optional().describe("Order price (required for LIMIT orders)"),
      time_in_force: z
        .enum(["GTC", "IOC", "FOK"])
        .optional()
        .describe("Time in force (default: GTC for LIMIT orders)"),
    },
    async ({ symbol, side, type, quantity, price, time_in_force }) => {
      try {
        return success(
          await client.createTestOrder({
            symbol,
            side,
            type,
            quantity,
            price,
            timeInForce: time_in_force,
          }),
        );
      } catch (err) {
        return error(err);
      }
    },
  );

  server.tool(
    "get_order",
    "Get details of a specific order",
    {
      symbol: z.string().describe("Trading pair (e.g. BTCUSDT)"),
      order_id: z.number().optional().describe("Order ID"),
      orig_client_order_id: z
        .string()
        .optional()
        .describe("Original client order ID"),
    },
    async ({ symbol, order_id, orig_client_order_id }) => {
      try {
        return success(
          await client.getOrder(symbol, order_id, orig_client_order_id),
        );
      } catch (err) {
        return error(err);
      }
    },
  );

  server.tool(
    "cancel_order",
    "Cancel an active order",
    {
      symbol: z.string().describe("Trading pair (e.g. BTCUSDT)"),
      order_id: z.number().optional().describe("Order ID to cancel"),
      orig_client_order_id: z
        .string()
        .optional()
        .describe("Original client order ID to cancel"),
    },
    async ({ symbol, order_id, orig_client_order_id }) => {
      try {
        return success(
          await client.cancelOrder(symbol, order_id, orig_client_order_id),
        );
      } catch (err) {
        return error(err);
      }
    },
  );

  server.tool(
    "get_open_orders",
    "Get all open orders, optionally filtered by trading pair",
    {
      symbol: z
        .string()
        .optional()
        .describe("Trading pair to filter (e.g. BTCUSDT)"),
    },
    async ({ symbol }) => {
      try {
        return success(await client.getOpenOrders(symbol));
      } catch (err) {
        return error(err);
      }
    },
  );

  server.tool(
    "get_all_orders",
    "Get all orders (active, canceled, filled) for a trading pair",
    {
      symbol: z.string().describe("Trading pair (e.g. BTCUSDT)"),
      order_id: z
        .number()
        .optional()
        .describe("Order ID to start from"),
      limit: z
        .number()
        .optional()
        .describe("Number of orders (default: 500, max: 1000)"),
    },
    async ({ symbol, order_id, limit }) => {
      try {
        return success(await client.getAllOrders(symbol, order_id, limit));
      } catch (err) {
        return error(err);
      }
    },
  );

  server.tool(
    "cancel_all_open_orders",
    "Cancel all open orders for a trading pair",
    {
      symbol: z.string().describe("Trading pair (e.g. BTCUSDT)"),
    },
    async ({ symbol }) => {
      try {
        return success(await client.cancelAllOpenOrders(symbol));
      } catch (err) {
        return error(err);
      }
    },
  );
}
