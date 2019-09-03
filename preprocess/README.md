# TwoRavens Preprocess

Python package to produce TwoRavens metadata

```
from raven_preprocess.preprocess_runner import PreprocessRunner

# process a data file
#
run_info = PreprocessRunner.load_from_file('input/path/my-data-file.csv')

# Did it work?
#
if not run_info.success:
    # nope :(
    #
    print(run_info.err_msg)
else:
    # yes :)
    #
    runner = run_info.result_obj

    # show the JSON (string)
    #
    print(runner.get_final_json(indent=4))

    # retrieve the data as a python OrderedDict
    #
    metadata = runner.get_final_dict()

    # iterate through the variables
    #
    for vkey, vinfo in metadata['variables'].items():
        print('-' * 40)
        print(f'--- {vkey} ---')
        print('nature:', vinfo['nature'])
        print('invalidCount:', vinfo['invalidCount'])
        print('validCount:', vinfo['validCount'])
        print('uniqueCount:', vinfo['uniqueCount'])
        print('median:', vinfo['median'])
        print('etc...')
```        

```
# -------------------------
# Preprocess a single file,
# Write output to screen
# -------------------------
from raven_preprocess.preprocess import run_preprocess
run_preprocess('path-to-input-file.csv')

# -------------------------
# Preprocess a single file,
# Write output to file
# -------------------------
from raven_preprocess.preprocess import run_preprocess
run_preprocess('path-to-input-file.csv', 'path-to-OUTPUT-file.csv')
```
