# Trace file columns definition

## compile tracemaker

c++ trace_maker.cpp -o trace_generator

## run gen_trace.py

run `py gen_trace.py` to create traces for the following feature combination:

- request size 4k, 16k, 64k, 256k, 1M, 4M, 16M, 64M
- start zone 1, (support 32 streams)
- 

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
## request type
0: write
1: read