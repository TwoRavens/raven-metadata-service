## preprocess script

```
# build image
#
docker build -t preprocess .

# run image against a single file
#
docker run --rm -ti -v /ravens_volume:/ravens_volume --name=raven_ingest preprocess:latest [input path]

# run bash
#
docker run --rm -ti -v /ravens_volume:/ravens_volume --name=raven_ingest --entrypoint=/bin/bash preprocess:latest

# run with /ravens_volume mapped to local input
#
docker run --rm -ti -v ~/Documents/github-rp/raven-metadata-service/preprocess/input:/ravens_volume --name=raven_ingest preprocess:latest
```

docker run --rm -ti -v /Users/ramanprasad/Desktop:/dtop --name=raven_ingest preprocess:latest [input path]


## preprocess web

```
# build
#
docker build -t preprocess_web -f Dockerfile .

# run
#
docker run --rm -p 8080:8080 -v /tmp:/tmp --env REDIS_HOST=docker.for.mac.localhost --env DJANGO_SETTINGS_MODULE=ravens_metadata.settings.docker_test_settings --name pweb preprocess_web

#--net="host"


# shell into running container
#
 docker exec -ti pweb /bin/bash


## Other

Travis env variables: https://docs.travis-ci.com/user/environment-variables/
