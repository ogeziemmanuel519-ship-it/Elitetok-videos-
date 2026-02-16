// ======================
// Global Variables
// ======================
let token = localStorage.getItem("token");
let coins = parseInt(localStorage.getItem("coins")) || 0;

const coinsElem = document.getElementById("coins");
if (coinsElem) coinsElem.textContent = `Coins: ${coins}`;

// ======================
// Signup
// ======================
async function signup() {
  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const referral = document.getElementById("referral")?.value || null;

  try {
    const res = await fetch("/api/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password, referral })
    });
    const data = await res.json();

    if (res.ok && data.token) {
      localStorage.setItem("token", data.token);
      localStorage.setItem("coins", data.coins || 0);
      window.location.href = "dashboard.html";
    } else {
      alert(data.detail || data.message || "Signup failed");
    }
  } catch (err) {
    alert("Signup error: " + err.message);
  }
}

// ======================
// Login
// ======================
async function login() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });
    const data = await res.json();

    if (res.ok && data.token) {
      localStorage.setItem("token", data.token);
      localStorage.setItem("coins", data.coins || 0);
      window.location.href = "dashboard.html";
    } else {
      alert(data.detail || data.message || "Login failed");
    }
  } catch (err) {
    alert("Login error: " + err.message);
  }
}

// ======================
// Video Analysis
// ======================
async function analyzeVideo() {
  if (!token) { alert("Please login first"); return; }
  if (coins < 5) { alert("Not enough coins!"); return; }

  try {
    const res = await fetch("/api/analyze", {
      method: "POST",
      headers: { 
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      }
    });
    const data = await res.json();
    if (res.ok) {
      coins = data.coins;
      localStorage.setItem("coins", coins);
      if (coinsElem) coinsElem.textContent = `Coins: ${coins}`;
      alert(`Video analyzed! AI rating: ${data.ai_rating}`);
    } else {
      alert(data.detail || data.message);
    }
  } catch (err) {
    alert("Analysis error: " + err.message);
  }
}

// ======================
// Buy Coins
// ======================
function buyCoins(amount, price) {
  alert(`Redirecting to Ko-fi for £${price} → ${amount} coins`);
  window.open(`https://ko-fi.com/yourusername?addFunds=${price}`, "_blank");
  coins += amount;
  localStorage.setItem("coins", coins);
  if (coinsElem) coinsElem.textContent = `Coins: ${coins}`;
}

// ======================
// Logout
// ======================
function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("coins");
  token = null;
  coins = 0;
  window.location.href = "index.html";
}

// ======================
// PayPal Hosted Button
// ======================
if (document.getElementById("paypal-container-A6XPR75K8KVXL")) {
  paypal.HostedButtons({
    hostedButtonId: "A6XPR75K8KVXL",
    onApprove: function() {
      alert("Payment approved! Coins added.");
      coins += 1000;
      localStorage.setItem("coins", coins);
      if (coinsElem) coinsElem.textContent = `Coins: ${coins}`;
    }
  }).render("#paypal-container-A6XPR75K8KVXL");
}