from inventory_update import update_stock_quantity

result = update_stock_quantity(
    product_id=101,
    new_quantity=15,
    approval_confirmed=True
)

print(result)