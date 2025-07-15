import streamlit as st
from data.engine import MatchedBetCalculator

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
    st.title("Matched Betting Calculator")
    
    # Select bet type
    bet_type_options = ["Qualifying Bet", "Free Bet", "Money Back if Bet Loses"]
    choice = st.radio(label='Select Bet Type', options=bet_type_options)
    
    is_bet_free = choice == "Free Bet"
    free_sr = False
    mbibl = choice == "Money Back if Bet Loses"
    
    if is_bet_free:
        free_sr = st.checkbox(label='Stake returned on free bet')
    
    # Input containers
    back_container = st.container(border=True)
    lay_container = st.container(border=True)
    
    with back_container:
        st.subheader("Back Bet")
        col_left, col_right = st.columns(2)
        with col_left:
            if is_bet_free:
                back_stake = safe_float_from_text('Free Bet Value (£)', placeholder='e.g. 10.0')
            else:
                back_stake = safe_float_from_text('Back Stake', placeholder='e.g. 10.0')
            back_percent = safe_float_from_text('Bookmaker Commission (%)', value='0', placeholder='e.g. 5')
        with col_right:
            back_odds = safe_float_from_text('Back Odds', placeholder='e.g. 3.5')
    
    with lay_container:
        st.subheader("Lay Bet")
        col_left, col_right = st.columns(2)
        with col_left:
            lay_odds = safe_float_from_text('Lay Odds', placeholder='e.g. 3.6')
        with col_right:
            lay_percent = safe_float_from_text('Exchange Commission (%)', value='0', placeholder='e.g. 2')
    
    # Validate required fields
    if None not in (back_stake, back_odds, lay_odds, back_percent, lay_percent):
        back_cms = back_percent / 100.0
        lay_cms = lay_percent / 100.0
        
        try:
            matched_bet = MatchedBetCalculator(
                back_stake=back_stake if not is_bet_free else 0.0,
                back_odds=back_odds,
                back_cms=back_cms,
                lay_odds=lay_odds,
                lay_cms=lay_cms,
                free_bet=is_bet_free,
                free_sr=free_sr,
                free_bet_val=back_stake if is_bet_free else 0.0,
                mbibl=mbibl
            )
            
            # Compute outputs
            lay_stake = matched_bet.get_required_lay_stake()
            liability = matched_bet.get_lay_liability(lay_stake)
            profits = matched_bet.get_total_profit()
            
            col1, col2 = st.columns(2)
            with col1:
                st.success(f"Required Lay Stake: £{lay_stake:.2f}")
            with col2:
                value = profits['back_wins']
                label = "Profit"
                if value > 0:
                    st.success(f"{label}: £{value:.2f}")
                else:
                    st.error(f"{label}: £{value:.2f}")


        except ValueError as e:
            st.error(str(e), icon="🚨")