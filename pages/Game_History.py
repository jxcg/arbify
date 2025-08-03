import streamlit as st
import pandas as pd
from data.engine import MatchedBetCalculator
from data.service import insert_bet, get_all_bets, update_bet_result

def safe_float_from_text(label: str, value: str = "", placeholder: str = "") -> float | None:
    text_val = st.text_input(label, value=value, placeholder=placeholder)
    try:
        if not text_val.strip():
            return None
    except Exception:
        return None
    try:
        return float(text_val)
    except ValueError:
        st.error(f'Invalid input for "{label}". Please enter a valid number.', icon="🚨")
        return None



def compute_row_profit(row):
    try:
        back_stake = float(row.get("Back Stake", 0.0))
        back_odds = float(row.get("Back Odds", 0.0))
        lay_odds = float(row.get("Lay Odds", 0.0))
        lay_cms = 0.02
        bet_type = row.get("Bet Type", "Qualifying Bet")
    except (ValueError, TypeError):
        return 0.0

    is_free_bet = "Free Bet" in bet_type

    calculator = MatchedBetCalculator(
        back_stake=back_stake if not is_free_bet else 0.0,
        back_odds=back_odds,
        back_cms=0.0,
        lay_odds=lay_odds,
        lay_cms=lay_cms,
        free_sr=False,  # Assuming stake not returned for free bets in history
        free_bet=is_free_bet,
        free_bet_val=back_stake if is_free_bet else 0.0
    )

    result = row["Result"]
    profits = calculator.get_bookie_exchange_breakdown()

    if result == "back":
        return profits['back_wins']['total']
    elif result == "lay":
        return profits['lay_wins']['total']
    elif result == "void":
        return 0.0
    else:
        return 0.0



def run():
    st.set_page_config(layout="wide")
    st.title("Game History & Bet Calculator")

    # Bet Calculator
    st.subheader("📊 Matched Betting Calculator")
    bet_type_options = ["Qualifying Bet", "Free Bet", "Money Back if Bet Loses"]
    choice = st.radio(label='Select Bet Type', options=bet_type_options)
    
    is_bet_free = choice == "Free Bet"
    free_sr = False
    mbibl = choice == "Money Back if Bet Loses"
    
    if is_bet_free:
        free_sr = st.checkbox(label='Stake returned on free bet')
    
    details_container = st.container(border=True)
    back_container = st.container(border=True)
    lay_container = st.container(border=True)
    
    with details_container:
        st.subheader("Bet Details")
        bookmaker = st.text_input("Bookmaker", placeholder="e.g., Bet365")
        exchange = st.text_input("Exchange", placeholder="e.g., Smarkets")
        event = st.text_input("Event", placeholder="e.g., Man Utd vs Chelsea")

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
            lay_percent = safe_float_from_text('Exchange Commission (%)', value='2', placeholder='e.g. 2')
    
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
            
            lay_stake = matched_bet.get_required_lay_stake()
            liability = matched_bet.get_lay_liability(lay_stake)
            profits = matched_bet.get_bookie_exchange_breakdown()
            
            col1, col2 = st.columns(2)
            with col1:
                st.success(f"Required Lay Stake: £{lay_stake:.2f}")
            with col2:
                value = profits['back_wins']['total']
                label = "Profit"
                if value > 0:
                    st.success(f"{label}: £{value:.2f}")
                else:
                    st.error(f"{label}: £{value:.2f}")

            if st.button("Save Bet"):
                bet_object = {
                    "bookmaker": bookmaker,
                    "exchange": exchange,
                    "event": event,
                    "bet_type": choice,
                    "back_stake": back_stake,
                    "back_odds": back_odds,
                    "lay_odds": lay_odds,
                    "lay_stake": lay_stake,
                    "lay_liability": liability,
                    "bookmaker_profit_loss": profits['back_wins']['bookie_pl'],
                    "exchange_profit_loss": profits['back_wins']['exchange_pl'],
                    "notes": ""
                }
                if insert_bet(bet_object):
                    st.success("Bet saved successfully!")
                    st.rerun()
                else:
                    st.error("Failed to save bet.")

        except ValueError as e:
            st.error(str(e), icon="🚨")

    # Game History
    st.subheader("📋 Your Previous Bets")
    try:
        bets_data = get_all_bets()
        if bets_data:
            columns = [
                "id", "bet_date", "bookmaker", "event", "bet_type", "back_stake",
                "back_odds", "exchange", "lay_odds", "lay_stake", "lay_liability",
                "bookmaker_profit_loss", "exchange_profit_loss", "net_profit_loss",
                "result", "notes"
            ]
            df = pd.DataFrame(bets_data, columns=columns)
            df = df.rename(columns={
                "bet_date": "Date",
                "bookmaker": "Bookmaker",
                "event": "Event",
                "bet_type": "Bet Type",
                "back_stake": "Back Stake",
                "back_odds": "Back Odds",
                "exchange": "Exchange",
                "lay_odds": "Lay Odds",
                "lay_stake": "Lay Stake",
                "lay_liability": "Liability",
                "bookmaker_profit_loss": "Bookmaker P/L",
                "exchange_profit_loss": "Exchange P/L",
                "net_profit_loss": "Net Profit",
                "result": "Result",
                "notes": "Notes"
            })
            for col in ["Bookmaker P/L", "Exchange P/L", "Net Profit"]:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            original_df = df.copy()
            st.info("You can edit the 'Result' column directly in the table below.")
            edited_df = st.data_editor(
                df,
                column_config={
                    "Result": st.column_config.SelectboxColumn(
                        "Result",
                        help="Set the result of the bet",
                        options=["unsettled", "back", "lay", "void"],
                        required=True,
                    ),
                    "id": None
                },
                disabled=[
                    "id", "Bookmaker", "Event", "Bet Type", "Back Stake", "Back Odds",
                    "Exchange", "Lay Odds", "Lay Stake", "Liability",
                    "Bookmaker P/L", "Exchange P/L", "Net Profit",
                    "Date", "Notes"
                ],
                hide_index=True,
                use_container_width=True,
            )
            edited_df["Calculated Profit"] = edited_df.apply(compute_row_profit, axis=1)
            total_profit = edited_df["Calculated Profit"].sum()
            profit_color = "green" if total_profit >= 0 else "red"
            st.markdown(
                f"### 💰 Total Profit: <span style='color:{profit_color}'>£{total_profit:.2f}</span>",
                unsafe_allow_html=True
            )
            if not original_df.equals(edited_df):
                changes = original_df["Result"] != edited_df["Result"]
                if changes.any():
                    changed_rows = edited_df[changes]
                    for index, row in changed_rows.iterrows():
                        bet_id = int(original_df.iloc[index]["id"])
                        new_result = row["Result"]
                        success = update_bet_result(bet_id, new_result)
                        if success:
                            st.success(f"✅ Updated result for Bet ID {bet_id} to '{new_result}'")
                            st.rerun()
                        else:
                            st.error(f"❌ Failed to update result for Bet ID {bet_id}")
        else:
            st.info("No bets found in your history.")
    except Exception as e:
        st.error(f"Could not load bet history: {e}")