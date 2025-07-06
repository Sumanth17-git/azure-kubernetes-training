## ⚠️ Pod STATUS FIELDS You Might See

Understanding what each pod status means helps you troubleshoot and debug your workloads.

### 📊 Quick Reference Table

| **Pod STATUS**        | **Meaning**                                                |
|------------------------|------------------------------------------------------------|
| `Running`              | At least one container is running                          |
| `Pending`              | Waiting to be scheduled or pulled                          |
| `Completed` / `Succeeded` | All containers exited successfully                    |
| `Error`                | Container failed with non-zero exit                        |
| `CrashLoopBackOff`     | Failing repeatedly, Kubernetes throttles restart attempts  |
| `ImagePullBackOff`     | Can't pull the image (e.g., registry error, 404)           |
| `ContainerCreating`    | Volume/image/network setup ongoing                         |
| `Terminating`          | Pod is being deleted                                       |

---

### 🧠 Detailed Phase Explanations

#### 1️⃣ `Pending`

What’s Happening:
- ✅ You submit a pod manifest using `kubectl apply -f pod.yaml`
- ✅ Kube API Server accepts it and writes to `etcd` (the Kubernetes database)
- 🔄 Scheduler looks for available nodes:
  - Enough CPU/memory
  - No taint conflicts
  - Affinity/anti-affinity rules satisfied
- 📌 Pod status = **Pending** if it hasn’t been scheduled or the container image hasn't been pulled yet.

---

#### 2️⃣ `Running`

What’s Happening:
- ✅ Scheduler assigns the Pod to a Node
- ✅ Kubelet on that Node:
  - Pulls the image using container runtime (e.g., `containerd`)
  - Mounts volumes (if any)
  - Sets up networking (pod sandbox)
  - Starts the container(s)
- 🎯 Once at least one container starts successfully, status = **Running**

---

#### 3️⃣ `Succeeded` (a.k.a. `Completed`)

What’s Happening:
- ✅ All containers in the pod **exit with code 0**
- ✅ Kubelet marks pod phase as `Succeeded`
- 💡 Common with **Jobs** or **CronJobs**, e.g., data processing task that exits cleanly

---

> 💡 **Pro Tip:** Use `kubectl describe pod <pod-name>` to see lifecycle events and root causes of stuck or failed pods.
## 💥 What Happens When a Liveness Probe Fails in Kubernetes?

A **liveness probe** checks whether your application inside the container is *still alive*.  
If it fails repeatedly, Kubernetes restarts the container — not the entire Pod.

---

### 🔄 Liveness Probe Failure Flow

1️⃣ **Probe Fails Once**
- Kubernetes waits and retries the check based on `periodSeconds` and `failureThreshold`.

2️⃣ **Probe Fails Multiple Times (e.g., 3 failures)**
- Container is marked as **unhealthy**
- Kubernetes **kills** and **restarts** the container inside the Pod
- The Pod **status remains `Running`**
- The container **restart count increases**

> ℹ️ This happens because the **Pod is still considered healthy** by the kubelet — only the container inside failed.

---

### 🧪 How to Observe This

```bash
# Apply the Pod with a liveness probe
kubectl apply -f pod.yaml

# Watch the Pod status and restarts
kubectl get pods -w

# Describe the Pod for probe events
kubectl describe pod <pod-name>

# Check logs (if any)
kubectl logs <pod-name>
```