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

async function loadCandles(){
  const r = await fetch(`${API}/market/candles?symbol=BTCUSDT&interval=1m&limit=200`);
  const d = await r.json();

  candle.setData(d.map(x=>({
    time:x.time, open:x.open, high:x.high, low:x.low, close:x.close
  })));
  ema20.setData(d.map(x=>({ time:x.time, value:x.ema20 })));
  rsiLine.setData(d.filter(x=>x.rsi14).map(x=>({ time:x.time, value:x.rsi14 })));
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
  const r = await fetch(API + "/stats/summary");
  const d = await r.json();

  document.getElementById("totalTrades").innerText = d.total_trades;
  document.getElementById("winRate").innerText = d.win_rate;
  document.getElementById("profit").innerText = d.profit;
}

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

async function login() {
  const user = document.getElementById("username").value;
  const pass = document.getElementById("password").value;
  const status = document.getElementById("loginStatus");

  try {
    const r = await fetch(API + "/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        username: user,
        password: pass
      })
    });

    if (!r.ok) {
      status.innerText = "Login failed";
      return;
    }

    const data = await r.json();

    localStorage.setItem("token", data.token);

    status.innerText = "Login successful";

    // OPTIONAL: redirect
    window.location.href = "/dashboard.html";

  } catch (e) {
    status.innerText = "Server error";
    console.error(e);
  }
}