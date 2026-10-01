import streamlit as st
from food_delivery import Customer, DeliveryPartner, Restaurant, MenuItem

st.set_page_config(
    page_title="OOP Food Delivery",
    page_icon="🍔",
    layout="wide",
)

st.title("🍔 OOP Food Delivery System")
st.caption("Simple Streamlit interface for your Python OOP food-delivery project.")


# -----------------------------
# Session state / sample data
# -----------------------------
if "customer" not in st.session_state:
    st.session_state.customer = None

if "delivery_partner" not in st.session_state:
    st.session_state.delivery_partner = None

if "restaurant" not in st.session_state:
    restaurant = Restaurant("Food Corner", "Aurangabad")
    restaurant.add_item(MenuItem("Veg Burger", 120, True))
    restaurant.add_item(MenuItem("Pizza", 220, True))
    restaurant.add_item(MenuItem("Chicken Biryani", 180, False))
    restaurant.add_item(MenuItem("French Fries", 90, True))
    restaurant.add_item(MenuItem("Cold Coffee", 80, True))
    st.session_state.restaurant = restaurant

if "current_order" not in st.session_state:
    st.session_state.current_order = None


customer = st.session_state.customer
restaurant = st.session_state.restaurant
delivery_partner = st.session_state.delivery_partner
order = st.session_state.current_order


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("📌 Project Flow")
    st.write("1. Create Customer")
    st.write("2. Add Wallet Balance")
    st.write("3. Show Restaurant Menu")
    st.write("4. Place Order")
    st.write("5. Create Delivery Partner")
    st.write("6. Accept Order")
    st.write("7. Enter OTP")
    st.write("8. Complete Delivery")


# -----------------------------
# 1. Create Customer
# -----------------------------
st.header("1️⃣ Create Customer")

with st.form("customer_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        customer_name = st.text_input("Customer Name")

    with col2:
        customer_phone = st.text_input("Phone Number")

    with col3:
        customer_address = st.text_input("Address")

    create_customer = st.form_submit_button("Create Customer")

if create_customer:
    if not customer_name or not customer_phone or not customer_address:
        st.error("Please fill all customer details.")
    else:
        st.session_state.customer = Customer(
            customer_name,
            customer_phone,
            customer_address,
        )
        st.session_state.current_order = None
        st.success(f"Customer '{customer_name}' created successfully.")
        st.rerun()

if customer:
    st.info(
        f"Customer: **{customer._name}** | "
        f"Phone: **{customer._phone}** | "
        f"Wallet: **₹{customer._wallet_balance:.2f}**"
    )


# -----------------------------
# 2. Add Wallet Balance
# -----------------------------
st.header("2️⃣ Add Wallet Balance")

if not customer:
    st.warning("Create a customer first.")
else:
    with st.form("wallet_form"):
        amount = st.number_input(
            "Enter amount (₹)",
            min_value=1.0,
            step=100.0,
            value=500.0,
        )
        add_money = st.form_submit_button("Add Money")

    if add_money:
        customer.add_wallet_balance(amount)
        st.success(f"₹{amount:.2f} added to wallet.")
        st.rerun()


# -----------------------------
# 3. Show Restaurant Menu
# -----------------------------
st.header("3️⃣ Restaurant Menu")

st.write(f"**{restaurant.name}** — {restaurant.location}")

menu_data = []
for item in restaurant.get_menu():
    menu_data.append(
        {
            "Item": item.name,
            "Price": f"₹{item.price:.2f}",
            "Type": "Veg 🟢" if item.is_veg else "Non-Veg 🔴",
        }
    )

st.table(menu_data)


# -----------------------------
# 4. Place Order
# -----------------------------
st.header("4️⃣ Place an Order")

if not customer:
    st.warning("Create a customer first.")
else:
    menu_items = restaurant.get_menu()

    selected_names = st.multiselect(
        "Select food items",
        options=[item.name for item in menu_items],
    )

    selected_items = [
        item for item in menu_items if item.name in selected_names
    ]

    if selected_items:
        subtotal = sum(item.price for item in selected_items)
        gst = subtotal * 0.05
        packaging = 20
        total = subtotal + gst + packaging

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Subtotal", f"₹{subtotal:.2f}")
        col2.metric("GST (5%)", f"₹{gst:.2f}")
        col3.metric("Packaging", f"₹{packaging:.2f}")
        col4.metric("Total", f"₹{total:.2f}")

        if st.button("🛒 Place Order"):
            try:
                order = customer.place_order(restaurant, selected_items)
                st.session_state.current_order = order
                st.success(f"Order #{order.order_id} placed successfully.")
                st.rerun()
            except ValueError as e:
                st.error(str(e))

    if order:
        st.success(
            f"Current Order #{order.order_id} | "
            f"Status: **{order.status}** | "
            f"Bill: **₹{order.calculate_bill():.2f}**"
        )

        # OTP is displayed for demo purposes so the complete OOP flow
        # can be tested in the Streamlit interface.
        st.info(f"🔐 Demo OTP: **{order.otp}**")


# -----------------------------
# 5. Create Delivery Partner
# -----------------------------
st.header("5️⃣ Create Delivery Partner")

with st.form("delivery_partner_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        dp_name = st.text_input("Partner Name")

    with col2:
        dp_phone = st.text_input("Partner Phone")

    with col3:
        dp_vehicle = st.selectbox(
            "Vehicle",
            ["Bike", "Scooter", "Car"],
        )

    create_partner = st.form_submit_button("Create Delivery Partner")

if create_partner:
    if not dp_name or not dp_phone:
        st.error("Please fill partner name and phone.")
    else:
        st.session_state.delivery_partner = DeliveryPartner(
            dp_name,
            dp_phone,
            dp_vehicle,
        )
        st.success(f"Delivery partner '{dp_name}' created.")
        st.rerun()

if delivery_partner:
    status = "Available 🟢" if delivery_partner.is_available else "Busy 🔴"
    st.info(
        f"Partner: **{delivery_partner._name}** | "
        f"Vehicle: **{delivery_partner.vehicle}** | "
        f"Status: **{status}**"
    )


# -----------------------------
# 6. Accept Order
# -----------------------------
st.header("6️⃣ Accept the Order")

if not order:
    st.warning("Place an order first.")
elif not delivery_partner:
    st.warning("Create a delivery partner first.")
elif order.status == "Delivered":
    st.success("This order has already been delivered.")
elif order.status == "Order Accepted":
    st.info("Order is already accepted by the delivery partner.")
else:
    if st.button("🚴 Accept Order"):
        try:
            delivery_partner.accept_order(order)
            st.success(f"Order #{order.order_id} accepted.")
            st.rerun()
        except ValueError as e:
            st.error(str(e))


# -----------------------------
# 7. Enter OTP
# -----------------------------
st.header("7️⃣ Enter OTP")

if not order:
    st.warning("Place an order first.")
elif order.status != "Order Accepted":
    st.warning("The delivery partner must accept the order first.")
else:
    entered_otp = st.text_input(
        "Enter 4-digit OTP",
        max_chars=4,
        type="password",
    )

    if st.button("Verify OTP"):
        try:
            otp = int(entered_otp)
        except ValueError:
            otp = -1

        if order.verify_otp(otp):
            st.success("OTP verified successfully.")
            st.session_state.otp_verified = True
        else:
            st.error("Invalid OTP.")


# -----------------------------
# 8. Complete Delivery
# -----------------------------
st.header("8️⃣ Complete Delivery")

if not order:
    st.warning("Place an order first.")
elif order.status != "Order Accepted":
    if order.status == "Delivered":
        st.success(f"🎉 Order #{order.order_id} is already delivered.")
    else:
        st.warning("Accept the order before completing delivery.")
else:
    if st.button("✅ Complete Delivery"):
        otp_verified = st.session_state.get("otp_verified", False)

        if otp_verified:
            if delivery_partner.deliver(order, order.otp):
                st.success(
                    f"🎉 Order #{order.order_id} delivered successfully!"
                )
                st.rerun()
        else:
            st.error("Please verify the OTP first.")


# -----------------------------
# Current order summary
# -----------------------------
st.divider()
st.header("📦 Current Order Summary")

if order:
    st.write(f"**Order ID:** #{order.order_id}")
    st.write(f"**Status:** {order.status}")
    st.write(f"**Estimated Time:** {order.estimated_time()} minutes")
    st.write(f"**Total Bill:** ₹{order.calculate_bill():.2f}")

    st.write("**Items:**")
    for item in order.items:
        st.write(f"- {item.name} — ₹{item.price:.2f}")
else:
    st.info("No order has been placed yet.")
