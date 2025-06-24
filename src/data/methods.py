

class BetInputCalculator:
    def __init__(self, back_stake: float, back_odds: float, back_cms: float, lay_odds: float, lay_cms: float, free_snr: bool, free_sr: bool, free_bet_val=None):
        # Values can be defaulted before class instantiation
        self.back_stake = back_stake
        self.back_odds  = back_odds
        self.back_cms   = back_cms
        self.lay_odds   = lay_odds
        self.lay_cms    = lay_cms
        # Stake Not Returned (Free Bet)
        self.free_snr   = free_snr
        # Stake Returned (Free Bet)
        self.free_sr    = free_sr
        self.fbv        = free_bet_val


    def get_lay_liability(self):
        return (self.lay_odds - 1) * self.back_stake


    def get_required_lay_stake(self):
        # If this bet is a Qualifying Bet
        if not (self.free_snr) and not (self.free_sr):
            return (self.back_odds * self.back_stake) / (self.lay_odds - self.lay_cms)

        if self.free_snr:
            return (self.back_odds - 1) / (self.lay_odds - self.lay_cms) * self.fbv
                
        if self.free_sr:
            return (self.back_odds * self.fbv) / (self.lay_odds - self.lay_cms)



    def back_bet_win_values(self):
        # Qualifying Bet
        if not (self.free_snr) and not (self.free_sr):
            bookmaker_profit_loss = self.back_stake * (self.back_odds - 1)
            exchange_profit_loss = self.get_lay_liability()
            net_profit_loss = bookmaker_profit_loss + exchange_profit_loss
            return net_profit_loss
        
        




    def lay_bet_win_values(self):
        pass



    def get_total_profit(self):
        pass

