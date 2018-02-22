"""Main module to call all sub modules"""
from os.path import abspath, dirname, join
import sys
from preprocess_runner import PreprocessRunner
from msg_util import msg, msgt, dashes


CURRENT_DIR = dirname(abspath(__file__))
INPUT_DIR = join(dirname(CURRENT_DIR), 'input')
OUTPUT_DIR = join(dirname(CURRENT_DIR), 'output')


def test_run(input_file, output_filepath=None):
    """Main test run class for this module"""

    if input_file.lower().endswith('.tab'):
        runner, err_msg = PreprocessRunner.load_from_tabular_file(input_file)
    else:
        runner, err_msg = PreprocessRunner.load_from_csv_file(input_file)

    if err_msg:
        msgt(err_msg)
        return

    runner.show_final_info()

    jstring = runner.get_final_json(indent=4)
    msg(jstring)

    if output_filepath:
        try:
            open(output_filepath, 'w').write(jstring)
            msgt('file written: %s' % output_filepath)
        except OSError as os_err:
            msgt('Failed to write file: %s' % os_err)

def show_instructions():
    """show command line instructions"""
    info = """
--------------------------
preprocess a single file
--------------------------

> python preprocess.py [input csv file]
> python preprocess.py [input csv file] [output file name]

OR

> python preprocess.py test

"""
    print(info)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'test':
            input_csv = join(INPUT_DIR, 'test_file_01.csv')
            output_file = join(OUTPUT_DIR, 'test_file_01_preprocess.json')
            test_run(input_csv, output_file)
        else:
            test_run(sys.argv[1])

    elif len(sys.argv) == 3:
        test_run(sys.argv[1], sys.argv[2])
    else:
        show_instructions()
