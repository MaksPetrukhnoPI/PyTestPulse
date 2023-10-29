import unittest

# Run the tests
class SuccessfulTest(unittest.TestCase):
    def test_multiplication(self):
        self.assertEqual(5 * 5, 25)
    def test_zero_division_error_is_thrown(self):
        with self.assertRaises(ZeroDivisionError):
            var = 1 / 0
    @unittest.skip
    def test_bar(self):
        print('Skipped test.')