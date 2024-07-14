# Requirements
- k3s (kubectl)
- kn
- docker

<br><br>


## Step 1
**Run script** from macropod/tools/deployment/master-kn.sh

`./master-kn.sh [ip add] [username]`

## Step 2
**Run script** from macropod/tools/workflow/kn
`./deploye-full-video.sh wob`

### Replace IP
`./set-host-ip-params.sh [old_ip] [new_ip]`
old: 127.0.0.1
new: actual ip


### Set IP
`./set-host-ip-params.sh [ip add] 172.20.46.114`

### Revert IP
`./set-host-ip-params.sh 172.20.46.114 [ip add]`

### POST request
curl -H "Content-Type: application/json" -d "{}" http://video-full.default.172.20.46.114.sslip.io


### Kn commands
kn func list
kn func delete [func-name]

### kubectl
kubectl get pods -A
kubectl get all -A

#### Troubleshoot
kubectl get ksvc
kubectl describe ksvc [name]
kubectl get pods -n istio-system

kubectl get pods -n knative-eventing -- not working

### DESTROY Cluster
kubectl delete --all namespaces


/usr/local/bin/k3s-uninstall.sh

macropod/tools/collection/metrics/metrics.go
go run metrics.go enps3 out.csv

kn func build --push=true