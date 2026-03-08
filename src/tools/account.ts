import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { BinanceClient } from "../client.js";
import { success, error } from "../utils.js";

export function registerAccountTools(server: McpServer, client: BinanceClient) {
  server.tool(
    "get_account_info",
    "Get current account information including all asset balances",
    {},
    async () => {
      try {
        return success(await client.getAccountInfo());
      } catch (err) {
        return error(err);
      }
    },
  );

  server.tool(
    "get_asset_balance",
    "Get balance for a specific asset",
    {
      asset: z
        .string()
        .describe("Asset symbol (e.g. BTC, USDT, ETH)"),
    },
    async ({ asset }) => {
      try {
        return success(await client.getAssetBalance(asset));
      } catch (err) {
        return error(err);
      }
    },
  );

  server.tool(
    "get_account_trades",
    "Get trade history for a specific trading pair",
    {
      symbol: z.string().describe("Trading pair (e.g. BTCUSDT)"),
      limit: z
        .number()
        .optional()
        .describe("Number of trades (default: 500, max: 1000)"),
      from_id: z
        .number()
        .optional()
        .describe("Trade ID to fetch from"),
    },
    async ({ symbol, limit, from_id }) => {
      try {
        return success(await client.getAccountTrades(symbol, limit, from_id));
      } catch (err) {
        return error(err);
      }
    },
  );

  server.tool(
    "get_account_status",
    "Get account status (normal or restricted)",
    {},
    async () => {
      try {
        return success(await client.getAccountStatus());
      } catch (err) {
        return error(err);
      }
    },
  );

  server.tool(
    "get_trade_fee",
    "Get trading fee rates for a symbol or all symbols",
    {
      symbol: z
        .string()
        .optional()
        .describe("Trading pair (e.g. BTCUSDT)"),
    },
    async ({ symbol }) => {
      try {
        return success(await client.getTradeFee(symbol));
      } catch (err) {
        return error(err);
      }
    },
  );

  server.tool(
    "get_asset_dividend_history",
    "Get asset dividend/distribution history",
    {
      asset: z.string().optional().describe("Asset symbol (e.g. BTC)"),
      start_time: z
        .number()
        .optional()
        .describe("Start time in milliseconds"),
      end_time: z.number().optional().describe("End time in milliseconds"),
    },
    async ({ asset, start_time, end_time }) => {
      try {
        return success(
          await client.getAssetDividendHistory(asset, start_time, end_time),
        );
      } catch (err) {
        return error(err);
      }
    },
  );

  server.tool(
    "get_dust_assets",
    "Get list of assets that can be converted to BNB (dust balances below 0.0012 BTC)",
    {},
    async () => {
      try {
        return success(await client.getDustAssets());
      } catch (err) {
        return error(err);
      }
    },
  );

  server.tool(
    "convert_dust_to_bnb",
    "Convert small balances (dust) to BNB. 2% fee applies. Can be used once every 6 hours.",
    {
      assets: z
        .array(z.string())
        .describe("List of asset symbols to convert (e.g. ['ETH', 'XRP', 'SOL'])"),
    },
    async ({ assets }) => {
      try {
        return success(await client.convertDustToBnb(assets));
      } catch (err) {
        return error(err);
      }
    },
  );
}
