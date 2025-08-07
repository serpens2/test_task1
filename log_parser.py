import argparse
import ast
import copy
from tabulate import tabulate

class LogParser:
    def __init__(self, file_paths: list[str,...]):
        self.file_paths = file_paths
    def make_report(self, group_by: str, report_name: str = None,
                    date: str = None, show_count: bool = True,
                    avg_fields: tuple[str,...] = (), min_fields: tuple[str,...] = (),
                    max_fields: tuple[str,...] = ()):
        """
        group_by is a field by which we're grouping the data (accepts only one field)
        report_name is a name of the output .txt file. If not provided, file is not created.
        date is a string in the form yyyy-mm-dd representing date constraint
        show_count = False will remove number of occurrences of each field from the report
        arguments to avg_fields, min_fields etc. should always be provided as tuples, even if its just one field
        """
        required_fields = tuple( set( avg_fields + min_fields + max_fields ) )
        if show_count == False and not any(required_fields):
            print('No fields were chosen to display')
            return None
        template = {}
        if show_count:
            template['count'] = 0
        for field in required_fields:
            template[field] = []
        report = {}
        for file_path in self.file_paths:
            with open(file_path,'r') as file:
                flag = True
                for line in file:
                    entry = ast.literal_eval(line)
                    if date:
                        flag = entry['@timestamp'].split('T')[0] == date
                    if flag:
                        if report.get( entry[group_by] ) is None:
                            report[entry[group_by]] = copy.deepcopy(template)
                        if show_count:
                            report[entry[group_by]]['count'] += 1
                        for field in required_fields:
                            report[entry[group_by]][field].append( float(entry[field]) )
        if not any(report):
            print('No data entries satisfy date constraint')
            return None
        for key in report:
            for avg_field in avg_fields:
                report[key]['avg ' + avg_field] = sum( report[key][avg_field] ) / len( report[key][avg_field] )
            for min_field in min_fields:
                report[key]['min ' + min_field] = min( report[key][min_field] )
            for max_field in max_fields:
                report[key]['max ' + max_field] = max( report[key][max_field] )
            for field in required_fields:
                del report[key][field]

        table_data = [ [key] + [ report[key][inner_key] for inner_key in report[key] ] for key in report ]
        headers = [group_by] + list(report[list(report.keys())[0]].keys())
        table_string = tabulate( table_data, headers=headers )
        print( table_string )

        if report_name:
            with open(report_name + '.txt','w') as file:
                file.write(table_string)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, nargs='+', required=True,
                        help='Path to log file (multiple paths are allowed)')
    parser.add_argument('--report', type=str, required=False,
                        help='Name of report file (optional)')
    parser.add_argument('--date', type=str, required=False,
                        help='Use only entries with given date (yyyy-mm-dd)')
    args = parser.parse_args()
    log_parser = LogParser(file_paths=args.file)
    log_parser.make_report(group_by="url", report_name=args.report, date=args.date,
                           avg_fields=("response_time",), max_fields=("response_time",))