# This script plots the timestamp vs PId to show the active time of each PId.
# Sample usage:
#    cd trace/real_trace_files
#    python3 ../plot_active_time_blkparse.py ycsb_rocksdb/ssdtrace-00 ../../graphs/0120-rocksdb-active-00.pdf ssdtrace.cfg

import csv
import matplotlib.pyplot as plt
import argparse
import os
import json
import logging, sys
import matplotlib.patches as mpatches

logging.basicConfig(stream=sys.stderr, level=logging.ERROR)

def plot_time_series(input_file, output_file, config):
    colors = ['b', 'g', 'c']
    pid_data = {}
    consecutive_state = {}  # Dictionary to store consecutive state for each PID
    # define the threshold for consecutive writes
    # when a pid has a write request, and it's not in consecutive state,
    # set the *begin_timestamp*, and this pid is in consecutive state.
    # Once the next write request of the same pid comes in, this pid will be in consecutive state.
    # Check if the timestamp difference between incoming timestamp and lastest write timestamp
    # is less than *threshold_in_ns*.
    # If yes, then it's a consecutive write, update latest write, then wait for the next write request.
    # If no, then set *end_timestamp*, this pid leaves consecutive state.
    threshold_in_ns = int(config['active_pid_threshold_in_ns'])
    threshold_in_sec = threshold_in_ns / 1000000000
    # After a pid has `countdown` number of consecutive writes, it will be considered as active.
    default_active_countdown = config['active_state_countdown']
    temp_begin_timestamp = 0


    with open(input_file, 'r') as infile:
        reader = csv.reader(infile, delimiter=' ')
        # total_lines = sum(1 for _ in reader)
        # infile.seek(0)  # Reset file pointer to the beginning

        # Calculate the target number of lines based on the given percentage
        # target_lines = int(config['percentage'] * total_lines / 100)



        for i, row in enumerate(reader):

            # Remove empty elements from the row
            row = [value for value in row if value != '']

            try:
                _, _, _, timestamp, pid, _, rw, lba, _, size_in_sector, _ = map(str.strip, row)

            except ValueError:
                logging.error("Invalid row format: " + str(row))
                continue

            if pid not in pid_data:
                consecutive_state[pid] = {'in_consecutive_state': False, 'state_countdown': default_active_countdown, 'last_write_timestamp': 0}
                if int(pid) in config['active_pid_list']['write_intensive']['pid_list']:
                    pid_data[pid] = {'type': 'write_intensive', 'consecutive_write': {'begin_timestamps':[], 'end_timestamps':[]}}
                elif int(pid) in config['active_pid_list']['read_write']['pid_list']:
                    pid_data[pid] = {'type': 'read_write', 'consecutive_write': {'begin_timestamps':[], 'end_timestamps':[]}}
                else:
                    continue

            timestamp = float(timestamp)

            if rw in {'W', 'WS', 'WFS', 'WM'}:
                time_difference = timestamp - consecutive_state[pid]['last_write_timestamp']
                
                if consecutive_state[pid]['in_consecutive_state'] == True:
                    if time_difference > threshold_in_sec:
                        # Consecutive state ended, update end timestamp
                        logging.debug(pid + " leave consecutive_state, difference: " + str(time_difference))
                        pid_data[pid]['consecutive_write']['end_timestamps'].append(consecutive_state[pid]['last_write_timestamp'])
                        consecutive_state[pid]['in_consecutive_state'] = False
                    else:
                        # Consecutive write, update latest write timestamp
                        logging.debug(pid + " remain consecutive_state, difference: " + str(time_difference))
                        consecutive_state[pid]['last_write_timestamp'] = timestamp
                else:
                    if consecutive_state[pid]['state_countdown'] == default_active_countdown:
                        logging.debug(pid + " start countdown" + str(timestamp))
                        consecutive_state[pid]['state_countdown'] -= 1
                        temp_begin_timestamp = timestamp

                    elif time_difference < threshold_in_sec:

                        if consecutive_state[pid]['state_countdown'] > 0:
                            consecutive_state[pid]['state_countdown'] -= 1
                            logging.debug(pid + " countdown = " + str(consecutive_state[pid]['state_countdown']))

                        else: # not in consecutive state and countdown has been reached
                            logging.debug(pid + " enter consecutive_state" + str(timestamp))
                            pid_data[pid]['consecutive_write']['begin_timestamps'].append(temp_begin_timestamp)
                            consecutive_state[pid]['last_write_timestamp'] = timestamp
                            consecutive_state[pid]['in_consecutive_state'] = True
                            consecutive_state[pid]['state_countdown'] = default_active_countdown

                    else: # not in consecutive state and time difference is greater than threshold
                        consecutive_state[pid]['state_countdown'] = default_active_countdown
                        logging.debug(pid + " stop countdown, difference in second: " + str(time_difference))
                
                consecutive_state[pid]['last_write_timestamp'] = timestamp

            else:
                continue # skip read requests

            # Break out of the loop if we've reached the target number of lines or end of file
            # if i + 1 >= target_lines:
            #     break

        

        # Check if  the number of consecutive state begin and end are the same
        for pid, data in pid_data.items():
            if len(data['consecutive_write']['begin_timestamps']) != len(data['consecutive_write']['end_timestamps']):
                data['consecutive_write']['begin_timestamps'] = data['consecutive_write']['begin_timestamps'][:-1]
                logging.debug("Number of consecutive state begin and end are not the same for pid: " + pid)
                logging.debug("Number of consecutive state begin: " + str(len(data['consecutive_write']['begin_timestamps'])))
                logging.debug("Number of consecutive state end: " + str(len(data['consecutive_write']['end_timestamps'])))
                logging.debug("Begin timestamps: " + str(data['consecutive_write']['begin_timestamps']))
                logging.debug("End timestamps: " + str(data['consecutive_write']['end_timestamps']))


    plt.figure(figsize=(25, 12))
    legend_patches = [mpatches.Patch(color=colors[0], label='write_intensive'),mpatches.Patch(color=colors[1], label='read_write')]  # List to store proxy artists for the legend


    for i, (pid, data) in enumerate(pid_data.items()):
        
        color = colors[0] if data['type'] == 'write_intensive' else colors[1]

        pid_array = [pid] * len(data['consecutive_write']['begin_timestamps'])

        plt.scatter(data['consecutive_write']['begin_timestamps'], pid_array, marker='+', color=color)

        plt.scatter(data['consecutive_write']['end_timestamps'], pid_array, marker='.', color=color)

        # Connect begin_timestamps with end_timestamps using lines
        for begin, end in zip(data['consecutive_write']['begin_timestamps'], data['consecutive_write']['end_timestamps']):
            plt.plot([begin, end], [pid, pid], color=color)


    # Add legend with proxy artists
    plt.legend(handles=legend_patches)

    plt.title(f'{os.path.splitext(input_file)[0]} - Time Series Plot of Active Consecutive Writes Requests')
    plt.xlabel('Timestamp')
    plt.ylabel('PID')
    plt.legend(handles=legend_patches)
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

    with open(args.config_file, 'r') as cfg_file:
        config = json.load(cfg_file)
        plot_time_series(args.input_file, args.output_file, config)
        print(f"Time series plot saved to {args.output_file}")

