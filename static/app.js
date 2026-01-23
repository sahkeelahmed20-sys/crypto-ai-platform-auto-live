const API = ""; // SAME DOMAIN (Render backend)

async function login() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const status = document.getElementById("status");

  status.innerText = "Logging in...";

  try {
    const res = await fetch("/login", {
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
      status.innerText = "Login failed";
      return;
    }

    const data = await res.json();
    localStorage.setItem("token", data.token);

    status.innerText = "Login success!";
    window.location.href = "/static/dashboard.html";

  } catch (err) {
    status.innerText = "Server error";
    console.error(err);
  }
}