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
import sys
import json
import os
import re
import xml.etree.ElementTree as ET

suite_tag = sys.argv[1]
if len(sys.argv) > 2:
    desc = sys.argv[2]
# define the folder path
folder_path = "results/"
suite_dict = {'tag': suite_tag, 'tests': []}

# loop through all XML files in the folder, this only applies to PageMap suite
for folder in os.listdir(folder_path+suite_tag+"/"):
    path = folder_path+suite_tag+"/"+folder
    print (f"##### {path} #####\n")
    
    for filename in os.listdir(path):
        if filename.endswith(".xml"):
            # parse XML data
            file_path = os.path.join(path, filename)
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

            # extract experiment tags
            request_size = re.search(r'(\d+)KB', filename)
            if re.search(r'sequential', filename):
                workload_type = 'sequential'
            elif re.search(r'random', filename):
                workload_type = 'random'
            elif re.search(r'mix', filename):
                workload_type = 'mix'
            else:
                workload_type = None
            if re.search(r'write', filename):
                workload_type2 = 'write'
            elif re.search(r'read', filename):
                workload_type2 = 'read'
            else:
                workload_type2 = None
            write_percent = re.search(r'(\d+)pct', filename)
            if suite_tag == 'ZoneSize':
                zone_size = desc
            else:
                zone_size = 'default'

            expriment_tag = {'req_size': request_size.group(1), 'workload_type': workload_type, 'workload_type2': workload_type2, 'write_percent': write_percent.group(1), 'zone_size': zone_size}
            # append the result to the suite_dict
            suite_dict.get("tests").append({'tags': expriment_tag, 'desc': folder, 'scenario': filename, 'workload': workload, 'bandwidth': bandwidth, 'iops': iops, 'Device_Response_Time': Device_Response_Time, 'interleave_program_cmd': interleave_program_cmd, 'multiplane_program_cmd': multiplane_program_cmd, 'copy_program_cmd': copy_program_cmd, 'Average Avg_Queue_Length': avg_avg_queue_length, 'Average STDev_Queue_Length': avg_stdev_queue_length})

with open(folder_path+suite_tag+'.json', 'w') as json_file:
    json.dump(suite_dict, json_file,  indent = 4)

