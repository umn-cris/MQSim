# This script transforms the trace file format from the SPC format to the format
# used by the MQSim simulator. -asu follows by the list of ASUs to output.

# Usage:
#     python3 trans_trace.py <input_trace_file> <output_trace_file_prefix> -asu <asu_list>
# Exaple:
#     cd traces/real_trace_files
#     python3 ../trans_trace.py Financial/Financial1.spc Financial/fin1_ascii -asu 0-23
#     python3 ../trans_trace.py Financial/Financial1.spc Financial/fin1_ascii -asu 0-2,5,7

import csv
import sys
import argparse
from datetime import datetime

def transform_format(input_file, output_prefix, selected_asu_set):
    output_files = {}

    for asu in selected_asu_set:
        output_file = f"{output_prefix}_asu{asu}"
        output_files[asu] = open(output_file, 'w', newline='')
        output_files[asu].writer = csv.writer(output_files[asu], delimiter=' ')

    with open(input_file, 'r') as infile:
        reader = csv.reader(infile)

        for line_number, row in enumerate(reader, start=1):
            try:
                asu, lba, block_size_bytes, rw, timestamp = row[0], int(row[1]), int(row[2]), row[3], float(row[4])
                if asu in selected_asu_set:
                    # Convert block size from bytes to sectors (rounded up to the nearest integer)
                    block_size_in_sector = (block_size_bytes + 511) // 512

                    # Convert timestamp to milliseconds
                    timestamp_nanoseconds = int(timestamp * 1000000)

                    # Map read (r) to 1, write (w) to 0
                    request_type = 1 if rw == 'r' else 0

                    # Write to the output file
                    output_files[asu].writer.writerow([timestamp_nanoseconds, 1, lba, block_size_in_sector, request_type])

            except IndexError:
                print(f"Error processing line {line_number}: {row}")
                # Optionally, you can continue processing other lines or exit the loop.

    for asu, output_file in output_files.items():
        output_file.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Transform trace file format.')
    parser.add_argument('input_trace', help='Path to the input trace file')
    parser.add_argument('output_prefix', help='Prefix for the output trace files')
    parser.add_argument('-asu', type=str, help='Comma-separated list or range of ASUs to include')

    args = parser.parse_args()

    if not args.asu:
        print("Error: -asu is required.")
        sys.exit(1)

    selected_asu_set = set()

    # Process the -asu argument to create the set of selected ASUs
    asu_ranges = args.asu.split(',')
    for asu_range in asu_ranges:
        if '-' in asu_range:
            start, end = map(int, asu_range.split('-'))
            selected_asu_set.update(range(start, end + 1))
        else:
            selected_asu_set.add(int(asu_range))

    selected_asu_set_as_strings = {str(asu) for asu in selected_asu_set}

    transform_format(args.input_trace, args.output_prefix, selected_asu_set_as_strings)
    print(f"Transformation complete. Output files written with prefix {args.output_prefix}_asu")
