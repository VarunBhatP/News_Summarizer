// src/components/Navbar.js
import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const Navbar = () => {
  const { user, logoutUser } = useContext(AuthContext);

  return (
    <nav className="navbar">
      <h2>NewsDigest</h2>
      <div className="nav-links">
        <Link to="/">Home</Link>
        <Link to="/sources">Sources</Link>
        <Link to="/articles">Articles</Link>
        <Link to="/favorites">Favorites</Link>
        <Link to="/history">History</Link>
        <Link to="/search">Search</Link>

        {user ? (
          <>
            <span className="welcome">Hi, {user.username}</span>
            <button onClick={logoutUser}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/signup">Signup</Link>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
