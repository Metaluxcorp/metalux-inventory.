import streamlit as st

# MUST be the first Streamlit command in your script
st.set_page_config(
    page_title="Metalux Quick-Order",
    page_icon="Metalux-Black-BackGround.jpeg", # This pulls your uploaded image
    layout="centered"
)

# Optional: Display the logo at the top of the app page too
st.image("Metalux-Black-BackGround.jpeg", width=200)
import datetime
import smtplib
from email.message import EmailMessage

# --- CONFIG ---
st.set_page_config(page_title="Metalux Inventory", page_icon="🔧")

# --- EMAIL SETTINGS ---
SENDER_EMAIL = "Metaluxcorp@gmail.com"
SENDER_PASSWORD = "jihihaxgrvtgcstz"
RECEIVER_EMAIL = "Metaluxcorp@gmail.com"

st.title("⚒️ Metalux Quick-Order")
st.write(f"Date: {datetime.date.today().strftime('%B %d, %Y')}")

# --- FULL DATA GROUPED BY SUPPLIER ---
shop_data = {
    "Amazon": [
        "Steel Cut (DCRED45)", "Steel Flap (MX45802T)", "Steel Grind (D4510)",
        "105Amp Nozzle (220990)", "45Amp Nozzle (220941)", "65Amp Nozzle (220819)",
        "85Amp Nozzle (220816)", "Electrode (220842)", "Finecut Nozzle (220930)",
        "Finecut Shield (220948)", "Ohmic Retaining Cap (220953)",
        "Shield - 105Amp (220993)", "Shield - 45-85Amp (220817)",
        "Alum Contact Tip 0.035", "Alum Nozzle (199613)", "Alum Wire 4043",
        "Anti Spatter Spray", "Steel Brushes", "Steel Contact Tips 0.035",
        "Steel Diffuser", "Steel Nozzle"
    ],
    "County Welding": [
        "Alum Blend Wheel", "Alum Cut Wheel", "Alum Flap Wheel", "Alum Grind Wheel",
        "Acetylene (145cft)", "Argon (80cft)", "Mixed 75/25 (80cft)", "Oxygen (337cft)",
        "Propane (30lbs)", "Trimix (125cft)", "Trimix (337cft)", "Steel Wire (0.35 33lbs)"
    ],
    "Lowes": [
        "Acetone", "Paint", "Tape Measures"
    ]
}

# Dictionary to hold orders by supplier: {"Amazon": ["- Item: 5"], "Lowes": ["- Item: 2"]}
order_by_supplier = {supplier: [] for supplier in shop_data.keys()}

st.info("Check the box for each item that needs to be ordered.")

# --- INTERFACE ---
for supplier, items in shop_data.items():
    with st.expander(f"📦 {supplier}", expanded=True):
        for item in items:
            col1, col2 = st.columns([2, 1])
            needs_order = col1.checkbox(item, key=f"check_{item}")

            if needs_order:
                qty = col2.number_input("Qty:", min_value=1, step=1, key=f"qty_{item}")
                order_by_supplier[supplier].append(f"- {item}: {qty}")

# --- ADDITIONAL NOTES ---
st.divider()
extra_notes = st.text_area("Additional items or notes for the office:", placeholder="Need more welding gloves, etc.")

# --- SENDING LOGIC ---
if st.button("SEND ORDER TO OFFICE", type="primary"):
    # Check if anything was selected across all suppliers
    has_items = any(len(items) > 0 for items in order_by_supplier.values())

    if not has_items and not extra_notes:
        st.warning("Please select at least one item or add a note.")
    else:
        # Construct the email body with Supplier Headers
        email_body = f"Metalux Inventory Report - {datetime.date.today()}\n"
        email_body += "=" * 30 + "\n\n"

        for supplier, ordered_list in order_by_supplier.items():
            if ordered_list:
                email_body += f"--- {supplier.upper()} ORDER ---\n"
                email_body += "\n".join(ordered_list) + "\n\n"

        if extra_notes:
            email_body += f"--- ADDITIONAL NOTES ---\n{extra_notes}"

        try:
            msg = EmailMessage()
            msg.set_content(email_body)
            msg['Subject'] = f"SHOP ORDER: {datetime.date.today().strftime('%m/%d/%Y')}"
            msg['From'] = SENDER_EMAIL
            msg['To'] = RECEIVER_EMAIL

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
                smtp.send_message(msg)

            st.balloons()
            st.success("Order Sent Successfully!")
            st.text_area("Sent Summary:", value=email_body, height=300)

        except Exception as e:

            st.error(f"Error sending email: {e}")

