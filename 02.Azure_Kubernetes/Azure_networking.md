---

## 🌐 Azure CNI vs Azure CNI Overlay Networking in AKS

Kubernetes networking in AKS can be configured using either **Azure CNI (Classic)** or **Azure CNI Overlay**. Understanding the difference is critical for scaling, IP management, and connectivity with Azure services.

---

### 🔹 Azure CNI (Classic / VNet-Integrated)

- 🟢 **Pods receive IPs directly from the Azure VNet subnet**.
- 🟢 Each pod is **addressable within the VNet** (first-class IP).
- ✅ Pods can communicate **natively with Azure resources** (e.g., VMs, databases).
- ❗ Can exhaust IPs quickly in large-scale deployments.



---

### ✅ Azure CNI Overlay (Recommended for Large-Scale / Virtual Nodes)

- 🚫 Pods **do not** get IPs from VNet subnet.
- 🟢 Nodes still get IPs from VNet (e.g., 10.10.0.0/16).
- 🟢 Pods are assigned IPs from a **separate overlay CIDR** (e.g., 192.168.0.0/16).
- 🔁 **VXLAN tunneling** is used to route pod-to-pod traffic.
- 🌐 Outbound pod traffic is **NATed via the node's IP**.
- 🧠 Saves subnet IPs and supports massive scale.



> 📝 Overlay CIDR is specified during cluster creation (e.g., `--pod-cidr 100.64.0.0/16`)

---

## 💡 Example Comparison

| Feature                     | Azure CNI (Classic)      | Azure CNI Overlay             |
|----------------------------|--------------------------|-------------------------------|
| Pod IP Source              | Azure VNet subnet        | Separate overlay CIDR         |
| Pod-to-Azure Services      | Direct (native routing)  | NATed through node            |
| Pod-to-Pod Communication   | Native within subnet     | VXLAN encapsulated            |
| IP Consumption             | High                     | Low                           |
| Scale Potential            | Limited by subnet size   | Massive (>100K pods/cluster)  |
| Virtual Nodes Compatibility| ❌ No                    | ✅ Yes                         |

---

## ⚡ Virtual Nodes & Azure CNI Overlay

When you enable **Virtual Nodes**, AKS automatically switches to **Azure CNI Overlay** networking.

### 🧠 Why?

- Virtual Nodes run pods in **Azure Container Instances (ACI)** — a serverless environment.
- These pods are **not part of your VM node pool**.
- Azure CNI Overlay allows **pod burst capacity** without needing IPs from the core subnet.

### 📦 What Happens When You Enable Virtual Nodes?

| Action                                | Result                                     |
|---------------------------------------|--------------------------------------------|
| Enable Virtual Nodes in AKS           | A **Virtual Kubelet** node is created      |
| Schedule extra pods to this node      | Pods run in **ACI**, not VM-based nodes    |
| Overlay networking used automatically | Pods get IPs from overlay CIDR             |
| ACI handles the compute & network     | You only pay per second used               |

---

## ✅ Summary

| Use Case                         | Recommended Network Plugin |
|----------------------------------|----------------------------|
| High-scale deployments (>1K pods)| Azure CNI Overlay          |
| VM-only workloads, small scale   | Azure CNI Classic          |
| Using Virtual Nodes / ACI        | Azure CNI Overlay (Required) |

> 📌 Azure CNI Overlay is ideal for scaling pods while conserving IPs and enabling features like **Virtual Nodes**, **burstable compute**, and **hybrid networking**.

---

---

## 💡 Example: Azure CNI vs Azure CNI Overlay with Virtual Nodes

Understanding how pod IP allocation and networking work is essential for scaling and secure connectivity in AKS.

---

### 📘 CNI Classic Example

If you create an AKS cluster with **Azure CNI (Classic)**:

- VNet/Subnet: `10.240.0.0/16`
- Pod IPs are assigned directly from the subnet


✅ Pods can **talk directly** to services in the VNet (SQL, Redis, VMs)

---

### ✅ CNI Overlay Example

If using **Azure CNI Overlay**:

- Node IP: from VNet subnet (e.g., `10.240.0.4`)
- Pod IP: from **overlay CIDR** (e.g., `192.168.0.5`, `192.168.0.6`)
- Overlay range: `--pod-cidr 192.168.0.0/16`

🔁 Traffic between pods is encapsulated with **VXLAN**  
🌐 Outbound internet traffic is **NATed** through node IP  
🚫 Azure services **cannot directly** reach pod IPs unless **Private Endpoints/NAT rules** are configured

---

## 🚀 What Happens When You Enable Virtual Nodes?

- Virtual Nodes use **Azure Container Instances (ACI)**
- Let you **burst workloads** instantly (no VM provisioning)
- **Overlay networking is required** and enabled by default

---

## 🔧 Step-by-Step: Create AKS Cluster with Azure CNI Overlay

```bash
az aks create \
  --name aks-overlay-demo \
  --resource-group myrg \
  --network-plugin azure \
  --network-plugin-mode overlay \
  --pod-cidr 192.168.0.0/16 \
  --service-cidr 10.0.0.0/16 \
  --dns-service-ip 10.0.0.10 \
  --vnet-subnet-id /subscriptions/<SUB-ID>/resourceGroups/myrg/providers/Microsoft.Network/virtualNetworks/myVnet/subnets/aks-subnet \
  --generate-ssh-keys

kubectl run nginx --image=nginx
kubectl get pod -o wide
kubectl exec -it nginx -- curl google.com
kubectl exec -it nginx -- ping <azure-sql-private-ip>
```
# 🌐 Kubernetes Networking & Service Discovery — Beginner to Pro

---

## 🧱 1. Kubernetes Networking Model (Flat Network)

Kubernetes networking is the system that allows **Pods to talk to each other** and to the **outside world**.

### 🔑 Core Rules of Kubernetes Networking:

1. 📦 Each **Pod gets a unique IP address**
2. 🔄 All Pods can **communicate directly** with each other — **no NAT required**
3. 🧭 Communication is **flat** — no gateways or routers between Pods
4. 🧵 **Containers in the same Pod** share the same network namespace (can use `localhost`)

---

## 📚 Topics Covered:

- ✅ What is a **Virtual Network (VNet)** in AKS
- ✅ What is a **subnet** and how `/16`, `/24` ranges work
- ✅ What are **Pod CIDR**, **Service CIDR**, and how Azure assigns them
- ✅ What is **DNS IP** and how **CoreDNS** works
- ✅ How all this relates to your **AKS VNet configuration**

---

## 🏢 Real-Life Analogy: Office Building

Think of a **Virtual Network (VNet)** as an office building in a corporate environment:

| Element        | Real World Analogy                 |
|----------------|------------------------------------|
| VNet           | Office Building                    |
| Subnet         | Rooms inside the office            |
| VMs / Nodes    | Employees in rooms                 |
| NSG / Firewall | Security Guards                    |

- Everyone inside (pods/VMs) can **communicate privately**
- **No need to go through the internet**
- Guards (**NSGs**) decide **who can enter or exit**

---

## ✅ Example Use Case: AKS + Azure SQL DB

Scenario:
- You have an AKS cluster in `aks-subnet`
- Azure SQL is in `sql-subnet`
- Both subnets are within the same VNet

💡 Want to ensure **secure, internal communication**?

### ✔️ Solution:
- Place both AKS and SQL **inside the same VNet**
- Communication happens **privately** using **private IPs**
- No public exposure, **no internet routing involved**

```plaintext
[VNet: company-network]
    ├── Subnet: aks-subnet → AKS Cluster
    └── Subnet: sql-subnet → Azure SQL DB

→ Private IP to Private IP
→ Fast, secure, no egress charges
```

# 🌐 Kubernetes Networking & Service Discovery — Beginner to Pro (Part 2–4)

---

## 🔗 PART 2: What is a Subnet?

### ✅ Basic Definition:
A **subnet** is a smaller, logical subdivision of a **Virtual Network (VNet)**. It allows better organization and isolation of networked resources.

### 🧱 Subnet Examples in an AKS Architecture:

| Subnet Name          | Purpose                              |
|----------------------|--------------------------------------|
| `aks-subnet`         | Hosts AKS nodes and Pod IPs          |
| `appgateway-subnet`  | Hosts Azure Application Gateway      |
| `database-subnet`    | Hosts Azure SQL / Database resources |

💡 Subnets help in applying **NSGs**, **routing rules**, and **segregating workloads** cleanly inside a VNet.

---

## 📐 PART 3: What is CIDR and /16, /24, /12?

### ✅ CIDR = Classless Inter-Domain Routing

CIDR determines how **many IP addresses** are available in your network/subnet.

| CIDR Notation | IP Range Size     | Example IP Range                     |
|---------------|-------------------|--------------------------------------|
| `/24`         | 256 IPs           | `10.0.0.0` → `10.0.0.255`            |
| `/16`         | 65,536 IPs        | `10.0.0.0` → `10.0.255.255`          |
| `/12`         | ~1 Million IPs    | `10.0.0.0` → `10.15.255.255`         |

> 🧠 **Why It Matters?**
> - AKS uses IPs for **VMs**, **Pods**, and **Services**
> - If you choose a **small CIDR** (e.g., `/24`), your cluster may **run out of IPs** quickly.

---

## 🐳 PART 4: How Does This Connect to AKS?

When you deploy an AKS cluster, several **network-related resources** come into play:

### 🔧 AKS Needs:

- ✅ A **subnet** to host the **worker nodes (VMs)**
- ✅ A **CIDR range** to assign IPs to **Pods** (`--pod-cidr`)
- ✅ A **CIDR range** to assign IPs to **Services** (`--service-cidr`)
- ✅ **DNS Service IP** (e.g., `10.0.0.10`) — used by **CoreDNS**
- ✅ Optional: Subnet for **Ingress Controllers** (e.g., App Gateway)

---

## 📌 Real AKS Network Parameter Example

```bash
az aks create \
  --name aks-network-demo \
  --resource-group rg-aks \
  --network-plugin azure \
  --vnet-subnet-id "/subscriptions/xxx/resourceGroups/rg-aks/providers/Microsoft.Network/virtualNetworks/vnet-demo/subnets/aks-subnet" \
  --pod-cidr 192.168.0.0/16 \
  --service-cidr 10.0.0.0/16 \
  --dns-service-ip 10.0.0.10 \
  --generate-ssh-keys
```

# 📡 Pod-to-Pod Communication in Kubernetes

This guide demonstrates how two applications (pods) in a Kubernetes cluster communicate **internally**, without exposing any services externally.

---

## ✅ Pod-to-Pod Communication (Flat Network Model)

In Kubernetes (including AKS), pods can talk to each other **directly** using their internal IP addresses.

### 🔍 Key Concepts:
- Each pod gets a **unique IP address** from the **Pod CIDR** range.
- Kubernetes provides a **flat, routable network**:
  - Pods across **nodes** and **namespaces** can communicate **without NAT**.
- No need to expose apps externally (e.g., LoadBalancer, NodePort) for **internal communication**.

---

## 🧪 Step-by-Step Demo: Frontend Pod → Backend Pod Communication

---

### 1️⃣ Create a Namespace

```bash
kubectl create namespace demo-ip
```
### 2️⃣ Deploy a Backend Pod That Responds to HTTP
``` bash
# backend-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: backend
  namespace: demo-ip
  labels:
    app: backend
spec:
  containers:
  - name: backend
    image: hashicorp/http-echo
    args:
      - "-text=Hello from Backend via IP"
    ports:
    - containerPort: 5678
```


---

### ✅ 3️⃣ Get Backend Pod IP

Once the backend pod is running, retrieve its internal IP address:

```bash
kubectl get pod -n demo-ip -o wide

## ✅ 4️⃣ Deploy a Frontend Pod to Curl the Backend Pod

Now let’s deploy a `curl`-based Pod that will attempt to connect to the backend using its **Pod IP**.

---

### 📄 `frontend-curl.yaml`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: frontend
  namespace: demo-ip
spec:
  containers:
  - name: curl
    image: curlimages/curl
    command: [ "sleep", "3600" ]
```
## 🚀 Apply the YAML

```bash
kubectl apply -f frontend-curl.yaml
```bash
kubectl exec -n demo-ip -it frontend -- sh
curl http://<backend_pod_ip>:5678

#### ✅ Expected Output
Hello from Backend via IP

# AKS Networking: Virtual Network, Subnet, Pod CIDR, and Service CIDR

---

## 🔹 Virtual Network / Subnet Address Space

- To check the nodes and their IPs in your AKS cluster:

```bash
kubectl get nodes -o wide
```
### Example Node IP

`10.22.0.4`

---

### How to Check Virtual Network and Subnet Range in Azure Portal

1. Navigate to your **Virtual Network** resource.

2. Click on **Settings** → **Subnets**.

3. View the subnet ranges and connected devices.


# 🚪 What is Pod Isolation?

Pod isolation means controlling which Pods can communicate with each other.

In a default Kubernetes setup:
- All pods can talk to all other pods, across all namespaces.
- This is not secure by default (no zero-trust).
- Pod isolation is achieved using **Network Policies**.

---

## 🧩 Two Types of Isolation

| Type    | Controls...                | Enabled via                   |
|---------|----------------------------|------------------------------|
| 🔐 Ingress | Who can talk to a pod      | `ingress` in a NetworkPolicy  |
| 🚫 Egress  | Who a pod can talk to      | `egress` in a NetworkPolicy   |

---

## 🧪 How Does Pod Isolation Work?

Pod isolation is **not automatic**.

A pod becomes **"isolated"** only when a matching NetworkPolicy exists that:
- Selects the pod, and
- Defines allowed traffic.

---

## 🚦 What is a Network Policy?

Think of it like a firewall for Pods — it controls who can talk to whom inside your Kubernetes cluster.

---

## 🎯 Why Do You Need Network Policies?

Without network policy:

- ✅ All Pods can talk to all other Pods.
- ❌ There’s no isolation between frontend, backend, database, etc.
- ❌ Security risk if one pod is hacked — it can reach everything!

With network policy:

- 🔐 You can allow only specific Pods or Namespaces to talk.
- 🔒 You can block egress to the internet or IP ranges.
- 👮 You define **“who can talk to whom”** inside your cluster.


| Mode   | Enforced by     | Supports Ingress | Supports Egress | Supports IPBlock | Use Case           |
|--------|-----------------|------------------|-----------------|------------------|--------------------|
| None   | ❌ No enforcement | ❌ No restrictions | ❌ No restrictions | ❌ No rules       | Dev/test clusters   |
| Azure  | ✅ Azure NSG     | ✅ Yes           | ❌ No           | ❌ No            | Basic secure apps   |
| Calico | ✅ Calico agent  | ✅ Yes           | ✅ Yes          | ✅ Yes           | Secure enterprise apps |


## 🔍 Let’s Break It Down One-by-One

### 🛑 1. Network Policy: None
This means no rules, no restrictions, and no enforcement.

**🔓 Example:**
- Your frontend, backend, and database Pods can freely communicate with each other.
- Even if you write a NetworkPolicy YAML — it will be ignored!

**🧪 Use case:**
- For quick testing, lab clusters, or where security is not a concern.

**📌 Azure default when you don't specify `--network-policy`.**

---

### 🛡️ 2. Network Policy: Azure
Enforced using Azure NSGs (Network Security Groups) under the hood.

**✅ Supports:**
- Ingress (Who can send traffic to a Pod)

**❌ Does NOT support:**
- Egress rules (You cannot restrict outgoing connections)
- IPBlocks (CIDRs)

**📦 Azure mode is good when:**
- You want basic intra-cluster security
- You want to block Pod-to-Pod communication except for allowed ones

---

### 🧱 3. Network Policy: Calico
Uses Calico plugin to enforce rules.

**✅ Supports:**
- Ingress
- Egress
- IP CIDR (IPBlock)
- Namespace selectors

This is full-featured, open-source, and CNCF compliant.

---

### 🔹 1. Flat Networking Model
- Every Pod gets its own IP address.
- All Pods are in the same flat network—no NAT is needed.
- This makes it easy to treat a Pod like a mini server.
## 📦 Key Rule
All Pods can talk to all other Pods in the cluster by default, across nodes and namespaces.

---

## 🔹 2. Pod-to-Pod Communication
Kubernetes uses CNI plugins like:
- **Azure CNI (AKS default):** Pods get IPs from Azure VNet.
- **Kubenet (legacy):** Pods get internal IPs NATed via nodes.

### 📍 Example:
If Pod A has IP `10.240.0.12`, and Pod B has `10.240.0.13`, they can directly curl each other.

---

## 🔹 4. Ingress and Egress
- **Ingress:** Traffic coming into the cluster from outside.  
  Handled via LoadBalancers, Ingress Controllers (like NGINX, AGIC).
- **Egress:** Traffic going out to the internet or other networks.  
  Can be unrestricted, or controlled via Network Policy or firewall.

---

## 🔐 Kubernetes Network Policies — for Isolation

### 🔒 Without policies:
Everything can talk to everything = 🧨 **not secure!**

### ✅ Why Use Network Policies?
- Prevent Pod A from accessing Pod B unless allowed
- Lock down database access to backend only
- Prevent apps from making outbound internet calls
- Ensure frontend can’t talk to another team’s namespace

---

## 🧱 How Network Policies Work
They work like firewalls at the Pod level.

- Based on:
  - Pod labels
  - Namespace selectors
  - IP blocks

If you apply any network policy to a Pod, Kubernetes **denies all traffic by default** — and only allows what’s explicitly defined.

In the diagram above you can see we have a **test-service** which requires accepting TCP connections **only from `client-green` pod** and **not from `client-red`**. In such a situation, a **NetworkPolicy** can help you control this traffic flow as desired.

---

### ❗ Can You Enforce Network Policies on a Cluster Created with `--network-policy none`?

❌ **No**, you cannot enforce network policies on a cluster with `network-policy=none`.

Even if you apply a NetworkPolicy YAML, it will **not** be enforced because the cluster is **not configured with a network policy engine**.

---

### 🔍 Why?

When you create an AKS cluster with:
--network-policy none
•	No network policy plugin (like Azure or Calico) is installed.
•	Kubernetes will accept your NetworkPolicy YAML (no errors), but will not enforce it.
•	All pods can freely communicate, regardless of any rules written.
✅ The API server stores the policy, but no CNI plugin applies it.

```bash
--network-policy none



az aks create \
  --resource-group sumi-testing \
  --name aks-none-demo \
  --location eastus \
  --node-count 2 \
  --node-vm-size Standard_B1ms \
  --enable-managed-identity \
  --network-plugin azure \
  --network-policy none \
  --generate-ssh-keys


```

# 🚀 PHASE 2: AKS with `network-policy=azure`

## 🧠 What is Azure Network Policy?

- Built-in policy support in AKS when using Azure CNI.
- Supports **only Ingress** rules (Egress blocking is **not supported**).
- Integrated with Azure NSGs and enforces policies at the VM level.
- Useful for internal microservices isolation.

## 🎯 Real-Time Scenario

You are deploying a frontend and backend microservice. You want to:

1. ✅ Allow frontend to access backend  
2. 🚫 Deny everything else  
3. ✅ Allow backend to talk to external services (Egress is always allowed with Azure policy)

```bash
az aks create \
  --resource-group sumi-testing \
  --name netpol-azure-cluster \
  --network-plugin azure \
  --network-policy azure \
  --node-vm-size Standard_B2s \
  --node-count 2 \
  --enable-managed-identity \
  --generate-ssh-keys

az aks get-credentials \
  --resource-group netpol-azure-rg \
  --name netpol-azure-cluster \
  --overwrite-existing
```

## Step 3: Deploy Frontend and Backend Pods

### 🧩 backend.yaml

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: backend
  labels:
    app: backend
spec:
  containers:
  - name: backend
    image: nginx
    ports:
    - containerPort: 80
```
🧩 frontend.yaml
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: frontend
  labels:
    app: frontend
spec:
  containers:
  - name: curlbox
    image: radial/busyboxplus:curl
    command: ["sleep", "3600"]
```
```bash
kubectl apply -f backend.yaml
kubectl apply -f frontend.yaml
```
### 🔹 Step 4: Test Default Communication (Pre-Policy)

```bash
kubectl exec -it frontend -- curl <ip address backend>
```
✅ Output: HTML from Nginx (success)
🧠 All pods can talk by default.

### 🔹 Step 5: Create a Deny-All Ingress Policy

#### deny-all-ingress.yaml

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all-ingress
spec:
  podSelector: {}
  policyTypes:
  - Ingress

```bash
kubectl apply -f deny-all-ingress.yaml
kubectl exec -it frontend -- curl backend
```

❌ Output: Connection refused — because ingress is denied for all pods.

---

### 🔹 Step 6: Allow Frontend → Backend Only

#### allow-frontend-to-backend.yaml

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-backend
spec:
  podSelector:
    matchLabels:
      app: backend
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
  policyTypes:
  - Ingress
```
```bash

kubectl apply -f allow-frontend-to-backend.yaml
kubectl get pods -o wide
kubectl exec -it frontend -- curl <backend ip address>
```

✅ Output: Nginx page (Success)

---

### 🔹 Step 7: Confirm Other Pods Are Still Blocked

Create a third pod:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: attacker
  labels:
    app: attacker
spec:
  containers:
  - name: curlbox
    image: radial/busyboxplus:curl
    command: ["sleep", "3600"]
```
```bash
kubectl apply -f attacker.yaml
Test connectivity from attacker pod to backend:
kubectl exec -it attacker -- curl backend
❌ Connection refused — since attacker is not allowed.
If you want, I can help with the next steps or explanation!
```

### 🔍 Real-Time Use Cases

| Use Case                 | Azure Network Policy                   |
|--------------------------|--------------------------------------|
| ✅ Frontend ↔ Backend     | Allowed (via label selector)          |
| 🚫 Unknown Pod ↔ Backend  | Denied                              |
| ✅ Backend to Internet    | Allowed (Egress is not enforced)      |
| 🚫 DNS to kube-system     | Always allowed by AKS                  |

---

### 🧱 Limitations

- ❌ No Egress enforcement  
- ❌ No CIDR/IPBlock support  
- ❌ No namespace-level rules  

## 🚀 PHASE 3: Calico Mode — Advanced Network Policies in AKS

Calico is the most advanced and complete network policy implementation in Kubernetes.

We'll now use **Calico Network Policies** on Azure Kubernetes Service (AKS), covering real-time enterprise use cases with both **Ingress** and **Egress** controls.

---

### 📊 Feature Comparison: Azure Policy vs Calico

| Feature                    | Azure Policy | Calico |
|----------------------------|--------------|--------|
| ✅ Ingress filtering       | Yes          | Yes    |
| ✅ Egress filtering        | ❌ No        | ✅ Yes |
| ✅ IPBlock/CIDR rules      | ❌ No        | ✅ Yes |
| ✅ DNS-based egress control| ❌ No        | ⚠️ Limited (requires sidecar/proxy) |
| ✅ Namespaced isolation    | Limited      | Yes    |
| ✅ Label-based enforcement | Yes          | Yes    |

---

### 🎯 Real-Time Enterprise Scenario

Let’s build **Calico Network Policies** from scratch with a complete, beginner-friendly, and step-by-step guide. This includes:

- 🚧 Default deny for all ingress and egress
- 🔓 Allow internal service-to-service traffic (e.g., frontend → backend)
- 🌐 Allow egress to internet for selected pods (e.g., curl google.com)
- 🔐 Restrict based on namespaces or labels
- 🌍 Allow specific CIDR IPBlock traffic
- 📦 Policy chaining and validation

---

> 🔧 We'll use `kubectl`, YAML manifests, and live testing commands to validate the effect of each rule. Ideal for DevOps, SREs, and Trainers explaining network security in Kubernetes using Calico.

---

✅ Ready to continue? Let me know if you'd like the first step: "Create a namespace and default deny policy".
```yaml
az aks create \
  --resource-group calico-lab-rg \
  --name calico-aks-demo \
  --node-count 2 \
  --node-vm-size Standard_B2s \
  --enable-managed-identity \
  --network-plugin azure \
  --network-policy calico \
  --generate-ssh-keys

```
## 🔥 Kubernetes NetworkPolicy: Phase 1 — Setup

A `NetworkPolicy` in Kubernetes is like a **firewall rule for Pods** — it controls:

- 🔐 **Ingress**: Who can talk **to** your Pod
- 🔐 **Egress**: Who your Pod can talk **to**

---

## 🧪 Phase 1: Setup — Namespaces & Pods

### 1️⃣ Create Namespaces

```bash
kubectl create namespace team-api
kubectl create namespace team-ui
kubectl create namespace testers

🔖 Add Namespace Labels (needed for network policy namespaceSelector)
kubectl label ns team-api name=team-api
kubectl label ns team-ui name=team-ui
kubectl label ns testers name=testers
```yaml
Create Pods in Each Namespace
✅ checkout.yaml (in team-api)
apiVersion: v1
kind: Pod
metadata:
  name: checkout
  namespace: team-api
  labels:
    role: checkout
spec:
  containers:
  - name: web
    image: nginx
    ports:
    - containerPort: 80
✅ frontend.yaml (in team-ui)

apiVersion: v1
kind: Pod
metadata:
  name: frontend
  namespace: team-ui
  labels:
    role: frontend
spec:
  containers:
  - name: curl
    image: radial/busyboxplus:curl
    command: ["sleep", "3600"]

✅ tester.yaml (in testers)

apiVersion: v1
kind: Pod
metadata:
  name: tester
  namespace: testers
  labels:
    role: tester
spec:
  containers:
  - name: curl
    image: radial/busyboxplus:curl
    command: ["sleep", "3600"]
```
```bash
kubectl apply -f checkout.yaml
kubectl apply -f frontend.yaml
kubectl apply -f tester.yaml

```
## 🔍 Phase 2: Baseline Test — Everything Should Work

Before applying any NetworkPolicy, Kubernetes allows **all pods to communicate** with each other — across namespaces and to the Internet.

We’ll validate this default behavior.

---

### ✅ 1. Frontend → Checkout

```bash
kubectl exec -n team-ui frontend -- curl -s checkout.team-api.svc.cluster.local
```
### ✅ 2. Tester → Checkout

```bash
kubectl exec -n testers tester -- curl -s checkout.team-api.svc.cluster.local
```
Expected: ✅ Successful response from the checkout service.

### ✅ 3. Checkout → Internet
```bash
kubectl exec -n team-api checkout -- curl -s https://ifconfig.me

All these should work before we apply any policies.
```
## 🔒 Phase 3: Use Case 1 — Deny All in `team-api`

We’ll apply a strict **"deny-all"** policy to the `team-api` namespace.  
This will **block all incoming and outgoing traffic** to/from any pod in that namespace.

---

### 🔐 NetworkPolicy: `deny-all.yaml`

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
  namespace: team-api
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```
kubectl apply -f deny-all.yaml
# Should fail - tester cannot access checkout
kubectl exec -n testers tester -- curl -s checkout.team-api.svc.cluster.local

# Should fail - checkout cannot access internet
kubectl exec -n team-api checkout -- curl -s https://ifconfig.me

### 🔬 Test After `deny-all`

After applying the `deny-all` network policy, run the following tests to confirm that all ingress and egress traffic is blocked.

| 🔁 Source          | 🎯 Target          | 🧪 Test Command                                                                 | ✅ Expected Result |
|-------------------|-------------------|--------------------------------------------------------------------------------|--------------------|
| `frontend`        | `checkout`        | `kubectl exec -n team-ui frontend -- curl -s checkout.team-api.svc.cluster.local` | ❌ Blocked         |
| `tester`          | `checkout`        | `kubectl exec -n testers tester -- curl -s checkout.team-api.svc.cluster.local`   | ❌ Blocked         |
| `checkout`        | Internet (Public) | `kubectl exec -n team-api checkout -- curl -s https://ifconfig.me`               | ❌ Blocked         |

🛡️ These test results confirm that both **Ingress** and **Egress** traffic have been successfully denied for all Pods in the `team-api` namespace.


## 🧩 Phase 4: Use Case 2 — Allow Frontend to Access Checkout

### 🎯 NetworkPolicy: `allow-frontend-checkout.yaml`

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-checkout
  namespace: team-api
spec:
  podSelector:
    matchLabels:
      role: checkout
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: team-ui
    - podSelector:
        matchLabels:
          role: frontend
  policyTypes:
  - Ingress
```
```bash
kubectl apply -f allow-frontend-checkout.yaml
```

### 🔬 Test After Adding Ingress Policy

| 🔁 Source   | 🎯 Target   | 🧪 Test Command                                                                 | ✅ Expected Result |
|------------|------------|----------------------------------------------------------------------------------|--------------------|
| frontend   | checkout   | `kubectl exec -n team-ui frontend -- curl -s checkout.team-api.svc.cluster.local` | ✅ Allowed          |
| tester     | checkout   | `kubectl exec -n testers tester -- curl -s checkout.team-api.svc.cluster.local`   | ❌ Blocked          |
| checkout   | Internet   | `kubectl exec -n team-api checkout -- curl -s https://ifconfig.me`                | ❌ Blocked          |


## 🌍 Phase 5: Use Case 3 — Allow `checkout` → Internet (Egress)

### 🌐 NetworkPolicy: `allow-egress-internet.yaml`

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-egress-internet
  namespace: team-api
spec:
  podSelector:
    matchLabels:
      role: checkout
  egress:
  - to:
    - ipBlock:
        cidr: 0.0.0.0/0
  policyTypes:
  - Egress
```
```bash
kubectl apply -f allow-egress-internet.yaml
```
## 🔬 Final Test Summary

| 🔁 Source     | 🎯 Target   | ✅ Expected Result |
|--------------|-------------|--------------------|
| frontend     | checkout    | ✅ Allowed          |
| tester       | checkout    | ❌ Blocked          |
| checkout     | Internet    | ✅ Allowed          |
| inventory    | net         | ❌ Blocked          |

```bash
kubectl delete ns team-api team-ui testers
```


## 🔐 Use Case: Isolate Pod A from Pod B

### 🎯 Objective
We have two pods in the same namespace:

- `pod-a` with label: `app: a`
- `pod-b` with label: `app: b`

We want:

- ❌ `pod-a` **must not** talk to `pod-b`
- ✅ Other pods (e.g., `frontend`, `tester`) **can** talk to `pod-b`

---

### ⚠️ Challenge with Kubernetes NetworkPolicy
- Kubernetes NetworkPolicy doesn't support **explicit denies** (no `deny` keyword).
- It follows **additive allow-listing logic**:
  - You allow traffic by defining who **can** talk.
  - Anything not explicitly allowed is **denied**.
- We must write a policy that allows **only selected pods**, excluding `pod-a`.

---

## ✅ Solution: Allow Only Specific Pods to Talk to Pod B

### 🧾 allow-from-not-a.yaml

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-not-a-to-b
  namespace: team-api
spec:
  podSelector:
    matchLabels:
      app: b  # Target is pod-b
  ingress:
  - from:
    - podSelector:
        matchLabels:
          allow-access: true
  policyTypes:
  - Ingress
```
