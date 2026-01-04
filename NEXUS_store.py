import streamlit as st
import pandas as pd
import json
from datetime import datetime

# --- CONFIG & STYLING ---
st.set_page_config(page_title="Nexus Data Marketplace", page_icon="📈", layout="wide")

# Custom CSS for the "Marketplace" feel
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; background-color: #0070ba; color: white; font-weight: bold; }
    .product-box { border: 1px solid #444; padding: 20px; border-radius: 15px; background-color: #1e2630; margin-bottom: 15px; }
    .price { font-size: 22px; color: #2ecc71; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. DYNAMIC DATASET CATALOG ---
# In a full version, this would be saved in a database (SQL or JSON file)
if 'my_datasets' not in st.session_state:
    st.session_state.my_datasets = [
        {
            "id": "DS-001",
            "name": "Bipedal Robot Failures (PH-Edition)",
            "category": "Robotics",
            "price": 250.00,
            "currency": "USD",
            "description": "High-fidelity sensor logs for humanoid bipedal units. Includes critical failure edge cases.",
            "file_type": "Parquet"
        }
    ]

# --- 2. ADMIN PANEL (ADD DATASETS) ---
with st.sidebar:
    st.header("👑 Admin Panel")
    with st.expander("➕ Add New Dataset for Sale"):
        new_name = st.text_input("Dataset Name")
        new_cat = st.selectbox("Category", ["Robotics", "LLM Training", "IoT", "Green Energy"])
        new_price = st.number_input("Price (USD)", min_value=1.0)
        new_desc = st.text_area("Description")

        if st.button("List for Sale"):
            new_entry = {
                "id": f"DS-00{len(st.session_state.my_datasets) + 1}",
                "name": new_name,
                "category": new_cat,
                "price": new_price,
                "currency": "USD",
                "description": new_desc,
                "file_type": "JSONL / Parquet"
            }
            st.session_state.my_datasets.append(new_entry)
            st.success("Dataset successfully listed!")

# --- 3. STOREFRONT LAYOUT ---
st.title("Nexus Synthetic Marketplace 🇵🇭")
st.markdown("### Premier Synthetic Data Provider for Global AI Training")

# Filter
category_filter = st.selectbox("Filter by Sector",
                               ["All"] + list(set(d['category'] for d in st.session_state.my_datasets)))

cols = st.columns(2)
for idx, dataset in enumerate(st.session_state.my_datasets):
    if category_filter == "All" or category_filter == dataset['category']:
        with cols[idx % 2]:
            st.markdown(f"""
                <div class="product-box">
                    <h3>{dataset['name']}</h3>
                    <p><b>Sector:</b> {dataset['category']} | <b>Format:</b> {dataset['file_type']}</p>
                    <p>{dataset['description']}</p>
                    <p class="price">${dataset['price']:.2f} {dataset['currency']}</p>
                </div>
            """, unsafe_allow_html=True)

            # --- 4. PAYPAL PAYMENT INTEGRATION ---
            # Using the 'PayPal Buttons' strategy (Safest for Streamlit 2026)
            paypal_link = f"https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business=YOUR_EMAIL@GMAIL.COM&item_name={dataset['name']}&amount={dataset['price']}&currency_code=USD"

            st.markdown(f"""
                <a href="{paypal_link}" target="_blank">
                    <button style="width:100%; cursor:pointer; background-color:#ffc439; color:#000; border:none; padding:10px; border-radius:20px; font-weight:bold;">
                        Pay with PayPal
                    </button>
                </a>
            """, unsafe_allow_html=True)
            st.write(" ")  # Padding

# --- 5. MY DOWNLOADS SECTION ---
st.divider()
st.subheader("📥 Post-Purchase Download")
st.info(
    "After payment, your unique download link will be sent to your PayPal email. Enter your Transaction ID below to verify.")
trans_id = st.text_input("Enter Transaction ID to Download")
if trans_id:
    st.button("Verify & Download Dataset")