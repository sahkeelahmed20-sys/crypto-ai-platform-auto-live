alert("app.js loaded");
const API = "https://crypto-ai-platform-auto-live.onrender.com";

document.getElementById("loginBtn").addEventListener("click", login);

async function login() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const msg = document.getElementById("msg");

  msg.innerText = "Logging in...";

  try {
    const res = await fetch("https://crypto-ai-platform-auto-live.onrender.com/login")
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        username: username,
        password: password
      })
    });

    if (!res.ok) {
      msg.innerText = "Login failed";
      return;
    }

    const data = await res.json();
    localStorage.setItem("token", data.token);

    msg.innerText = "Login success ✅";
    console.log("TOKEN:", data.token);

  } catch (err) {
    msg.innerText = "Server error";
    console.error(err);
  }
}
