import streamlit as st
from data.service import get_profit_over_time


def run():
    st.title("📈 Net Profit Over Time")

    stats = get_profit_over_time()

    if stats:
        df = pd.DataFrame(stats, columns=["Date", "Net Profit"])
        df["Date"] = pd.to_datetime(df["Date"])

        st.line_chart(df.set_index("Date"))
    else:
        st.info("No profit data available yet.")