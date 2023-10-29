import csv, json, xml.dom.minidom
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from logger import logger


class ReportFormat(ABC):
    @abstractmethod
    def format_report(self, report):
        pass

    @abstractmethod
    def display_formatted_report(self, formatted_report):
        pass

    @abstractmethod
    def save_to_file(self, formatted_reports, save_dir):
        pass


class JsonFormat(ReportFormat):
    def format_report(self, report):
        return report.__dict__

    def display_formatted_report(self, formatted_report):
        logger.info(json.dumps(formatted_report, indent=4))

    def save_to_file(self, formatted_reports, save_dir):
        with open(f"{save_dir}/pytestpulse_report.json", "w") as outfile:
            json.dump(formatted_reports, outfile, indent=4)


class XmlFormat(ReportFormat):

    def format_report(self, report):
        tests = ET.Element('tests')
        tests.set('name', report.tests_file_name)
        self.__set_tests_result(report, tests)
        self.__set_tests_status(report, tests)
        self.__set_tests_exec_time(report, tests)
        return ET.ElementTree(tests)

    def display_formatted_report(self, formatted_report):
        xml_string = ET.tostring(formatted_report.getroot(), encoding="unicode")
        pretty_xml = xml.dom.minidom.parseString(xml_string).toprettyxml()
        logger.info(pretty_xml)

    def save_to_file(self, formatted_reports, save_dir):
        report_el = ET.Element('report')
        for xml_report in formatted_reports:
            report_el.append(xml_report.getroot())
        element_tree = ET.ElementTree(report_el)
        ET.indent(element_tree, space="\t", level=0)
        element_tree.write(f"{save_dir}/pytestpulse_report.xml")

    def __set_tests_exec_time(self, report, tests):
        execution_time = ET.SubElement(tests, 'executionTime')
        execution_time.text = str(report.tests_exec_time)

    def __set_tests_status(self, report, tests):
        tests_status = ET.SubElement(tests, 'testsStatus')
        tests_status.text = report.tests_status

    def __set_tests_result(self, report, tests):
        test_results = ET.SubElement(tests, 'testResults')
        self.__set_passed_tests(report, test_results)
        self.__set_failed_tests(report, test_results)

    def __set_failed_tests(self, report, test_results):
        failed_tests = ET.SubElement(test_results, 'failedTests')
        for failed_test in report.tests_result['failed_tests']:
            element = ET.SubElement(failed_tests, 'test')
            for test, cause in failed_test.items():
                element.set('name', test)
                element.set('cause', cause)

    def __set_passed_tests(self, report, test_results):
        passed_tests = ET.SubElement(test_results, 'passedTests')
        for passed_test in report.tests_result['passed_tests']:
            element = ET.SubElement(passed_tests, 'test')
            element.set('name', passed_test)


class CsvFormat(ReportFormat):
    def format_report(self, report):
        # concat passed tests with failed
        tests = (report.tests_result['passed_tests'] +
                 list(map(lambda test: list(test)[0], report.tests_result['failed_tests'])))
        # get tests status
        tests_status = (['OK' for report in report.tests_result['passed_tests']]
                        + ['Fail' for report in report.tests_result['failed_tests']])
        # parse tests error cause
        error_cause = ([None for _ in report.tests_result['passed_tests']]
                       + list(map(lambda test: list(test.values())[0], report.tests_result['failed_tests'])))
        # return dict with tests results and its exec time
        return {
            'tests': list(zip(tests, tests_status, error_cause)),
            'execution_time': report.tests_exec_time,
        }

    def display_formatted_report(self, formatted_report):
        divider = "=" * 55 + "\n"
        # Add headers to the formatted string
        formatted_string = '\n' + divider
        formatted_string += "{:<20} | {:<10} | {:<20}\n".format('Test', 'Status', 'Error Cause')
        formatted_string += divider

        # Add tests result to the formatted string
        for test, status, error_cause in formatted_report['tests']:
            formatted_string += "{:<20} | {:<10} | {:<20}\n".format(test, status, str(error_cause).replace('\n', ' '))

        # Add execution time to the formatted string
        formatted_string += divider
        formatted_string += f'Execution time: {formatted_report["execution_time"]}\n'
        # Display formatted string
        logger.info(formatted_string)

    def save_to_file(self, formatted_reports, save_dir):
        with open(f"{save_dir}/pytestpulse_report.csv", "w", newline='') as csvfile:
            # write headers
            csv_writer = csv.DictWriter(csvfile, fieldnames=['Test', 'Status', 'Error cause'], delimiter=';')
            csv_writer.writeheader()
            csv_writer = csv.writer(csvfile, delimiter=';')
            # write all test reports to file
            csv_writer.writerows([tests for report in formatted_reports for tests in report['tests']])
            # write total execution time for all reports
            csv_writer.writerow([f'Execution Time = {sum(report["execution_time"] for report in formatted_reports)}'])
