import { createHmac } from "node:crypto";

export class BinanceApiError extends Error {
  constructor(
    public code: number,
    message: string,
  ) {
    super(message);
    this.name = "BinanceApiError";
  }
}

export class BinanceClient {
  private apiKey?: string;
  private apiSecret?: string;
  private baseUrl: string;

  constructor(options?: {
    apiKey?: string;
    apiSecret?: string;
    testnet?: boolean;
  }) {
    this.apiKey = options?.apiKey;
    this.apiSecret = options?.apiSecret;
    this.baseUrl = options?.testnet
      ? "https://testnet.binance.vision"
      : "https://api.binance.com";
  }

  get isAuthenticated(): boolean {
    return !!(this.apiKey && this.apiSecret);
  }

  private cleanParams(
    params?: Record<string, string | number | undefined>,
  ): Record<string, string> {
    const result: Record<string, string> = {};
    if (params) {
      for (const [key, value] of Object.entries(params)) {
        if (value !== undefined) result[key] = String(value);
      }
    }
    return result;
  }

  async publicRequest(
    endpoint: string,
    params?: Record<string, string | number | undefined>,
  ): Promise<any> {
    const url = new URL(endpoint, this.baseUrl);
    for (const [key, value] of Object.entries(this.cleanParams(params))) {
      url.searchParams.set(key, value);
    }

    const response = await fetch(url.toString());
    const data = await response.json();

    if (data.code !== undefined && data.msg) {
      throw new BinanceApiError(data.code, data.msg);
    }
    return data;
  }

  async signedRequest(
    method: string,
    endpoint: string,
    params?: Record<string, string | number | undefined>,
  ): Promise<any> {
    if (!this.apiKey || !this.apiSecret) {
      throw new Error(
        "API key and secret are required for authenticated endpoints. Set BINANCE_API_KEY and BINANCE_API_SECRET environment variables.",
      );
    }

    const queryParams = new URLSearchParams(this.cleanParams(params));
    queryParams.set("timestamp", Date.now().toString());
    queryParams.set("recvWindow", "5000");

    const signature = createHmac("sha256", this.apiSecret)
      .update(queryParams.toString())
      .digest("hex");
    queryParams.set("signature", signature);

    const url = new URL(endpoint, this.baseUrl);
    let response: Response;

    if (method === "GET" || method === "DELETE") {
      url.search = queryParams.toString();
      response = await fetch(url.toString(), {
        method,
        headers: { "X-MBX-APIKEY": this.apiKey },
      });
    } else {
      response = await fetch(url.toString(), {
        method,
        headers: {
          "X-MBX-APIKEY": this.apiKey,
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: queryParams.toString(),
      });
    }

    const data = await response.json();
    if (data.code !== undefined && data.msg) {
      throw new BinanceApiError(data.code, data.msg);
    }
    return data;
  }

  // ── Market Data ──

  async getTickerPrice(symbol?: string) {
    return this.publicRequest("/api/v3/ticker/price", { symbol });
  }

  async getTicker24h(symbol?: string) {
    return this.publicRequest("/api/v3/ticker/24hr", { symbol });
  }

  async getOrderBook(symbol: string, limit?: number) {
    return this.publicRequest("/api/v3/depth", { symbol, limit });
  }

  async getRecentTrades(symbol: string, limit?: number) {
    return this.publicRequest("/api/v3/trades", { symbol, limit });
  }

  async getKlines(
    symbol: string,
    interval: string,
    limit?: number,
    startTime?: number,
    endTime?: number,
  ) {
    return this.publicRequest("/api/v3/klines", {
      symbol,
      interval,
      limit,
      startTime,
      endTime,
    });
  }

  async getAvgPrice(symbol: string) {
    return this.publicRequest("/api/v3/avgPrice", { symbol });
  }

  async getExchangeInfo(symbol?: string) {
    const data = await this.publicRequest(
      "/api/v3/exchangeInfo",
      symbol ? { symbol } : undefined,
    );
    if (symbol && data.symbols?.length) {
      return data.symbols[0];
    }
    return data;
  }

  async getBookTicker(symbol?: string) {
    return this.publicRequest("/api/v3/ticker/bookTicker", { symbol });
  }

  // ── Account ──

  async getAccountInfo() {
    return this.signedRequest("GET", "/api/v3/account");
  }

  async getAssetBalance(asset: string) {
    const account = await this.getAccountInfo();
    const balance = account.balances?.find(
      (b: any) => b.asset === asset.toUpperCase(),
    );
    return balance ?? { asset: asset.toUpperCase(), free: "0.00000000", locked: "0.00000000" };
  }

  async getAccountTrades(symbol: string, limit?: number, fromId?: number) {
    return this.signedRequest("GET", "/api/v3/myTrades", {
      symbol,
      limit,
      fromId,
    });
  }

  async getAccountStatus() {
    return this.signedRequest("GET", "/sapi/v1/account/status");
  }

  async getTradeFee(symbol?: string) {
    return this.signedRequest("GET", "/sapi/v1/asset/tradeFee", { symbol });
  }

  async getAssetDividendHistory(
    asset?: string,
    startTime?: number,
    endTime?: number,
  ) {
    return this.signedRequest("GET", "/sapi/v1/asset/assetDividend", {
      asset,
      startTime,
      endTime,
    });
  }

  // ── Trading ──

  async createOrder(params: {
    symbol: string;
    side: string;
    type: string;
    quantity: string;
    price?: string;
    timeInForce?: string;
    stopPrice?: string;
  }) {
    return this.signedRequest(
      "POST",
      "/api/v3/order",
      params as Record<string, string>,
    );
  }

  async createTestOrder(params: {
    symbol: string;
    side: string;
    type: string;
    quantity: string;
    price?: string;
    timeInForce?: string;
  }) {
    return this.signedRequest(
      "POST",
      "/api/v3/order/test",
      params as Record<string, string>,
    );
  }

  async getOrder(
    symbol: string,
    orderId?: number,
    origClientOrderId?: string,
  ) {
    return this.signedRequest("GET", "/api/v3/order", {
      symbol,
      orderId,
      origClientOrderId,
    });
  }

  async cancelOrder(
    symbol: string,
    orderId?: number,
    origClientOrderId?: string,
  ) {
    return this.signedRequest("DELETE", "/api/v3/order", {
      symbol,
      orderId,
      origClientOrderId,
    });
  }

  async getOpenOrders(symbol?: string) {
    return this.signedRequest("GET", "/api/v3/openOrders", { symbol });
  }

  async getAllOrders(symbol: string, orderId?: number, limit?: number) {
    return this.signedRequest("GET", "/api/v3/allOrders", {
      symbol,
      orderId,
      limit,
    });
  }

  async cancelAllOpenOrders(symbol: string) {
    return this.signedRequest("DELETE", "/api/v3/openOrders", { symbol });
  }
}
