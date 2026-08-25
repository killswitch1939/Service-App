import streamlit as st

st.set_page_config(page_title="Transport Rates", page_icon="🚖", layout="centered")

st.title("🚖 Regional Rate Calculator")

# Restricted origins
ORIGINS = ["NIAGARA FALLS", "NIAGARA ON THE LAKE", "WELLAND"]

# Destination options
ALL_LOCATIONS = [
    "NIAGARA FALLS",
    "TORONTO AIRPORT",
    "DOWNTOWN TORONTO",
    "BUFFALO AIRPORT",
    "HAMILTON AIRPORT",
    "NIAGARA ON THE LAKE",
    "WELLAND"
]

# Fixed rates in Canadian Dollars (CAD)
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

# Fixed independent rates in US Dollars (USD)
RATES_USD = {
    ("NIAGARA FALLS", "TORONTO AIRPORT"): 150.00,
    ("NIAGARA FALLS", "DOWNTOWN TORONTO"): 165.00,
    ("NIAGARA FALLS", "BUFFALO AIRPORT"): 85.00,
    ("NIAGARA FALLS", "HAMILTON AIRPORT"): 105.00,
    ("NIAGARA FALLS", "NIAGARA ON THE LAKE"): 35.00,
    ("NIAGARA FALLS", "WELLAND"): 30.00,

    ("NIAGARA ON THE LAKE", "TORONTO AIRPORT"): 145.00,
    ("NIAGARA ON THE LAKE", "DOWNTOWN TORONTO"): 160.00,
    ("NIAGARA ON THE LAKE", "BUFFALO AIRPORT"): 95.00,
    ("NIAGARA ON THE LAKE", "HAMILTON AIRPORT"): 110.00,
    ("NIAGARA ON THE LAKE", "WELLAND"): 40.00,

    ("WELLAND", "TORONTO AIRPORT"): 150.00,
    ("WELLAND", "DOWNTOWN TORONTO"): 160.00,
    ("WELLAND", "BUFFALO AIRPORT"): 90.00,
    ("WELLAND", "HAMILTON AIRPORT"): 100.00,
}

# Inputs
origin = st.selectbox("From (Origin)", ORIGINS)
destination = st.selectbox("To (Destination)", ALL_LOCATIONS)
passengers = st.number_input("Number of Passengers", min_value=1, value=1, step=1)

if origin == destination:
    st.error("Origin and Destination cannot be the same location.")
else:
    # Look up base rates for CAD and USD independently
    base_cad = RATES_CAD.get((origin, destination)) or RATES_CAD.get((destination, origin), 150.00)
    base_usd = RATES_USD.get((origin, destination)) or RATES_USD.get((destination, origin), 115.00)

    # 35% Large vehicle surcharge applied to both currency bases if passengers > 4
    surcharge_cad = base_cad * 0.35 if passengers > 4 else 0.0
    surcharge_usd = base_usd * 0.35 if passengers > 4 else 0.0

    total_cad = base_cad + surcharge_cad
    total_usd = base_usd + surcharge_usd

    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Total Rate (CAD)", value=f"${total_cad:.2f} CAD")
    with col2:
        st.metric(label="Total Rate (USD)", value=f"${total_usd:.2f} USD")

    if passengers > 4:
        st.info("Includes 35% Van Surcharge for groups larger than 4.")
