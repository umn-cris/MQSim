import csv
import sys
from datetime import datetime

def transform_format(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile, delimiter=' ')

        for line_number, row in enumerate(reader, start=1):
            try:
                asu, lba, block_size_bytes, rw, timestamp = row[0], int(row[1]), int(row[2]), row[3], float(row[4])

                # Convert block size from bytes to kilobytes (rounded up to the nearest integer)
                block_size_in_kb = (block_size_bytes + 1023) // 1024

                # Convert timestamp to milliseconds
                timestamp_nanoseconds = int(timestamp * 1000000)

                # Map read (r) to 1, write (w) to 0
                request_type = 1 if rw == 'r' else 0

                # Write to the output file
                writer.writerow([timestamp_nanoseconds, 1, lba, block_size_in_kb, request_type])

            except IndexError:
                print(f"Error processing line {line_number}: {row}")
                # Optionally, you can continue processing other lines or exit the loop.

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python trans_trace.py input_trace output_trace")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    transform_format(input_file, output_file)
    print(f"Transformation complete. Output written to {output_file}")
