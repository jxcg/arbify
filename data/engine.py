import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BetInputCalculator:
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
        mbibl: bool = False,
        cashback_retention: float = 0.7
    ):
        self.back_stake = back_stake  # Back bet stake
        self.back_odds = back_odds    # Back bet odds
        self.back_cms = back_cms      # Back commission
        self.lay_odds = lay_odds      # Lay bet odds
        self.lay_cms = lay_cms        # Lay commission
        self.free_sr = free_sr        # Free bet stake returned
        self.free = free_bet          # Is free bet
        self.mbibl = mbibl            # Money Back If Bet Loses
        self.free_bet_val = free_bet_val  # Cashback/free bet value
        self.cashback_retention = cashback_retention  # Cashback retention %



    def get_required_lay_stake(self):
        if self.mbibl:
            # MBIBL lay stake formula
            stake = (self.back_stake * (self.back_odds - 1)) / (self.lay_odds * (1 - self.lay_cms))
            logger.info(f"MBIBL - Required Lay Stake: {stake}")
            return stake

        if not self.free:
            # Qualifying bet lay stake formula
            stake = (self.back_odds * self.back_stake) / (self.lay_odds - self.lay_cms)
            logger.info(f"Qualifying Bet - Required Lay Stake: {stake}")
            return stake

        if self.free and not self.free_sr:
            # Free bet SNR lay stake formula
            stake = (self.back_odds - 1) / (self.lay_odds - self.lay_cms) * self.back_stake
            logger.info(f"Free Bet (SNR) - Required Lay Stake: {stake}")
            return stake

        if self.free and self.free_sr:
            # Free bet SR lay stake formula
            stake = (self.back_odds * self.back_stake) / (self.lay_odds - self.lay_cms)
            logger.info(f"Free Bet (SR) - Required Lay Stake: {stake}")
            return stake



    def get_lay_liability(self, lay_stake=None):
        if lay_stake is None:
            lay_stake = self.get_required_lay_stake()
        # Lay liability formula
        liability = (self.lay_odds - 1) * lay_stake
        logger.info(f"Lay Liability calculated: {liability}")
        return liability



    def simulate_cashback_value(self):
        # Cashback/free bet retention calculation
        value = self.free_bet_val * self.cashback_retention
        logger.info(f"Simulated Cashback Value (SNR): {value}")
        return value



    def back_bet_win_values(self):
        lay_stake = self.get_required_lay_stake()
        lay_liability = self.get_lay_liability(lay_stake)

        if self.free and not self.free_sr:
            # Free bet SNR bookmaker profit
            bookmaker_profit = self.back_stake * (self.back_odds - 1)
        elif self.free and self.free_sr:
            # Free bet SR bookmaker profit
            bookmaker_profit = self.back_stake * self.back_odds
        else:
            # Qualifying/MBIBL bookmaker profit
            bookmaker_profit = self.back_stake * (self.back_odds - 1)

        # Net profit if back bet wins
        net_profit = bookmaker_profit - lay_liability
        logger.info(f"Back Bet Wins - Net Profit: {net_profit}")
        return net_profit



    def lay_bet_win_values(self):
        lay_stake = self.get_required_lay_stake()
        # Exchange profit calculation
        exchange_profit = lay_stake * (1 - self.lay_cms)

        if self.free:
            # Free bet bookmaker loss
            bookmaker_loss = 0
        elif self.mbibl:
            # MBIBL bookmaker loss with cashback
            cashback = self.simulate_cashback_value()
            bookmaker_loss = -self.back_stake + cashback
            logger.info(f"MBIBL - Bookmaker Loss: -{self.back_stake} + Cashback {cashback}")
        else:
            # Qualifying bet bookmaker loss
            bookmaker_loss = -self.back_stake

        # Net profit if lay bet wins
        net_profit = exchange_profit + bookmaker_loss
        logger.info(f"Lay Bet Wins - Net Profit: {net_profit}")
        return net_profit



    def get_total_profit(self):
        back_profit = self.back_bet_win_values()
        lay_profit = self.lay_bet_win_values()
        # Return rounded profits for both outcomes
        logger.info(f"Total Profit - Back Wins: {back_profit}, Lay Wins: {lay_profit}")
        return {
            "back_wins": round(back_profit, 2),
            "lay_wins": round(lay_profit, 2)
        }