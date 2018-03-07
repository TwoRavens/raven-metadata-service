
# early dev note...

```
# window 1
redis-server /usr/local/etc/redis.conf
redis-cli flushall  /usr/local/etc/redis.conf

# window 2
cd /preprocess_service/code
celery -A basic_preprocess worker --loglevel=info

#celery -A basic_preprocess worker --loglevel=info -Ofair
#celery -A basic_preprocess worker --loglevel=warning --concurrency=2 -n worker1@%h
#celery -A basic_preprocess worker --loglevel=warning --concurrency=2 -n worker2@%h

# window 3
cd /preprocess_web/code
python manage.py runserver
```
