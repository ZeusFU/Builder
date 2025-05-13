import streamlit as st

# Base one-time price mapping for static drawdown levels (in USD)
# These values come from our reviewed calculator screenshots.
base_price_map = {
    1500: 399,
    1750: 429,
    2000: 449,
    2250: 479,
    2500: 499,
    2750: 529,
    3000: 549,
    3250: 689,
    3500: 719,
    5000: 499,  # pricing out of promotional tiers
    5250: 529,
    5500: 969,
    5750: 989,
    6000: 1009
}

st.title("Plan Builder Calculator 🚀")
st.sidebar.header("Configure Your Plan")

# 1) Drawdown selection
drawdown = st.sidebar.select_slider(
    "Static Drawdown (max loss) 🌊",
    options=sorted(base_price_map.keys()),
    value=3000,
    help="Your maximum allowed drawdown; determines base price, profit goal, and daily loss limit."
)

# Calculate derived goals
profit_goal = drawdown * 2
daily_loss_limit = drawdown * 0.4

daily_goal = daily_loss_limit  # daily profit target = daily loss limit

# 2) Contracts slider (minis ↔ micros)
minis = st.sidebar.slider(
    "Contracts (minis) 🤏",
    min_value=6,
    max_value=12,
    value=7,
    help="Number of mini contracts (each mini = 10 micro); +$10 one-time per mini above or below 7."
)
micros = minis * 10

# 3) Data feed surcharge
rhythmic_feed = st.sidebar.checkbox(
    "Rhythmic Data Feed (+$20) 📊",
    help="Adds $20 one-time for the rhythmic market data feed."
)

# 4) Calculate prices
base_price = base_price_map.get(drawdown)
if base_price is None:
    st.error("Drawdown level not supported: please choose a valid drawdown option.")
    st.stop()

# One-time cost = base + contract addon + feed surcharge
contract_addon = (minis - 7) * 10
one_time_cost = base_price + contract_addon + (20 if rhythmic_feed else 0)

# Recurring details (constant)
monthly_extension_fee = 29  # $29/month for extensions
reset_credit = 150         # $150 credit for resets/extensions

# 5) Display summary
st.subheader("Plan Summary 💼")
col1, col2 = st.columns(2)
with col1:
    st.metric("Static Drawdown", f"${drawdown}")
    st.metric("Profit Goal", f"${int(profit_goal)}")
    st.metric("Daily Loss Limit", f"${int(daily_loss_limit)}")
    st.metric("Daily Goal", f"${int(daily_goal)}")
    st.metric("Contracts", f"{minis} mini / {micros} micro")
with col2:
    st.metric("One-Time Cost", f"${one_time_cost}")
    st.metric("Monthly Extension", f"${monthly_extension_fee}/mo")
    st.metric("Resets Credit", f"${reset_credit}")
    if rhythmic_feed:
        st.write("**Includes Rhythmic Data Feed surcharge: $20**")

st.markdown("---")
st.caption("Use the sidebar controls to adjust drawdown, contracts, and data feed options.")
