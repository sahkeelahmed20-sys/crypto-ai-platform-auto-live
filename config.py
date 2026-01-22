
import os

TRADING_ENABLED = os.getenv("TRADING_ENABLED", "false").lower() == "true"
MAX_RISK_PER_TRADE = 0.01
MAX_LEVERAGE = 10
BINANCE_TESTNET = True

STRATEGY_PARAMS = {
    "rsi_period": 14,
    "rsi_overbought": 70,
    "rsi_oversold": 30,
    "ema_fast": 9,
    "ema_slow": 21
}

TRADING_PAIRS = ["BTCUSDT", "ETHUSDT"]
TIMEFRAMES = ["5m", "15m"]

# === STRATEGY TUNING ===
MIN_SCORE = 1        # lower = more signals
RSI_OVERSOLD = 35
RSI_OVERBOUGHT = 65