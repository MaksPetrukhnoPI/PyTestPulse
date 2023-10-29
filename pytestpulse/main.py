from unit_test_executor import execute
import report_format
test_path = "/Users/maksimus/IdeaProjects/PyTestPulse/unit_tests"

execute(test_path, report_format.JsonFormat(), True)
# from test_report import TestReport
# import json
# import re

# test_string = """
# test_multiplication (test_fail.FailingTest) ... FAIL
# test_zero_division_error_is_thrown (test_fail.FailingTest) ... FAIL
#
# ======================================================================
# FAIL: test_multiplication (test_fail.FailingTest)
# ----------------------------------------------------------------------
# Traceback (most recent call last):
#   File "/Users/maksimus/IdeaProjects/PyTestPulse/unit_tests/test_fail.py", line 5, in test_multiplication
#     self.assertEqual(5 * 5, 35)
#     File "/Users/maksimus/IdeaProjects/PyTestPulse/unit_tests/test_fail.py", line 5, in test_multiplication
#     self.assertEqual(5 * 5, 35)
#     File "/Users/maksimus/IdeaProjects/PyTestPulse/unit_tests/test_fail.py", line 5, in test_multiplication
#     self.assertEqual(5 * 5, 35)
#     File "/Users/maksimus/IdeaProjects/PyTestPulse/unit_tests/test_fail.py", line 5, in test_multiplication
#     self.assertEqual(5 * 5, 35)
# AssertionError: 25 != 35
#
# ======================================================================
# FAIL: test_zero_division_error_is_thrown (test_fail.FailingTest)
# ----------------------------------------------------------------------
# Traceback (most recent call last):
#   File "/Users/maksimus/IdeaProjects/PyTestPulse/unit_tests/test_fail.py", line 8, in test_zero_division_error_is_thrown
#     var = 1 / 1
# AssertionError: ZeroDivisionError not raised
#
# ----------------------------------------------------------------------
# Ran 2 tests in 0.000s
#
# FAILED (failures=2)
# """
# test_result = {}
# passed_tests = re.findall("(.*)... ok", test_string)
# failed_tests = re.findall("(.*)... FAIL", test_string)
# tests_time = float(re.findall("tests in (.*?)s", test_string)[0])
# tests_status = re.findall(r"\bFAILED|OK\b", test_string)[0]
# passed = []
# for test in passed_tests:
#     passed.append(test.strip())
# test_result['passed_tests'] = passed
#
# failed = []
# for test in failed_tests:
#     stripped = test.strip()
#     cause = re.findall(rf"FAIL: {re.escape(stripped)}\n-+\n(.*?)\n\n", test_string, re.DOTALL)[0]
#     failed.append({stripped: cause})
# test_result['failed_tests'] = failed
# test_report = TestReport(test_result, tests_time, tests_status)
# print(json.dumps(test_report.__dict__,indent=4))
# print(tests_time)
# print(tests_status)

