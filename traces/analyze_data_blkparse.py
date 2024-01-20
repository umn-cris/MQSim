import csv
import sys
import os
import matplotlib.pyplot as plt

def analyze_pid(input_file, output_graph, extension):
    pid_data = {}

    with open(input_file, 'r') as infile:
        reader = csv.reader(infile, delimiter=' ')

        for row in reader:
            try:
                # Remove empty elements from the row
                row = [value for value in row if value != '']

                _, _, _, timestamp, pid, _, _, _, _, _, _ = map(str.strip, row)

                if pid not in pid_data:
                    pid_data[pid] = {'total_records': 0, 'read_count': 0, 'write_count': 0}

                pid_data[pid]['total_records'] += 1

                if 'D' in row:  # Assuming 'D' indicates a disk request
                    if 'R' in row or 'RS' in row:
                        pid_data[pid]['read_count'] += 1
                    elif 'W' in row or 'WS' in row or 'WFS' in row or 'WM' in row:
                        pid_data[pid]['write_count'] += 1

            except ValueError:
                print("Invalid row format: " + str(row))
                continue

    sorted_pid_data = dict(sorted(pid_data.items(), key=lambda item: item[1]['total_records'], reverse=True))

    for pid, data in sorted_pid_data.items():
        total_records = data['total_records']
        read_percentage = (data['read_count'] / total_records) * 100 
        write_percentage = (data['write_count'] / total_records) * 100 

        print(f"[pid={pid}, {total_records} records, read={read_percentage:.2f}%, write={write_percentage:.2f}%]")

    plot_histogram(sorted_pid_data, output_graph, extension)

def plot_histogram(pid_data, output_graph, extension):
    pid_numbers = list(pid_data.keys())

    read_percentages = [(data['read_count'] / data['total_records']) * 100 for data in pid_data.values()]
    write_percentages = [(data['write_count'] / data['total_records']) * 100 for data in pid_data.values()]

    read_counts = [data['read_count'] for data in pid_data.values()]
    write_counts = [data['write_count'] for data in pid_data.values()]

    plot_and_save(pid_numbers, read_percentages, write_percentages, output_graph, '_pct', 'Percentage', extension)
    plot_and_save(pid_numbers, read_counts, write_counts, output_graph, '_cnt', 'Count', extension)

def plot_and_save(pid_numbers, read_values, write_values, output_graph, suffix, ylabel, extension):
    plt.figure(figsize=(12, 6))
    plt.bar(pid_numbers, read_values, color='blue', label='Read Requests', alpha=0.7)
    plt.bar(pid_numbers, write_values, color='green', label='Write Requests', alpha=0.7, bottom=read_values)

    plt.title(f'{os.path.splitext(input_file)[0]} - PID Requests Distribution {ylabel}')
    plt.xlabel('PID Number')
    plt.ylabel(ylabel)
    plt.xticks(rotation='vertical')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{os.path.splitext(output_graph)[0]}{suffix}.{extension}')

    plt.clf()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python analyze_pid.py input_file output_graph extension")
        sys.exit(1)

    input_file = sys.argv[1]
    output_graph = sys.argv[2]
    extension = sys.argv[3]

    analyze_pid(input_file, output_graph, extension)
