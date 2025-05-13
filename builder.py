import streamlit as st

# Streamlit app: Plan Builder Pricing Simulator
st.set_page_config(page_title="Plan Builder", layout="wide")

# ─── Sidebar ────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Configure Plan")

    drawdown = st.slider(
        label="Static Drawdown (Max Loss)",
        min_value=1000, max_value=6000, value=1000, step=500,
        help="Your total allowable drawdown. Governs base price & rules."
    )

    contracts = st.slider(
        label="Contracts (Minis)",
        min_value=1, max_value=12, value=1, step=1,
        help="Number of mini contracts. Each additional mini adds $10."
    )

    days = st.slider(
        label="Minimum Trading Days",
        min_value=5, max_value=12, value=12, step=1,
        help="Your required trading days. Fewer days → higher surcharge."
    )

    rhythmic = st.checkbox(
        label="Rhythmic Data Feed (+$20)",
        help="Add our premium real-time data feed for $20 extra."
    )

    split = st.checkbox(
        label="Split Payment (64% now, remainder on passing)",
        help="Pay 64% up front, then pay the rest after you pass."
    )

# ─── Calculations ───────────────────────────────────────────────────────
# Base price scales linearly from $149 at 1000 to $649 at 6000 drawdown
base_price = 149 + (drawdown - 1000) * (500 / 5000)

# Contracts: $10 per mini above the first
contract_add = (contracts - 1) * 10

# Days surcharge: $15 for each day below 12
days_surcharge = max(0, (12 - days) * 15)

# Data feed surcharge
feed_surcharge = 20 if rhythmic else 0

# Trading rules
profit_target = drawdown * 2
daily_loss_limit = drawdown * 0.4
daily_profit_target = profit_target / days

# Subtotal and split payment
subtotal = base_price + contract_add + days_surcharge + feed_surcharge
if split:
    deposit = subtotal * 0.64
    remainder = subtotal - deposit
else:
    deposit = subtotal
    remainder = 0

# ─── Layout ────────────────────────────────────────────────────────────
col1, col2 = st.columns([2, 1])

with col1:
    st.header("💡 Price & Rules Breakdown")
    st.markdown(f"- **Base Price** (drawdown): ${base_price:,.2f}")
    st.markdown(f"- **Contracts** ({contracts} minis): +${contract_add:,.2f}")
    st.markdown(f"- **Days Surcharge** (12 - {days}): +${days_surcharge:,.2f}")
    if rhythmic:
        st.markdown(f"- **Data Feed**: +${feed_surcharge:,.2f}")
    st.markdown("---")
    st.subheader("🚩 Trading Rules")
    st.markdown(f"- **Profit Target** (2× drawdown): ${profit_target:,.0f}")
    st.markdown(f"- **Daily Loss Limit** (0.4× drawdown): ${daily_loss_limit:,.0f}")
    st.markdown(f"- **Daily Profit Target** (profit/days): ${daily_profit_target:,.0f}")

    if split:
        st.markdown("---")
        st.subheader("💳 Split Payment")
        st.markdown(f"- **Now (64%)**: ${deposit:,.2f}")
        st.markdown(f"- **On Passing**: ${remainder:,.2f}")

with col2:
    st.header("💵 Up-Front Price")
    st.markdown(
        f"<h1 style='text-align:right'>${deposit:,.2f}</h1>",
        unsafe_allow_html=True
    )
    if split:
        st.caption("Remaining balance due after passing")
    else:
        st.caption("Full payment due up-front")
