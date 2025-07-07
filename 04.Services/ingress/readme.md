## 🚀 Setup AKS + AGIC (Application Gateway Ingress Controller)

### 🔧 Azure CLI Command

```bash
az aks create \
  --name aks-agic \
  --resource-group sumi-testing \
  --network-plugin azure \
  --enable-managed-identity \
  --enable-addons ingress-appgw \
  --appgw-name myApplicationGateway \
  --appgw-subnet-cidr "10.225.0.0/16" \
  --node-vm-size Standard_B2s \
  --node-count 1 \
  --generate-ssh-keys \
  --location eastus
```

### ✅ What This Command Does

- 🚀 Deploys **AKS** with **Azure CNI** (Advanced Networking)
- 🔐 Uses **Managed Identity** for secure access to Azure resources
- 🌐 Integrates **Application Gateway Ingress Controller (AGIC)**
- 🏗️ Creates a new **Application Gateway** named `myApplicationGateway`
- 📍 Uses a **subnet with CIDR `10.225.0.0/16`** for the Application Gateway  
  *(Azure creates this automatically if it doesn't already exist)*

## 🛠️ AGIC Installation & Namespace Setup

### ✅ Step 1: Verify AGIC Installation (if not already managed by addon)

Since you used `--enable-addons ingress-appgw`, **AGIC is already deployed**.

To verify:

```bash
kubectl get pods -n kube-system -l app=ingress-appgw
```

## 🌐 Step 3: Deploy a Sample NGINX App

Create a YAML file named `nginx-app.yaml`:

```yaml
# nginx-app.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
  namespace: ingress-nginx
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
  namespace: ingress-nginx
spec:
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80

kubectl apply -f nginx-app.yaml
```
## 🌐 Step 4: Deploy the Ingress Resource

Create a YAML file named `nginx-ingress.yaml`:

```yaml
# nginx-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: nginx-ingress
  namespace: ingress-nginx
  annotations:
    kubernetes.io/ingress.class: azure/application-gateway
spec:
  rules:
  - http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: nginx-service
            port:
              number: 80

kubectl apply -f nginx-ingress.yaml
```

## 🌐 Step 5: Get the Application Gateway Public IP

### 🔍 Find the Application Gateway Name:

```bash
az network application-gateway list -g MC_sumi-testing_aks-agic_eastus -o table
kubectl get ingress -n ingress-nginx
kubectl get svc -n ingress-nginx
```

## 🚪 Setup Ingress Controller (NGINX-based)

### 🔍 Check Existing Ingress Resources

```bash
kubectl get ingress
kubectl create namespace ingress-basic

helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm show values ingress-nginx/ingress-nginx

helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-basic \
  --set controller.replicaCount=2 \
  --set controller.nodeSelector."kubernetes\.io/os"=linux \
  --set defaultBackend.nodeSelector."kubernetes\.io/os"=linux \
  --set controller.service.externalTrafficPolicy=Local \
  --set controller.publishService.enabled=true


helm install ingress-nginx ingress-nginx/ingress-nginx `
  --namespace ingress-basic `
  --set controller.replicaCount=2 `
  --set "controller.nodeSelector.kubernetes\.io/os=linux" `
  --set "defaultBackend.nodeSelector.kubernetes\.io/os=linux" `
  --set controller.service.externalTrafficPolicy=Local `
  --set controller.publishService.enabled=true


kubectl get pods,svc -n ingress-basic
```

## 🔎 What You’ll See After Ingress-NGINX Installation

- ✅ **2 `ingress-nginx-controller` pods** running in `ingress-basic` namespace  
- 🌐 A **`LoadBalancer` service** with an assigned **EXTERNAL-IP**

---

### 📋 Check Services with Labels

```bash
kubectl get service -l app.kubernetes.io/name=ingress-nginx --namespace ingress-basic
kubectl get pods -n ingress-basic
kubectl get all -n ingress-basic
http://<Public-IP-created-for-Ingress>
404 Not Found from Nginx
# Verify Load Balancer on Azure Mgmt Console
```

## 🌐 Ingress - Context Path Based Routing

### 📄 Ingress Manifest: `2.Ingress-Context-Path-Based-Routing.yml`

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-cpr
  # annotations:
  #   kubernetes.io/ingress.class: nginx
spec:
  ingressClassName: nginx
  rules:
    - http:
        paths:
          - path: /app1
            pathType: Prefix
            backend:
              service:
                name: app1-nginx-clusterip-service
                port:
                  number: 80
          - path: /app2
            pathType: Prefix
            backend:
              service:
                name: app2-nginx-clusterip-service
                port:
                  number: 80
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: springboot-app-service
                port:
                  number: 80
```
## 🌍 Access Your Applications

### 🔗 [http://20.43.241.149/app1/index.html](http://20.43.241.149/app1/index.html)  
Routes to `app1-nginx-clusterip-service`

### 🔗 [http://20.43.241.149/app2/index.html](http://20.43.241.149/app2/index.html)  
Routes to `app2-nginx-clusterip-service`

### 🔗 [http://20.43.241.149/api](http://20.43.241.149/api)  
Routes to `springboot-app-service`
