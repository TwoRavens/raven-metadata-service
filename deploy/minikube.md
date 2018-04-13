# Minikube

Build local docker images and run on minikube.  
Commands may be run from the top of the directory, e.g. right under `raven-metadata-service`


### Startup

```
minikube start --vm-driver=xhyve
eval $(minikube docker-env)
minikube dashboard
```

### Build images

```
docker build -t tworavens/raven-metadata-service:latest -f Dockerfile-web .
```

### Run it!

```
# get the pod running
#
kubectl apply -f deploy/mk-metadata-deploy.yml --validate=false

# Run service and view locally
#
kubectl apply -f deploy/mk-metadata-service.yml
minikube service ravens-preprocess-svc

```

### Stop it!

```
# Shutdown svc and deploy
#
kubectl delete -f deploy/mk-metadata-service.yml   # stop service
kubectl delete -f deploy/mk-metadata-deploy.yml  # stop deploy
```


### Other commands

```
# show pods
kubectl get pods

# Log into running container
# xkubectl exec -it [pod name] -- /bin/bash
kubectl exec -it  [pod name] -c preprocess-web /bin/bash


# describe containers in pod
kubectl describe pod/[pod name]

```

## Old/Other

```
# forward to local ports
#
kubectl get pods # get pod name
kubectl port-forward [pod name] 8080:8080

# Create service via command
#
kubectl expose deployment  ravens-preprocess-web --type="LoadBalancer" --port=8080 --target-port=8080
```
