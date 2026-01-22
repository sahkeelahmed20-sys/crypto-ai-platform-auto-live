
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
from binance_data import get_price_history
from config import STRATEGY_PARAMS, TRADING_PAIRS, TIMEFRAMES
from ml_model import ml_model

def get_all_signals():
    signals=[]
    for pair in TRADING_PAIRS:
        for tf in TIMEFRAMES:
            df=get_price_history(pair,tf)
            rsi=RSIIndicator(df["close"],STRATEGY_PARAMS["rsi_period"]).rsi()
            emaf=EMAIndicator(df["close"],STRATEGY_PARAMS["ema_fast"]).ema_indicator()
            emas=EMAIndicator(df["close"],STRATEGY_PARAMS["ema_slow"]).ema_indicator()
            score=0; reasons=[]
            if rsi.iloc[-1]<30: score+=2; reasons.append("RSI oversold")
            if emaf.iloc[-1]>emas.iloc[-1]: score+=2; reasons.append("EMA bullish")
            ml=ml_model.predict([df["close"].pct_change().iloc[-1]])
            if ml>0.3: score+=1
             if score >= 2:
    side = "LONG"
elif score <= -2:
    side = "SHORT"
else:
    return None
                price=df["close"].iloc[-1]
                signals.append({
                    "pair":pair,"timeframe":tf,"side":"LONG",
                    "entry":round(price,2),
                    "tp":round(price*1.02,2),
                    "sl":round(price*0.99,2),
                    "leverage":5,
                    "confidence":min(95,score*20),
                    "reasons":reasons
                })
    return signals
