# 🚦 Init Containers in Kubernetes

## 📘 What is an Init Container?

**Init containers** are special containers in Kubernetes that **run before the main application containers** in a Pod. They are designed to **perform setup or initialization tasks** that must complete successfully **before** the main containers can start.

Kubernetes Pods can have **multiple containers** working together. Init containers help **prepare the environment** for the main application containers to run smoothly.

---

## 🧠 Key Concepts

- Init containers always **run to completion** before any app containers start.
- If any init container **fails**, the pod is considered to be in a failed state and retries.
- They run **sequentially** — each waits for the previous one to complete.

---

## 🎯 Real-Time Use Case

You’re deploying a **web application** that:

- Requires a **database** (like PostgreSQL) to be up and running
- Needs **configuration files** placed into a shared volume

👉 The init container can:
- Wait for the DB to be ready
- Clone a Git repo with config files to a volume
- Set the right permissions
- Only then allow the main web app to start
```bash
kubectl apply -f init_pod.yaml
kubectl get pods -o wide
kubectl get pods -w
kubectl describe pod <pod-name>
kubectl get pod <pod-name> -o yaml
To check the specific container logs
kubectl logs <pod-name> -c <container-name>
kubectl logs init-wait-db -c wait-for-db
```
### To Fix this issue:
### Option1:
```bash
kubectl create deployment db --image=postgres --port=5432
kubectl set env deployment/db POSTGRES_PASSWORD=pass
kubectl expose deployment db --name=db-service --port=5432
```

### Option 2
```
kubectl apply -f postgress.yaml
```
```bash
kubectl apply -f postgres-deployment.yaml
kubectl get pods
kubectl logs init-wait-db
```




---

## ✅ Common Init Container Use Cases

### 1️⃣ Waiting for External Services

- **Scenario**: Application depends on a database or cache service
- **Use Case**: Init container runs `curl`, `nc`, or `wget` to **probe the DB endpoint** until reachable

### 2️⃣ Cloning Git Repositories
Scenario: Application requires configuration or assets from Git

Use Case: Init container clones a Git repo to a shared volume

### 3️⃣ Permission Fixes
Scenario: A mounted volume has incorrect permissions for the app user

Use Case: Init container runs chmod or chown to fix permissions
### 5️⃣ Security Checks or Token Fetch
Scenario: Your app needs a secret token from a secure store
Use Case: Init container fetches the token from Azure Key Vault, AWS Secrets Manager, or HashiCorp Vault and writes it to a shared volume



