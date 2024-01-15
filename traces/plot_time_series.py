import csv
import sys
import matplotlib.pyplot as plt
import argparse
import os

def plot_time_series(input_file, output_file, asu_list, percentage):
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']  # Add more colors as needed
    asu_data = {}
    print(asu_list)

    with open(input_file, 'r') as infile:
        reader = csv.reader(infile)
        total_lines = sum(1 for _ in reader)
        infile.seek(0)  # Reset file pointer to the beginning

        # Calculate the target number of lines based on the given percentage
        target_lines = int(percentage * total_lines / 100)

        for i, row in enumerate(reader):
            if i % 10 != 0:
                continue
            asu, lba, _, rw, timestamp = map(str.strip, row)
            lba = int(lba)
            timestamp = float(timestamp)

            if asu not in asu_data:
                asu_data[asu] = {'write': {'timestamps': [], 'lbas': []}, 'read': {'timestamps': [], 'lbas': []}}

            if rw.lower() == 'w':
                asu_data[asu]['write']['timestamps'].append(timestamp)
                asu_data[asu]['write']['lbas'].append(lba)
            elif rw.lower() == 'r':
                asu_data[asu]['read']['timestamps'].append(timestamp)
                asu_data[asu]['read']['lbas'].append(lba)

            # Break out of the loop if we've reached the target number of lines or end of file
            if i + 1 >= target_lines:
                break

    plt.figure(figsize=(30, 6)) 
    color_num = 0
    for i, (asu, data) in enumerate(asu_data.items()):
        if '-' in asu:
            start, end = map(int, asu.split('-'))
            if int(asu_list[0]) not in range(start, end + 1):
                continue
        elif int(asu) not in asu_list:
            continue

        color = colors[color_num]
        color_num += 1

        total_records = len(data['write']['timestamps']) + len(data['read']['timestamps'])
        write_percentage = (len(data['write']['timestamps']) / total_records) * 100
        read_percentage = (len(data['read']['timestamps']) / total_records) * 100

        # Plot write requests with solid lines
        plt.scatter(data['write']['timestamps'], data['write']['lbas'], marker='+', color=color, label=f'ASU={asu} {write_percentage:.2f}% Write')

        # Plot read requests with solid lines
        plt.scatter(data['read']['timestamps'], data['read']['lbas'], marker='.', color=color, label=f'ASU={asu} {read_percentage:.2f}% Read')

    plt.title(f'{os.path.splitext(input_file)[0]} - Time Series Plot of Read and Write Requests (First {percentage}%)')
    plt.xlabel('Timestamp')
    plt.ylabel('Logical Block Address (LBA)')
    plt.legend()
    plt.grid(True)
    plt.savefig(output_file)
    # plt.show()
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot time series of read and write requests for specified ASUs.')
    parser.add_argument('input_file', help='Path to the input file')
    parser.add_argument('output_file', help='Path to save the output graph')
    parser.add_argument('-asu', nargs='+', type=str, help='List of ASUs to plot (e.g., 10-14)')
    parser.add_argument('-pct', type=float, help='Percentage of data to plot')

    args = parser.parse_args()

    if not args.asu or not args.pct:
        print("Error: Both -asu and -pct are required.")
        sys.exit(1)

    asu_list = []
    for asu_item in args.asu:
        if '-' in asu_item:
            start, end = map(int, asu_item.split('-'))
            asu_list.extend(range(start, end + 1))
        else:
            asu_list.append(int(asu_item))

    plot_time_series(args.input_file, args.output_file, asu_list, args.pct)
    print(f"Time series plot saved to {args.output_file}")
