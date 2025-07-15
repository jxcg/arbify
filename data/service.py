import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from data.db import get_db
bet_object = {
    "bookmaker": "Bet365",
    "event": "Team A vs Team B",
    "bet_type": "Match Winner",
    "back_stake": 100.0,
    "back_odds": 2.5,
    "exchange": "Betfair",
    "lay_odds": 2.4,
    "lay_stake": 104.17,
    "lay_liability": 150.0,
    "bookmaker_profit_loss": 150.0,
    "exchange_profit_loss": -150.0,
    "net_profit_loss": 0.0,
    "notes": "Arbitrage opportunity"
}



def insert_bet(bet_object):
    bookmaker       = bet_object.get('bookmaker')
    event           = bet_object.get('event')
    bet_type        = bet_object.get('bet_type')
    back_stake      = bet_object.get('back_stake')
    back_odds       = bet_object.get('back_odds')
    exchange        = bet_object.get('exchange')
    lay_odds        = bet_object.get('lay_odds')
    lay_stake       = bet_object.get('lay_stake')
    lay_liability   = bet_object.get('lay_liability')
    bookmaker_pl    = bet_object.get('bookmaker_profit_loss') or bet_object.get('bookie_pl')
    exchange_pl     = bet_object.get('exchange_profit_loss') or bet_object.get('exchange_pl')
    notes           = bet_object.get('notes')
    result          = bet_object.get('result', 'unsettled')  # default to 'unsettled' if missing

    query = """
    INSERT INTO matched_bets (
        bookmaker, event, bet_type, back_stake, back_odds, 
        exchange, lay_odds, lay_stake, lay_liability,
        bookmaker_profit_loss, exchange_profit_loss, notes, result
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    params = (
        bookmaker, 
        event, 
        bet_type, 
        back_stake, 
        back_odds, 
        exchange, 
        lay_odds,
        lay_stake,
        lay_liability,
        bookmaker_pl,
        exchange_pl,
        notes,
        result
    )

    with get_db() as db:
        result = db.execute(query, params)
        logger.info("Added bet")
        return True



def delete_bet(bet_id):
    query = """
    DELETE FROM bets
    WHERE id = %s
    RETURNING id;
    """
    params = (bet_id,)
    with get_db() as db:
        result = db.execute(query, params)
        return result



def get_all_bets():
    query = """
    SELECT
        id,
        bookmaker,
        event,
        bet_type,
        back_odds,
        lay_odds,
        back_stake,
        lay_stake,
        bookmaker_profit_loss,
        exchange_profit_loss,
        bet_date,
        notes,
        lay_liability,
        result
    FROM
        matched_bets
    ORDER BY
        bet_date DESC;
    """

    with get_db() as db:
        result = db.execute(query)
        return result



def update_bet_result(bet_id: int, result: str) -> bool:
    """Update the result of a bet (e.g., 'back', 'lay', 'void', 'unsettled')."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE bets SET result = ? WHERE id = ?",
            (result, bet_id)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating bet result: {e}")
        return False
