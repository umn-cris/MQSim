import matplotlib.pyplot as plt
import json
import numpy as np


def read_json(path) -> dict:
    """Read json file and return a dictionary"""
    with open(path, 'r') as f:
        return json.load(f)


def select_tests_by_intensity(tests, intensity_in_us):
    """Return a list of x values"""
    return [test for test in tests if intensity_in_us in test['workload']]

def select_from_tag(tests, tag):
    """Return a list of x values"""
    return [test['tags'][tag] for test in tests]

def select_y_array(tests, y_key):
    """Return a list of y values"""
    return [test[y_key] for test in tests]

def plot_y_key(tests, y_key, title) -> plt:
    x = select_from_tag(tests, 'desc')
    y = select_y_array(tests, y_key)

    fig, ax = plt.subplots()
    ax.bar(x, y)
    ax.set_title(title)

    plt.xticks(rotation='vertical')
    plt.xlabel('Page mapping scheme')
    plt.ylabel(y_key)

    tags = tests[0]['tags']
    diff = (max(y)-min(y))/10
    ax.set_ylim(bottom=min(y)-diff, top=max(y)+diff)
    plt.text(len(x)+1, max(y)-diff, 'request_size:'+tags['request_size']+'\nworkload:'+tags['workload_type']+'\n               '+tags['workload_type2']+'\nwrite%:'+tags['write_percent']+'\nzone_size:'+tags['zone_size'])
    
    for i, value in enumerate(y):
        plt.text(x[i], y[i], str(value), horizontalalignment='center', verticalalignment='bottom')

    return plt

def plot_multi_y_key(n,tests, y_key, title) -> plt:
    fig, ax = plt.subplots()
    ymax = 0
    ymin = 1000000
    bar_width = 1/(n+1)
    x_pos = list()
    for i in range(n):
        x_pos.append([x + bar_width*i for x in np.arange(len(tests)//n)])

    
    x = select_from_tag(tests[:len(tests)//n], 'desc')
    
    for i in range(n):
        y=select_y_array(tests[i*len(tests)//n:(i+1)*len(tests)//n], y_key)
        ax.bar(x_pos[i], y, width=bar_width, label=str(i*2+50)+'us')
        ymax = max(ymax, max(y))
        ymin = min(ymin, min(y))
    
        # for j, value in enumerate(y):
        #     plt.text(x_pos[i][j], y[j], str(value), horizontalalignment='center', verticalalignment='bottom')

    
    ax.set_title(title)
    ax.legend()
    
    ax.set_xticks([r + bar_width for r in range(len(x))])
    ax.set_xticklabels(x)
    plt.xticks(rotation='vertical', fontsize=8)
    plt.tick_params(axis='x', which='major', width=4)
    plt.xlabel('Page mapping scheme')
    plt.ylabel(y_key)
   

    tags = tests[0]['tags']
    diff = (ymax-ymin)/10
    ax.set_ylim(bottom=ymin-diff, top=ymax+diff)
    plt.text(len(x)+1, ymax-diff, 'request_size:'+tags['request_size']+'\nworkload:'+tags['workload_type']+'\n               '+tags['workload_type2']+'\nwrite%:'+tags['write_percent']+'\nzone_size:'+tags['zone_size'])

    plt.figure(figsize=(600, 100))
    plt.tight_layout()
    return plt

if __name__ == "__main__":
    result = read_json("results/result.json")
    pm = [suite['tests'] for suite in result if suite['suite'] == "PageMapIntensity"][0]
    
    tests_50us = select_tests_by_intensity(pm,"50us")
    tests_52us = select_tests_by_intensity(pm,"52us")
    tests_54us = select_tests_by_intensity(pm,"54us")
    tests_56us = select_tests_by_intensity(pm,"56us")
    tests_58us = select_tests_by_intensity(pm,"58us")
    tests_60us = select_tests_by_intensity(pm,"60us")
    

    # plot_y_key(tests_50us, 'Average Avg_Queue_Length', '[PageMap] Average Queue Length for 50us intensity').show()
    # plot_y_key(tests_50us, 'Device_Response_Time', '[PageMap] Device Response Time for 50us intensity').show()
    plot_y_key(tests_60us, 'Average Avg_Queue_Length', '[PageMap] Average Queue Length for 60us intensity').show()
    plot_y_key(tests_60us, 'Device_Response_Time', '[PageMap] Device Response Time for 50us intensity').show()

    #plot_multi_y_key(6,tests_50us+tests_52us+tests_54us+tests_56us+tests_58us+tests_60us, 'Average Avg_Queue_Length', '[PageMap] Average Queue Length for all intensities').show()
    #plot_multi_y_key(6,tests_50us+tests_52us+tests_54us+tests_56us+tests_58us+tests_60us, 'Device_Response_Time', '[PageMap] Device Response Time for all intensities').show()