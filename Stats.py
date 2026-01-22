from datetime import datetime

TRADES = []

def log_trade(signal, result):
    TRADES.append({
        "time": datetime.utcnow().isoformat(),
        "pair": signal["pair"],
        "side": signal["side"],
        "entry": signal["entry"],
        "result": result.get("status", "unknown")
    })

def get_stats():
    total = len(TRADES)
    executed = len([t for t in TRADES if t["result"] == "executed"])
    disabled = len([t for t in TRADES if t["result"] == "disabled"])

    return {
        "total_trades": total,
        "executed": executed,
        "blocked": disabled
    }
