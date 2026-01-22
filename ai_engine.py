from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator

from binance_data import get_price_history
from config import (
    STRATEGY_PARAMS,
    TRADING_PAIRS,
    TIMEFRAMES,
    MIN_SCORE,
    RSI_OVERSOLD,
    RSI_OVERBOUGHT,
)
from ml_model import ml_model


def get_all_signals():
    signals = []

    for pair in TRADING_PAIRS:
        for tf in TIMEFRAMES:
            df = get_price_history(pair, tf)

            if df is None or len(df) < 50:
                continue

            close = df["close"]

            rsi = RSIIndicator(
                close, STRATEGY_PARAMS["rsi_period"]
            ).rsi()

            ema_fast = EMAIndicator(
                close, STRATEGY_PARAMS["ema_fast"]
            ).ema_indicator()

            ema_slow = EMAIndicator(
                close, STRATEGY_PARAMS["ema_slow"]
            ).ema_indicator()

            score = 0
            reasons = []

            # RSI logic
            if rsi.iloc[-1] < RSI_OVERSOLD:
                score += 1
                reasons.append("RSI oversold")

            if rsi.iloc[-1] > RSI_OVERBOUGHT:
                score -= 1
                reasons.append("RSI overbought")

            # EMA logic
            if ema_fast.iloc[-1] > ema_slow.iloc[-1]:
                score += 1
                reasons.append("EMA bullish")
            else:
                score -= 1
                reasons.append("EMA bearish")

            # ML assist (safe)
            ret = close.pct_change().iloc[-1]
            if ret != ret:  # NaN check
                ret = 0

            ml_score = ml_model.predict([ret])

            if ml_score > 0.3:
                score += 1
            elif ml_score < -0.3:
                score -= 1

            # Decision
            if score >= MIN_SCORE:
                side = "LONG"
            elif score <= -MIN_SCORE:
                side = "SHORT"
            else:
                continue

            price = close.iloc[-1]

            signals.append({
                "pair": pair,
                "timeframe": tf,
                "side": side,
                "entry": round(price, 2),
                "tp": round(
                    price * (1.02 if side == "LONG" else 0.98), 2
                ),
                "sl": round(
                    price * (0.99 if side == "LONG" else 1.01), 2
                ),
                "leverage": 5,
                "confidence": min(95, abs(score) * 25),
                "reasons": reasons
            })

    return signals