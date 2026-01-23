const API = "https://crypto-ai-platform-auto-live.onrender.com";

document.getElementById("loginBtn").onclick = async () => {
  alert("Login clicked");

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const msg = document.getElementById("msg");

  try {
    const r = await fetch(API + "/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });

    if (!r.ok) {
      msg.innerText = "Login failed";
      return;
    }

    const d = await r.json();
    localStorage.setItem("token", d.token);
    msg.innerText = "Login success";
  } catch (e) {
    msg.innerText = "JS error";
    console.error(e);
  }
};
