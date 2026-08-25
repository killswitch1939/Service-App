import streamlit as st
import requests

st.set_page_config(page_title="Transport Rates", page_icon="🚖", layout="centered")

# Helper function to fetch live exchange rate (cached for 1 hour to keep the app fast)
@st.cache_data(ttl=3600)
def get_cad_to_usd_rate():
    try:
        url = "https://api.frankfurter.dev/v1/latest?base=CAD&symbols=USD"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data["rates"]["USD"], True
    except Exception:
        pass
    # Fallback exchange rate if offline or request fails
    return 0.73, False

# Fetch rate
cad_to_usd_rate, is_live = get_cad_to_usd_rate()

st.title("🚖 Regional Rate Calculator")

# Display exchange rate status in sidebar or header
if is_live:
    st.caption(f"🌐 Live Exchange Rate: 1 CAD = ${cad_to_usd_rate:.4f} USD")
else:
    st.caption(f"⚠️ Offline Rate Used: 1 CAD = ${cad_to_usd_rate:.4f} USD")

# Locations
ORIGINS = ["NIAGARA FALLS", "NIAGARA ON THE LAKE", "WELLAND"]
ALL_LOCATIONS = [
    "NIAGARA FALLS",
    "TORONTO AIRPORT",
    "DOWNTOWN TORONTO",
    "BUFFALO AIRPORT",
    "HAMILTON AIRPORT",
    "NIAGARA ON THE LAKE",
    "WELLAND"
]

# Base rates in Canadian Dollars (CAD)
RATES_CAD = {
    ("NIAGARA FALLS", "TORONTO AIRPORT"): 195.00,
    ("NIAGARA FALLS", "DOWNTOWN TORONTO"): 215.00,
    ("NIAGARA FALLS", "BUFFALO AIRPORT"): 110.00,
    ("NIAGARA FALLS", "HAMILTON AIRPORT"): 135.00,
    ("NIAGARA FALLS", "NIAGARA ON THE LAKE"): 45.00,
    ("NIAGARA FALLS", "WELLAND"): 40.00,

    ("NIAGARA ON THE LAKE", "TORONTO AIRPORT"): 190.00,
    ("NIAGARA ON THE LAKE", "DOWNTOWN TORONTO"): 210.00,
    ("NIAGARA ON THE LAKE", "BUFFALO AIRPORT"): 120.00,
    ("NIAGARA ON THE LAKE", "HAMILTON AIRPORT"): 140.00,
    ("NIAGARA ON THE LAKE", "WELLAND"): 50.00,

    ("WELLAND", "TORONTO AIRPORT"): 195.00,
    ("WELLAND", "DOWNTOWN TORONTO"): 210.00,
    ("WELLAND", "BUFFALO AIRPORT"): 115.00,
    ("WELLAND", "HAMILTON AIRPORT"): 125.00,
}

# Inputs
origin = st.selectbox("From (Origin)", ORIGINS)
destination = st.selectbox("To (Destination)", ALL_LOCATIONS)
passengers = st.number_input("Number of Passengers", min_value=1, value=1, step=1)

if origin == destination:
    st.error("Origin and Destination cannot be the same location.")
else:
    # Look up CAD rate
    base_cad = RATES_CAD.get((origin, destination)) or RATES_CAD.get((destination, origin), 150.00)

    # Apply 35% Van Surcharge if passenger count exceeds 4
    surcharge_cad = base_cad * 0.35 if passengers > 4 else 0.0

    # Total calculations
    total_cad = base_cad + surcharge_cad
    total_usd = total_cad * cad_to_usd_rate

    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Total Rate (CAD)", value=f"${total_cad:.2f} CAD")
    with col2:
        st.metric(label="Total Rate (USD)", value=f"${total_usd:.2f} USD")

    if passengers > 4:
        st.info("Includes 35% Van Surcharge for groups larger than 4.")
