# Usage: python3 run_tests.py
# This script will run all tests specified in run_tests.config
# Suite tag name in run_test.config must match the folder name
# in workload/ and results/ folder

import os
import xml.etree.ElementTree as ET
import parse_result as pr

tree = ET.parse('run_tests.config')
root = tree.getroot()
cwd = os.getcwd()

def index_of_nth(text, substring, n):
    """Used to find second / in file path when building result path"""
    index = 0
    for _ in range(n):
        index = text.index(substring, index) + 1
    return index - 1

def main():
    for suite in root.iter('Suite'):
        suite_name = suite.attrib["name"]
        run = suite.attrib["run"].title() == 'True'
        if run:
            pr.parse_init(suite_name)
            for test in suite.iter('Test'):
                ssdcfg = test.find('SSDConfig').text
                workload = test.find('Workload').text
                test_tags = gather_tags(test, workload)

                result_dir = "results/"+suite_name+"/"+test_tags['desc']

                # run individual tests spicified by suite "run" attribute
                # if run==false, but uid is specified as arg, run it
                
                if not os.path.exists(result_dir):
                    os.makedirs(result_dir)

                cmd = os.getcwd()+"/MQSim -i "+ssdcfg+" -w "+workload
                os.system(cmd)
        
                # move all scenario xml to result directory
                os.chdir('workload/'+suite_name)
                os.system('mv *_scenario* ../../'+result_dir)
                os.chdir(cwd)

                pr.parse(suite_name, test_tags)
            pr.parse_flush(suite_name)



def gather_tags(test, workload):
    """Gather test tags"""
    tags = {}
    tags['desc'] = test.attrib['desc'].title().upper()
    tags['request_size'] = test.attrib['request_size'].title().upper()
    tags['workload_type'] = test.attrib['workload_type'].title().lower()
    tags['workload_type2'] = test.attrib['workload_type2'].title().lower()
    tags['write_percent'] = test.attrib['write_percent'].title()
    tags['zone_size'] = test.attrib['zone_size'].title()
    return tags

if __name__ == "__main__":
    main()