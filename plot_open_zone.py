# python plot_open_zone.py results/ZoneSizeReal/96MB/open_zone.log
# python plot_open_zone.py results/ZoneSizeReal/96MB/open_zone.log
# Too many x-axis datapoint. This script won't finish.
import matplotlib.pyplot as plt
import sys

# Check if the filename argument is provided
if len(sys.argv) < 2:
    print("Usage: python plot_open_zone.py open_zone.log")
    sys.exit(1)

# Read the contents of the open_zone.log file
filename = sys.argv[1]
with open(filename, 'r') as file:
    lines = file.readlines()

# Initialize lists to store zone_ids and request_ids
zone_ids = []
request_ids = []

# Process each line in the file
for line in lines:
    # Split the line into zone_ids
    zone_list = line.strip().split()
    # Convert zone_ids to integers
    zone_list = list(map(int, zone_list))
    # Add zone_ids to the list
    zone_ids.append(zone_list)

# Plotting
fig, ax = plt.subplots()

# Plotting each zone's request_ids
for i, zone_list in enumerate(zone_ids):
    for j, zone_id in enumerate(zone_list):
        ax.plot([i, i+1], [zone_id, zone_id], color='b')

# Setting labels and title
ax.set_xlabel('Time')
ax.set_ylabel('Zone ID')
ax.set_title('Zone ID vs. Time')

plt.show()
