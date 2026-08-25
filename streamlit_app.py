import streamlit as st
import requests

# Page setup
st.set_page_config(page_title="Niagara Airlink Quotes", page_icon="🚖", layout="centered")

# Custom CSS for Dark Theme & Receipt Formatting
st.markdown("""
    <style>
    /* Dark Theme Background Setup */
    .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }

    /* Reduce default top padding */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }

    /* Card container styling */
    div[data-testid="stVerticalBlock"] > div[data-testid="stBlock"] {
        background-color: #121212 !important;
        border: 1px solid #262626 !important;
        border-radius: 12px;
    }

    /* Side-by-Side Rate Card Layout */
    .rate-container {
        display: flex;
        flex-direction: row;
        gap: 12px;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    
    .rate-card {
        flex: 1;
        background-color: #1a1a1a;
        border: 1px solid #333333;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }

    .rate-label {
        font-size: 0.85rem;
        color: #aaaaaa;
        font-weight: 600;
        margin-bottom: 4px;
    }

    .rate-value {
        font-size: 1.6rem;
        color: #ffffff;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# Fetch exchange rate
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
    
    valid_destinations = [loc for loc in DESTINATIONS if loc != origin]
    destination = st.selectbox("Dropoff (To)", valid_destinations, index=0)
    
    passengers = st.number_input("Passengers", min_value=1, max_value=14, value=1, step=1)
    
    if passengers > 4:
        st.caption("🚐 **XL Passenger Van required** (35% group surcharge applied)")
    else:
        st.caption("🚗 **Standard Sedan / SUV vehicle**")

# Calculation
base_cad = RATES_CAD.get((origin, destination)) or RATES_CAD.get((destination, origin), 150.00)
surcharge = base_cad * 0.35 if passengers > 4 else 0.0

total_cad = base_cad + surcharge
total_usd = total_cad * cad_to_usd

# Rate Display Card
st.markdown("### 💰 Estimated Rate")

st.markdown(f"""
    <div class="rate-container">
        <div class="rate-card">
            <div class="rate-label">TOTAL (CAD)</div>
            <div class="rate-value">${total_cad:.2f}</div>
        </div>
        <div class="rate-card">
            <div class="rate-label">TOTAL (USD)</div>
            <div class="rate-value">${total_usd:.2f}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Format Route Names Nicely (e.g. "NIAGARA FALLS" -> "Niagara Falls")
origin_formatted = origin.title()
destination_formatted = destination.title()

# Generate Confirmation Email / Receipt Template
receipt_template = f"""Hello [Customer Name],

Thank you for contacting Niagara Airlink.

We currently have availability for your requested transfer:

Pick-up Location : {origin_formatted}
Drop-off Location : {destination_formatted} 

Number of Guests: {passengers}
Date: [Date, e.g. September 12th 2026]
Time: [Time, e.g. 4:30 am]

The price for the service is {total_cad:.2f} canadian dollars.

We will require your flight details for pickup.

Once you confirm the details, we’ll send a secure payment link. Upon receiving your payment, your reservation will be confirmed.

We look forward to hearing from you soon.

Best regards,
[Your Name]
Niagara Airlink 
905-357-8368"""

# Receipt Card Section
st.markdown("### ✉️ Client Confirmation Email")
with st.container(border=True):
    st.text_area(
        label="Copy & Edit Receipt Template:",
        value=receipt_template,
        height=380,
        help="You can quickly change [Customer Name], [Date], [Time], or [Your Name] right here before copying."
    )

    st.caption("💡 Tap inside the text box above to edit customer details or copy the entire receipt directly.")
