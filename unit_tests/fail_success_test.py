import unittest
print(dir('fail_success_tests'))

class FaiSuccessTests(unittest.TestCase):
    def test_multiplication(self):
        self.assertEqual(5 * 5, 25)
    def test_zero_division_error_is_thrown(self):
        with self.assertRaises(ZeroDivisionError):
            var = 1 / 1
    def bar(self):
        print('bar')