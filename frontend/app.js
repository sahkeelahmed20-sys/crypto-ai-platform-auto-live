const API = "https://crypto-ai-platform-auto-live.onrender.com";

async function login() {
  const user = document.getElementById("username").value;
  const pass = document.getElementById("password").value;

  const res = await fetch(API + "/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      username: user,
      password: pass
    })
  });

  if (!res.ok) {
    document.getElementById("loginStatus").innerText = "Login failed";
    return;
  }

  const data = await res.json();
  localStorage.setItem("token", data.token);

  document.getElementById("loginStatus").innerText = "Login successful";
  document.getElementById("loginCard").style.display = "none";
  document.getElementById("dashboard").style.display = "block";
}