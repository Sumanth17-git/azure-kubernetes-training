## 🛠 Step-by-Step Interaction Between Kubernetes Components

This section explains what happens **behind the scenes** when you deploy something to Kubernetes using `kubectl`.

---

### 🧾 Step 1: `kubectl` Sends a Request to the API Server

```bash
kubectl apply -f my-app.yaml
```
This command sends a request to the Kubernetes API Server (kube-apiserver).
🔍 What Happens:
✅ The API Server receives and parses the YAML file.

✅ It checks for proper syntax.

✅ It validates if the API version is supported.

✅ It checks RBAC policies to ensure the user is allowed to perform the action.

🔧 Components Involved:
kube-apiserver

RBAC (Role-Based Access Control)

✅ If the validation and permission checks pass, Kubernetes proceeds to process the request.

🧠 Step 2: API Server Stores Deployment Data in etcd
After validating the request, the API Server stores the desired state (e.g., a deployment or pod) in etcd.

📦 etcd Stores:
The deployment specification

The namespace and metadata

Number of replicas, image info, container ports, labels, etc.

📂 etcd acts as the source of truth for the entire cluster — maintaining the desired state of all objects.

🔧 Components Involved:
kube-apiserver
etcd

🧠 etcd now holds the desired configuration — e.g., “I want 3 replicas of nginx running in the dev namespace.”