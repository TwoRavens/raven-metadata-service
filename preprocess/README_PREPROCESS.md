# TwoRavens Preprocess

Python package to produce TwoRavens metadata

```
# -------------------------
# Preprocess a single file,
# Write output to screen
# -------------------------
fab run_preprocess:[input file name]

# Example:
fab run_preprocess:../../test_data/fearonLaitin.csv


# -------------------------
# Preprocess a single file,
# Write output to file
# -------------------------
fab run_preprocess:[input file name],[output file]
fab run_preprocess:../../test_data/fearonLaitin.csv,/tmp/fearonLaitin.json
```
