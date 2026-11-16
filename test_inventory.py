
import unittest

from inventory_tools import (
    get_inventory_summary,
    get_low_stock_products,
    get_replenishment_recommendations
)


class TestInventoryTools(unittest.TestCase):

    def test_inventory_summary(self):
        result = get_inventory_summary()

        self.assertEqual(result["total_products"], 3)
        self.assertEqual(result["total_stock_units"], 70)

    def test_low_stock_products(self):
        result = get_low_stock_products()

        product_names = [
            product["product_name"]
            for product in result
        ]

        self.assertEqual(
            product_names,
            ["Wireless Mouse", "Monitor"]
        )

    def test_replenishment_recommendations(self):
        result = get_replenishment_recommendations()

        expected = {
            "Wireless Mouse": 10,
            "Monitor": 5
        }

        actual = {
            product["product_name"]: product["recommended_quantity"]
            for product in result
        }

        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
