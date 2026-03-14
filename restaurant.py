import streamlit as st

# 🍔 Step 1: Setup Menu Data
menu = [
    {"name": "Paneer Curry", "price": 250, "type": "Veg"},
    {"name": "Chicken Biryani", "price": 300, "type": "Non-Veg"},
    {"name": "Dal Tadka", "price": 150, "type": "Veg"},
    {"name": "Fish Fry", "price": 280, "type": "Non-Veg"},
    {"name": "Salad", "price": 100, "type": "Veg"}
]

# 💰 Step 2: Calculate Bill
def calculate_bill(cart):
    total = sum(qty * price for _, (qty, price, _) in cart.items())
    free_dessert = None
    if total > 1000:
        free_dessert = "Ice Cream "
        cart[free_dessert] = (1, 0, "Dessert")
    return total, free_dessert

# 🧾 Step 3: Display Order Summary
def show_summary(cart, total, free_dessert):
    st.subheader(" Order Summary")
    st.write("---")
    if not cart:
        st.warning(" No items in your order yet!")
        return

    summary = []
    for item, (qty, price, typ) in cart.items():
        summary.append(
            {
                "Item": item,
                "Type": typ,
                "Qty": qty,
                "Price (₹)": price,
                "Subtotal (₹)": qty * price
            }
        )

    st.table(summary)
    st.write(f"###  Total Bill: ₹{total}")
    if free_dessert:
        st.success(f" Free Dessert Added: {free_dessert}")
    st.info("Thank you for dining with us! ")

# 🚀 Step 4: Main Streamlit App
def restaurant_system():
    st.set_page_config(page_title="Restaurant Ordering System", page_icon="", layout="centered")
    st.title(" Welcome to Python Restaurant")

    # Select mode
    veg_mode = st.radio("Select Mode", ["Veg Only", "Veg + Non-Veg"])
    veg_only = veg_mode == "Veg Only"

    # Filter menu based on mode
    filtered_menu = [item for item in menu if not (veg_only and item["type"] == "Non-Veg")]

    st.subheader(" Menu Card")
    st.write("---")
    st.table([{ "Item": i["name"], "Price (₹)": i["price"], "Type": i["type"] } for i in filtered_menu])

    # Cart dictionary
    if "cart" not in st.session_state:
        st.session_state.cart = {}

    st.write("###  Select Items")
    for item in filtered_menu:
        qty = st.number_input(f"{item['name']} ({item['type']}) - ₹{item['price']}", 0, 10, 0)
        if qty > 0:
            st.session_state.cart[item["name"]] = (qty, item["price"], item["type"])

    if st.button(" Generate Bill"):
        if not st.session_state.cart:
            st.warning("Please select at least one item to proceed.")
        else:
            total, free_dessert = calculate_bill(st.session_state.cart)
            show_summary(st.session_state.cart, total, free_dessert)

    if st.button(" New Order"):
        st.session_state.cart = {}
        st.experimental_rerun()

# Run app
if __name__ == "__main__":
    restaurant_system()
