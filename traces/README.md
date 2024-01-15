# Trace file columns definition


## Trace Format

You can define a trace-based workload for MQSim, using the <IO_Flow_Parameter_Set_Trace_Based> XML tag. Currently, MQSim can execute ASCII disk traces define in [8] in which each line of the trace file has the following format:

**1.Request_Arrival_Time
2.Device_Number
3.Starting_Logical_Sector_Address
4.Request_Size_In_Sectors
5.Type_of_Requests[0 for write, 1 for read]**

[request arrival time] [device number] [start LBA] [request size] [request type]

``` bash
==> sequential_write_8KB_from_zone1_1GB <==
4851300 1 524288 16 0
4864300 1 524304 16 0
4871300 1 524320 16 0
4886300 1 524336 16 0
4887300 1 524352 16 0
```

the time unit is defined in workload xml, for example, wordload_zone_max.xml defines it with <Time_Unit>NANOSECOND</Time_Unit>.

## Real Traces

1. OLTP traces
Download real OLTP traces from [here](https://traces.cs.umass.edu/index.php/Storage/Storage) and store them to MQSim/traces/real_trace_files/

```bash
cd traces/real_trace_files/
python3 ../trans_trace.py Financial/Financial1.spc Financial/fin1_ascii -asu 0-23
python3 ../trans_trace.py Financial/Financial2.spc Financial/fin2_ascii -asu 0-18
python3 ../trans_trace.py WebSearch/WebSearch1.spc WebSearch/ws1_ascii -asu 0-2
python3 ../trans_trace.py WebSearch/WebSearch2.spc WebSearch/ws2_ascii -asu 0-2
python3 ../trans_trace.py WebSearch/WebSearch3.spc WebSearch/ws3_ascii -asu 0-2
```

2. YCSB on RocksDB traces

Download YCSB traces from [here](http://iotta.snia.org/traces/block-io) and store them to MQSim/traces/real_trace_files/

```bash
cd traces/real_trace_files/

```

## Synthetic Traces

### compile trace generator

```bash
c++ trace_maker.cpp -o trace_generator_sequential
c++ trace_maker_random.cpp -o trace_generator_random
mv trace_generator_sequential trace_generator_random trace_files
```

Or run `python3 gen_trace.py` to compile the trace generator.

### run gen_trace.py

run `python3 gen_trace.py` to create traces for the following feature combination (default):

- request size: [4k,8k,16k,32k,64k]
- intensity_us: [50,52,54,56,58,60]
- starting zone: [0,1,17,33,49]
- type: ["write", "read", "mixed"]
- read_percentage = [10,25,50,75,90], only used when type is "mixed"

