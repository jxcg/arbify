import streamlit as st
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
    st.title("Calculator")

    # Function variables
    bet_type_options    = ["Qualifying Bet", "Free Bet", "Money Back if Bet Loses"]
    is_bet_free         = False # Free Bet
    free_sr             = False # Free bet + stake returned
    mbibl               = False

    # Back Bet
    back_stake          = None
    back_cms            = 0.0
    back_odds           = None

    # Lay Bet
    lay_odds            = None
    lay_cms             = 0.0

    # Streamlit styling variables
    choice              = st.radio(label='Select Bet Type', options=bet_type_options)
    if choice == "Free Bet":
        is_bet_free     = True
        free_sr         = st.checkbox(label='Stake returned')
    
    if choice == "Money Back if Bet Loses":
        mbibl = True

    back_container      = st.container(border=True)
    lay_container       = st.container(border=True)
    lay_st_container    = st.container(border=True)


    with back_container:
        st.subheader("Back Bet")
        col_left, col_right = st.columns(2)
        
        with col_left:
            back_stake = safe_float_from_text('Back Stake', value=None, placeholder='i.e., 10 (£)')
            back_percent = safe_float_from_text("Back Commission (%)", value=0, placeholder='i.e., 3%')
            

        with col_right:
            back_odds = safe_float_from_text('Back Odds', value=None, placeholder='i.e., 3.5')
            cashback = safe_float_from_text('Cashback', value=None, placeholder='i.e., 10 (£)') if mbibl else None

    with lay_container:
        st.subheader("Lay Bet")
        col_left, col_right = st.columns(2)
        
        with col_left:
            lay_odds = safe_float_from_text('Lay Odds', placeholder='i.e., 3.6')

        with col_right:
            lay_percent = safe_float_from_text("Lay Commission (%)", value=2.0, placeholder='i.e., 3%')

    # - Require validation here
    if back_stake is not None and back_odds is not None and lay_odds is not None:
        back_cms = back_percent / 100.0
        lay_cms = lay_percent / 100.0
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




