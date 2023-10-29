import unittest

class FailingTest(unittest.TestCase):
    def test_multiplication(self):
        self.assertEqual(5 * 5, 35)
    def test_zero_division_error_is_thrown(self):
        with self.assertRaises(ZeroDivisionError):
            var = 1 / 1