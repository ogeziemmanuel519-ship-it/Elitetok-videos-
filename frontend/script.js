const API = "/api";

async function signup() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const ref = document.getElementById("ref").value;

  const res = await fetch(API + "/signup", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({email, password, ref})
  });
  const data = await res.json();
  alert(data.message || JSON.stringify(data));
}

async function login() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const res = await fetch(API + "/login", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({email, password})
  });
  const data = await res.json();
  if(data.token){
    alert("Login successful! Coins: " + data.coins);
    window.location.href = "dashboard.html";
  } else alert("Login failed");
}