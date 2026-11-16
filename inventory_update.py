
from database import get_database_connection
from user_management import can_approve_stock


def update_stock_quantity(
    product_id,
    new_quantity,
    approved_by
):
    # 1. Check administrator permission.
    if not can_approve_stock(approved_by):
        raise PermissionError(
            "Only authorized administrators can approve stock updates."
        )

    # 2. Validate the new stock quantity.
    if type(new_quantity) is not int or new_quantity < 0:
        raise ValueError(
            "Stock quantity must be a non-negative integer."
        )

    # 3. Get the approver's details.
    user_id = approved_by.get("user_id")
    username = approved_by.get("username")

    if not user_id or not username:
        raise PermissionError(
            "Valid administrator account details are required."
        )

    connection = get_database_connection()

    try:
        cursor = connection.cursor()

        # 4. Read the existing product details.
        cursor.execute(
            """
            SELECT product_name, available_stock
            FROM inventory
            WHERE product_id = ?
            """,
            (product_id,)
        )

        product = cursor.fetchone()

        if product is None:
            return "Product not found."

        product_name = product[0]
        old_quantity = product[1]

        # 5. Avoid recording an update if nothing changed.
        if old_quantity == new_quantity:
            return "No stock change was made."

        # 6. Update the inventory quantity.
        cursor.execute(
            """
            UPDATE inventory
            SET available_stock = ?
            WHERE product_id = ?
            """,
            (new_quantity, product_id)
        )

        # 7. Record the approved change in the audit table.
        cursor.execute(
            """
            INSERT INTO stock_audit (
                product_id,
                product_name,
                old_quantity,
                new_quantity,
                approved_by_user_id,
                approved_by_username
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                product_id,
                product_name,
                old_quantity,
                new_quantity,
                user_id,
                username
            )
        )

        # 8. Save both changes together.
        connection.commit()

        return "Stock updated successfully. Audit record created."

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
