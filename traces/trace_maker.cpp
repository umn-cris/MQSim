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
unsigned int biggest_zone_number = 14;
unsigned int total_size_of_accessed_file_in_GB = 1;
unsigned int total_no_of_request = 10000;
unsigned int read_write = 1;
unsigned int intensity_us = 50;
string arrival_time;
string start_LBA;
string device_number;
string request_size_in_sector;
string type_of_request;

int main(int argc, char** argv) {

    if (argc != 6) {
        cout << "This generates a sequential write requets." << endl;
        cout << "Usage: ./trace_generator [request size in KB] [begin zone number] [total request size] [read(1)/write(0)] [intensity in us]"<<endl;
        return -1;
    }

    request_size_in_KB = atoi(argv[1]);
    smallest_zone_number = atoi(argv[2]);
    total_size_of_accessed_file_in_GB = atoi(argv[3]);
    read_write = atoi(argv[4]);
    intensity_us = atoi(argv[5]);

    type_of_request = read_write==1?"read":"write";   // 0 means that it's a write reqeust, read request is "1"

    string outputfile = "sequential_"+type_of_request+"_" + to_string(request_size_in_KB)+ "KB_from_zone"  \
                        + to_string(smallest_zone_number) + "_" + to_string(total_size_of_accessed_file_in_GB) + "GB_" + to_string(intensity_us) + "us";
    cout << "output file name is " << outputfile << endl;

    srand(time(NULL));

    ofstream writeFile;
    writeFile.open(outputfile);
    string trace_line = "";

    //cout << "request size is " << request_size_in_KB << " KB" << endl;
    total_no_of_request = total_size_of_accessed_file_in_GB * 1024 * 1024 / request_size_in_KB;
    cout << "total number of requests is " << total_no_of_request << endl;

    // unsigned long long int first_arrival_time = 4851300;
    unsigned long long int first_arrival_time = 51300;
    unsigned long long int first_start_LBA = smallest_zone_number * 512 * 1024; //256 * 1024 * 1024 / 512; == 256 MB / 512 B
    // |---------512 byte-------||---------512 byte-------|
    // LBA :       1                         2


    unsigned long long int prev_arrival_time = first_arrival_time;
    unsigned long long int prev_start_LBA = first_start_LBA;
    for (int i = 0; i < total_no_of_request; i++) {
        arrival_time = to_string(prev_arrival_time);
        start_LBA = to_string(prev_start_LBA);
        device_number = "1";
        request_size_in_sector = to_string(request_size_in_KB * 2); // 2 == 1024 / sector_size_in_bytes
        
        trace_line = arrival_time + " " + device_number + " " + start_LBA + " " + request_size_in_sector + " " + to_string(read_write) + "\n";
        
        writeFile.write(trace_line.c_str(), trace_line.size());
        trace_line.clear();
        //sscanf(arrival_time.c_str(), "%llu", &prev_arrival_time); 
        //sscanf(start_LBA.c_str(), "%llu", &prev_start_LBA); 

        // prev_arrival_time = prev_arrival_time + ((rand() % 15 + 1) * 1000);
        prev_arrival_time = prev_arrival_time + (intensity_us * 1000);
        prev_start_LBA = prev_start_LBA + request_size_in_KB * 2; // 2 == 1024 / sector_size_in_bytes;
    }
    writeFile.close();
    return 0;
}
