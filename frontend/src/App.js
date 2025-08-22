// src/App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Navbar from "./components/Navbar";

import Login from "./pages/Login";
import Signup from "./pages/Signup";

// Dummy pages (replace with real ones later)
const Home = () => <h2>Welcome to NewsDigest</h2>;
const Sources = () => <h2>Sources Page</h2>;
const Articles = () => <h2>Articles Page</h2>;
const Favorites = () => <h2>Favorites Page</h2>;
const History = () => <h2>History Page</h2>;
const Search = () => <h2>Search Articles</h2>;

function App() {
  return (
    <Router>
      <AuthProvider>
        <Navbar />
        <div className="container">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/sources" element={<Sources />} />
            <Route path="/articles" element={<Articles />} />
            <Route path="/favorites" element={<Favorites />} />
            <Route path="/history" element={<History />} />
            <Route path="/search" element={<Search />} />

            {/* Auth Pages */}
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
          </Routes>
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;
