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
