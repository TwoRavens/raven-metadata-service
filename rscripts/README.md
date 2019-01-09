# preprocess.R

This folder contains the `preprocess.R` script.  In addition, `runPreprocess.R` is a wrapper for the script.

1. **preprocess.R** - contains the `preprocess` function
2. **runPreprocess.R** - Runs the `preprocess` function, passing in command line arguments.

## Usage:

```
# Format
#
Rscript runPreprocess.R [input file] [directory containing preprocess.R file]

# Example
#
Rscript runPreprocess.R ../test_data/fearonLaitin.csv .
```
