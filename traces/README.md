# Trace file columns definition

## compile trace generator

```bash
c++ trace_maker.cpp -o trace_generator_sequential
c++ trace_maker_random.cpp -o trace_generator_random
mv trace_generator_sequential trace_generator_random trace_files
```

Or run `python3 gen_trace.py` to compile the trace generator.

## run gen_trace.py

run `python3 gen_trace.py` to create traces for the following feature combination (default):

- request size: [4k,8k,16k,32k,64k]
- intensity_us: [50,52,54,56,58,60]
- starting zone: [0,1,17,33,49]
- type: ["write", "read", "mixed"]
- read_percentage = [10,25,50,75,90], only used when type is "mixed"

## trace format

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
