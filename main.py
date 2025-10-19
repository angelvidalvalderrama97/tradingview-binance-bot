from fastapi import FastAPI, Request
import ccxt
import os

app = FastAPI()

# Claves desde variables de entorno (seguras en Render)
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

binance = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
})

@app.get("/")
async def home():
    return {"status": "running", "message": "TradingView → Binance bot activo 🚀"}

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print("📩 Webhook recibido:", data)

    symbol = data.get("symbol", "BTC/USDC")
    side = data.get("side", "BUY").lower()
    usd_amount = float(data.get("usd_amount", 6.5))

    try:
        # Obtener precio actual de mercado
        ticker = binance.fetch_ticker(symbol)
        price = ticker['last']
        amount = usd_amount / price  # Convertir USDC a BTC

        order = binance.create_market_order(symbol, side, amount)
        print(f"✅ Orden {side.upper()} ejecutada correctamente:", order)
        return {"status": "success", "order": order}
    except Exception as e:
        print("❌ Error ejecutando orden:", e)
        return {"status": "error", "message": str(e)}
