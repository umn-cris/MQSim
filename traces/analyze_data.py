# This script analyze the input spc files based on the asu number. It counts the number 
# of read and write requests for each asu and plot two graphs: percentage of rw requests per asu,
# and number of rw requests per asu.
# Sample usage:
#    cd real_trace_files
#    python3 analyze_asu.py UMassFinancial/Financial1.spc ../graphs/fin1 png

import csv
import sys
import os
import matplotlib.pyplot as plt

def analyze_asu(input_file, output_graph, extension):
    asu_data = {}

    with open(input_file, 'r') as infile:
        reader = csv.reader(infile)

        for row in reader:
            try:
                asu, lba, _, rw, timestamp = map(str.strip, row)

                if asu not in asu_data:
                    asu_data[asu] = {'total_records': 0, 'read_lba': [], 'write_lba': [], 'write_count': 0, 'read_count': 0, 'read_timestamps': [], 'write_timestamps': []}

                asu_data[asu]['total_records'] += 1

                if rw == 'W' or rw == 'w':
                    asu_data[asu]['write_count'] += 1
                    asu_data[asu]['write_lba'].append(lba)
                    asu_data[asu]['write_timestamps'].append(float(timestamp))
                elif rw == 'R' or rw == 'r':
                    asu_data[asu]['read_count'] += 1
                    asu_data[asu]['read_lba'].append(lba)
                    asu_data[asu]['read_timestamps'].append(float(timestamp))
            except ValueError:
                print("Invalid row format: " + str(row))
                continue

    for asu, data in asu_data.items():
        total_records = data['total_records']
        read_percentage = (data['read_count'] / total_records) * 100 
        write_percentage = (data['write_count'] / total_records) * 100 

        print(f"[asu={asu}, {total_records} records, read={read_percentage:.2f}%, write={write_percentage:.2f}%]")

    plot_histogram(asu_data, output_graph, extension)

def plot_histogram(asu_data, output_graph, extension):
    asu_numbers = list(asu_data.keys())

    read_percentages = [(data['read_count'] / data['total_records']) * 100 for data in asu_data.values()]
    write_percentages = [(data['write_count'] / data['total_records']) * 100 for data in asu_data.values()]
    
    read_counts = [data['read_count'] for data in asu_data.values()]
    write_counts = [data['write_count'] for data in asu_data.values()]

    plot_and_save(asu_numbers, read_percentages, write_percentages, output_graph, '_pct', 'Percentage', extension)
    plot_and_save(asu_numbers, read_counts, write_counts, output_graph, '_cnt', 'Count', extension)

    # plt.show()

def plot_and_save(asu_numbers, read_values, write_values, output_graph, suffix, ylabel, extension):
    plt.bar(asu_numbers, read_values, color='blue', label='Read Requests', alpha=0.7)
    plt.bar(asu_numbers, write_values, color='green', label='Write Requests', alpha=0.7, bottom=read_values)

    plt.title(f'{os.path.splitext(input_file)[0]} - ASU Requests Distribution {ylabel}')
    plt.xlabel('ASU Number')
    plt.ylabel(ylabel)
    plt.legend()
    plt.savefig(f'{os.path.splitext(output_graph)[0]}{suffix}.{extension}')

    plt.clf()
    

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python analyze_asu.py input_file output_graph extension")
        sys.exit(1)

    input_file = sys.argv[1]
    output_graph = sys.argv[2]
    extension = sys.argv[3]

    analyze_asu(input_file, output_graph, extension)
