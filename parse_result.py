import json
import os
import xml.etree.ElementTree as ET
import time
import run_tests as rt
import re

def parse_init(suite):
    global suite_dict
    suite_dict = {'suite': suite, 'tests': []}

def parse(suite, tags = {}):
    # loop through all XML files in the folder, this only applies to PageMap suite
    result_dir = "results/"+suite+"/"+tags['desc']
    
    for filename in os.listdir(result_dir):
        if filename.endswith(".xml"):
            # parse XML data
            file_path = os.path.join(result_dir, filename)
            workload = ET.parse(file_path).find(".//Name").text
            root = ET.parse(file_path).getroot()
            bandwidth = float(root.find(".//Bandwidth").text)
            iops = float(root.find(".//IOPS").text)
            Device_Response_Time = float(root.find(".//Device_Response_Time").text)
            # round them to 2 decimal places
            bandwidth = round(bandwidth, 2)
            iops = round(iops, 2)
            
            interleave_program_cmd = float(root.find('.//SSDDevice.FTL').attrib['Issued_Flash_Interleaved_Program_CMD'])
            multiplane_program_cmd = float(root.find('.//SSDDevice.FTL').attrib['Issued_Flash_Multiplane_Program_CMD'])
            zone_opened_count = float(root.find('.//SSDDevice.FTL').attrib['Zone_Opened_Count'])
            copyback_program_cmd = float(root.find('.//SSDDevice.FTL').attrib['Issued_Flash_Copyback_Program_CMD'])

            # Define the XPath query
            xpath_query = './/SSDDevice.TSU.User_Write_TR_Queue.Priority.HIGH'

            # Extract the values of Avg_Queue_Length and STDev_Queue_Length
            avg_queue_lengths = []
            stdev_queue_lengths = []
            
            for element in root.findall(xpath_query):
                avg_queue_lengths.append(float(element.get('Avg_Queue_Length')))
                stdev_queue_lengths.append(float(element.get('STDev_Queue_Length')))
                
            # Compute the average of Avg_Queue_Length and STDev_Queue_Length
            avg_avg_queue_length = round(sum(avg_queue_lengths) / len(avg_queue_lengths),2)
            avg_stdev_queue_length = round(sum(stdev_queue_lengths) / len(stdev_queue_lengths),2)
            
            # append the result to the suite_dict
            # now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            now = time.ctime(os.path.getctime(file_path))

            # Add worklload types to tags for RequestSize suite
            mTags = tags.copy()
            # if "RequestSize" in suite or "MultiStream" in suite or "ZoneSize" in suite:
            if "sequential" in workload:
                mTags['workload_type']= "sequential"
            else:
                mTags['workload_type']= "random"
            if "write" in workload:
                mTags['workload_type2']= "write"
                mTags['write_percent'] = "100"
            elif "mixed" in workload:
                mTags['workload_type2']= "mixed"
                mTags['write_percent']= str(100-int(re.findall(r'\d+', workload)[0]))
            elif "read" in workload:
                mTags['workload_type2']= "read"
                mTags['write_percent'] = "0"
            global suite_dict
            suite_dict.get("tests").append({'time': now, 'tags': mTags, 'scenario': filename, 'workload': workload, 'bandwidth': bandwidth, 'iops': iops, 'Device_Response_Time': Device_Response_Time, 'interleave_program_cmd': interleave_program_cmd, 'multiplane_program_cmd': multiplane_program_cmd, 'copy_program_cmd': copyback_program_cmd, 'zone_opened_count': zone_opened_count, 'Average Avg_Queue_Length': avg_avg_queue_length, 'Average STDev_Queue_Length': avg_stdev_queue_length})
            

def parse_flush(suite):
    json_file = "results/result.json"
    if not os.path.exists(json_file) or os.stat(json_file).st_size == 0:
        existing_data = []
    else:
        with open(json_file, 'r') as file:
            existing_data = json.load(file)

    index_to_replace = -1
    for i, obj in enumerate(existing_data):
        if obj['suite'] == suite:
            index_to_replace = i
            break
    
    global suite_dict
    if suite_dict != None:
        if index_to_replace != -1:
            if "PageMap" in suite:
                existing_data[index_to_replace]['tests'].extend(suite_dict['tests'])
            else:
                existing_data[index_to_replace] = suite_dict
        else:
            existing_data.append(suite_dict)

    with open(json_file, 'w') as file:
        json.dump(existing_data, file, indent = 4,  sort_keys=True)


# Only used when parse result needed to be run by hand, not triggered by run_tests.py
# Content copied from run_tests.py main()
def main():
    tree = ET.parse('run_tests.config')
    root = tree.getroot()
    cwd = os.getcwd()

    for suite in root.iter('Suite'):
        suite_name = suite.attrib["name"]
        run = suite.attrib["run"].title() == 'True'
        if run:
            parse_init(suite_name)
            for test in suite.iter('Test'):
                workload = test.find('Workload').text
                test_tags = rt.gather_tags(test, workload)
                parse(suite_name, test_tags)
            parse_flush(suite_name)

if __name__ == "__main__":
    main()