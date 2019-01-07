"""
Script for running R preprocess
"""
import sys
from os.path import isfile
import delegator    # helper package for subprocess
import json


def parse_preprocess_output(pout):
    """Parse output for preprocess JSON"""
    phrase = '---START-PREPROCESS-JSON---'
    idx = pout.find(phrase)
    if idx == -1:
        print('Not found!')
        return None

    end_phrase = '---STOP-PREPROCESS-JSON---'
    end_idx = pout.find(end_phrase, idx+len(phrase))
    if end_idx == -1:
        print('Not found!')
        return None


    print('got it')
    pout_formatted = pout[idx+len(phrase):end_idx]

    #line1_fmt = '[1] "'
    #pout_formatted = pout_formatted.replace(line1_fmt, '')

    return pout_formatted

def run_r_preprocess(filename):
    """Run the R script"""
    if not isfile(filename):
        print('File not found: %s' % filename)
        return

    rscript_cmd = 'Rscript runPreprocess.R %s' % filename

    sub = delegator.run(rscript_cmd)

    metadata = parse_preprocess_output(sub.out)
    metadata = metadata.strip()
    print('-' * 40)
    print(metadata)
    print('-' * 40)

    m2 = json.loads(metadata)
    print(json.dumps(m2, indent=4))
    #print(m2.keys())

if __name__ == '__main__':

    args = sys.argv
    print('args:', args)
    if len(args) == 1:
        print('filename argument needed')
    elif len(args) == 2:
        run_r_preprocess(args[1])
    else:
        print('Please supply a *single* file name argument')
