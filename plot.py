import matplotlib.pyplot as plt
import json


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

def plot_avg_queue_length(tests, title) -> plt:
    x_50us = select_from_tag(tests, 'desc')
    y_avg_queue = select_y_array(tests, 'Average Avg_Queue_Length')

    fig, ax = plt.subplots()
    ax.bar(x_50us, y_avg_queue)
    ax.set_title(title)

    plt.xticks(rotation='vertical')
    plt.xlabel('Page mapping scheme')
    plt.ylabel('Avg_Queue_Length')

    tags = tests[0]['tags']
    ax.set_ylim([52.0, 52.7])
    plt.text(25, 52.5, 'request_size:'+tags['request_size']+'\nworkload:'+tags['workload_type']+'\n               '+tags['workload_type2']+'\nwrite%:'+tags['write_percent']+'\nzone_size:'+tags['zone_size'])
    
    for i, value in enumerate(y_avg_queue):
        plt.text(x_50us[i], y_avg_queue[i], str(value), horizontalalignment='center', verticalalignment='bottom')

    return plt

if __name__ == "__main__":
    result = read_json("results/result.json")
    pm = [suite['tests'] for suite in result if suite['suite'] == "PageMap"][0]
    tests_50us = select_tests_by_intensity(pm,"50us")
    plt = plot_avg_queue_length(tests_50us, '[PageMap] Average Queue Length for 50us intensity')

    plt.show()