from fastapi import FastAPI, Request
import ccxt
import os

app = FastAPI()

# Claves seguras (Render las leerá de variables de entorno)
api_key = os.getenv("G2MW54fsG3LzB0zURNUuOA752RMuwBkZ3Dn0vVU7NtzRwufl9YFAuksfPaVxwMRC")
api_secret = os.getenv("Paovqmp2b9MUKspJi3o6Fqi0Rk96diPEXqmypErEtXC9xZN0GPS4DF4M5ol397Fi")

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

    symbol = data.get("symbol", "BTC/USDT")
    side = data.get("side", "BUY").lower()
    amount = float(data.get("amount", 0.001))

    try:
        order = binance.create_market_order(symbol, side, amount)
        print(f"✅ Orden {side.upper()} ejecutada correctamente:", order)
        return {"status": "success", "order": order}
    except Exception as e:
        print("❌ Error ejecutando orden:", e)
        return {"status": "error", "message": str(e)}
