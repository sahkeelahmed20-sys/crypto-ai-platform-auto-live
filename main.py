
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ai_engine import get_all_signals
from auto_trader import auto_trade

app=FastAPI()
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])

DEMO_USER={
 "api_key":"PUT_TESTNET_KEY",
 "api_secret":"PUT_TESTNET_SECRET",
 "balance":1000,
 "auto_trade":True
}

@app.get("/signals")
def signals():
    sigs=get_all_signals()
    out=[]
    for s in sigs:
        s["auto"]=auto_trade(s,DEMO_USER)
        out.append(s)
    return out
