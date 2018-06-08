
## example of putting file contents in a secrets

```shell

@cloudshell:~ (raven2-186120)$ echo husky > dogs.txt

@cloudshell:~ (raven2-186120)$  kubectl create secret generic test-env-variable --from-file=TEST_ENV_VARIABLE=./dogs.txt                                                      
secret "test-env-variable" created


@cloudshell:~ (raven2-186120)$ kubectl get secrets
NAME                  TYPE                                  DATA      AGE
apikey                Opaque                                1         23h
default-token-j9xm1   kubernetes.io/service-account-token   3         197d
test-env-variable     Opaque                                   1         19h

@cloudshell:~ (raven2-186120)$ kubectl get secret test-env-variable -o yaml
apiVersion: v1
data:
  TEST_ENV_VARIABLE: aHVza3kK
kind: Secret
metadata:
  creationTimestamp: 2018-06-01T15:43:37Z
  name: test-env-variable
  namespace: default
  resourceVersion: "22992407"
  selfLink: /api/v1/namespaces/default/secrets/test-env-variable
  uid: 8cfd80a2-65b2-11e8-9157-42010a800057
type: Opaque

@cloudshell:~ (raven2-186120)$ echo 'aHVza3kK' | base64 --decode
husky
```
