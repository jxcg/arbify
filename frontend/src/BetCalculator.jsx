// src/BetCalculator.js
import React, { useState } from 'react';
import './BetCalculator.css';

function BetCalculator() {
  const [betType, setBetType] = useState('qualifying');
  const [form, setForm] = useState({
    backStake: '10.00',
    backOdds: '',
    backCommission: '0',
    layOdds: '',
    layCommission: '2',
  });

  const handleFormChange = (e) => {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: value }));
  };

  const layStakeRequired = '0.00';
  const totalProfit = '0.00';

  return (
    <div className="calculator-main">
      <div className="calculator-grid">

        {/* --- LEFT COLUMN (FORM) --- */}
        <div className="form-column">
          <div className="card">
            <div className="bet-type-section">
              <h2>Select bet type</h2>
              <label className="radio-option">
                <input type="radio" name="betType" value="qualifying" checked={betType === 'qualifying'} onChange={(e) => setBetType(e.target.value)} />
                <div className="radio-custom"><div className="radio-custom-dot"></div></div>
                <div className="radio-label">
                  <strong>Qualifying Bet</strong>
                  <span> - Use when placing a bet to qualify for a free bet or bonus.</span>
                </div>
              </label>
              <label className="radio-option">
                <input type="radio" name="betType" value="freebet" checked={betType === 'freebet'} onChange={(e) => setBetType(e.target.value)} />
                <div className="radio-custom"><div className="radio-custom-dot"></div></div>
                <div className="radio-label">
                  <strong>Free Bet</strong>
                  <span> - Use when converting a free bet or bonus into cash.</span>
                </div>
              </label>
              <label className="radio-option">
                <input type="radio" name="betType" value="moneyback" checked={betType === 'moneyback'} onChange={(e) => setBetType(e.target.value)} />
                <div className="radio-custom"><div className="radio-custom-dot"></div></div>
                <div className="radio-label">
                  <strong>Money Back if Bet Loses</strong>
                  <span> - Use when losing stakes are refunded.</span>
                </div>
              </label>
            </div>
          </div>

          <div className="bet-section back-bet">
            <div className="section-header"><h3>Back Bet (Bookie)</h3></div>
            <div className="input-grid">
              <div className="input-group">
                <label htmlFor="backStake">Back stake</label>
                <input id="backStake" name="backStake" type="number" value={form.backStake} onChange={handleFormChange} />
              </div>
              <div className="input-group">
                <label htmlFor="backOdds">Back odds (decimal)</label>
                <input id="backOdds" name="backOdds" type="number" value={form.backOdds} onChange={handleFormChange} />
              </div>
            </div>
          </div>

          <div className="bet-section lay-bet">
            <div className="section-header"><h3>Lay Bet (Betting Exchange)</h3></div>
            <div className="input-grid">
              <div className="input-group">
                <label htmlFor="layOdds">Lay odds (decimal)</label>
                <input id="layOdds" name="layOdds" type="number" value={form.layOdds} onChange={handleFormChange} />
              </div>
              <div className="input-group">
                <label htmlFor="layCommission">Lay commission %</label>
                <input id="layCommission" name="layCommission" type="number" value={form.layCommission} onChange={handleFormChange} />
              </div>
            </div>
          </div>
        </div>

        {/* --- RIGHT COLUMN (RESULTS) --- */}
        <div className="results-column">
          <div className="card">
            <div className="results-table">
              <div className="results-row">
                <span className="results-label">If back (bookie) bet wins</span>
                <span className="results-value">£0.00</span>
              </div>
              <div className="results-row">
                <span className="results-label">If lay (exchange) bet wins</span>
                <span className="results-value">£0.00</span>
              </div>
              <div className="results-row">
                <span className="results-label">Lay stake required</span>
                <span className="results-value">£{layStakeRequired}</span>
              </div>
            </div>
          </div>
          
          <div className="summary-card">
            <p>Total Profit</p>
            <div className="profit-value">£{totalProfit}</div>
          </div>
        </div>
        
      </div>
    </div>
  );
}

export default BetCalculator;