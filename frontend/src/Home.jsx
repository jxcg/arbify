// In Home.jsx (or App.jsx)
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './Navbar';
import BetCalculator from './BetCalculator';
import BetsTable from './BetsTable';

// Import the App.css file which we will edit next
import './App.css'; 

function Home() {
  return (
    // This wrapper div is key
    <div className="app-wrapper"> 
      <Navbar />
      <main className="app-layout">
        <Routes>
          <Route path="/" element={<BetCalculator />} />
          <Route path="/bets" element={<BetsTable />} />
        </Routes>
      </main>
    </div>
  );
}

export default Home;