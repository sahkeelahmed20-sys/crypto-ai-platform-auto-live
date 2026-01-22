
from executor import execute_trade
from config import TRADING_ENABLED

def auto_trade(signal,user):
    if not TRADING_ENABLED: return {"status":"blocked"}
    return execute_trade(user["api_key"],user["api_secret"],signal,user["balance"])
