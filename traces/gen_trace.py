import os
import subprocess

req_size_in_kb = ["4", "8", "16", "32", "64"]
intensity_us = ["50","52","54","56","58","60"]
trace_size_in_GB = "1"
begin_zone = [0,1,17,33,49]
type_of_request = ["write", "read", "mixed"]
read_percentage = [10, 25, 50, 75, 90]

commands = [
    "c++ trace_maker.cpp -o trace_generator_sequential",
    "c++ trace_maker_random.cpp -o trace_generator_random",
    "mv trace_generator_sequential trace_generator_random trace_files"
]

# Run the commands one by one
for cmd in commands:
    subprocess.run(cmd, shell=True)

os.chdir('trace_files')

for req_size in req_size_in_kb:
    for zone in begin_zone:
        for intensity in intensity_us:
            for tor, type in enumerate(type_of_request):
                for read_percent in read_percentage:
                    if type == "mixed":
                        trace_file_seq = "sequential_"+type+"_read"+str(read_percentage)+"_" + req_size+ "KB_from_zone"+str(zone)+ "_" + trace_size_in_GB + "GB_"+intensity+"us"
                        trace_file_rand = "random_"+type+"_read"+str(read_percentage)+"_" + req_size+ "KB_from_zone"+str(zone)+ "_" + trace_size_in_GB + "GB_"+intensity+"us"
                    else:
                        trace_file_seq = "sequential_"+type+"_" + req_size+ "KB_from_zone"+str(zone)+ "_" + trace_size_in_GB + "GB_"+intensity+"us"
                        trace_file_rand = "random_"+type+"_" + req_size+ "KB_from_zone"+str(zone)+ "_" + trace_size_in_GB + "GB_"+intensity+"us"
                
                    if not os.path.exists(trace_file_seq):
                        cmd = os.getcwd()+"/trace_generator_sequential "+req_size+" "+str(zone)+" "+trace_size_in_GB+" "+str(tor)+" "+str(read_percent)+" "+intensity
                        os.system(cmd)
                    if not os.path.exists(trace_file_rand):
                        cmd = os.getcwd()+"/trace_generator_random "+req_size+" "+str(zone)+" "+trace_size_in_GB+" "+str(tor)+" "+str(read_percent)+" "+intensity
                        os.system(cmd)
