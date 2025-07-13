// src/Navbar.js
import React from 'react';
import { NavLink } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
  return (
    <nav className="main-nav">
      <div className="nav-logo">
        <a href="/">Arbify</a>
      </div>
      <div className="nav-links">
        <NavLink to="/" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
          Calculator
        </NavLink>
        <NavLink to="/bets" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
          Bets Table
        </NavLink>
      </div>
    </nav>
  );
}

export default Navbar;