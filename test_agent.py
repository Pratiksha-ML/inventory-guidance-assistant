
import unittest

from agentic_inventory import ask_inventory_agent


class TestInventoryAgent(unittest.TestCase):

    def test_low_stock_question(self):
        answer = ask_inventory_agent(
            "Which products are currently low on stock?"
        )

        answer = answer.lower()

        self.assertIn("wireless mouse", answer)
        self.assertIn("monitor", answer)

    def test_replenishment_question(self):
        answer = ask_inventory_agent(
            "How many units should we replenish?"
        )

        answer = answer.lower()

        self.assertIn("wireless mouse", answer)
        self.assertIn("monitor", answer)
        self.assertIn("10", answer)
        self.assertIn("5", answer)

    def test_sop_approval_question(self):
        answer = ask_inventory_agent(
            "What does the SOP say about approval "
            "for stock-changing actions?"
        )

        answer = answer.lower()

        self.assertIn("authorized team member", answer)

    def test_unrelated_question(self):
        answer = ask_inventory_agent(
            "What is the company's annual revenue?"
        )

        self.assertIn("outside my scope", answer.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
