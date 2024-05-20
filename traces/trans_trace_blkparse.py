# Description: This script transforms the trace file format from blkparse to the format used by the simulator.
# python3 trans_trace_blkparse.py $trace_path/ssdtrace-purged-00 $trace_path/ssdtrace-ascii-00
# python3 trans_trace_blkparse.py $trace_path/ssdtrace-purged-01 $trace_path/ssdtrace-ascii-01
# python3 trans_trace_blkparse.py $trace_path/ssdtrace-purged-26 $trace_path/ssdtrace-ascii-26
import csv
import sys
import argparse

def transform_format(input_file, output_prefix):
    output_file = open(output_prefix, 'w', newline='')
    output_writer = csv.writer(output_file, delimiter=' ')

    with open(input_file, 'r') as infile:
        reader = csv.reader(infile, delimiter=' ')

        for line_number, row in enumerate(reader, start=1):
            try:
                # Remove empty elements from the row
                row = [value for value in row if value != '']

                if row[5].upper() == 'D':
                    timestamp = int(float(row[3])* 1e9)  # Convert seconds to nanoseconds
                    device_number = 1
                    lba = row[7]  # Extract LBA 
                    size_sectors = ( int(row[9]) + 511 ) // 512 # Extract size in sectors
                    request_type = 0 if row[6].upper() in {'W', 'WS'} else 1  # 0 for write, 1 for read

                    output_writer.writerow([timestamp, device_number, lba, size_sectors, request_type])

            except IndexError:
                print(f"Error processing line {line_number}: {row}")
                # Optionally, you can continue processing other lines or exit the loop.

    output_file.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Transform trace file format.')
    parser.add_argument('input_trace', help='Path to the input trace file')
    parser.add_argument('output_prefix', help='Output trace file')

    args = parser.parse_args()

    transform_format(args.input_trace, args.output_prefix)
    print(f"Transformation complete. Output file written with prefix {args.output_prefix}")
