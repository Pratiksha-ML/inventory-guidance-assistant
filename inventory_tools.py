
from database import get_database_connection


def get_inventory_summary():

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COUNT(*),
            COALESCE(SUM(available_stock), 0)
        FROM inventory
    """)

    result = cursor.fetchone()
    connection.close()

    return {
        "total_products": result[0],
        "total_stock_units": result[1]
    }


def get_low_stock_products():

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT product_name, available_stock, minimum_stock
        FROM inventory
        WHERE available_stock < minimum_stock
    """)

    records = cursor.fetchall()
    connection.close()

    low_stock_products = []

    for record in records:
        low_stock_products.append({
            "product_name": record[0],
            "available_stock": record[1],
            "minimum_stock": record[2]
        })

    return low_stock_products


def get_replenishment_recommendations():

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            product_name,
            available_stock,
            minimum_stock,
            minimum_stock - available_stock
        FROM inventory
        WHERE available_stock < minimum_stock
    """)

    records = cursor.fetchall()
    connection.close()

    recommendations = []

    for record in records:
        recommendations.append({
            "product_name": record[0],
            "available_stock": record[1],
            "minimum_stock": record[2],
            "recommended_quantity": record[3]
        })

    return recommendations


if __name__ == "__main__":

    print("\nINVENTORY SUMMARY")
    print("-----------------")
    print(get_inventory_summary())

    print("\nLOW STOCK PRODUCTS")
    print("------------------")
    print(get_low_stock_products())

    print("\nREPLENISHMENT RECOMMENDATIONS")
    print("-----------------------------")
    print(get_replenishment_recommendations())
