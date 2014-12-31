__author__ = 'keith'

import argparse
import os
import csv
import sys

import pypred


get_elements = lambda search_list, indices: [search_list[i] for i in indices]


class ZipCodes:
    def __init__(self):
        self.input_file_path = None
        self.requested_fields = []
        self.zip_code_field = 'zip'
        self.predicate = None

        self.available_fields = ()
        self.export_indices = []
        self.export_fields = []

        self.parse_args()

    def parse_args(self):
        # create the argument parser
        parser = argparse.ArgumentParser(description='This program will extract a subset of zip code data from an '
                                                     'input file and export it to another file',
                                         add_help=True)

        # add an argument for the input file
        parser.add_argument('--input-file',
                            help='path to the zip code input file (should be in CSV format)',
                            required=True,
                            action='store')

        parser.add_argument('--fields',
                            help='comma-separated list of fields to be exported',
                            required=False,
                            action='store')

        parser.add_argument('--zip-code-field',
                            help='the name of the field containing the zip code',
                            required=False,
                            action='store',
                            default='zip')

        parser.add_argument('--predicate',
                            help='Boolean expression to filter out unwanted data (only matches will be exported)',
                            required=False,
                            action='store')

        # parse the arguments
        args = parser.parse_args()

        # get the input file path
        self.input_file_path = args.input_file
        if not os.path.exists(self.input_file_path):
            raise Exception('File not found: {}'.format(self.input_file_path))
        if os.path.isdir(self.input_file_path):
            raise Exception('Input file must be an actual file, not a directory')

        # get the list of fields to export
        if args.fields is not None:
            self.requested_fields = args.fields.split(',')

        # get the name of the field containing the zip code
        self.zip_code_field = args.zip_code_field

        # get the predicate if there is one
        if args.predicate is not None:
            self.predicate = pypred.Predicate(args.predicate)

    def load(self):
        print 'Reading Zip Codes from {}...'.format(self.input_file_path)

        print self.predicate.description()
        print self.predicate.is_valid()

        with open(self.input_file_path) as f:
            # process the first row as the header
            self.process_header(f.readline())

            # use a CSV Dictionary Reader for the rest of file
            reader = csv.DictReader(f, self.available_fields)
            try:
                for row in reader:
                    if self.predicate is not None and self.predicate.evaluate(row):
                        self.process_row(row)
            except csv.Error as e:
                sys.exit('file %s, line %d: %s' % (self.input_file_path, reader.line_num, e))

    def process_header(self, line):
        self.available_fields = line.split(',')
        print 'Available fields: {}'.format(', '.join(self.available_fields))

        if self.zip_code_field not in self.available_fields:
            raise Exception('The required zip code field "{}" is not one of the available fields'.
                            format(self.zip_code_field))

        if len(self.requested_fields) == 0:
            # export all fields
            self.export_indices = range(len(self.available_fields))
            print 'All available fields will be exported'
        else:
            for field in self.requested_fields:
                if field in self.available_fields:
                    self.export_indices.append(self.available_fields.index(field))
                else:
                    print 'Field "{}" is not available for export and will be ignored'.format(field)

            if len(self.export_indices) > 0:
                self.export_fields = get_elements(self.available_fields, self.export_indices)
                print 'The following fields will be exported: {}'.format(', '.join(self.export_fields))
            else:
                print 'All available fields will be exported'

    def process_row(self, row):
        zip_code_record = {k: row[k] for k in self.export_fields}

        print zip_code_record

    def export(self):
        pass


if __name__ == '__main__':
    zips = ZipCodes()
    zips.load()
    zips.export()