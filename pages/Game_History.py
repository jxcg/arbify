import streamlit as st
import pandas as pd
import numpy as np
from data.engine import MatchedBetCalculator
from data.service import insert_bet, get_all_bets, update_bet_result
from datetime import datetime

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
    result = row["Result"]
    if result == "back":
        return row["Bookie P/L"]
    elif result == "lay":
        return row["Exchange P/L"]
    elif result == "void":
        return 0.0
    else:  # unsettled or anything else
        return 0.0



def run():
    st.set_page_config(layout="wide")
    st.title("Game History")

    bet_object = None
    is_bet_free = False
    free_sr = False
    mbibl = False

    back_stake = None
    back_cms = 0.0
    back_odds = None
    lay_odds = None
    lay_cms = 0.0

    with st.form("bet_form"):
        col1, col2 = st.columns(2)
        with col1:
            back_stake = safe_float_from_text("Back Stake*")
            back_odds = safe_float_from_text("Back Odds*")
            lay_odds = safe_float_from_text("Lay Odds*")
            back_cms = safe_float_from_text("Back Commission (%)", value="0")
            lay_cms = safe_float_from_text("Lay Commission (%)", value="2")

        with col2:
            bookmaker = st.text_input("Bookmaker*", max_chars=100)
            bookmaker = bookmaker.upper() if bookmaker and isinstance(bookmaker, str) else None
            event = st.text_input("Event*")
            bet_type = st.selectbox("Bet Type*", options=["Qualifying", "Free", "Money Back if Bet Loses"])
            exchange = st.text_input("Exchange (optional)", max_chars=100)
            exchange = exchange.upper() if exchange and isinstance(exchange, str) else None
            notes = st.text_input(label='Add bet specific notes', value='Note')

        submitted = st.form_submit_button("Submit Bet")
        required_fields = [bookmaker, event, bet_type, back_stake, back_odds, lay_odds]

        if back_stake is not None and back_odds is not None and lay_odds is not None:
            back_cms = back_cms / 100.0
            lay_cms = lay_cms / 100.0
            matched_bet = MatchedBetCalculator(
                back_stake=back_stake,
                back_odds=back_odds,
                back_cms=back_cms,
                lay_odds=lay_odds,
                lay_cms=lay_cms,
                free_bet=is_bet_free,
                free_sr=free_sr,
                mbibl=mbibl
            )
            lay_stake = round(matched_bet.get_required_lay_stake(), 2)
            st.success(f"Required Lay Stake £{lay_stake}")
            breakdown = matched_bet.get_bookie_exchange_breakdown()

            bet_object = {
                'bookmaker': bookmaker,
                'event': event,
                'bet_type': bet_type,
                'back_stake': back_stake,
                'back_odds': back_odds,
                'exchange': exchange,
                'lay_odds': lay_odds,
                'lay_stake': lay_stake,
                'lay_liability': matched_bet.get_lay_liability(lay_stake),
                'bookie_pl': breakdown['lay_wins']['bookie_pl'],
                'exchange_pl': breakdown['lay_wins']['exchange_pl'],
                'net_profit': breakdown['lay_wins']['total'],
                'notes': notes,
                'result': 'unsettled'
            }

        if submitted:
            if any(x in (None, "", np.nan) for x in required_fields):
                st.error("Please fill in all required fields")
            else:
                if insert_bet(bet_object):
                    st.success("Bet submitted!")
                    st.rerun()
                else:
                    st.error("Could not insert bet")

        st.subheader("📋 Your Previous Bets")

        try:
            # 1. Fetch all bets from your database function
            bets_data = get_all_bets()

            if bets_data:
                # 2. Define the column names in the correct order
                # This must match the order of columns in your get_all_bets() SELECT statement
                columns = [
                    "id", "Bookie", "Event", "Type", 
                    "B.Odds", "L.Odds", "B.Stake", "L.Stake", 
                    "Bookie P/L", "Exchange P/L",
                    "Date", "Notes", "Liability", "Result"
                ]

                # 3. Create a pandas DataFrame
                df = pd.DataFrame(bets_data, columns=columns)
                
                # Keep a copy of the original DataFrame to detect changes
                original_df = df.copy()

                # 4. Use st.data_editor to display and edit the data
                st.info("You can edit the 'result' column directly in the table below.")
                
                edited_df = st.data_editor(
                    df,
                    # Configure the 'result' column to be a dropdown selectbox
                    column_config={
                        "Result": st.column_config.SelectboxColumn(
                            "Result",
                            help="Set the result of the bet",
                            options=["unsettled", "back", "lay", "void"],
                            required=True,
                        ),
                        # Hide the ID column as users shouldn't edit it
                        "id": None, 
                    },
                    # Disable editing for all other columns
                    disabled=["id", "bookmaker", "event", "bet_type", "back_odds", "lay_odds",
                            "Back Stake", "lay_stake",
                            "bookmaker_profit_loss", "exchange_profit_loss",
                            "bet_date", "notes", "lay_liability"],
                    hide_index=True,
                    use_container_width=True, # Use the full width of the page
                )

                # Apply the computation
                edited_df["Calculated Profit"] = edited_df.apply(compute_row_profit, axis=1)

                # Calculate total profit
                total_profit = edited_df["Calculated Profit"].sum()

                # Display total profit
                profit_color = "green" if total_profit >= 0 else "red"
                st.markdown(f"### 💰 Total Profit: <span style='color:{profit_color}'>£{total_profit:.2f}</span>", unsafe_allow_html=True)
                                

                # 5. Find and process the changes
                # Compare the original DataFrame with the edited one
                changes = (original_df['Result'] != edited_df['Result'])
                if changes.any():
                    # Get the rows where the 'result' was changed
                    changed_rows = edited_df[changes]
                    
                    for index, row in changed_rows.iterrows():
                        bet_id = original_df.iloc[index]['id'] # Get ID from original df
                        new_result = row['Result']
                        
                        # Update the database
                        success = update_bet_result(bet_id, new_result)
                        if success:
                            st.success(f"Updated result for Bet ID {bet_id} to '{new_result}'!")
                        else:
                            st.error(f"Failed to update result for Bet ID {bet_id}.")
                    
                    # Add a button to easily rerun the app and see the persisted change
                    if st.button("Refresh Data"):
                        st.rerun()

            else:
                st.info("No bets found in your history.")

        except Exception as e:
            st.error(f"Could not load bet history: {e}")