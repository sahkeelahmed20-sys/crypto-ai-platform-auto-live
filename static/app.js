const API = "https://crypto-ai-platform-auto-live.onrender.com";

let chart;

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