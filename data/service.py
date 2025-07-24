import logging
from data.db import get_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def get_profit_over_time():
    query = """
        SELECT 
            DATE(bet_date) AS date,
            SUM(net_profit_loss) AS daily_profit
        FROM matched_bets
        WHERE net_profit_loss IS NOT NULL
        GROUP BY DATE(bet_date)
        ORDER BY date ASC;
    """
    try:
        with get_db() as db:
            rows = db.execute(query)
            return rows
    except Exception as e:
        logger.error(f"❌ Failed to get stats: {e}")
        return []



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
    result          = bet_object.get('result', 'unsettled')

    query = """
        INSERT INTO matched_bets (
            bookmaker, event, bet_type, back_stake, back_odds, 
            exchange, lay_odds, lay_stake, lay_liability,
            bookmaker_profit_loss, exchange_profit_loss, notes, result
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    params = (
        bookmaker, event, bet_type, back_stake, back_odds,
        exchange, lay_odds, lay_stake, lay_liability,
        bookmaker_pl, exchange_pl, notes, result
    )

    try:
        with get_db() as db:
            db.execute(query, params)
            logger.info("✅ Bet added successfully.")
            return True
    except Exception as e:
        logger.error(f"❌ Failed to insert bet: {e}")
        return False


def delete_bet(bet_id):
    query = "DELETE FROM matched_bets WHERE id = %s RETURNING id;"
    try:
        with get_db() as db:
            result = db.execute(query, (bet_id,))
            return result.fetchone() is not None
    except Exception as e:
        logger.error(f"❌ Failed to delete bet {bet_id}: {e}")
        return False


def get_all_bets():
    query = """
        SELECT
            id,
            bet_date,
            bookmaker,
            event,
            bet_type,
            back_stake,
            back_odds,
            exchange,
            lay_odds,
            lay_stake,
            lay_liability,
            bookmaker_profit_loss,
            exchange_profit_loss,
            net_profit_loss,
            result,
            notes
        FROM matched_bets
        ORDER BY bet_date DESC;
    """
    try:
        with get_db() as db:
            result = db.execute(query)
            return result
    except Exception as e:
        logger.error(f"❌ Failed to fetch bets: {e}")
        return []



def update_bet_result(bet_id: int, result: str) -> bool:
    """Update the result of a bet ('back', 'lay', 'void', 'unsettled')."""
    query = "UPDATE matched_bets SET result = %s WHERE id = %s;"
    try:
        with get_db() as db:
            db.execute(query, (result, bet_id))
            logger.info(f"✅ Updated result for bet {bet_id} to '{result}'")
            return True
    except Exception as e:
        logger.error(f"❌ Failed to update result for bet {bet_id}: {e}")
        return False
