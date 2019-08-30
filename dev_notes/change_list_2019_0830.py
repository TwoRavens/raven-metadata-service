"""
One-time update for repository.
When changing /preprocess/code to preprocess/raven_preprocess
"""
import os
from os.path import join

CHANGE_PAIRS = (\
  ('from basic_utils', 'from raven_preprocess.basic_utils'),
  ('from col_info_constants', 'from raven_preprocess.col_info_constants'),
  ('from column_info', 'from raven_preprocess.column_info'),
  ('from custom_statistics_util', 'from raven_preprocess.custom_statistics_util'),
  ('from data_source_info', 'from raven_preprocess.data_source_info'),
  ('from dataset_level_info_util', 'from raven_preprocess.dataset_level_info_util'),

  ('from file_format_constants', 'from raven_preprocess.file_format_constants'),
  ('from file_format_util', 'from raven_preprocess.file_format_util'),
  ('from msg_util', 'from raven_preprocess.msg_util'),
  ('from np_json_encoder', 'from raven_preprocess.np_json_encoder'),

  ('from plot_values', 'from raven_preprocess.plot_values'),
  ('from preprocess_runner', 'from raven_preprocess.preprocess_runner'),
  ('from summary_stats_util', 'from raven_preprocess.summary_stats_util'),

  ('from type_guess_util', 'from raven_preprocess.type_guess_util'),
  ('from update_constants', 'from raven_preprocess.update_constants'),
  ('from variable_display_util', 'from raven_preprocess.variable_display_util'),
  ('from version_number_util', 'from raven_preprocess.version_number_util'),

  ('import col_info_constants', 'import raven_preprocess.col_info_constants'),
  ('import update_constants', 'import raven_preprocess.update_constants'),

  ('to__fi_nd', 'to_rep_lace'),

  )

def make_changes():

    rootdir = '/Users/ramanprasad/Documents/github-rp/raven-metadata-service/'

    # Find files
    #
    files_to_check = []
    for subdir, _dirs, files in os.walk(rootdir):
        for file in files:
            fullpath = join(subdir, file)
            if fullpath.endswith('.py') and \
                fullpath.find('/__pycache__') == -1 and \
                fullpath.find('/node_modules') == -1 and \
                fullpath.find('/migrations') == -1:
                files_to_check.append(fullpath)

    print('\n'.join(files_to_check))
    print(len(files_to_check))

    # Update files
    #
    cnt = 0
    for fname in files_to_check:
        cnt += 1
        print('(%s) check: %s' % (cnt, fname))

        content = None
        with open(fname, 'r') as reader:
            content = reader.read()

        for find_val, replace_val in CHANGE_PAIRS:
            content = content.replace(find_val, replace_val)

        with open(fname, 'w') as updated_file:
            updated_file.write(content)

        print('file updated:', fname)

if __name__ == '__main__':
    make_changes()
