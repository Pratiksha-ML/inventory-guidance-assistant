from inventory_data import inventory

from inventory_logic import (
    check_low_stock,
    get_total_products,
    get_total_inventory_value,
    get_replenishment_recommendations,
    search_product
)
print("===================================")
print("   INVENTORY GUIDANCE ASSISTANT")
print("===================================")

# Low stock report
low_stock_products = check_low_stock(inventory)

print("\nLOW STOCK REPORT")

for product in low_stock_products:
    print(
        product["product_name"],
        "- Stock:",
        product["available_stock"]
    )

# Inventory summary
total_products = get_total_products(inventory)

total_value = get_total_inventory_value(inventory)

print("\nINVENTORY SUMMARY")
print("-------------------------------")

print("Total Products:", total_products)

print("Total Inventory Value: ₹", round(total_value, 2))

print("Low Stock Products:", len(low_stock_products))
from inventory_logic import (
    check_low_stock,
    get_total_products,
    get_total_inventory_value,
    get_replenishment_recommendations
)

recommendations = get_replenishment_recommendations(inventory)

print("\nREPLENISHMENT RECOMMENDATIONS")
print("-------------------------------")

for item in recommendations:

    print("Product:", item["product_name"])
    print("Suggested Quantity:", item["required_quantity"])
    print("-------------------------------")
    print("\nPRODUCT SEARCH")
    print("-------------------------------")

    search_result = search_product(inventory, "Keyboard")

    if search_result:

        print("Product Found:", search_result["product_name"])
        print("Available Stock:", search_result["available_stock"])
        print("Price:", search_result["price"])

    else:
        print("Product not found.")