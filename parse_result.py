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

suite_tag = ''
desc = ''

# define the folder path
folder_path = "results/"
suite_dict = {'tag': suite_tag, 'tests': []}
test_tags= {}

def parse(suite, tags = {}):
    # loop through all XML files in the folder, this only applies to PageMap suite
    for folder in os.listdir(folder_path+suite+"/"):
        path = folder_path+suite+"/"+folder
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

                # append the result to the suite_dict
                suite_dict.get("tests").append({'tags': tags, 'scenario': filename, 'workload': workload, 'bandwidth': bandwidth, 'iops': iops, 'Device_Response_Time': Device_Response_Time, 'interleave_program_cmd': interleave_program_cmd, 'multiplane_program_cmd': multiplane_program_cmd, 'copy_program_cmd': copy_program_cmd, 'Average Avg_Queue_Length': avg_avg_queue_length, 'Average STDev_Queue_Length': avg_stdev_queue_length})
                jstr = json.dumps(suite_dict, indent = 4)

    with open(folder_path+suite+'.json', 'a') as json_file:
        json_file.write(jstr + '\n')

if __name__ == "__main__":
    if len(sys.argv) > 2:
        suite_tag = sys.argv[1]
        test_tags = sys.argv[2]
    parse(suite_tag, test_tags)