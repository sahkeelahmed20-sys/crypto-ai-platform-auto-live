@app.get("/signals")
def signals():
    try:
        signals = get_all_signals()
        return {
            "count": len(signals),
            "signals": signals
        }
    except Exception as e:
        return {
            "error": str(e),
            "type": type(e).__name__
        }
