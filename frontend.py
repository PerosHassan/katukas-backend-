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
           # === TEMPORARY BULK UPLOAD BUTTON ===
st.sidebar.header("Admin Tools")
if st.sidebar.button("🚀 Run One-Time Bulk Upload"):
    BULK_ITEMS = [
        {"name": "Tea/Egg & Bread", "description": "Breakfast - Hot tea, eggs, and bread", "price": 3000.0, "is_available": True},
        {"name": "Chips Egg & Bottle Water", "description": "Breakfast - Crispy chips served with egg and a bottle of water", "price": 4400.0, "is_available": True},
        {"name": "Yam Egg Sauce & Bottle Water", "description": "Breakfast - Boiled/fried yam with egg sauce and a bottle of water", "price": 3400.0, "is_available": True},
        {"name": "Yam, Fish & Bottle Water", "description": "Breakfast - Yam paired with prepared fish and a bottle of water", "price": 3900.0, "is_available": True},
        {"name": "Yam, Beef & Bottle Water", "description": "Breakfast - Yam served with beef and a bottle of water", "price": 3000.0, "is_available": True},
        {"name": "Yam with Chicken/Fresh Fish", "description": "Breakfast - Yam served with chicken or fresh fish", "price": 5400.0, "is_available": True},
        {"name": "Moi-Moi", "description": "Breakfast - Classic steamed bean pudding", "price": 500.0, "is_available": True},
        {"name": "Moi-Moi with Egg", "description": "Breakfast - Steamed bean pudding with egg inside", "price": 1000.0, "is_available": True},
        {"name": "Indomie, Egg & Bottle Water", "description": "Breakfast - Instant noodles with egg and a bottle of water", "price": 3900.0, "is_available": True},
        {"name": "Spaghetti with Beef and Bottle Water", "description": "Breakfast - Cooked spaghetti served with beef and a bottle of water", "price": 2700.0, "is_available": True},
        {"name": "Spaghetti with Fish & Bottle Water", "description": "Breakfast - Cooked spaghetti served with fish and a bottle of water", "price": 3400.0, "is_available": True},
        {"name": "Spaghetti with Chicken/Fresh Fish & Bottle Water", "description": "Breakfast - Spaghetti served with chicken or fresh fish and water", "price": 4900.0, "is_available": True},
        {"name": "Basmatic", "description": "Breakfast - Basmati rice dish", "price": 3000.0, "is_available": True},
        {"name": "Beans with Beef & Bottle Water", "description": "Breakfast - Plain beans with beef and a bottle of water", "price": 3200.0, "is_available": True},
        {"name": "Beans with Fish/Goatmeat & Bottle Water", "description": "Breakfast - Plain beans with choice of fish or goat meat and water", "price": 3900.0, "is_available": True},
        {"name": "Beans with Chicken/Fresh Fish & Bottle Water", "description": "Breakfast - Plain beans with chicken or fresh fish and water", "price": 4900.0, "is_available": True},
        {"name": "Pepper Soup (Intestine)", "description": "Pepper Soup - Spicy local intestine pepper soup", "price": 3000.0, "is_available": True},
        {"name": "Pepper Soup (Goat Meat)", "description": "Pepper Soup - Savory spicy goat meat pepper soup", "price": 3000.0, "is_available": True},
        {"name": "Pepper Soup (Cow Leg)", "description": "Pepper Soup - Rich spicy cow leg pepper soup", "price": 3000.0, "is_available": True},
        {"name": "Pepper Soup (Fresh Fish)", "description": "Pepper Soup - Light and spicy fresh fish pepper soup", "price": 3000.0, "is_available": True},
        {"name": "Pepper Soup (Esiewu)", "description": "Pepper Soup - Traditional spicy goat head soup", "price": 3000.0, "is_available": True},
        {"name": "Pepper Soup (Chicken)", "description": "Pepper Soup - Warm spicy chicken pepper soup", "price": 3000.0, "is_available": True},
        {"name": "Shawarma with Sausage", "description": "Pastries - Grilled wrap filled with meat and sausage", "price": 5000.0, "is_available": True},
        {"name": "Shawarma without Sausage", "description": "Pastries - Grilled wrap filled with classic ingredients (no sausage)", "price": 4500.0, "is_available": True},
        {"name": "Meat Pie", "description": "Pastries - Baked pastry with savory minced meat filling", "price": 1500.0, "is_available": True},
        {"name": "Samosa", "description": "Pastries - Crispy fried triangular snack shell with savory filling", "price": 500.0, "is_available": True},
        {"name": "Donuts", "description": "Pastries - Sweet fried dough confectionery snack", "price": 1000.0, "is_available": True},
        {"name": "Fish Roll", "description": "Pastries - Baked or fried pastry rolled with fish filling", "price": 1000.0, "is_available": True},
        {"name": "Fresh Juice", "description": "Pastries/Drinks - Refreshing cold fresh fruit juice", "price": 2000.0, "is_available": True},
        {"name": "Fruits Salad", "description": "Pastries/Healthy - Freshly cut assorted seasonal fruit mix", "price": 1500.0, "is_available": True},
        {"name": "Pizza", "description": "Pastries - Baked flatbread topped with tomato sauce, cheese, and meats", "price": 10000.0, "is_available": True},
        {"name": "Burger", "description": "Pastries - Grilled patty inside a sliced bun with fresh toppings", "price": 4000.0, "is_available": True},
        {"name": "Rice (Jellof, Fried, White) Beef & Bottle Water", "description": "Lunch - Choice of rice served with beef and bottled water", "price": 2700.0, "is_available": True},
        {"name": "Rice (Jellof, Fried, White) Fish/Goat Meat & Bottle Water", "description": "Lunch - Choice of rice served with fish/goat meat and water", "price": 3400.0, "is_available": True},
        {"name": "Rice (Jellof, Fried, White) Chicken/Fresh Fish & Bottle Water", "description": "Lunch - Choice of rice served with chicken/fresh fish and water", "price": 4900.0, "is_available": True},
        {"name": "Salads", "description": "Lunch - Freshly prepared vegetable or side salad", "price": 1000.0, "is_available": True},
        {"name": "Swallow (Semo/Akpu/Amala/Eba/Wheat/Tuwo) with Beef & Bottle Water", "description": "Swallow - Selected swallow type served with soup, beef, and water", "price": 2700.0, "is_available": True},
        {"name": "Swallow (Semo/Akpu/Amala/Eba/Wheat/Tuwo) with Fish/Goatmeat & Bottle Water", "description": "Swallow - Selected swallow type served with soup, fish/goat meat, and water", "price": 3400.0, "is_available": True},
        {"name": "Swallow (Semo/Akpu/Amala/Eba/Wheat/Tuwo) with Chicken/Fresh Fish & Bottle Water", "description": "Swallow - Selected swallow type served with soup, chicken/fresh fish, and water", "price": 4900.0, "is_available": True},
        {"name": "Swallow (Semo/Akpu/Amala/Eba/Wheat/Tuwo) with Bottle Water", "description": "Swallow - Selected swallow type served with soup base and a bottle of water", "price": 1900.0, "is_available": True},
        {"name": "Pounded Yam with Beef & Bottle Water", "description": "Swallow II - Fresh pounded yam served with choice of soup, beef, and water", "price": 3200.0, "is_available": True},
        {"name": "Pounded Yam with Fresh Fish/Chicken & Bottle Water", "description": "Swallow II - Fresh pounded yam served with soup, fresh fish/chicken, and water", "price": 5400.0, "is_available": True},
        {"name": "Pounded Yam with Goatmeat/Fish & Bottle Water", "description": "Swallow II - Fresh pounded yam served with soup, goat meat/fish, and water", "price": 3900.0, "is_available": True},
        {"name": "Take Away Pack", "description": "Extra - Premium food packaging container fee", "price": 400.0, "is_available": True}
    ]
    
    st.sidebar.write("Uploading items...")
    success_count = 0
    for item in BULK_ITEMS:
        try:
            res = requests.post(API_URL, json=item)
            if res.status_code == 200:
                success_count += 1
        except:
            pass
    st.sidebar.success(f"🎉 Uploaded {success_count} items successfully!")         
