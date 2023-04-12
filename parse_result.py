# Usage: python3 parse_result.py <suite_tag>
# Example: python3 parse_result.py PageMap
#   Create a json file for each suite, `parse_result.py` will parse each Test in the Suite (e.g. CDWP, CDPW ... in PageMap)
#   and produce a joint json file for each suite, named after the suite tag (e.g. PageMap.json)
# JSON structure:
#  {
#     "tag": "PageMap",
#     "tests": [{"desc": "CDWP", "bandwidth": 0.0, "iops": 0.0, "Device_Response_Time": "0.0", "interleave_program_cmd": "0", "multiplane_program_cmd": "0", "copy_program_cmd": "0", "Average Avg_Queue_Length": 0.0, "Average STDev_Queue_Length": 0.0},
#               {"desc": "CDPW", "bandwidth": 0.0, "iops": 0.0, "Device_Response_Time": "0.0", "interleave_program_cmd": "0", "multiplane_program_cmd": "0", "copy_program_cmd": "0", "Average Avg_Queue_Length": 0.0, "Average STDev_Queue_Length": 0.0},
#               {"desc": "PDWC", "bandwidth": 0.0, "iops": 0.0, "Device_Response_Time": "0.0", "interleave_program_cmd": "0", "multiplane_program_cmd": "0", "copy_program_cmd": "0", "Average Avg_Queue_Length": 0.0, "Average STDev_Queue_Length": 0.0}]
#  }
import json
import os
import xml.etree.ElementTree as ET
import time

def parse_init(suite):
    global suite_dict
    suite_dict = {'suite': suite, 'tests': []}

def parse(suite, tags = {}):
    # loop through all XML files in the folder, this only applies to PageMap suite
    if suite == "PageMap":
        result_dir = "results/"+suite+"/"+tags['desc']
    else:
        result_dir = "results/"+suite
    
    for filename in os.listdir(result_dir):
        if filename.endswith(".xml"):
            # parse XML data
            file_path = os.path.join(result_dir, filename)
            workload = ET.parse(file_path).find(".//Name").text
            root = ET.parse(file_path).getroot()
            bandwidth = float(root.find(".//Bandwidth").text)
            iops = float(root.find(".//IOPS").text)
            Device_Response_Time = root.find(".//Device_Response_Time").text
            # round them to 2 decimal places
            bandwidth = round(bandwidth, 2)
            iops = round(iops, 2)
            
            interleave_program_cmd = root.find('.//SSDDevice.FTL').attrib['Issued_Flash_Interleaved_Program_CMD']
            multiplane_program_cmd = root.find('.//SSDDevice.FTL').attrib['Issued_Flash_Multiplane_Program_CMD']
            copy_program_cmd = root.find('.//SSDDevice.FTL').attrib['Issued_Flash_Copyback_Program_CMD']

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
            global suite_dict
            suite_dict.get("tests").append({'time': now, 'tags': tags, 'scenario': filename, 'workload': workload, 'bandwidth': bandwidth, 'iops': iops, 'Device_Response_Time': Device_Response_Time, 'interleave_program_cmd': interleave_program_cmd, 'multiplane_program_cmd': multiplane_program_cmd, 'copy_program_cmd': copy_program_cmd, 'Average Avg_Queue_Length': avg_avg_queue_length, 'Average STDev_Queue_Length': avg_stdev_queue_length})
            

def parse_flush(suite):
    json_file = "results/result.json"
    if os.path.exists(json_file):
        with open(json_file, 'r') as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    index_to_replace = -1
    for i, obj in enumerate(existing_data):
        if obj['suite'] == suite:
            index_to_replace = i
            break
    
    global suite_dict
    if suite_dict != None:
        if index_to_replace != -1:
            if suite == "PageMap":
                existing_data[index_to_replace]['tests'].extend(suite_dict['tests'])
            existing_data[index_to_replace] = suite_dict
        else:
            existing_data.append(suite_dict)

    with open(json_file, 'w') as file:
        json.dump(existing_data, file, indent = 4)