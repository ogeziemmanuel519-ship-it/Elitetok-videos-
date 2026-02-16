// ======================
// Global Variables
// ======================
let token = localStorage.getItem("token");
let coins = parseInt(localStorage.getItem("coins")) || 0;

const coinsElem = document.getElementById("coins");
if (coinsElem) coinsElem.textContent = `Coins: ${coins}`;

// Redirect dashboard if not logged in
if (document.body.contains(coinsElem) && !token) {
  console.log("No token found, redirecting to login...");
  window.location.href = "login.html";
}

// ======================
// Signup
// ======================
async function signup() {
  console.log("Signup clicked");
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
    console.log("Response received", res);
    const data = await res.json();
    console.log("Parsed data", data);

    if (res.ok && data.token) {
      localStorage.setItem("token", data.token);
      localStorage.setItem("coins", data.coins || 0);
      window.location.href = "dashboard.html";
    } else {
      alert(data.detail || data.message || "Signup failed");
    }
  } catch (err) {
    alert("Signup error: " + err.message);
    console.error(err);
  }
}

// ======================
// Login
// ======================
async function login() {
  console.log("Login clicked");
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });
    console.log("Response received", res);
    const data = await res.json();
    console.log("Parsed data", data);

    if (res.ok && data.token) {
      localStorage.setItem("token", data.token);
      localStorage.setItem("coins", data.coins || 0);
      window.location.href = "dashboard.html";
    } else {
      alert(data.detail || data.message || "Login failed");
    }
  } catch (err) {
    alert("Login error: " + err.message);
    console.error(err);
  }
}

// ======================
// Video Analysis
// ======================
async function analyzeVideo() {
  if (!token) { alert("Please login first"); return; }
  if (coins < 5) { alert("Not enough coins!"); return; }

  const videoLink = document.getElementById("video-link")?.value;
  const videoFile = document.getElementById("video-file")?.files[0];

  if (!videoLink && !videoFile) {
    alert("Please provide a video link or upload a file");
    return;
  }

  const formData = new FormData();
  if (videoLink) formData.append("link", videoLink);
  if (videoFile) formData.append("file", videoFile);

  try {
    const res = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Authorization": `Bearer ${token}` },
      body: formData
    });

    const data = await res.json();

    if (res.ok) {
      // Deduct 5 coins
      coins = data.coins;
      localStorage.setItem("coins", coins);
      if (coinsElem) coinsElem.textContent = `Coins: ${coins}`;

      alert(`Video analyzed! AI rating: ${data.ai_rating}`);
    } else {
      alert(data.detail || data.message || "Analysis failed");
    }
  } catch (err) {
    alert("Analysis error: " + err.message);
    console.error(err);
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