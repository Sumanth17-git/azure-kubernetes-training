## 🛠 Step-by-Step Interaction Between Kubernetes Components

This section explains what happens **behind the scenes** when you deploy something to Kubernetes using `kubectl`.

---

### 🧾 Step 1: `kubectl` Sends a Request to the API Server

```bash
kubectl apply -f my-app.yaml
```
This command sends a request to the Kubernetes API Server (kube-apiserver).

#### 🔍 What Happens:

- ✅ The **API Server** receives and parses the YAML file.
- ✅ It checks for **proper syntax**.
- ✅ It validates whether the **API version** is supported.
- ✅ It checks **RBAC policies** to ensure the user is authorized to perform the action.

🔧 Components Involved:
kube-apiserver

#### 🔧 Components Involved:
- `kube-apiserver`
- **RBAC** (Role-Based Access Control)

---

✅ If the validation and permission checks pass, Kubernetes proceeds to process the request.

---

### 🧠 Step 2: API Server Stores Deployment Data in etcd

After validating the request, the **API Server** stores the **desired state** (e.g., a Deployment or Pod) in **etcd**.

---

#### 📦 etcd Stores:

- The **deployment specification**
- The **namespace** and metadata
- Number of **replicas**
- **Image** information
- **Container ports**, **labels**, and other pod settings

---

#### 📂 etcd = Source of Truth

> etcd acts as the **source of truth** for the entire cluster — maintaining the **desired state** of all Kubernetes objects.

🧠 Example:
> “I want 3 replicas of `nginx` running in the `dev` namespace.”

---

#### 🔧 Components Involved:
- `kube-apiserver`
- `etcd`
🧠 etcd now holds the desired configuration — e.g., “I want 3 replicas of nginx running in the dev namespace.”
---

---

### 🧠 Step 3: Scheduler Decides Where to Run the Pod

The **Kubernetes Scheduler** is responsible for selecting the best **worker node** for each unassigned Pod.

---

#### 🧠 Scheduler Says:

> "Hmm... Where should I run these Pods? Let me find the best node."

---

#### 🔍 What the Scheduler Does:

- 🔄 Watches the **API Server** for Pods that **don't yet have a node assigned**
- ⚙️ **Finds the new unassigned Pod**
- 📊 Evaluates cluster-wide resources:
  - Available **CPU**, **memory**
  - **Taints and tolerations**
  - **Node affinity/anti-affinity rules**
  - **Pod affinity rules**
  - Custom constraints or priorities

---

#### ✅ Once a Node is Selected:

- Updates the **Pod specification** with the chosen node:

```yaml
spec:
  nodeName: "worker-node-1"
```
- Sends this assignment back to the API Server
- The API Server then updates etcd with the new scheduled Pod state

---

### 🧱 Step 4: Kubelet on the Worker Node Creates the Pod

Once the Scheduler has assigned a Pod to a node, the **Kubelet** on that node takes responsibility for creating it.

---

#### 👷 Kubelet on the Node Says:

> "Alright! I’ve got the job. Time to bring up this pod."

---

#### 🔍 What the Kubelet Does:

- 📥 **Detects** that a new Pod has been scheduled to its node
- 🔗 **Pulls the Pod specification** from the API Server
- 🤝 **Communicates** with the **Container Runtime** (like `containerd`, `CRI-O`, or `Docker`) to:
  - 🔄 Pull the required **container images**
  - 🚀 **Start the containers** as defined in the Pod spec
- 📝 **Monitors** the container status and reports back to the API Server

---

#### 🛠️ Components Involved:

- `kubelet` (running on the worker node)
- **Container Runtime** (e.g., `containerd`, `CRI-O`, or legacy Docker)
- `kube-apiserver`

---

> ✅ The Pod is now created and running on the worker node!

---

### 🧪 Step 5: Container Runtime Runs the Application

The **Container Runtime** is responsible for pulling and running your application inside the container.

---

#### 🔍 What the Container Runtime Does:

- 📦 Pulls the **container image** (e.g., `nginx`, `springboot-app`) from a **container registry**  
  _Examples: Docker Hub, Azure Container Registry (ACR), ECR, GCR, etc._
- 🚀 **Creates and starts the container** on the assigned **worker node**

---

#### 🛠️ Components Involved:

- **Container Runtime** (`containerd`, `CRI-O`, or legacy Docker)
- Node filesystem and network stack

---

### 📡 Step 6: Kubelet Reports Pod Status to API Server

Once the Pod is up and running, the **Kubelet** takes on the job of monitoring and reporting.

---

#### 🧠 Kubelet Says:

> "Hey API Server, I started the pod — it’s running fine!"

---

#### 🔍 What Happens:

- 📈 The **Kubelet continuously monitors** the Pod's health and state:
  - `Running`, `Failed`, `Pending`, `CrashLoopBackOff`, etc.
- 📤 It **reports this status** to the **API Server**
- 📥 The **API Server updates etcd** with the latest Pod status

---

#### 🛠️ Components Involved:

- `kubelet`
- `kube-apiserver`
- `etcd`

---

### 🌐 Step 7: Exposing the Application Using a Service

To make the application accessible, Kubernetes uses **Services**.

---

#### 🔍 What Happens:

- 🧭 If a **Kubernetes Service** is defined:
  - It assigns a **ClusterIP**, **NodePort**, or **LoadBalancer IP**
- 🔁 The **Service Controller** ensures network traffic is routed to the correct Pods
- 🔌 Internal and external users can now access the application

---

#### 🛠️ Components Involved:

- `Service` object
- `kube-proxy`
- **Service Controller**
- **Load Balancer (if cloud)**

---

✅ At this point, the application is fully deployed, running, and accessible!

---

## ✅ Kubernetes Lifecycle Summary

| Step | Component(s)            | Description                                             |
|------|-------------------------|---------------------------------------------------------|
| 1    | `kubectl`, API Server   | Submit and validate YAML                               |
| 2    | API Server, etcd        | Store desired state                                     |
| 3    | Scheduler               | Assign Pod to a Node                                    |
| 4    | Kubelet, Container Runtime | Create and run container                            |
| 5    | Container Runtime       | Pull and launch app                                     |
| 6    | Kubelet, API Server, etcd | Report and update pod status                         |
| 7    | Service, kube-proxy     | Expose and route traffic to the app                    |

---

> 💡 This end-to-end lifecycle shows how Kubernetes handles everything — from code to a running, networked container — automatically and intelligently.

---

## 💥 What Happens When a Pod Crashes?

---

#### 😵 Pod Says:
> "Oops! I crashed!"

#### 🤖 Controller Replies:
> "Don’t worry, I’ll replace you."

---

### 🔄 Recovery Process:

1. 🧩 **Kubelet** on the node detects that the Pod has **failed**.
2. 📤 Kubelet **updates the Pod status** (e.g., `CrashLoopBackOff`, `Failed`) to the **API Server**.
3. 🧠 The **Deployment Controller** monitors the cluster state via etcd.
4. 📉 It notices that the **actual number of Pods** is **less than the desired count**.
5. 🛠️ It **automatically creates a new Pod** to replace the failed one.
6. 🧠 The **Scheduler** assigns the new Pod to a suitable node.
7. 👷 The **Kubelet** on that node pulls the image and starts the new Pod again.
---
### 🛠️ Components Involved:
- `kubelet`
- `kube-apiserver`
- `etcd`
- **Deployment Controller**
- `kube-scheduler`
- **Container Runtime**
---
> 💡 Kubernetes' **self-healing** nature ensures minimal downtime by **automatically recovering** failed Pods based on the desired state.

### 🌩️ What is the Azure Cloud Controller Manager?
- The Cloud Controller Manager (CCM) in Kubernetes is responsible for integrating your cluster with the underlying cloud provider (in this case, Azure).In AKS, Azure Cloud Controller Manager handles cloud-specific resources like:
