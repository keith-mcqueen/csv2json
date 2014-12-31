csv2json
========
Will export fields from a CSV file to a JSON file.

Usage
=====
csv2json accepts the following arguments:

| argument (short) | argument (long) | description |
|------------------|-----------------|-------------|
| -h               | --help         | Prints a message describing the arguments and their usage |
| -i INPUT FILE    | --input INPUT FILE | **Required** The path to the input file (CSV format) |
| -o OUTPUT FILE   | --output OUTPUT FILE | **Required** The path to the output file (JSON format).  This file will be overwritten if it exists. |
| -n NUM ROWS      | --num-rows NUM ROWS | *Optional* The maximum number of rows to be exported.  If the value is less than 0, then all rows will be exported (default).  If the value is greater than 0 then no more than that value will be exported.  If the value is 0, then no rows will be exported, but the header row will be read and parsed. |
| -f FIELDS        | --fields FIELDS | *Optional* A comma-separated list of field names that should be exported.  If this argument is ommitted (default) or none of the requested fields actually appear in the header, then all fields will be exported, otherwise only the requested fields will be exported. |
| -c CONDITION     | --condition CONDITION | *Optional* A 'natural language' predicate string that can be used to export only the rows matching the predicate.  For example, if dealing with a file with U.S. zip codes, it may be that you only want zip codes for a certain state.  In this case you could supply a condition like "state is 'CO'". |
