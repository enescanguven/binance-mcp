import { BinanceApiError } from "./client.js";

export function success(data: unknown) {
  return {
    content: [{ type: "text" as const, text: JSON.stringify(data, null, 2) }],
  };
}

export function error(err: unknown) {
  let message: string;
  if (err instanceof BinanceApiError) {
    message = `Binance API Error (${err.code}): ${err.message}`;
  } else if (err instanceof Error) {
    message = err.message;
  } else {
    message = String(err);
  }
  return {
    content: [{ type: "text" as const, text: message }],
    isError: true,
  };
}
