import React, { useState } from "react";
import "./index.css";

const API = "/api";

export default function App() {
  const [token, setToken] = useState("");
  const [coins, setCoins] = useState(0);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [ref, setRef] = useState("");

  const signup = async () => {
    if (!email || !password) return alert("Enter email & password");
    try {
      const res = await fetch(API + "/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password, ref }),
      });
      const text = await res.text();
      alert(res.ok ? "Signup successful!" : "Signup failed: " + text);
    } catch (err) {
      alert("Error: " + err.message);
    }
  };

  const login = async () => {
    if (!email || !password) return alert("Enter email & password");
    try {
      const res = await fetch(API + "/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();
      if (data.token) {
        setToken(data.token);
        setCoins(data.coins);
        alert("Login successful!");
      } else alert("Login failed");
    } catch (err) {
      alert("Error: " + err.message);
    }
  };

  if (!token) {
    return (
      <div className="center">
        <div className="card">
          <h1 className="title">ELITE TOK</h1>
          <input placeholder="Email" onChange={e => setEmail(e.target.value)} />
          <input type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
          <input placeholder="Referral Code" onChange={e => setRef(e.target.value)} />
          <button onClick={signup}>Sign Up</button>
          <button onClick={login}>Login</button>
        </div>
      </div>
    );
  }

  return (
    <div className="center">
      <div className="card">
        <h2>Coins: {coins}</h2>
        <h3>Buy Coins</h3>
        <button onClick={() => window.open("https://ko-fi.com/elitetok", "_blank")}>£10 → 1000 Coins</button>
      </div>
    </div>
  );
}