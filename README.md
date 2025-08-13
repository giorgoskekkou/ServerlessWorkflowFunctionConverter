# ServerlessWorkflowFunctionConverter
This is a Compiler based project that gets as input server-less benchmarks and does full reduction on them by combining them all in the same file and container

---

## Table of Contents
- [Requirements](#requirements)
- [Setup steps](#setup-steps)
- [Status](#status)
- [Script to count the number of lines](#script-to-count-the-number-of-lines)

---

# Requirements
```
update

Python3
pip
make

pip install requirements.txt
pip install -r requirements.txt
```

# Setup steps

Requirements:
- k3s (kubectl)
- kn
- docker



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
`curl -H "Content-Type: application/json" -d "{}" http://video-full.default.172.20.46.114.sslip.io`

### Kn commands
`kn func list`
`kn func delete [func-name]`

### kubectl
`kubectl get pods -A`
`kubectl get all -A`

#### Troubleshoot
`kubectl get ksvc`
`kubectl describe ksvc [name]`
`kubectl get pods -n istio-system`

`kubectl get pods -n knative-eventing -- not working`

### DESTROY Cluster
`kubectl delete --all namespaces`


`/usr/local/bin/k3s-uninstall.sh`

`macropod/tools/collection/metrics/metrics.go`
`go run metrics.go enps3 out.csv`

### first time build
`kn func build --push=true`

### DEPLOY
`kn func deploy --build=true --push=true`
 
### TEST
`curl -H "Content-Type: application/json" -d "{}" http://video-all.default.10.0.2.15.sslip.io`

### create function
`func create -l python function-name`

---

# Status
## MODULES
- [X] YAML merger 
- [X] Import merger
- [X] Requirements merger
- [ ] Post Request replacer
- [ ] Function merger



## Merge requirements

### Handle conflicts:
- same depedancy with version and without -> wins the one with version ?
- same depedancy wih 2 different versions -> wins the one with the newer version? NO the earliest ?
- **Deal with mulitple versions**


## Merge imports

### Handle conflicts:
- import pandas as pd vs import pandas pan -> OK to have multiple aliases
- same module but different function -> merge on the same line

## Other
- Why is there 2 different locations for requirements -> **Just Ignore utils/tracing/.**


---

### Script to count the number of lines

Command that will print the total number of lines of all the .py files:
<!-- #### NEW -->
`find src -name "*.py" -type f -exec wc -l {} \; | awk '{total += $1} END {print total}'`

**Can also be found in the `count_lines.sh`**

--- 