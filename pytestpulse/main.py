import os

import report_format


# test_path = "/Users/maksimus/IdeaProjects/PyTestPulse/unit_tests"


def parse_path_command(args):
    if '-p' not in args:
        raise Exception('Path to tests directory is required')
    return args[args.index('-p') + 1]


def parse_report_format_command(args):
    if '-f' in args:
        format_argument = args[args.index('-f') + 1].lower()
        if format_argument == 'json':
            return report_format.JsonFormat()
        elif format_argument == 'xml':
            return report_format.XmlFormat()
        elif format_argument == 'csv':
            return report_format.CsvFormat()
        else:
            raise Exception('Unknown format')
    return None


def parse_save_to_file_command(args):
    return '-s' in args


def parse_save_dir_command(args):
    if '-d' in args:
        return args[args.index('-d') + 1]
    return os.getcwd()


if __name__ == "__main__":
    from pytestpulse.unit_tests_executor import execute
    import sys
    path = parse_path_command(sys.argv)
    format = parse_report_format_command(sys.argv)
    save_to_file = parse_save_to_file_command(sys.argv)
    save_dir = parse_save_dir_command(sys.argv)
    execute(path, format, save_to_file, save_dir)
