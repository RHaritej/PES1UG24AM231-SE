"""Basic security-focused tests for restaurant order operations."""

import unittest

from restaurant_order_system import (
    calculate_discounted_bill,
    generate_pos_pin,
    generate_ticket_hash,
)


class SecurityTests(unittest.TestCase):
    """Verify safe billing and ticket utility behavior."""

    def test_discount_rate_out_of_range_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_discounted_bill("T1", 1.5)

    def test_unknown_table_is_rejected(self):
        with self.assertRaises(KeyError):
            calculate_discounted_bill("UNKNOWN")

    def test_pin_is_four_digits(self):
        pin = generate_pos_pin()
        self.assertGreaterEqual(pin, 1000)
        self.assertLessEqual(pin, 9999)

    def test_ticket_hash_is_sha256_length(self):
        self.assertEqual(len(generate_ticket_hash("T1")), 64)

    def test_expression_string_is_rejected(self):
        """Reject expression strings instead of evaluating them."""
        with self.assertRaises(TypeError):
            calculate_discounted_bill(
                "T1",
                "__import__('os').system('echo unsafe')",
            )

if __name__ == "__main__":
    unittest.main()