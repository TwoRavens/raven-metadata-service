import os
from os.path import isfile, isdir, join
import time
from basic_preprocess import preprocess_csv_file

file_dir = '../test_input'
output_dir = '../test_output'


def try_1_file():
    fname = 'data_student.tab'# 'fearonLaitin.tab' # 'full1960.tab'
    r = preprocess_csv_file.delay(join(file_dir, fname), output_dir)

    print(r)

    is_ready = r.ready()
    while not is_ready:
        time.sleep(3)
        is_ready = r.ready()

    print(r.result)

def try_directory():
    start_time = time.time()

    task_items = []
    num_files = 0
    cnt = 0
    for loop_num in range(1):
        for item in os.listdir(file_dir):
            if not item.endswith('.tab'):
                continue
            if item.endswith('1960.tab') or item.endswith('NLSYfull.tab'):
                continue
            full_path = join(file_dir, item)

            try:
                r = preprocess_csv_file.delay(full_path, output_dir)
                num_files += 1
            except Exception as ex_obj:
                print('Failed: %s' % ex_obj)
            print(r.id, item)
            task_items.append(r)

    while len(task_items) > 0:
        cnt = 0
        to_remove = []
        for ye_task in task_items:
            cnt += 1
            if ye_task.ready():
                result_str = '%s' % ye_task.result
                #print(t.result.keys())
                print(ye_task.id, 'DONE!',
                      ye_task.result['success'],
                      ye_task.result['input_file'])

                if ye_task.result['success']:
                    print('   Elapsed time: %s' % ye_task.result['elapsed_time'])

                to_remove.append(ye_task)
            else:
                print(ye_task.id, 'not ready')

        for tdone in to_remove:
            print('removed: ', tdone)
            tdone.forget()
            task_items.remove(tdone)

        if len(task_items) == 0:
            break
        print('remaining: %s' % len(task_items))
        ptime = 5
        print('pause %d seconds...' % ptime)
        time.sleep(ptime)

        elapsed_time = time.time() - start_time
        elapsed_time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        print('   - elapsed time: %s' % (elapsed_time_str))

    elapsed_time = time.time() - start_time
    elapsed_time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
    print('Total elapsed time: %s' % (elapsed_time_str))
    print('Number files: %d' % num_files)

if __name__ == '__main__':
    #try_1_file()
    try_directory()

"""
# window 1
redis-server /usr/local/etc/redis.conf
redis-cli flushall  /usr/local/etc/redis.conf

# window 2
celery -A basic_preprocess worker --loglevel=info -Ofair
celery -A basic_preprocess worker --loglevel=warning --concurrency=2 -n worker1@%h
celery -A basic_preprocess worker --loglevel=warning --concurrency=2 -n worker2@%h

# window 3
python test_01.py
"""
