CREATE TABLE IF NOT EXISTS matched_bets (
    -- A unique ID for each bet record
    id SERIAL PRIMARY KEY,

    -- The date and time the bet was placed
    bet_date TIMESTAMPTZ DEFAULT NOW(),

    -- Details from your spreadsheet
    bookmaker VARCHAR(100) NOT NULL,
    event VARCHAR(255) NOT NULL,
    bet_type VARCHAR(50) NOT NULL,
    
    -- Back Bet details
    back_stake DECIMAL NOT NULL,
    back_odds DECIMAL NOT NULL,

    -- Lay Bet details
    exchange VARCHAR(100),
    lay_odds DECIMAL,
    lay_stake DECIMAL,
    lay_liability DECIMAL,

    -- Outcome and Profit/Loss
    -- Outcome can be 'Won' (back bet won), 'Lost' (back bet lost), 'Void', or 'Pending'
    bookmaker_profit_loss DECIMAL,
    exchange_profit_loss DECIMAL,
    net_profit_loss DECIMAL,
    
    -- Optional field for any extra notes
    notes TEXT
);
