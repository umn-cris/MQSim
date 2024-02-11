# This script plots the timestamp vs LBA graph for the specified PIDs requests of blkparse output format.
# Sample usage:
#    cd trace/real_trace_files
#    python3 ../plot_time_series.py ycsb_rocksdb/ssdtrace-00 ../../graphs/0118-rocksdb-00.pdf ssdtrace.cfg
# Note: Change `color` accordingly to the number of PIDs you want to plot.
#       By default, 7 colors are available.

import csv
import sys
import matplotlib.pyplot as plt
import argparse
import os
import json

def plot_time_series(input_file, output_file, config_file):
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']  # Add more colors as needed
    pid_data = {}
    
    with open(config_file, 'r') as cfg_file:
        config = json.load(cfg_file)

    with open(input_file, 'r') as infile:
        reader = csv.reader(infile, delimiter=' ')
        total_lines = sum(1 for _ in reader)
        infile.seek(0)  # Reset file pointer to the beginning

        # Calculate the target number of lines based on the given percentage
        target_lines = int(config['percentage'] * total_lines / 100)

        for i, row in enumerate(reader):
            # if i % 10 != 0:
            #     continue

            # Remove empty elements from the row
            row = [value for value in row if value != '']

            try:
                _, _, _, timestamp, pid, _, rw, lba, _, size_in_sector, _ = map(str.strip, row)

            except ValueError:
                print("Invalid row format: " + str(row))
                continue


            if pid not in str(config['pid_list']):
                continue

            lba = int(lba)
            timestamp = float(timestamp)

            if pid not in pid_data:
                pid_data[pid] = {'write': {'timestamps': [], 'lbas': []}, 'read': {'timestamps': [], 'lbas': []}}

            if 'D' in row:  # Assuming 'D' indicates a disk request
                if config['plot_write'] and 'W' in row or 'WS' in row or 'WFS' in row or 'WM' in row:
                    pid_data[pid]['write']['timestamps'].append(timestamp)
                    pid_data[pid]['write']['lbas'].append(lba)
                elif config['plot_read'] and 'R' in row or 'RS' in row:
                    pid_data[pid]['read']['timestamps'].append(timestamp)
                    pid_data[pid]['read']['lbas'].append(lba)

            # Break out of the loop if we've reached the target number of lines or end of file
            if i + 1 >= target_lines:
                break

    plt.figure(figsize=(30, 6)) 
    color_num = 0
    for i, (pid, data) in enumerate(pid_data.items()):

        color = colors[color_num]
        color_num = (color_num + 1) % len(colors) 

        total_records = len(data['write']['timestamps']) + len(data['read']['timestamps'])
        write_percentage = (len(data['write']['timestamps']) / total_records) * 100
        read_percentage = (len(data['read']['timestamps']) / total_records) * 100

        if config['plot_write']:
            plt.scatter(data['write']['timestamps'], data['write']['lbas'], marker='+', color=color, label=f'pid={pid} {write_percentage:.2f}% Write')

        if config['plot_read']:
            plt.scatter(data['read']['timestamps'], data['read']['lbas'], marker='.', color=color, label=f'pid={pid} {read_percentage:.2f}% Read')

    plt.title(f'{os.path.splitext(input_file)[0]} - Time Series Plot of Read and Write Requests (First {config["percentage"]}%)')
    plt.xlabel('Timestamp')
    plt.ylabel('Logical Block Address (LBA)')
    plt.legend(bbox_to_anchor=(1, 0.5))
    plt.grid(True)
    plt.savefig(output_file)
    # plt.show()
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot time series of read and write requests for specified pids.')
    parser.add_argument('input_file', help='Path to the input file')
    parser.add_argument('output_file', help='Path to save the output graph')
    parser.add_argument('config_file', help='Path to the configuration file')

    args = parser.parse_args()

    plot_time_series(args.input_file, args.output_file, args.config_file)
    print(f"Time series plot saved to {args.output_file}")
