import streamlit as st
import requests

# Set page layout and title
st.set_page_config(page_title="Regional Express Rates", page_icon="🚖", layout="centered")

# Custom CSS for polished mobile styling
st.markdown("""
    <style>
    /* Compact top padding for mobile */
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    
    /* Card container styling */
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column"] {
        background-color: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
    }
    
    /* High contrast price metrics */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Live exchange rate fetcher
@st.cache_data(ttl=3600)
def get_cad_to_usd_rate():
    try:
        url = "https://api.frankfurter.dev/v1/latest?base=CAD&symbols=USD"
        res = requests.get(url, timeout=4)
        if res.status_code == 200:
            return res.json()["rates"]["USD"], True
    except Exception:
        pass
    return 0.73, False

cad_to_usd, is_live = get_cad_to_usd_rate()

# Header & Status
st.title("🚖 Transport Quote")
status_badge = f"🟢 Live Exchange: 1 CAD = ${cad_to_usd:.4f} USD" if is_live else f"🟡 Offline Rate: 1 CAD = ${cad_to_usd:.4f} USD"
st.caption(status_badge)

# Locations setup
ORIGINS = ["NIAGARA FALLS", "NIAGARA ON THE LAKE", "WELLAND"]
DESTINATIONS = [
    "TORONTO AIRPORT",
    "DOWNTOWN TORONTO",
    "BUFFALO AIRPORT",
    "HAMILTON AIRPORT",
    "NIAGARA FALLS",
    "NIAGARA ON THE LAKE",
    "WELLAND"
]

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

# Input Section Card
with st.container(border=True):
    st.subheader("📍 Trip Details")
    origin = st.selectbox("Pickup (From)", ORIGINS, index=0)
    
    # Filter destinations to prevent picking the same location as origin
    valid_destinations = [loc for loc in DESTINATIONS if loc != origin]
    destination = st.selectbox("Dropoff (To)", valid_destinations, index=0)
    
    passengers = st.number_input("Passengers", min_value=1, max_value=14, value=1, step=1)
    
    if passengers > 4:
        st.caption("🚐 **XL Passenger Van required** (35% group surcharge applied)")
    else:
        st.caption("🚗 **Standard Sedan / SUV vehicle**")

# Calculation Logic
base_cad = RATES_CAD.get((origin, destination)) or RATES_CAD.get((destination, origin), 150.00)
surcharge = base_cad * 0.35 if passengers > 4 else 0.0

total_cad = base_cad + surcharge
total_usd = total_cad * cad_to_usd

# Results Display Card
st.markdown("### 💰 Estimated Rate")

with st.container(border=True):
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(label="CAD Total", value=f"${total_cad:.2f}")
    with col2:
        st.metric(label="USD Total", value=f"${total_usd:.2f}")

    st.markdown("---")
    st.caption(f"**Route:** {origin} ➔ {destination}")
    if surcharge > 0:
        st.caption(f"Base: ${base_cad:.2f} CAD | Van Surcharge: +${surcharge:.2f} CAD")
