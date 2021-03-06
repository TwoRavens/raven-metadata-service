# Deploying EventData on Google Compute Engine (gce)

These steps deploy the TwoRavens EventData application using Docker images from https://hub.docker.com/r/tworavens/

- **Prerequisite**: admin permissions on the gce kubernetes cluster running event data


## Shortcuts (if you've done it before)

1. Go to the cluster list and "connect" to a Terminal
    - https://console.cloud.google.com/kubernetes/list

```
#
# Retrieve the config file + configmap
#    
mkdir metadata-deploy
cd metadata-deploy
wget https://raw.githubusercontent.com/TwoRavens/raven-metadata-service/master/deploy/metadata-pod-with-svc.yml
wget https://raw.githubusercontent.com/TwoRavens/raven-metadata-service/master/deploy/metadata-python-configmap.yml


#
# Create the configmap (rarely updated)
#
kubectl create -f metadata-python-configmap.yml

# activate the deployment and service
#
kubectl apply -f metadata-pod-with-svc.yml   # start the pod/service

# delete the deployment and service (you can leave the service running)
#
kubectl delete -f metadata-pod-with-svc.yml  # stop the pod/service
# OR: (stop if immediately)
kubectl delete -f metadata-pod-with-svc.yml --grace-period=0 --force

# ---------------
# other
# ---------------

# list pods, the name of the metadata pod is "ravens-preprocess-app"
#
kubectl get pods

# describe pod using name from "kubectl get pods"
#   - will tell if there are errors starting containers
#
kubectl describe pod ravens-preprocess-app

- See a log for a container, e.g. what you see in the rook Terminal when running locally
  - `kubectl logs -f .....` will stream the log

  ```
  kubectl logs ravens-preprocess-app preprocess-web  
  kubectl logs ravens-preprocess-app celery-worker
  kubectl logs ravens-preprocess-app redis  
  ```

# Log into a running container with full admin rights
#   - e.g. look around, see if files are being created, stop/start things, etc
#
kubectl exec -ti  ravens-preprocess-app -c preprocess-web /bin/bash
kubectl exec -ti  ravens-preprocess-app -c celery-worker /bin/bash
kubectl exec -ti  ravens-preprocess-app -c redis /bin/bash

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
