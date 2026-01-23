const API = "https://crypto-ai-platform-auto-live.onrender.com";

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