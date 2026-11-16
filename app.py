
import streamlit as st

from database import get_database_connection
from inventory_update import update_stock_quantity
from user_management import authenticate_user
from agentic_inventory import ask_inventory_agent


# ----------------------------------
# PAGE CONFIGURATION
# ----------------------------------

st.set_page_config(
    page_title="Inventory Guidance Assistant",
    page_icon="📦"
)


# ----------------------------------
# USER LOGIN
# ----------------------------------

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

if st.session_state.logged_in_user is None:

    st.title("📦 Inventory Assistant Login")

    username = st.text_input("Username")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        user = authenticate_user(username, password)

        if user:
            st.session_state.logged_in_user = user
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password.")

    st.stop()


# ----------------------------------
# LOGGED-IN USER
# ----------------------------------

current_user = st.session_state.logged_in_user

st.sidebar.title("User Account")
st.sidebar.write("Username:", current_user["username"])
st.sidebar.write("Role:", current_user["role"])

if st.sidebar.button("Logout"):

    st.session_state.logged_in_user = None
    st.session_state.messages = []
    st.session_state.pending_stock_update = None

    st.rerun()


# ----------------------------------
# MAIN APPLICATION
# ----------------------------------

st.title("📦 Inventory Guidance Assistant")

st.write(
    "Your AI-powered assistant for inventory management."
)


# ----------------------------------
# INVENTORY CHAT ASSISTANT
# ----------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


question = st.chat_input("Ask your inventory question...")

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):

        with st.spinner("Analyzing inventory..."):

            answer = ask_inventory_agent(question)

            st.write(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })


# ----------------------------------
# DATABASE INVENTORY RECORDS
# ----------------------------------

def get_inventory_records():

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT product_id, product_name, available_stock
        FROM inventory
    """)

    records = cursor.fetchall()
    connection.close()

    return records


def get_stock_audit_records():

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            audit_id,
            product_name,
            old_quantity,
            new_quantity,
            approved_by_username,
            approved_at
        FROM stock_audit
        ORDER BY audit_id DESC
    """)

    records = cursor.fetchall()
    connection.close()

    return records

# ----------------------------------
# STOCK UPDATE APPROVAL SECTION
# ----------------------------------


# ----------------------------------
# STOCK AUDIT HISTORY
# ----------------------------------

if current_user["role"] == "admin":

    st.divider()

    st.header("📋 Stock Audit History")

    audit_records = get_stock_audit_records()

    if audit_records:

        audit_data = []

        for record in audit_records:

            audit_data.append({
                "Audit ID": record[0],
                "Product": record[1],
                "Previous Stock": record[2],
                "New Stock": record[3],
                "Approved By": record[4],
                "Approval Time": record[5]
            })

        st.dataframe(
            audit_data,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No stock audit records found.")


st.divider()

st.header("📦 Inventory Stock Update")

st.write(
    "Review a proposed stock change and approve it before updating the database."
)


products = get_inventory_records()

if products:

    product_options = {
        f"{p[1]} (ID: {p[0]})": p
        for p in products
    }

    with st.form("stock_update_form"):

        selected_product = st.selectbox(
            "Select product",
            list(product_options.keys())
        )

        product = product_options[selected_product]

        new_quantity = st.number_input(
            "New available stock",
            min_value=0,
            value=int(product[2]),
            step=1
        )

        review_clicked = st.form_submit_button(
            "Review proposed update"
        )


    # ----------------------------------
    # SAVE PROPOSED UPDATE
    # ----------------------------------

    if review_clicked:

        connection = get_database_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT product_name, available_stock
            FROM inventory
            WHERE product_id = ?
            """,
            (product[0],)
        )

        current_product = cursor.fetchone()
        connection.close()

        if current_product is None:

            st.error("Product not found.")

        else:

            st.session_state.pending_stock_update = {
                "product_id": product[0],
                "product_name": current_product[0],
                "old_quantity": int(current_product[1]),
                "new_quantity": int(new_quantity)
            }


    # ----------------------------------
    # REVIEW PROPOSED UPDATE
    # ----------------------------------

    pending = st.session_state.get(
        "pending_stock_update"
    )

    if pending:

        st.subheader("Review your proposed change")

        st.write("Product:", pending["product_name"])

        st.write(
            "Current stock:",
            pending["old_quantity"]
        )

        st.write(
            "Proposed stock:",
            pending["new_quantity"]
        )


        # ----------------------------------
        # ADMIN APPROVAL
        # ----------------------------------

        if current_user["role"] == "admin":

            if st.button("Approve and update stock"):

                try:

                    result = update_stock_quantity(
                        product_id=pending["product_id"],
                        new_quantity=pending["new_quantity"],
                        approved_by=current_user
                    )

                    st.success(result)

                    del st.session_state.pending_stock_update

                    st.rerun()

                except Exception as error:

                    st.error(str(error))


        # ----------------------------------
        # REGULAR USER RESTRICTION
        # ----------------------------------

        else:

            st.warning(
                "Only administrators can approve stock updates."
            )


        # ----------------------------------
        # CANCEL PROPOSED UPDATE
        # ----------------------------------

        if st.button("Cancel update"):

            del st.session_state.pending_stock_update

            st.info("Stock update cancelled.")

            st.rerun()

else:

    st.warning("No inventory products found.")
