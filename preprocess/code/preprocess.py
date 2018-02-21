"""Main module to call all sub modules"""
from os.path import abspath, dirname, join
import json
from preprocess_runner import PreprocessRunner


CURRENT_DIR = dirname(abspath(__file__))
INPUT_DIR = join(dirname(CURRENT_DIR), 'input')
OUTPUT_DIR = join(dirname(CURRENT_DIR), 'output')


def test_run(input_file, output_filepath):
    """Main test run class for this module"""

    runner, err_msg = PreprocessRunner.load_from_csv_file(input_file)
    if err_msg:
        print(err_msg)
        return

    if runner.has_error:
        print(runner.error_message)
        return

    runner.show_final_info()

    jstring = runner.get_final_json(indent=4)
    print(jstring)

    open(output_filepath, 'w').write(jstring)

    print('file written: %s' % output_filepath)


if __name__ == '__main__':
    input_csv = join(INPUT_DIR, 'test_file_01.csv')
    output_file = join(OUTPUT_DIR, 'test_file_01_preprocess.json')

    test_run(input_csv, output_file)
