import streamlit as st

# Page setup for mobile screens
st.set_page_config(page_title="Transport Rates", page_icon="🚖", layout="centered")

st.title("🚖 Regional Rate Calculator")

# Location lists
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

RATES = {
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

CAD_TO_USD = 0.72

# Mobile Dropdown Inputs
origin = st.selectbox("From (Origin)", ORIGINS)
destination = st.selectbox("To (Destination)", ALL_LOCATIONS)
passengers = st.number_input("Number of Passengers", min_value=1, value=1, step=1)

if origin == destination:
    st.error("Origin and Destination cannot be the same location.")
else:
    # Calculation
    base_rate = RATES.get((origin, destination)) or RATES.get((destination, origin), 150.00)
    xl_surcharge = base_rate * 0.35 if passengers > 4 else 0.0
    
    total_cad = base_rate + xl_surcharge
    total_usd = total_cad * CAD_TO_USD

    st.markdown("---")
    
    # Display Results in neat cards
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Total Rate (CAD)", value=f"${total_cad:.2f} CAD")
    with col2:
        st.metric(label="Total Rate (USD)", value=f"${total_usd:.2f} USD")

    if xl_surcharge > 0:
        st.info("Includes 35% Van Surcharge for groups larger than 4.")
