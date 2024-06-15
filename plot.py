import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
import numpy as np


def read_json(path) -> dict:
    """Read json file and return a dictionary"""
    with open(path, 'r') as f:
        return json.load(f)

def select_tests_by_trace_size(trace_size_in_gb, tests):
    """Return a list of tests"""
    return [test for test in tests if trace_size_in_gb in test['workload']]

def select_tests_by_intensity(tests, intensity_in_us):
    """Return a list of x values"""
    return [test for test in tests if intensity_in_us in test['workload']]

def select_tests_by_workload(tests,workload_type, workload_type2):
    """Return a list of x values"""
    return [test for test in tests if workload_type in test['tags']['workload_type'] and workload_type2 in test['tags']['workload_type2']]

def select_tests_by_desc(tests, desc):
    """Return a list of x values"""
    return [test for test in tests if test['tags']['desc'] == desc]

# private method used by plot_multi_y_key
def select_from_tag(tests, tag):
    """Return a list of x values"""
    return [test['tags'][tag] for test in tests]

def select_y_array(tests, y_key):
    """Return a list of y values"""
    return [test[y_key] for test in tests]

import matplotlib.pyplot as plt

def plot_y_key(tests, x_key, y_key, title, output_path, is_sorted=False):
    x = select_from_tag(tests, 'desc')
    y = select_y_array(tests, y_key)
    
    if is_sorted:
        # Sort the x and y arrays together based on y values
        sorted_pairs = sorted(zip(x, y), key=lambda pair: pair[1])
        x, y = zip(*sorted_pairs)
    
    if y_key == "Device_Response_Time":
        y_key = "Device Response Time" + " (ns)"

    fig, ax = plt.subplots()

    tags = tests[0]['tags']
    diff = (max(y)-min(y))/8
    ax.set_ylim(bottom=min(y)-diff, top=max(y)+diff)
    if "PageMap" in title:
        ax.text(len(x)+1, max(y)-diff, 'request_size:'+tags['request_size']+'\nworkload:'+tags['workload_type']+'\n               '+tags['workload_type2']+'\nwrite%:'+tags['write_percent']+'\nzone_size:'+tags['zone_size'])
    elif "ZoneSize" in title:
        ax.text(len(x)+1, max(y)-diff, 'request_size:'+tags['request_size']+'\nworkload:'+tags['workload_type']+'\n               '+tags['workload_type2']+'\nwrite%:'+tags['write_percent'])

    ax.set_title(title)
    ax.set_xlabel(x_key)
    ax.set_ylabel(y_key)
    
    for i, value in enumerate(y):
        ax.text(x[i], y[i], str(value), horizontalalignment='center', verticalalignment='bottom')

    ax.bar(x, y)

    plt.xticks(rotation='vertical')
    plt.tight_layout()

    plt.savefig(output_path)
    plt.close()

def plot_multi_y_key(n, tests, x_key, y_key, title, output_path):
    """Plot multiple y keys in one figure"""
    fig, ax = plt.subplots()
    ymax = 0
    ymin = 1000000
    bar_width = 1 / (n + 1)
    x_pos = list()
    for i in range(n):
        x_pos.append([x + bar_width * i for x in np.arange(len(tests) // n)])

    x = select_from_tag(tests[:len(tests) // n], 'desc')

    for i in range(n):
        test_id = i * len(tests) // n
        # y = select_y_array(tests[i * len(tests) // n:(i + 1) * len(tests) // n], y_key)
        y = select_y_array(tests[test_id:test_id+len(tests) // n], y_key)

        patterns = ["/", "\\", "|", "+", "x", "o", "O", ".", "*"]

        if "PageMap" in title:
            ax.bar(x_pos[i], y, width=bar_width, label=str(i * 2 + 50) + 'us')
        elif "ZoneSize" in title or "MultiStream" in title:
            ax.bar(x_pos[i], y, width=bar_width, label=tests[test_id]['tags']['workload_type']+' '+tests[test_id]['tags']['workload_type2'],  hatch=patterns[i % len(patterns)])
        else: # catch default case
            ax.bar(x_pos[i], y, width=bar_width, label=tests[test_id]['tags']['workload_type']+' '+tests[test_id]['tags']['workload_type2'])
        ymax = max(ymax, max(y))
        ymin = min(ymin, min(y))

        ### Display text on top of each bar
        # for j, value in enumerate(y):
        #     plt.text(x_pos[i][j], y[j], str(value), horizontalalignment='center', verticalalignment='bottom')

    if y_key == "Device_Response_Time":
            y_key = "Device Response Time" + " (ns)"
            
    ax.set_title(title)
    ax.legend()

    ax.set_xticks([r + bar_width for r in range(len(x))])
    ax.set_xticklabels(x)
    plt.xticks(rotation='horizontal', fontsize=8)
    plt.tick_params(axis='x', which='major', width=4)
    plt.xlabel(x_key)
    plt.ylabel(y_key)

    tags = tests[0]['tags']
    diff = (ymax - ymin) / 8
    ax.set_ylim(bottom=ymin - diff, top=ymax + diff)
    if "PageMap" in title:
        ax.text(len(x) + 1, ymax - diff, 'request_size:' + tags['request_size'] +
            '\nworkload:' + tags['workload_type'] + '\n               ' + tags['workload_type2'] +
            '\nwrite%:' + tags['write_percent'] + '\nzone_size:' + tags['zone_size'])
    elif "ZoneSize" in title:
        ax.text(len(x) + 1, ymax - diff, 'request_size:' + tags['request_size'] +
                '\nworkload:' + tags['workload_type'] + '\n               ' + tags['workload_type2'] +
                '\nwrite%:' + tags['write_percent'])

    plt.tight_layout()

    ax.set_facecolor('white')  # Set the background color to white
    
    plt.savefig(output_path)
    plt.close()


def plot_suite_pagemapinsentisy(result):
    pm = [suite['tests'] for suite in result if suite['suite'] == "PageMapIntensity"][0]
    
    tests_50us = select_tests_by_intensity(pm,"50us")
    tests_52us = select_tests_by_intensity(pm,"52us")
    tests_54us = select_tests_by_intensity(pm,"54us")
    tests_56us = select_tests_by_intensity(pm,"56us")
    tests_58us = select_tests_by_intensity(pm,"58us")
    tests_60us = select_tests_by_intensity(pm,"60us")
    
    plot_y_key(tests_50us, 'Page mapping scheme', 'Average Avg_Queue_Length', '[PageMap] Average Queue Length for 50us intensity',"graphs/pagemap1.pdf")
    plot_y_key(tests_50us, 'Page mapping scheme', 'Device_Response_Time', '[PageMap] Device Response Time for 50us intensity',"graphs/pagemap2.pdf")
    plot_y_key(tests_60us, 'Page mapping scheme', 'Average Avg_Queue_Length', '[PageMap] Average Queue Length for 60us intensity',"graphs/pagemap3.pdf")
    plot_y_key(tests_60us, 'Page mapping scheme', 'Device_Response_Time', '[PageMap] Device Response Time for 50us intensity',"graphs/pagemap4.pdf")

    plot_multi_y_key(6,tests_50us+tests_52us+tests_54us+tests_56us+tests_58us+tests_60us, 'Page mapping scheme', 'Average Avg_Queue_Length', '[PageMap] Average Queue Length for all intensities',"graphs/pagemap5.pdf")
    plot_multi_y_key(6,tests_50us+tests_52us+tests_54us+tests_56us+tests_58us+tests_60us, 'Page mapping scheme', 'Device_Response_Time', '[PageMap] Device Response Time for all intensities',"graphs/pagemap6.pdf")

def plot_suite_requestsize(result):
    rs = [suite['tests'] for suite in result if suite['suite'] == "RequestSize"][0]
    
    tests_seq_w = select_tests_by_workload(rs,"sequential", "write")
    tests_seq_r = select_tests_by_workload(rs,"sequential", "read")
    tests_rand_w = select_tests_by_workload(rs,"random", "write")
    tests_rand_r = select_tests_by_workload(rs,"random", "read")

    # plot_y_key(tests_seq_w, 'RequestSize', 'Average Avg_Queue_Length', '[RequestSize] Average Avg_Queue_Length for sequential write',"graphs/requestsize1.pdf")
    # plot_y_key(tests_seq_r, 'RequestSize', 'Average Avg_Queue_Length', '[RequestSize] Average Avg_Queue_Length for sequential read',"graphs/requestsize2.pdf")
    # plot_y_key(tests_rand_w, 'RequestSize', 'Average Avg_Queue_Length', '[RequestSize] Average Avg_Queue_Length for random write',"graphs/requestsize3.pdf")
    # plot_y_key(tests_rand_r, 'RequestSize', 'Average Avg_Queue_Length', '[RequestSize] Average Avg_Queue_Length for random read',"graphs/requestsize4.pdf")

    # plot_y_key(tests_seq_w, 'RequestSize', 'Device_Response_Time', '[RequestSize] Device_Response_Time for sequential write',"graphs/requestsize5.pdf")
    # plot_y_key(tests_seq_r, 'RequestSize', 'Device_Response_Time', '[RequestSize] Device_Response_Time for sequential read',"graphs/requestsize6.pdf")
    # plot_y_key(tests_rand_w, 'RequestSize', 'Device_Response_Time', '[RequestSize] Device_Response_Time for random write',"graphs/requestsize7.pdf")
    # plot_y_key(tests_rand_r, 'RequestSize', 'Device_Response_Time', '[RequestSize] Device_Response_Time for random read',"graphs/requestsize8.pdf")
    plot_multi_y_key(4, tests_seq_w+tests_seq_r+tests_rand_w+tests_rand_r, 'RequestSize', 'Average Avg_Queue_Length', '[RequestSize] Average Avg_Queue_Length for all workloads',"graphs/requestsize1.pdf")
    plot_multi_y_key(4, tests_seq_w+tests_seq_r+tests_rand_w+tests_rand_r, 'RequestSize', 'Device_Response_Time', '[RequestSize] Device_Response_Time for all workloads',"graphs/requestsize2.pdf")

def plot_suite_multistream(result):
    ms = [suite['tests'] for suite in result if suite['suite'] == "MultiStream"][0]
    ms_seq_w = select_tests_by_workload(ms,"sequential", "write")
    ms_seq_r = select_tests_by_workload(ms,"sequential", "read")
    ms_seq_m = select_tests_by_workload(ms,"sequential", "mixed")
    ms_rand_w = select_tests_by_workload(ms,"random", "write")
    ms_rand_r = select_tests_by_workload(ms,"random", "read")
    ms_rand_m = select_tests_by_workload(ms,"random", "mixed")

    # plot_y_key(ms, 'Number of Streams', 'Average Avg_Queue_Length', '[MultiStream] Average Avg_Queue_Length for sequential/random read/write',"graphs/multistream1.pdf")

    # plot_y_key(ms_seq_w, 'Number of Streams', 'Device_Response_Time', '[MultiStream] Device_Response_Time for sequential write',"graphs/multistream_seq_w.pdf")
    # plot_y_key(ms_seq_r, 'Number of Streams', 'Device_Response_Time', '[MultiStream] Device_Response_Time for sequential read',"graphs/multistream_seq_r.pdf")
    # plot_y_key(ms_seq_m, 'Number of Streams', 'Device_Response_Time', '[MultiStream] Device_Response_Time for sequential mixed read 50%',"graphs/multistream_seq_m.pdf")
    # plot_y_key(ms_rand_w, 'Number of Streams', 'Device_Response_Time', '[MultiStream] Device_Response_Time for random write',"graphs/multistream_seq_rand_w.pdf")
    # plot_y_key(ms_rand_r, 'Number of Streams', 'Device_Response_Time', '[MultiStream] Device_Response_Time for random read',"graphs/multistream_seq_rand_r.pdf")
    # plot_y_key(ms_rand_m, 'Number of Streams', 'Device_Response_Time', '[MultiStream] Device_Response_Time for random mixed read 50%',"graphs/multistream_seq_rand_m.pdf")
    
    plot_multi_y_key(6, ms_seq_r+ms_rand_r+ms_rand_m+ms_seq_m+ms_seq_w+ms_rand_w, 'Number of Streams', 'Device_Response_Time', '[MultiStream] Device_Response_Time for all workloads',"graphs/multistream_drt.pdf")
    plot_multi_y_key(4, ms_rand_m+ms_seq_m+ms_seq_w+ms_rand_w, 'Number of Streams', 'multiplane_program_cmd', '[MultiStream] multiplane_program_cmd for all workloads',"graphs/multistream_multiplane.pdf")
    plot_multi_y_key(6, ms_seq_r+ms_rand_r+ms_rand_m+ms_seq_m+ms_seq_w+ms_rand_w, 'Number of Streams', 'iops', '[MultiStream] multiplane_program_cmd for sequential/random read/write',"graphs/multistream_iops.pdf")
    
def plot_suite_zonesize(result):
    zs = [suite['tests'] for suite in result if suite['suite'] == "ZoneSize"][0]
    # looking to compare same workload (e.g. sequential mixed read 50%) of same intensity with different zone sizes
    # intensity I chose whichever intensity resulted in avg_queue_length~=2 to 4
    tests_seq_w = select_tests_by_trace_size("5GB",select_tests_by_intensity(select_tests_by_workload(zs,"sequential", "write"),"54us"))
    tests_seq_r = select_tests_by_trace_size("5GB",select_tests_by_intensity(select_tests_by_workload(zs,"sequential", "read"),"40us")) #avg_queue_length is always 0, read is too fast to queue up
    tests_seq_m = select_tests_by_trace_size("5GB",select_tests_by_intensity(select_tests_by_workload(zs,"sequential", "mixed"),"46us"))
    tests_rand_w = select_tests_by_trace_size("5GB",select_tests_by_intensity(select_tests_by_workload(zs,"random", "write"),"56us"))
    tests_rand_r = select_tests_by_trace_size("5GB",select_tests_by_intensity(select_tests_by_workload(zs,"random", "read"),"40us")) #avg_queue_length is always 0, read is too fast to queue up
    tests_rand_m = select_tests_by_trace_size("5GB",select_tests_by_intensity(select_tests_by_workload(zs,"random", "mixed"), "50us"))

    plot_y_key(tests_seq_w, 'Zone Size', 'Device_Response_Time', '[ZoneSize] Device_Response_Time for sequential writes',"graphs/zonesize_seq_w.pdf")
    plot_y_key(tests_seq_r, 'Zone Size', 'Device_Response_Time', '[ZoneSize] Device_Response_Time for sequential read',"graphs/zonesize_seq_r.pdf")
    plot_y_key(tests_seq_m, 'Zone Size', 'Device_Response_Time', '[ZoneSize] Device_Response_Time for sequential mixed read 50%',"graphs/zonesize_seq_m.pdf")
    plot_y_key(tests_rand_w, 'Zone Size', 'Device_Response_Time', '[ZoneSize] Device_Response_Time for random write',"graphs/zonesize_rand_w.pdf")
    plot_y_key(tests_rand_r, 'Zone Size', 'Device_Response_Time', '[ZoneSize] Device_Response_Time for random read',"graphs/zonesize_rand_r.pdf")
    plot_y_key(tests_rand_m, 'Zone Size', 'Device_Response_Time', '[ZoneSize] Device_Response_Time for random mixed read 50%',"graphs/zonesize_rand_m.pdf")
   
    # plot_multi_y_key(3,tests_seq_w+tests_seq_r+tests_seq_m, 'Zone Size', 'Device_Response_Time', '[ZoneSize] Sequential workloads with various zone sizes',"graphs/zonesize_seq.pdf")
    # plot_multi_y_key(3,tests_rand_w+tests_rand_r+tests_rand_m, 'Zone Size', 'Device_Response_Time', '[ZoneSize] Random workloads with various zone sizes',"graphs/zonesize_rand.pdf")

def plot_suite_page_mapping_scheme(result, suite_name_full="ZN540FioWrite", is_sorted=False):
    print("Sorted"+str(is_sorted))
    suite_tests = [suite['tests'] for suite in result if suite['suite'] == suite_name_full][0]
    plot_y_key(suite_tests, 'Page mapping scheme', 'Average Avg_Queue_Length', '['+suite_name_full+']'+'Average Queue Length',"graphs/"+suite_name_full+"avg-qlen" + ("_sorted" if sorted else "") + ".pdf", sorted)
    plot_y_key(suite_tests, 'Page mapping scheme', 'Device_Response_Time', '['+suite_name_full+']'+'Device Response Time',"graphs/"+suite_name_full+"_resp-time" + ("_sorted" if is_sorted else "") + ".pdf", is_sorted)
    plot_y_key(suite_tests, 'Page mapping scheme', 'multiplane_program_cmd', '['+suite_name_full+']'+'multiplane_program_cmd',"graphs/"+suite_name_full+"_multiplane" + ("_sorted" if sorted else "") + ".pdf", sorted)
    plot_y_key(suite_tests, 'Page mapping scheme', 'iops', '['+suite_name_full+']'+'IOPS',"graphs/"+suite_name_full+"_iops" + ("_sorted" if sorted else "") + ".pdf", sorted)

def plot_suite_zonesize_real(result):
    zs = [suite['tests'] for suite in result if suite['suite'] == "ZoneSizeReal"][0]
    plot_y_key(zs, 'Zone Size', 'Average Avg_Queue_Length', '[ZoneSizeReal] Average Queue Length for YCSB_RocksDB',"graphs/zonesizereal1.pdf")
    plot_y_key(zs, 'Zone Size', 'Device_Response_Time', '[ZoneSizeReal] Device Response Time for YCSB_RocksDB',"graphs/zonesizereal2.pdf")
    plot_y_key(zs, 'Zone Size', 'multiplane_program_cmd', '[ZoneSizeReal] multiplane_program_cmd for YCSB_RocksDB',"graphs/zonesizereal3.pdf")


if __name__ == "__main__":
    result = read_json("results/result.json")
    # plot_suite_pagemapinsentisy(result)
    # plot_suite_requestsize(result)
    # plot_suite_multistream(result)
    # plot_suite_zonesize(result)
    # plot_suite_page_mapping_scheme(result,"YCSB_RocksDB")
    plot_suite_page_mapping_scheme(result,"ZN540FioWrite")
    plot_suite_page_mapping_scheme(result,"ZN540RocksDBOverwrite")
    plot_suite_page_mapping_scheme(result,"ZN540RocksDBReadWhileWriting")
    # plot_suite_zonesize_real(result)