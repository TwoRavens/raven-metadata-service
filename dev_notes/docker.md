
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
