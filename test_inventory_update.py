
from inventory_update import update_stock_quantity

print("TEST 1: Update without approval")

try:
    update_stock_quantity(
        product_id=101,
        new_quantity=30
    )

except PermissionError as error:
    print("Update blocked:", error)


print("\nTEST 2: Update with approval")

try:
    result = update_stock_quantity(
        product_id=101,
        new_quantity=30,
        approval_confirmed=True
    )

    print(result)

except Exception as error:
    print("Error:", error)

print("\nRESTORING ORIGINAL INVENTORY")

result = update_stock_quantity(
    product_id=101,
    new_quantity=15,
    approval_confirmed=True
)

print(result)
