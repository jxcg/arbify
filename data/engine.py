import streamlit as st

class MatchedBetCalculator:
    """
    Matched bet calculator for qualifying bets, welcome bets, and free bets.
    """
    
    def __init__(
        self,
        back_stake: float,
        back_odds: float,
        back_cms: float,
        lay_odds: float,
        lay_cms: float,
        free_sr: bool,
        free_bet: bool = False,
        free_bet_val: float = 0.0,
        mbibl: bool = False
    ):
        """
        Initialise the matched bet calculator.
        
        Parameters:
        - back_stake: Back stake amount
        - back_odds: Back bet odds
        - back_cms: Back commission (as decimal, e.g., 0.05 for 5%)
        - lay_odds: Lay bet odds
        - lay_cms: Lay commission (as decimal, e.g., 0.05 for 5%)
        - free_sr: True if free bet stake is returned, False if not
        - free_bet: True if this is a free bet calculation
        - free_bet_val: Value of the free bet
        - mbibl: Money back if bet loses (not implemented in formulas provided)
        """
        self.back_stake = back_stake
        self.back_odds = back_odds
        self.back_cms = back_cms
        self.lay_odds = lay_odds
        self.lay_cms = lay_cms
        self.free_sr = free_sr
        self.free_bet = free_bet
        self.free_bet_val = free_bet_val
        self.mbibl = mbibl
    
    def get_bet_type(self) -> str:
        """Return the type of bet being calculated"""
        if self.free_bet:
            return 'Free Bet (Stake Returned)' if self.free_sr else 'Free Bet (Stake Not Returned)'
        return 'Qualifying/Welcome Bet'
    
    def get_required_lay_stake(self) -> float:
        """Calculate the ideal lay stake for even profit"""
        if self.free_bet:
            if self.free_sr:
                # Free bet - stake returned (SR)
                return (self.back_odds * self.free_bet_val) / (self.lay_odds - self.lay_cms)
            else:
                # Free bet - stake NOT returned (SNR)
                return (self.back_odds - 1) / (self.lay_odds - self.lay_cms) * self.free_bet_val
        else:
            # Qualifying/welcome bet
            return self.back_odds * self.back_stake / (self.lay_odds - self.lay_cms)
    
    def get_lay_liability(self, lay_stake: float) -> float:
        """Calculate the lay liability (potential loss on lay bet)"""
        return lay_stake * (self.lay_odds - 1)
    
    def get_total_profit(self) -> dict:
        """Calculate profits for both win scenarios"""
        lay_stake = self.get_required_lay_stake()
        
        if self.free_bet:
            if self.free_sr:
                # Free bet - stake returned (SR)
                back_wins = self.free_bet_val * self.back_odds - lay_stake * (self.lay_odds - 1)
                lay_wins = (1 - self.lay_cms) * lay_stake
            else:
                # Free bet - stake NOT returned (SNR)
                back_wins = (self.back_odds - 1) * self.free_bet_val - (self.lay_odds - 1) * lay_stake
                lay_wins = lay_stake * (1 - self.lay_cms)
        else:
            # Qualifying/welcome bet
            back_wins = self.back_stake * (self.back_odds - 1) - lay_stake * (self.lay_odds - 1)
            lay_wins = lay_stake * (1 - self.lay_cms) - self.back_stake
        
        return {
            'back_wins': back_wins,
            'lay_wins': lay_wins
        }



    def get_bookie_exchange_breakdown(self) -> dict:
        """
        Returns a detailed breakdown of bookie and exchange P&L for both outcomes:
        back bet wins and lay bet wins.
        """
        lay_stake = self.get_required_lay_stake()
        liability = lay_stake * (self.lay_odds - 1)
        lay_profit = lay_stake * (1 - self.lay_cms)

        if self.free_bet:
            stake_used = self.free_bet_val
            if self.free_sr:
                bookie_win = stake_used * self.back_odds
            else:
                bookie_win = stake_used * (self.back_odds - 1)
            bookie_loss = 0
        else:
            stake_used = self.back_stake
            bookie_win = stake_used * self.back_odds
            bookie_loss = -stake_used

        # Build output dict
        back_win_bookie_pl = (bookie_win - stake_used) if not self.free_bet or self.free_sr else bookie_win
        lay_win_bookie_pl = bookie_loss

        back_win_exchange_pl = -liability
        lay_win_exchange_pl = lay_profit

        return {
            'back_wins': {
                'bookie_pl': round(back_win_bookie_pl, 2),
                'exchange_pl': round(back_win_exchange_pl, 2),
                'total': round(back_win_bookie_pl + back_win_exchange_pl, 2)
            },
            'lay_wins': {
                'bookie_pl': round(lay_win_bookie_pl, 2),
                'exchange_pl': round(lay_win_exchange_pl, 2),
                'total': round(lay_win_bookie_pl + lay_win_exchange_pl, 2)
            }
        }

    
    
    def get_final_profit(self) -> float:
        """Calculate the final expected profit"""
        lay_stake = self.get_required_lay_stake()
        
        if self.free_bet:
            # For free bets, final profit is the lay wins scenario
            return lay_stake * (1 - self.lay_cms) if self.free_sr else lay_stake * (1 - self.lay_cms)
        else:
            # For qualifying/welcome bets
            return lay_stake * (1 - self.lay_cms) - self.back_stake
    
    def summary(self) -> str:
        """Return a formatted summary of the calculation"""
        lay_stake = self.get_required_lay_stake()
        liability = self.get_lay_liability(lay_stake)
        profits = self.get_total_profit()
        return (
            f"Required Lay Stake: £{lay_stake:.2f}\n"
            f"Lay Liability: £{liability:.2f}\n"
            f"Profit if Back Wins: £{profits['back_wins']:.2f}\n"
            f"Profit if Lay Wins: £{profits['lay_wins']:.2f}"
        )
    
    def detailed_summary(self) -> str:
        """Return a detailed formatted summary"""
        lay_stake = self.get_required_lay_stake()
        liability = self.get_lay_liability(lay_stake)
        profits = self.get_total_profit()
        final_profit = self.get_final_profit()
        
        stake_used = self.free_bet_val if self.free_bet else self.back_stake
        
        return (
            f"{'='*50}\n"
            f"MATCHED BET CALCULATOR RESULTS\n"
            f"{'='*50}\n"
            f"Bet Type: {self.get_bet_type()}\n"
            f"Back Stake: £{stake_used:.2f}\n"
            f"Back Odds: {self.back_odds:.2f}\n"
            f"Lay Odds: {self.lay_odds:.2f}\n"
            f"Lay Commission: {self.lay_cms*100:.1f}%\n\n"
            f"RECOMMENDED LAY STAKE: £{lay_stake:.2f}\n"
            f"LAY LIABILITY: £{liability:.2f}\n\n"
            f"PROFIT SCENARIOS:\n"
            f"  If back bet wins: £{profits['back_wins']:.2f}\n"
            f"  If lay bet wins:  £{profits['lay_wins']:.2f}\n\n"
            f"FINAL PROFIT: £{final_profit:.2f}\n"
            f"{'='*50}"
        )

