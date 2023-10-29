import unittest


@unittest.skip
class TestExample(unittest.TestCase):
    def test_success_1(self):
        self.assertEqual(1, 1)

    def test_failure_1(self):
        self.assertEqual(1, 2)  # This will fail

    def test_failure_2(self):
        self.assertEqual(3, 4)  # This will fail

    def test_failure_3(self):
        self.assertEqual(5, 6)  # This will fail

    def test_failure_4(self):
        self.assertEqual(7, 8)  # This will fail

    def test_success_6(self):
        self.assertEqual(6, 6)

    def test_success_7(self):
        self.assertEqual(7, 7)

    def test_success_8(self):
        self.assertEqual(8, 8)

    def test_success_9(self):
        self.assertEqual(9, 9)

    def test_success_10(self):
        self.assertEqual(10, 10)

    def test_failure_5(self):
        self.assertEqual(9, 10)  # This will fail

    def test_failure_6(self):
        self.assertEqual(11, 12)  # This will fail

    def test_success_2(self):
        self.assertEqual(2, 2)

    def test_success_3(self):
        self.assertEqual(3, 3)

    def test_success_4(self):
        self.assertEqual(4, 4)

    def test_success_5(self):
        self.assertEqual(5, 5)

    def test_failure_7(self):
        self.assertEqual(13, 14)  # This will fail

    def test_failure_8(self):
        self.assertEqual(15, 16)  # This will fail

    def test_failure_9(self):
        self.assertEqual(17, 18)  # This will fail

    def test_failure_10(self):
        self.assertEqual(19, 20)  # This will fail

    def test_failure_11(self):
        self.assertEqual(21, 22)  # This will fail

    def test_failure_12(self):
        self.assertEqual(23, 24)  # This will fail

    def test_failure_13(self):
        self.assertEqual(25, 26)  # This will fail

    def test_failure_14(self):
        self.assertEqual(27, 28)  # This will fail

    def test_failure_15(self):
        self.assertEqual(29, 30)  # This will fail
