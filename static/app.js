const API = "https://crypto-ai-platform-auto-live.onrender.com";

const chart = LightweightCharts.createChart(
  document.getElementById('chart'),
  {
  layout: { background: { color: '#0b1220' }, textColor: '#cbd5e1' },
  grid: { vertLines: { color: '#1f2937' }, horzLines: { color: '#1f2937' } },
  timeScale: { timeVisible: true }
});

const candleSeries = chart.addCandlestickSeries({
  upColor: '#22c55e',
  downColor: '#ef4444',
  borderUpColor: '#22c55e',
  borderDownColor: '#ef4444',
  wickUpColor: '#22c55e',
  wickDownColor: '#ef4444'
});

const chart = LightweightCharts.createChart(
  document.getElementById('chart'),
  { width: window.innerWidth - 40, height: 400 }
);

const candleSeries = chart.addCandlestickSeries();

fetch("/market/candles?symbol=BTCUSDT&interval=1h")
  .then(res => res.json())
  .then(data => {
    candleSeries.setData(
      data.map(c => ({
        time: c.time / 1000,
        open: c.open,
        high: c.high,
        low: c.low,
        close: c.close
      }))
    );
  });

const ema20 = chart.addLineSeries({ color:'#60a5fa', lineWidth:2 });

const rsiChart = LightweightCharts.createChart(document.getElementById('rsi'), {
  height:160, layout:{ background:{color:'#0b1220'}, textColor:'#cbd5e1' }
});
const rsiLine = rsiChart.addLineSeries({ color:'#f59e0b', lineWidth:2 });

// Load candles from backend
fetch('/market/candles?symbol=BTCUSDT')
  .then(res => res.json())
  .then(data => {
    candleSeries.setData(data);
  });
  
const vwapLine = chart.addLineSeries({
  color: '#eab308',
  lineWidth: 2
});

const macdChart = LightweightCharts.createChart(
  document.getElementById('macd'),
  {
    height: 160,
    layout: { background: { color: '#0b1220' }, textColor: '#cbd5e1' },
    grid: { vertLines: { color: '#1f2937' }, horzLines: { color: '#1f2937' } }
  }
);

const macdLine = macdChart.addLineSeries({ color: '#60a5fa', lineWidth: 2 });
const macdSignal = macdChart.addLineSeries({ color: '#f97316', lineWidth: 2 });
const macdHist = macdChart.addHistogramSeries({
  color: '#22c55e',
  priceFormat: { type: 'volume' }
});

let chart;

async function loadCandles() {
  const r = await fetch(`${API}/market/candles?symbol=BTCUSDT&interval=1m&limit=200`);
  1m`);
  const data = await res.json();

  candleSeries.setData(
    data.map(c => ({
      time: c.time,
      open: c.open,
      high: c.high,
      low: c.low,
      close: c.close
    }))
  );
}

loadCandles();

  ema20.setData(d.map(x => ({ time: x.time, value: x.ema20 })));
  vwapLine.setData(d.map(x => ({ time: x.time, value: x.vwap })));

  rsiLine.setData(d.filter(x => x.rsi14).map(x => ({
    time: x.time, value: x.rsi14
  })));

  macdLine.setData(d.map(x => ({ time: x.time, value: x.macd })));
  macdSignal.setData(d.map(x => ({ time: x.time, value: x.macd_signal })));
  macdHist.setData(d.map(x => ({
    time: x.time,
    value: x.macd_hist,
    color: x.macd_hist >= 0 ? '#22c55e' : '#ef4444'
  })));
}

async function loadTrades(){
  const r = await fetch(`${API}/trades`);
  const t = await r.json();
  candle.setMarkers(t.map(x=>({
    time: x.time,
    position: x.side === "BUY" ? "belowBar" : "aboveBar",
    color: x.side === "BUY" ? "#22c55e" : "#ef4444",
    shape: x.side === "BUY" ? "arrowUp" : "arrowDown",
    text: x.side
  })));
}

loadCandles();
loadTrades();
setInterval(loadCandles, 5000);

async function loadStats() {
  const token = localStorage.getItem("token");

  const res = await fetch(`${API}/stats/summary`, {
    headers: { Authorization: `Bearer ${token}` }
  });

  const d = await res.json();
  document.getElementById("stats").innerText =
    `Balance: $${d.balance} | Profit: ${d.profit}% | Trades: ${d.trades}`;
}

loadStats();

async function loadChart() {
  const r = await fetch(API + "/stats/chart");
  const d = await r.json();

  const ctx = document.getElementById("tradeChart");

  if (chart) chart.destroy();

  chart = new Chart(ctx, {
    type: "line",
    data: {
      labels: d.labels,
      datasets: [{
        label: "Profit",
        data: d.profits,
        borderColor: "green",
        tension: 0.3
      }]
    }
  });
}

loadStats();
loadChart();
setInterval(() => {
  loadStats();
  loadChart();
}, 5000);

if (user.role === "admin") {
  document.getElementById("adminPanel").style.display = "block";
}

const API = "https://crypto-ai-platform-auto-live.onrender.com";

async function login() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const res = await fetch(`${API}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
    "username": "admin",
    "role": "admin"
}
  });

  if (!res.ok) {
    document.getElementById("loginStatus").innerText = "Login failed";
    return;
  }
  
if user["role"] != "admin":
    raise HTTPException(status_code=403)

  const data = await res.json();
  localStorage.setItem("token", data.token);

  document.getElementById("login").style.display = "none";
  document.getElementById("dashboard").style.display = "block";
}

    // OPTIONAL: redirect
    window.location.href = "/dashboard.html";

  } catch (e) {
    status.innerText = "Server error";
    console.error(e);
  }
}