#include <string>
#include <stdio.h>
#include <iostream>
#include <fstream>
#include <time.h>

using namespace std;

const unsigned int sector_size_in_bytes = 512;
const unsigned int zone_size_MB = 256;
unsigned int request_size_in_KB = 8;
unsigned int smallest_zone_number = 2;
unsigned int biggest_zone_number;
unsigned int total_size_of_accessed_file_in_GB = 1;
unsigned int total_no_of_request = 10000;
unsigned int read_write = 1; // 0: write, 1: read, 2: mixed read/write
unsigned int read_percentage = 50; // used only when read_write == 2
unsigned int intensity_us = 60;
unsigned int zone_number;
string type_of_request;

struct zone {
    unsigned int zone_ID;
    unsigned long long int start_LBA;
    unsigned long long int writepoint_LBA;
    bool available;
};

struct zone *zonelist;

bool all_zonelist_false()
{
    for (int k = 0; k < zone_number; k++) {
        if(zonelist[k].available == true)
            return false;
    }
    return true;   
}

int main(int argc, char** argv) {

    if (argc != 7) {
        cout << "This generates a random write requests." << std::endl;
        cout << "Usage: ./trace_generator_random [request size in KB] [begin zone number] [total request size] [write(0)/read(1)/mixed(2)] [read_percentage] [intensity in us]"<<endl;
        return -1;
    }

    request_size_in_KB = atoi(argv[1]);
    smallest_zone_number = atoi(argv[2]);
    total_size_of_accessed_file_in_GB = atoi(argv[3]);
    read_write = atoi(argv[4]);
    read_percentage = atoi(argv[5]);
    intensity_us = atoi(argv[6]);
    switch(read_write) {
        case 0: type_of_request = "write";
            break;
        case 1: type_of_request = "read";
            break;
        case 2: type_of_request = "mixed_read"+to_string(read_percentage);
            break;
        default:
            cout << "read_write should be 0, 1, or 2" << endl;
            return -1;
    }

    string outputfile = "random_"+type_of_request+"_" + to_string(request_size_in_KB) + "KB_from_zone" \
                        + to_string(smallest_zone_number) + "_" + to_string(total_size_of_accessed_file_in_GB) + "GB_" + to_string(intensity_us) + "us";
    cout << "output file: " << outputfile << endl;
    
    zone_number = total_size_of_accessed_file_in_GB * 1024 / zone_size_MB;
    cout << "We are gonna access " << zone_number << " zones" << endl;

    zonelist = (struct zone*)malloc(sizeof(struct zone) * (zone_number+1));

    // zonelist initialization
    for (int i = 0; i < zone_number + 1; i++) {
        zonelist[i].zone_ID = smallest_zone_number + i;
        zonelist[i].start_LBA = zonelist[i].zone_ID * 1024 * 512; // 256 MB / 512 B
        // cout << "zone" << zonelist[i].zone_ID << "'s start_LBA: " << zonelist[i].start_LBA << endl;
        zonelist[i].writepoint_LBA = zonelist[i].start_LBA;
        zonelist[i].available = true;
    }
    zonelist[zone_number].available = false;
    // The reason why the number of zonelist is zone_number+1 is for the checking zone fillup

    srand(time(NULL));

    ofstream writeFile;
    writeFile.open(outputfile);
    string trace_line = "";

   // cout << "request size is " << request_size_in_KB << " KB" << endl;
    total_no_of_request =  total_size_of_accessed_file_in_GB * 1024 * 1024 / request_size_in_KB;

    unsigned long long int first_arrival_time = 51300;

    string arrival_time;
    string start_LBA;
    string device_number;
    string request_size_in_sector;

    unsigned long long int prev_arrival_time = first_arrival_time;
    unsigned long long int prev_start_LBA;
    unsigned int read_count = 0, write_count = 0;
    int i, j;
    int zone_id;
    for (i = 0; i < total_no_of_request; i++) {
        do {
            if (all_zonelist_false()) {
                cout << "Every zone is filled up!" << endl;
                writeFile.close();
                return 0;
            }
            zone_id = rand() % zone_number;
        } while (zonelist[zone_id].available == false);

        int access_count_in_one_zone = rand() % 50;
        prev_start_LBA = zonelist[zone_id].writepoint_LBA;

        for (j = 0; j < access_count_in_one_zone; j++, i++) {
            arrival_time = to_string(prev_arrival_time);
            start_LBA = to_string(prev_start_LBA);
            device_number = "1";
            request_size_in_sector = to_string(request_size_in_KB * 2); // 2 == 1024 / sector_size_in_bytes
            
            if (type_of_request == "mixed_read"+to_string(read_percentage)) {
                if (rand() % 100 < read_percentage) {
                    read_write = 1;
                    read_count++;
                } else {
                    read_write = 0;
                    write_count++;
                }
            }

            trace_line = arrival_time + " " + device_number + " " + start_LBA + " " + request_size_in_sector + " " + to_string(read_write) + "\n";
            
            writeFile.write(trace_line.c_str(), trace_line.size());
            trace_line.clear();
            
            prev_arrival_time = prev_arrival_time + (intensity_us * 1000); // this assumes the time unit defined in workload.xml is in NANOSECOND
            prev_start_LBA = prev_start_LBA + (request_size_in_KB * 2); // 2 == 1024 / sector_size_in_bytes
            zonelist[zone_id].writepoint_LBA = prev_start_LBA;
            if (zonelist[zone_id].writepoint_LBA >= zonelist[zone_id+1].start_LBA) {
                zonelist[zone_id].available = false;
                cout << "zone #" << zonelist[zone_id].zone_ID << " is filled up! no more write request!!" << endl;
                break;
            }
        }
    }
    cout << "total number of requests: " << total_no_of_request << ", read count: " << read_count << ", write count: "<< write_count << endl;
    writeFile.close();
    return 0;
}
