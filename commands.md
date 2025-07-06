# 🚀 Azure AKS & Kubernetes Command Cheat Sheet

## 🧩 Azure AKS Cluster Setup & Access

```bash
az login
az account set --subscription <subscription-id>
az aks get-credentials --resource-group <rg-name> --name <aks-name> --overwrite-existing
az aks command invoke --resource-group <rg-name> --name <aks-name> --command "kubectl get pods -A"
```
### 🛠️ AKS Node Pool Management
```bash
az aks nodepool list --resource-group <rg-name> --name <aks-name> -o table
az aks nodepool scale --resource-group <rg-name> --cluster-name <aks-name> --name agentpool --node-count 2
az aks nodepool scale --resource-group <rg-name> --cluster-name <aks-name> --name workerpool --enable-cluster-autoscaler --min-count 1 --max-count 2
az aks start --resource-group <rg-name> --name <aks-name>
```
### ⚙️ Node Tainting & Labeling
```bash
kubectl label node <node-name> node-role.kubernetes.io/system=true
kubectl taint nodes <node-name> CriticalAddonsOnly=true:NoSchedule
kubectl describe node <node-name> | grep Taints
```

###📦 Cluster Info & Node Management
```bash
kubectl cluster-info
kubectl config view
kubectl version
kubectl api-resources
kubectl get nodes
kubectl get nodes -o wide
kubectl describe node <node-name>
kubectl get nodes --show-labels
```

### 🚀 Pod & Deployment Operations
``` bash
kubectl run nginx-test --image=nginx
kubectl run mynginx --image=nginx:latest --port=8081
kubectl run myjenkins --image=jenkins/jenkins --port=8080
kubectl create deployment nginx --image=nginx
kubectl scale deployment nginx --replicas=3
kubectl delete deployment <name>
```

### 🌐 Service Exposure
```bash
kubectl expose deployment nginx --type=ClusterIP --port=80 --target-port=80
kubectl expose deployment nginx --type=NodePort --port=80
kubectl expose deployment nginx --type=LoadBalancer --port=80 --target-port=80
kubectl expose deployment hello-world-rest-api --type=LoadBalancer --port=8080
```

### 🔍 Observability & Debugging
```bash
kubectl get pods
kubectl get pods -A
kubectl get pods -o wide
kubectl describe pod <pod-name>
kubectl get pod <pod-name> -o yaml
kubectl logs <pod-name>
kubectl top pods
```
### 🧠 Deployment Inspection & Labeling
```bash
kubectl get deployments
kubectl describe deployment nginx
kubectl get deployments --show-labels
kubectl label deployment nginx app=web
```
