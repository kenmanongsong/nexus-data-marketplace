import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Nexus Data Philippines", page_icon="🇵🇭", layout="wide")

# Custom CSS for E-commerce Look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #1f538d; color: white; }
    .price-tag { font-size: 24px; font-weight: bold; color: #2ecc71; }
    .product-card { border: 1px solid #333; padding: 20px; border-radius: 10px; background-color: #161b22; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE (Your Catalog) ---
products = {
    "ROBO-PH-01": {
        "name": "Humanoid Bipedal Telemetry",
        "category": "Robotics",
        "price": "₱14,500",
        "rows": "1,000,000",
        "format": "Parquet",
        "description": "High-fidelity torque and gyro data for bipedal robots. Includes 5% failure edge cases.",
        "tags": ["IoT", "Robotics", "Anomaly Detection"]
    },
    "LLM-IND-PH": {
        "name": "PH Industrial Instruction Set",
        "category": "LLM Tuning",
        "price": "₱25,000",
        "rows": "50,000 Pairs",
        "format": "JSONL",
        "description": "Chain-of-Thought tuning data for industrial troubleshooting assistants.",
        "tags": ["NLP", "CoT", "Fine-tuning"]
    },
    "GRID-WIND-26": {
        "name": "Renewable Grid Stress Test",
        "category": "Energy",
        "price": "₱18,200",
        "rows": "500,000",
        "format": "Parquet / CSV",
        "description": "Wind turbine telemetry specifically modeled on Philippine Signal #4 Typhoon conditions.",
        "tags": ["Energy", "Predictive Maintenance", "Weather"]
    }
}

# --- HEADER ---
st.title("Nexus Data Philippines 🇵🇭")
st.markdown("### The Archipelago's First Sovereign Synthetic Data Marketplace")
st.info("Verified Privacy-Compliant under PH Data Privacy Act (DPA).")

# --- SHOPPING CART STATE ---
if 'cart' not in st.session_state:
    st.session_state.cart = []

# --- MARKETPLACE LAYOUT ---
tabs = st.tabs(["🛍️ All Datasets", "📥 My Downloads", "🛠️ Custom Request"])

with tabs[0]:
    st.header("Available Datasets")

    # Filter Row
    col_f1, col_f2 = st.columns([1, 3])
    with col_f1:
        category_filter = st.selectbox("Category", ["All", "Robotics", "LLM Tuning", "Energy"])

    # Product Grid
    for pid, info in products.items():
        if category_filter == "All" or category_filter == info['category']:
            with st.container():
                st.markdown(f"---")
                col_img, col_desc, col_buy = st.columns([1, 2, 1])

                with col_img:
                    # You would replace these with actual thumbnails
                    st.image(f"https://placehold.co/400x400/1f538d/white?text={info['category']}",
                             use_column_width=True)

                with col_desc:
                    st.subheader(info['name'])
                    st.write(info['description'])
                    st.caption(f"**Specs:** {info['rows']} rows | Format: {info['format']}")
                    st.write(f"🏷️ {' | '.join(info['tags'])}")

                with col_buy:
                    st.markdown(f"<p class='price-tag'>{info['price']}</p>", unsafe_allow_html=True)
                    if st.button(f"Add to Cart", key=pid):
                        st.session_state.cart.append(info['name'])
                        st.success(f"Added {info['name']}!")

# --- SIDEBAR CART ---
with st.sidebar:
    st.header("🛒 Your Cart")
    if not st.session_state.cart:
        st.write("Cart is empty.")
    else:
        for item in st.session_state.cart:
            st.write(f"- {item}")

        st.divider()
        st.button("Proceed to Checkout (PayMongo)")
        if st.button("Clear Cart"):
            st.session_state.cart = []
            st.rerun()

    st.divider()
    st.markdown("#### 🛡️ Pioneer Trust Seal")
    st.caption("Nexus Data uses verified stochastic physics engines. No real PI/PHI is used.")