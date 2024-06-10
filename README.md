# BenchmarkFusion
This is a Compiler based project that gets as input server-less benchmarks and do full reduction on them by combining them all in the same file and container


## To run


## To stop


### Script to count the number of lines

Command that will print the total number of lines of all the .py files:
#### NEW
`find src -name "*.py" -type f -exec wc -l {} \; | awk '{total += $1} END {print total}'`

#### OLD
`find . -name "*.py" -type f -exec wc -l {} \; | awk '{total += $1} END {print total}'`
