const API = "https://crypto-ai-platform-auto-live.onrender.com";

async function login() {
  const user = document.getElementById("username").value;
  const pass = document.getElementById("password").value;

  const r = await fetch(API + "/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username: user, password: pass })
  });

  if (!r.ok) {
    alert("Login failed");
    return;
  }

  const d = await r.json();
  localStorage.setItem("token", d.token);

  window.location.href = "dashboard.html";
}

async function loadChart() {
  const r = await fetch(API + "/stats/history");
  const data = await r.json();

  new Chart(document.getElementById("profitChart"), {
    type: "line",
    data: {
      labels: data.map(d => new Date(d.time).toLocaleString()),
      datasets: [{
        label: "Profit",
        data: data.map(d => d.profit),
        borderColor: "lime"
      }]
    }
  });
}

loadChart();

async function enable() {
  const r = await fetch(API + "/control/enable", {
    method: "POST",
    headers: {
      "Authorization": "Bearer " + localStorage.getItem("token")
    }
  });
  document.getElementById("output").innerText = await r.text();
}

async function disable() {
  const r = await fetch(API + "/control/disable", {
    method: "POST",
    headers: {
      "Authorization": "Bearer " + localStorage.getItem("token")
    }
  });
  document.getElementById("output").innerText = await r.text();
}
