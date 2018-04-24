# Deploying EventData on Google Compute Engine (gce)

These steps deploy the TwoRavens EventData application using Docker images from https://hub.docker.com/r/tworavens/

- **Prerequisite**: admin permissions on the gce kubernetes cluster running event data


## Shortcuts (if you've done it before)

1. Go to the cluster list and "connect" to a Terminal
    - https://console.cloud.google.com/kubernetes/list

```
# pull the latest config code
#
cd raven-metadata-service
git pull

# activate the deployment and service
#
kubectl apply -f deploy/metadata-deploy.yml  # start a new deployment
kubectl apply -f deploy/metadata-service.yml  # expose the app to the web/external IP

# delete the deployment and service (you can leave the service running)
#
kubectl delete -f deploy/metadata-deploy.yml  # stop the current deployment
kubectl delete -f deploy/metadata-service.yml # stop the service

# ---------------
# other
# ---------------

# list pods, the name of the eventdata pod is "ravens-eventdata-web-xxxxxx-xxxx"
#
kubectl get pods

# describe pod using name from "kubectl get pods"
#   - will tell if there are errors starting containers
#
kubectl describe pod ravens-eventdata-web-xxxxxx-xxxx

# See a log for a container, e.g. what you see in the rook Terminal when running locally
#   - `kubectl logs -f .....` will stream the log
#
kubectl logs ravens-eventdata-web-xxxxxx-xxxx rook-service  # rook server log
kubectl logs ravens-eventdata-web-xxxxxx-xxxx ta3-main  # python server log
kubectl logs ravens-eventdata-web-xxxxxx-xxxx ravens-nginx  # nginx log

# Log into a running container with full admin rights
#   - e.g. look around, see if files are being created, stop/start things, etc
#
kubectl exec -ti  ravens-eventdata-web-xxxxxx-xxxx -c rook-service /bin/bash
kubectl exec -ti  ravens-eventdata-web-xxxxxx-xxxx -c ta3-main /bin/bash
kubectl exec -ti  ravens-eventdata-web-xxxxxx-xxxx -c ravens-nginx /bin/bash

```

## Open a Terminal within a browser (Chrome)

1. Go to the cluster list:
    - https://console.cloud.google.com/kubernetes/list
    - `cluster-1` should appear as a row in the main part of the page
1. Click "connect" which opens a shell in the browser
1. Click "Run in Cloud Shell"
    - A Terminal window opens in the browser
1. Press the "return" key to execute the auto-added line.  Usually something like this:
    - `gcloud container clusters get-credentials cluster-1 --zone us-central1-a --project raven2-186120`


---


### downsize cluster

- Set size to zero

```
gcloud container clusters resize cluster-1 --size=0 --zone=us-central1-a
```

### get cluster going again

- Set size back to 3 (or 2)

```
gcloud container clusters resize cluster-1 --size=2 --zone=us-central1-a
```
