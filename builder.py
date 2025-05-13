import streamlit as st

# ---- Helper functions ----

def compute_base_price(drawdown: int) -> float:
    """
    Piecewise base one-time price based on static drawdown:
    - Up to $2,250: 0.10*drawdown + 249
    - $2,250 to $3,000: +$75 upgrade
    - Above $3,000: 0.34*drawdown - 471
    """
    if drawdown < 2250:
        return 0.10 * drawdown + 249
    elif drawdown < 3000:
        return 0.10 * drawdown + 249 + 75
    else:
        return 0.34 * drawdown - 471


def compute_contract_addon(minis: int) -> float:
    """
    Each extra mini (10 micros) adds $10 to price, relative to 1 mini base.
    """
    return (minis - 1) * 10


def compute_days_adjustment(days: int) -> float:
    """
    Decreasing minimum days (from baseline 12) alternately adds $10, $20 per day removed.
    Pattern: 12->11: +10, 11->10: +20, 10->9: +10, etc.
    """
    pattern = [10, 20] * 4  # enough for up to 8 days reduction
    steps = max(0, 12 - days)
    return sum(pattern[:steps])


def compute_rhythmic_surcharge(is_rhythmic: bool) -> float:
    """
    Rhythmic data feed adds flat $20.
    """
    return 20 if is_rhythmic else 0


def compute_split_payment(one_time: float, drawdown: int) -> tuple[float, float]:
    """
    Split payment: deposit = 6.4% of drawdown, rounded to nearest dollar.
    Balance after passing = one_time - deposit
    """
    deposit = round(0.064 * drawdown)
    balance = one_time - deposit
    return deposit, balance


# ---- Streamlit UI ----
st.set_page_config(page_title="Plan Builder Calculator", layout="centered")
st.title("📊 Plan Builder Pricing Simulator")

st.sidebar.header("⚙️ Configure Plan")

# Static drawdown selection
drawdown = st.sidebar.slider(
    "Static Drawdown (Max Loss)",
    min_value=1000,
    max_value=6000,
    step=250,
    value=3000,
    help="Your maximum allowed drawdown; major driver of pricing steps."
)

# Contract selection
minis = st.sidebar.slider(
    "Contracts (Minis)",
    min_value=1,
    max_value=12,
    value=1,
    help="Number of mini contracts (each mini = 10 micro); +$10 per extra mini."
)

# Minimum days selection
days = st.sidebar.slider(
    "Minimum Trading Days",
    min_value=5,
    max_value=12,
    value=12,
    help="Minimum number of trading days required; reducing days adds cost (+$10/$20 alternation)."
)

# Data feed option
rhythmic_feed = st.sidebar.checkbox(
    "Rhythmic Data Feed (+$20)",
    value=False,
    help="Toggle for Rhythmic market data feed surcharge."
)

# Split payment option
split_pay = st.sidebar.checkbox(
    "Split Payment (Pay after passing)",
    value=False,
    help="Enable to pay a deposit now (6.4% of drawdown) and the remainder after passing."
)

# ---- Calculations ----
base_price = compute_base_price(drawdown)
contract_addon = compute_contract_addon(minis)
days_add = compute_days_adjustment(days)
rhythm_surcharge = compute_rhythmic_surcharge(rhythmic_feed)
one_time_price = base_price + contract_addon + days_add + rhythm_surcharge

deposit = balance = None
if split_pay:
    deposit, balance = compute_split_payment(one_time_price, drawdown)

# ---- Display ----
st.header("💡 Price Breakdown")

st.markdown(
    f"**Base Price** (from drawdown): ${base_price:,.2f}\n"
    f"**Contract Add-on** ({minis} mini): ${contract_addon:.2f}\n"
    f"**Days Adjustment** ({days} days): +${days_add:.2f}\n"
    f"**Data Feed** (Rhythmic): +${rhythm_surcharge:.2f}\n"
    "---"
)

if split_pay:
    st.metric("Deposit Up-Front", f"${deposit}")
    st.metric("Balance on Pass", f"${balance}")
else:
    st.metric("One-Time Up-Front Price", f"${one_time_price:,.2f}")

st.caption("Adjust the controls in the sidebar to see real-time price changes.")
