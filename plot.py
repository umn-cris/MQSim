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

if __name__ == "__main__":
    result = read_json("results/result.json")
    pm = [suite['tests'] for suite in result if suite['suite'] == "PageMapIntensity"][0]
    tests_50us = select_tests_by_intensity(pm,"50us")
    plot_y_key(tests_50us, 'Average Avg_Queue_Length', '[PageMap] Average Queue Length for 50us intensity').show()
    plot_y_key(tests_50us, 'Device_Response_Time', '[PageMap] Device Response Time for 50us intensity').show()
    tests_52us = select_tests_by_intensity(pm,"60us")
    plot_y_key(tests_52us, 'Average Avg_Queue_Length', '[PageMap] Average Queue Length for 60us intensity').show()
    plot_y_key(tests_52us, 'Device_Response_Time', '[PageMap] Device Response Time for 50us intensity').show()