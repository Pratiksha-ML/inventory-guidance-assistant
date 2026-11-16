def check_low_stock(inventory):

    low_stock_products = []

    for product in inventory:

        if product["available_stock"] < product["minimum_stock"]:

            low_stock_products.append(product)

    return low_stock_products

def get_total_products(inventory):

    return len(inventory)


def get_total_inventory_value(inventory):

    total_value = 0

    for product in inventory:

        product_value = (
            product["available_stock"] * product["price"]
        )

        total_value = total_value + product_value

    return total_value

def get_replenishment_recommendations(inventory):

    recommendations = []

    for product in inventory:

        available = product["available_stock"]
        minimum = product["minimum_stock"]

        if available < minimum:

            required_quantity = minimum - available

            recommendation = {
                "product_name": product["product_name"],
                "required_quantity": required_quantity
            }

            recommendations.append(recommendation)

    return recommendations

def search_product(inventory, search_name):

    for product in inventory:

        if product["product_name"].lower() == search_name.lower():

            return product

    return None