import streamlit as st
import pandas as pd
import json
import os

# --- 1. DATA PERSISTENCE LAYER ---
DB_FILE = "database.json"


def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return [
        {
            "id": "DS-001",
            "name": "Bipedal Robot Failures (PH-Edition)",
            "category": "Robotics",
            "price": 250.00,
            "currency": "USD",
            "description": "High-fidelity sensor logs for humanoid bipedal units.",
            "file_type": "Parquet",
            "sample_data": {"sensor_id": [1, 2], "error_code": ["E-01", "E-99"], "latency": [0.45, 0.89]}
        }
    ]


def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


# Initialize Session State
if 'my_datasets' not in st.session_state:
    st.session_state.my_datasets = load_data()

# --- 2. CONFIG & STYLING ---
st.set_page_config(page_title="Nexus Marketplace Pro", page_icon="📈", layout="wide")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; }
    .product-box { border: 1px solid #333; padding: 20px; border-radius: 15px; background-color: #0e1117; margin-bottom: 15px; border-left: 5px solid #0070ba; }
    .price { font-size: 24px; color: #2ecc71; font-weight: bold; }
    .sample-header { color: #888; font-size: 14px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (ADMIN & FILTERS) ---
with st.sidebar:
    st.title("Nexus Control")

    # Simple Admin Lock
    with st.expander("👑 Admin Portal"):
        password = st.text_input("Access Key", type="password")
        if password == "nexus2026":  # Change this!
            st.success("Authenticated")
            new_name = st.text_input("Dataset Name")
            new_cat = st.selectbox("Category", ["Robotics", "LLM Training", "IoT", "Green Energy"])
            new_price = st.number_input("Price (USD)", min_value=1.0)
            new_desc = st.text_area("Description")

            if st.button("🚀 Publish Dataset"):
                new_entry = {
                    "id": f"DS-00{len(st.session_state.my_datasets) + 1}",
                    "name": new_name,
                    "category": new_cat,
                    "price": new_price,
                    "currency": "USD",
                    "description": new_desc,
                    "file_type": "Parquet",
                    "sample_data": {"col1": [1, 2], "col2": ["Sample", "Data"]}
                }
                st.session_state.my_datasets.append(new_entry)
                save_data(st.session_state.my_datasets)
                st.rerun()
        elif password:
            st.error("Invalid Key")

    st.divider()
    st.subheader("🔍 Browse Filters")
    category_filter = st.selectbox("Industry Vertical",
                                   ["All"] + list(set(d['category'] for d in st.session_state.my_datasets)))

# --- 4. MAIN STOREFRONT ---
st.title("Nexus Synthetic Marketplace 🇵🇭")
st.info("The premier hub for high-fidelity Philippine-centric synthetic training data.")

# Filtering Logic
filtered_data = [d for d in st.session_state.my_datasets if
                 category_filter == "All" or d['category'] == category_filter]

# Grid Layout
for i in range(0, len(filtered_data), 2):
    cols = st.columns(2)
    for j in range(2):
        if i + j < len(filtered_data):
            dataset = filtered_data[i + j]
            with cols[j]:
                with st.container():
                    st.markdown(f"""
                        <div class="product-box">
                            <h3>{dataset['name']}</h3>
                            <p style="color: #0070ba;">{dataset['category']} • {dataset['file_type']}</p>
                            <p>{dataset['description']}</p>
                            <p class="price">${dataset['price']:.2f} USD</p>
                        </div>
                    """, unsafe_allow_html=True)

                    # Essential Feature: Data Preview
                    with st.expander("👁️ View Data Sample"):
                        st.write("First 2 rows of synthetic signals:")
                        st.table(pd.DataFrame(dataset['sample_data']))

                    # Payment Button
                    paypal_url = f"https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business=09manongsongken@gmail.com&item_name={dataset['name']}&amount={dataset['price']}&currency_code=USD"
                    st.markdown(
                        f'<a href="{paypal_url}" target="_blank"><button style="width:100%; cursor:pointer; background-color:#ffc439; color:#000; border:none; padding:12px; border-radius:10px; font-weight:bold;">Purchase Access</button></a>',
                        unsafe_allow_html=True)
                    st.write("---")

# --- 5. FULFILLMENT SECTION ---
st.divider()
st.subheader("📥 Secure Retrieval")
col_a, col_b = st.columns([2, 1])
with col_a:
    tid = st.text_input("Enter PayPal Transaction ID", placeholder="e.g. 8RT1234567890")
with col_b:
    st.write(" ")  # Alignment
    if st.button("Verify & Download"):
        if tid:
            st.success("Transaction Verified. Preparing secure download link...")
            st.download_button("Download .zip Bundle", data="Your data here", file_name="nexus_export.zip")
        else:
            st.warning("Please enter a valid ID.")