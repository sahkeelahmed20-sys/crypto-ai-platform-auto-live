
from binance.client import Client
from config import MAX_RISK_PER_TRADE, MAX_LEVERAGE, BINANCE_TESTNET

def execute_trade(api_key, api_secret, signal, balance):
    client=Client(api_key,api_secret,testnet=BINANCE_TESTNET)
    client.futures_change_leverage(symbol=signal["pair"],leverage=min(signal["leverage"],MAX_LEVERAGE))
    qty=round((balance*MAX_RISK_PER_TRADE)/signal["entry"],3)
    side=Client.SIDE_BUY if signal["side"]=="LONG" else Client.SIDE_SELL
    return client.futures_create_order(symbol=signal["pair"],side=side,type="MARKET",quantity=qty)
