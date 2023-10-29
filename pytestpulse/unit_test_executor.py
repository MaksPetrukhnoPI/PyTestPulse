# python -m unittest -v unit_tests/test_success.py
import os
import re
import subprocess
from logger import logger
from tests_report import TestsReport


def execute(path, report_formatter=None, save_to_file=False, reports_save_dir=os.getcwd()):
    unit_tests_files = find_unit_tests_files(path)
    if unit_tests_files:
        reports = []
        for file in unit_tests_files:
            output, errors = execute_unit_tests(file)
            formatted_report = format_report(errors, report_formatter, file)
            reports.append(formatted_report)
        if save_to_file:
            save_reports_to_file(report_formatter, reports, reports_save_dir)


def find_unit_tests_files(path):
    os.chdir(path)
    logger.info('Searching for tests...')
    unit_tests = [f for f in os.listdir() if re.match("^(test_.*|.*_test)\.py$", f)]
    if not unit_tests:
        logger.error('Could not find unit tests in specified directory')
        return None
    return unit_tests


def execute_unit_tests(file):
    logger.info(f'Executing tests in {file}...')
    command = ["python", "-m", "unittest", "-v", file]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process.communicate()


def format_report(errors, report_formatter, file):
    if report_formatter is None:
        formatted_report = errors.decode('UTF-8')
        logger.info(formatted_report)
        return formatted_report
    report = _parse_report(errors.decode('UTF-8'), file)
    formatted_report = report_formatter.format_report(report)
    report_formatter.display_formatted_report(formatted_report)
    return formatted_report


def save_reports_to_file(report_formatter, formatted_reports, save_dir):
    if report_formatter:
        report_formatter.save_to_file(formatted_reports, save_dir)
    else:
        with open(f"{save_dir}/pytestpulse_report.txt", 'w') as f:
            f.write('\n\n'.join(formatted_reports))


def _parse_report(output, file):
    logger.info('Parsing test report...')
    passed_tests = re.findall("(.*)... ok", output)
    failed_tests = re.findall("(.*)... FAIL", output)
    tests_time = float(re.findall("tests in (.*?)s", output)[0])
    tests_status = re.findall(r"\bFAILED|OK\b", output)[0]
    tests_result = _parse_tests_result(output, passed_tests, failed_tests)
    return TestsReport(tests_file_name=file, tests_result=tests_result, tests_exec_time=tests_time, tests_status=tests_status)


def _parse_tests_result(output, passed_tests, failed_tests):
    def find_failed_test_cause(test):
        return re.findall(rf"FAIL: {re.escape(test.strip())}\n-+\n(.*?)\n\n", output, re.DOTALL)[0]

    return {
        'passed_tests': [test.strip() for test in passed_tests],
        'failed_tests': [
            {test.strip(): find_failed_test_cause(test.strip())}
            for test in failed_tests
        ]
    }
