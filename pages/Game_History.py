import streamlit as st
import pandas as pd
import numpy as np
from data.engine import BetInputCalculator

def safe_float_from_text(label: str, value: str = "", placeholder: str = "") -> float | None:
    text_val = st.text_input(label, value=value, placeholder=placeholder)
    # If the input is empty or just whitespace, return None
    try:
        if not text_val.strip():
            return None

    except Exception as e:
        return None
    # Try to convert to float, show an error on failure
    try:
        return float(text_val)
    except ValueError:
        st.error(f'Invalid input for "{label}". Please enter a valid number.', icon="🚨")
        return None


def run():
    st.title("Game History")

    with st.form("bet_form"):
        col1, col2 = st.columns(2)
        with col1:
            back_stake      = safe_float_from_text("Back Stake*")
            back_odds       = safe_float_from_text("Back Odds*")
            lay_odds        = safe_float_from_text("Lay Odds*")
            back_cms        = safe_float_from_text("Back Commission (%)", value=0)
            lay_cms         = safe_float_from_text("Lay Commission (%)",value=2)

        with col2:
            bookmaker       = st.text_input("Bookmaker*", max_chars=100)
            bookmaker       = bookmaker.upper() if bookmaker and isinstance(bookmaker, str) else None
            event           = st.text_input("Event*")
            bet_type        = st.selectbox("Bet Type*", options=["Qualifying", "Free", "Money Back if Bet Loses"])
            exchange        = st.text_input("Exchange (optional)", max_chars=100)
            exchange        = exchange.upper() if exchange and isinstance(exchange, str) else None


        submitted = st.form_submit_button("Submit Bet")
        required_fields = [
            bookmaker, event, bet_type, back_stake, back_odds, lay_odds
        ]
        if back_stake is not None and back_odds is not None and lay_odds is not None:
            back_cms = back_cms / 100.0
            lay_cms = lay_cms / 100.0
            matched_bet = BetInputCalculator(
                back_stake=back_stake, 
                back_odds=back_odds, 
                back_cms=back_cms,
                lay_odds=lay_odds, 
                lay_cms=lay_cms,
                free_bet=is_bet_free,
                free_sr=free_sr,
                free_bet_val=cashback,
                mbibl=mbibl
            )
            lay_stake = matched_bet.get_required_lay_stake()
            lay_stake = round(lay_stake, 2)
            st.success(f"Required Lay Stake £{lay_stake}")

        if submitted:
            if any(x in (None, "", np.nan) for x in required_fields):
                st.error("Please fill in all required fields")
            else:
                st.success("Bet submitted!")


    st.subheader("📋 Your Previous Bets")
