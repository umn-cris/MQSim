import os

#req_size_in_kb = ["4", "16", "64", "256", "1024", "4096", "16384", "65536"]
req_size_in_kb = ["4","8","16","32"]
intensity_us = ["58"]
trace_size_in_GB = "1"
begin_zone = [0]
#begin_zone = [16*i+1 for i in xrange(32)]
type_of_request = "write"

os.chdir('trace_files')

for req_size in req_size_in_kb:
    for zone in begin_zone:
        for intensity in intensity_us:
            trace_file = "sequential_"+type_of_request+"_" + req_size+ "KB_from_zone"+str(zone)+ "_" + trace_size_in_GB + "GB_"+intensity+"us"
            #print (trace_file)

            file_exists = os.path.exists(trace_file)
            #print (file_exists)
            
            if not file_exists:
                cmd = os.getcwd()+"/trace_generator "+req_size+" "+str(zone)+" "+trace_size_in_GB+" 0 "+intensity
                os.system(cmd)
                print ("Created "+trace_file)