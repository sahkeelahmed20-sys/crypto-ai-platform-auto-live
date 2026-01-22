from executor import execute_trade
from config import AUTO_TRADING_STATE

def auto_trade(signal, user):
    if not AUTO_TRADING_STATE["enabled"]:
        return {"status": "disabled"}

    return execute_trade(
        user["api_key"],
        user["api_secret"],
        signal,
        user["balance"]
    )