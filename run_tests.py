import os
import xml.etree.ElementTree as ET

tree = ET.parse('run_tests.config')
root = tree.getroot()
cwd = os.getcwd()

def index_of_nth(text, substring, n):
    """Used to find second / in file path when building result path"""
    index = 0
    for _ in range(n):
        index = text.index(substring, index) + 1
    return index - 1


for suite in root.iter('Suite'):
    tag = suite.attrib["tag"]
    run = suite.attrib["run"].title() == 'True'
    if run:
        for test in suite.iter('Test'):
            uid = test.find('UID').text
            ssdcfg = test.find('SSDConfig').text
            workload = test.find('Workload').text
            result_dir = "results/"+tag

            # run individual tests spicified by suite "run" attribute
            # if run==false, but uid is specified as arg, run it
            
            if not os.path.exists(result_dir):
                os.makedirs(result_dir)

            result = result_dir+workload[index_of_nth(workload,"/",2 ):-4]+"_scenario_1"+workload[-4:]

            print (uid, ssdcfg, workload, result)

            cmd = os.getcwd()+"/MQSim -i "+ssdcfg+" -w "+workload
            os.system(cmd)
    
        # move all scenario xml to result directory
        os.chdir('workload/'+tag)
        os.system('mv *_scenario* ../../'+result_dir)
        os.chdir(cwd)