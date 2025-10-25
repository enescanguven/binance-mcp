"""Test Binance API connection."""

import os
from dotenv import load_dotenv
from binance.client import Client

# Load environment variables
load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

print(f"API Key: {api_key[:10]}...")
print(f"API Secret: {api_secret[:10]}...")

try:
    # Create client
    client = Client(api_key=api_key, api_secret=api_secret)

    # Test 1: Get server time
    print("\n1. Testing server connection...")
    server_time = client.get_server_time()
    print(f"✓ Server time: {server_time}")

    # Test 2: Get BTC price
    print("\n2. Testing market data (BTC price)...")
    btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
    print(f"✓ BTC Price: ${btc_price['price']}")

    # Test 3: Get account info
    print("\n3. Testing account access...")
    account = client.get_account()
    print(f"✓ Account type: {account['accountType']}")
    print(f"✓ Can trade: {account['canTrade']}")
    print(f"✓ Can withdraw: {account['canWithdraw']}")

    # Test 4: Get balances
    print("\n4. Testing balances...")
    balances = [b for b in account['balances'] if float(b['free']) > 0 or float(b['locked']) > 0]
    if balances:
        print("✓ Non-zero balances:")
        for balance in balances[:5]:  # Show first 5
            total = float(balance['free']) + float(balance['locked'])
            print(f"  - {balance['asset']}: {total}")
    else:
        print("✓ No balances found (account is empty)")

    print("\n✅ All tests passed! API connection is working correctly.")

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nPlease check:")
    print("1. Your API keys are correct")
    print("2. Your API key has the required permissions")
    print("3. Your IP is whitelisted (if IP restrictions are enabled)")
