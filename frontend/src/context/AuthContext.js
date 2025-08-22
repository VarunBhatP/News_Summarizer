// src/context/AuthContext.js
import React, { createContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [authTokens, setAuthTokens] = useState(() =>
    localStorage.getItem("authTokens")
      ? JSON.parse(localStorage.getItem("authTokens"))
      : null
  );
  const [user, setUser] = useState(() =>
    authTokens ? { username: "User" } : null
  );
  const [loading, setLoading] = useState(true);

  const navigate = useNavigate();

  // Login function
  const loginUser = async (username, password) => {
    let response = await fetch("http://127.0.0.1:8000/api/token/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    let data = await response.json();

    if (response.status === 200) {
      setAuthTokens(data);
      setUser({ username });
      localStorage.setItem("authTokens", JSON.stringify(data));
      navigate("/"); // redirect after login
    } else {
      alert("Invalid credentials");
    }
  };

  // Signup function
  const signupUser = async (username, email, password) => {
    let response = await fetch("http://127.0.0.1:8000/api/register/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password }),
    });

    if (response.status === 201) {
      alert("Signup successful! You can now login.");
      navigate("/login");
    } else {
      alert("Error during signup");
    }
  };

  // Logout function
  const logoutUser = () => {
    setAuthTokens(null);
    setUser(null);
    localStorage.removeItem("authTokens");
    navigate("/login");
  };

  let contextData = {
    user,
    authTokens,
    loginUser,
    signupUser,
    logoutUser,
  };

  useEffect(() => {
    if (authTokens) {
      setUser({ username: "User" }); // Placeholder, could decode JWT for real user info
    }
    setLoading(false);
  }, [authTokens]);

  return (
    <AuthContext.Provider value={contextData}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

