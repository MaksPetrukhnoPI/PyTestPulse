# PyTestPulse
This is test discovery tool which searches for tests executes them and displays result, which you can run inside your python script or launch gui app in **pytestdemoapp** folder. Repository contains 3 directories pytestdemoapp, pytestpulse and unit_tests. **pytestdemoapp** is gui application for using pytestpulse tool in action. **unit_tests** folder are sample tests that you can run to see pytestpulse result.
To simply use pytestpulse tool in your python scripts:
```python
from pytestpulse.unit_tests_executor import execute
execute(path="$YOUR_PATH")
```
`execute(PATH)` function runs pytestpulse flow:

<img width="1049" alt="Снимок экрана 2023-10-30 в 14 43 17" src="https://github.com/MaksPetrukhnoPI/PyTestPulse/assets/94057303/f94ad925-e95b-401b-a3a2-5d613e138843">

pytestpulse available arguments:
| Argument      | Type          | Description          |
| ------------- | ------------- | ------------- |
| **path**(required)  | string  | Tests directory path  |
| report_format  | ReportFormat object  | Format of tests report. Default value is `None`, meaning that the format will be text. Available formats are `JsonFormat`, `XmlFormat` and `CsvFormat`  |
| save_to_file  | bool  | Whether or not tests reports should be saved to file. File will be saved with the name `pytestpulse_report.<format>`. Default value is `False` |
| save_dir  | string  | Directory where tests report should be saved. **Note:** If save_to_file is set to False then this argument has no effect. Default value is current working directory |

pytestpulse have options for formatting result report. For that case you need to pass report_format argument in execute function. For now, you can pass JsonFormat(), XmlFormat() or CsvFormat():
```python
from pytestpulse.unit_tests_executor import execute
from pytestpulse import report_format
execute("$YOUR_PATH", report_format.JsonFormat())
```
But you can also pass your own format. For that you need to override `ReportFormat` object:
```python
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
```
**Note:** format_report is the most crucial method that you need to override as display_formatted_report and save_to_file methods use value that returns format_report.
format_report takes as argument `TestReport` object:
| Argument      | Type          | Description          |
| ------------- | ------------- | ------------- |
| tests_file_name  | string  | Name of unit tests file  |
| tests_result  | dict  | Contains info about tests_result. It has two keys passed_tests and failed_tests. passed_tests is list of test's names and failed tests is dict where test's names is key and value is fail cause    |
| tests_status  | string  | Status of executed tests. Status can be `OK` or `Failed`  |
| tests_exec_time  | float  | Execution time of unit tests in file  |

Here is example how to define CsvFormat():
```python
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
                       + list(map(lambda test: list(test.values())[0].replace('\n', ''), report.tests_result['failed_tests'])))
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

```
In pytestpulse folder you can find sample reports files in json, xml and csv format.

