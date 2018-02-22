import os
from os.path import isfile, isdir, join
import time
from basic_preprocess import preprocess_csv_file

file_dir = '../test_input'
output_dir = '../test_output'


def try_1_file():
    r = preprocess_csv_file.delay(join(file_dir, 'fearonLaitin.tab'), output_dir)

    print(r)

    is_ready = r.ready()
    while not is_ready:
        time.sleep(3)
        is_ready = r.ready()

    print(r.result)


def try_directory():
    task_items = []
    cnt = 0
    for item in os.listdir(file_dir):
        if not item.endswith('.tab'):
            continue
        full_path = join(file_dir, item)
        r = preprocess_csv_file.delay(full_path, output_dir)
        task_items.append(r)

    time.sleep(5)
    cnt = 0
    for t in task_items:
        cnt += 1
        if t.ready():
            print(cnt, t.result)
        else:
            print(cnt, 'not ready')

if __name__ == '__main__':
    try_1_file()

"""
# window 1
redis-server /usr/local/etc/redis.conf

# window 2
celery -A basic_preprocess worker --loglevel=info
"""
