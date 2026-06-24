import streamlit as st
import requests

# Your live Render API URL
API_URL = "https://katukas-backend.onrender.com/menu/"

st.set_page_config(page_title="Katukas Kitchen Admin", page_icon="🍳", layout="centered")

st.title("🍳 Katukas Kitchen Management Dashboard")
st.write("Manage your cloud menu items live on the internet.")

# Create two tabs: One to view the menu, one to add items
tab1, tab2 = st.tabs(["📋 View Live Menu", "➕ Add New Dish"])

with tab1:
    st.header("Current Menu")
    if st.button("🔄 Refresh Menu"):
        st.rerun()
        
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            menu_items = response.json()
            if not menu_items:
                st.info("The kitchen database is currently empty. Go to the next tab to add a dish!")
            else:
                for item in menu_items:
                    # Checkbox to show availability
                    status = "🟢 Available" if item.get("is_available", True) else "🔴 Out of Stock"
                    
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.subheader(f"{item['name']}")
                            st.write(f"_{item['description']}_")
                        with col2:
                            st.subheader(f"₦{item['price']:,}")
                            st.caption(status)
                    st.divider()
        else:
            st.error(f"Could not fetch menu items. Server responded with code: {response.status_code}")
    except Exception as e:
        st.error(f"Error connecting to backend server: {e}")

with tab2:
    st.header("Add a Delicious New Dish")
    with st.form("add_dish_form", clear_on_submit=True):
        name = st.text_input("Dish Name (e.g., Pounded Yam & Egusi)")
        description = st.text_area("Description / Ingredients")
        price = st.number_input("Price (₦)", min_value=0.0, step=500.0, value=1500.0)
        is_available = st.checkbox("Available immediately?", value=True)
        
        submit_button = st.form_submit_button("Save Dish to Cloud Database")
        
        if submit_button:
            if not name:
                st.warning("Please provide a name for the dish.")
            else:
                payload = {
                    "name": name,
                    "description": description,
                    "price": price,
                    "is_available": is_available
                }
                try:
                    res = requests.post(API_URL, json=payload)
                    if res.status_code == 200:
                        st.success(f"🎉 '{name}' has been successfully stored in your cloud database!")
                    else:
                        st.error(f"Failed to add item. Error: {res.text}")
                except Exception as e:
                    st.error(f"Connection error: {e}")
