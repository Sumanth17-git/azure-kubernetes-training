# 🚀 Azure Kubernetes Deployment Options

Azure provides multiple ways to deploy or manage Kubernetes clusters depending on your use case — whether you're a developer deploying an app or a cloud engineer managing hybrid clusters.

---

## 🔹 1. Deploy Application (New)

Use this if:  
You already have a **Kubernetes cluster (AKS or Arc-connected)** and want to deploy an application quickly — without touching infrastructure.

### 🧪 Real-World Scenario:
You're a developer who wants to deploy a containerized app from a **GitHub repo** to a **pre-existing AKS cluster** — similar to GKE’s "deploy from marketplace" or "autopilot with app config."

### ✅ Key Points:

- 🚫 No cluster creation needed
- 🎯 Application-focused workflow
- 🔁 Uses **GitOps** or **Bicep templates** under the hood
- 💼 Great for DevOps teams

---

## 🔹 2. Kubernetes Cluster

Use this if:  
You want **full control** over how the Kubernetes cluster is set up — including **VM size**, **node pools**, **networking**, **scaling**, and **monitoring**.

### 🧪 Real-World Scenario:
You're an SRE or cloud engineer setting up a **production-grade AKS cluster** with custom VNet, autoscaling, multiple node pools, and integrations.

### ✅ Key Points:

- 🔧 Full flexibility and control
- 📈 Ideal for **production** or **complex environments**
- 🧠 Requires more decisions (which is good for custom setups)
- 🚀 Most common choice for **serious workloads**

---

## 🔹 3. Automatic Kubernetes Cluster (Preview)

Use this if:  
You want a **hands-off experience**, similar to **GKE Autopilot** — Azure handles the infrastructure.

### 🧪 Real-World Scenario:
You’re prototyping or running a **dev/test environment** and want a quick, minimal-effort setup.

### ✅ Key Points:

- 🧪 Still in **preview**
- 🧘‍♂️ Minimal configuration; Azure manages infra
- 🔄 Azure handles upgrades, autoscaling, and maintenance
- ⚠️ Not recommended for **production workloads** yet

---

## 🔹 4. Add a Kubernetes Cluster with Azure Arc

Use this if:  
You already have a Kubernetes cluster **outside Azure** (on-prem, AWS, GCP) and want to **manage it via Azure**.

### 🧪 Real-World Scenario:
Your organization has Kubernetes clusters on-prem and wants **central governance, security, policy, and monitoring** via Azure.

### ✅ Key Points:

- 🔗 Registers existing clusters in Azure
- 🚫 Does **not** create a new cluster
- 🌐 Ideal for **hybrid cloud** strategies
- 🔐 Enables **Azure Policy, Defender for Kubernetes**, and more

---

## 🔹 5. Create a Kubernetes Cluster with Azure Arc

Use this if:  
You want to **provision a Kubernetes cluster** on **non-Azure infrastructure** (e.g., your own data center or another cloud), but still manage it with Azure tooling.

### 🧪 Real-World Scenario:
You’re building a hybrid or edge solution where the cluster runs **outside Azure**, but you want **Azure-native control and observability**.

### ✅ Key Points:

- 🏗️ Provisions and connects cluster to Azure
- 🧭 Fully **Azure Arc-enabled Kubernetes**
- 🌍 Extends Azure’s capabilities to **on-prem and multi-cloud environments**

---

> 💡 Choose the option that best matches your role and use case — from fast dev deployments to full production-grade or hybrid cloud clusters.


# ✅ Azure AKS Fundamentals: Subscription, Resource Groups & Node Pools

---

## ✅ 1. Subscription

### 📌 What it is:
Your **billing account** in Azure.

Every resource (e.g., AKS cluster, VM, storage) must be associated with a **Subscription** to track:
- 💰 Cost
- 📊 Usage
- 🔒 Role-Based Access Control (RBAC)

---

## ✅ 2. Resource Group

### 📌 What it is:
A **logical container** in Azure to **group related resources** together.

### 🔍 Real-world Example:
You're building a shopping app → you might create a resource group:


And group within it:
- AKS Cluster
- Load Balancer
- Azure Storage Account
- Azure Key Vault

### ✅ Benefits:
- 👥 Manage permissions at group level
- 🧹 Delete or clean up all resources in one go
- 📦 Logical grouping for better organization

---

## ✅ 3. Cluster Preset Configuration (AKS)

### 📌 What it is:
A **preset template** that lets you pick how much **control vs simplicity** you want while creating the AKS cluster.

### 🧰 Preset Types:

| Preset     | Use Case                       | Notes                                             |
|------------|--------------------------------|---------------------------------------------------|
| Dev/Test   | Learning, temporary testing     | Low cost, fewer nodes, simplified config          |
| Production | Critical services               | Autoscaling, multi-node pools, secure defaults    |
| Custom     | Advanced/pro users              | Full control over network, identity, VM sizes     |

### 🔍 Real-world Scenario:

- ✅ For testing/demo → choose **Dev/Test**
- ✅ For business-critical services → go **Production** or **Custom**

> 💡 **Tip:** If you're learning AKS, start with **Dev/Test** for quick setup.

---

# 🧱 What is a Node Pool in AKS?

### 📌 Definition:
A **Node Pool** is a group of **VMs (nodes)** with the **same OS, size, and configuration**.

- You can run **Linux** and **Windows** pools in the same cluster.
- You can isolate different **workloads** using different pools.

---

## 🔹 System Node Pool — Why It’s Needed?

### 📌 Purpose:
Runs **core Kubernetes and AKS components**, such as:

- `kube-proxy` — handles networking rules
- `CoreDNS` — provides internal cluster DNS
- `metrics-server` — provides resource metrics
- **AKS Add-ons**, including:
  - `azure-ip-masq-agent`
  - `kube-addon-manager`
  - `coredns-autoscaler`

### 💡 Best Practices:

- Keep system node pool **small** (1–2 nodes).
- Use smaller VM sizes like `Standard_DS2_v2`.
- **Mark node pool as `type=system`** explicitly.

---

## 🔸 User Node Pool — Why It's Important?

### 📌 Purpose:
Runs **your application workloads (Pods)**.

- You can have **multiple user pools** for different apps:
  - 🌐 Web apps
  - 🧮 Batch jobs
  - 🧠 ML workloads (GPU)
  - 💾 Memory-heavy services

### 🎯 Benefits:

- 🔒 **Workload isolation**: System and app workloads are separated.
- 📈 **Scalability**: You can autoscale user pools independently.
- 💰 **Cost optimization**: Use different VM sizes per workload type.

---

## 🧠 Summary

| Component         | Purpose                                            |
|------------------|----------------------------------------------------|
| Subscription      | Billing & access boundary                         |
| Resource Group    | Logical folder to group resources                 |
| Cluster Preset    | Simplifies AKS setup for common use cases         |
| System Node Pool  | Runs core Kubernetes and AKS system components    |
| User Node Pool    | Runs actual applications with isolated scaling    |

> ✅ Understanding these foundational concepts is key to mastering AKS in production.

---

## ✅ Best Practices: Node Pools in Azure Kubernetes Service (AKS)

---

### ⚠️ Taint the System Node Pool (Highly Recommended)

To avoid scheduling your workloads on **system node pools**, **taint the nodes** to allow only critical AKS components:

```bash
kubectl taint nodes <node-name> CriticalAddonsOnly=true:NoSchedule
```
---

## 🧠 Why Separate Node Pools Matter

Separating **system** and **user** node pools in AKS is a best practice for improving resilience, security, and operational efficiency.

---

### ✅ Benefits of Separating Node Pools

1. **🛠️ Reliability**  
   - Prevents user application crashes or resource exhaustion from affecting critical system components like CoreDNS or kube-proxy.

2. **🔐 Security**  
   - Apply **RBAC**, **Network Security Groups (NSGs)**, **taints**, and **node selectors** separately on user/system pools.

3. **💸 Flexibility**  
   - Use **Spot VMs** or **different VM sizes** in user pools for cost savings and workload optimization.

4. **📈 Scalability**  
   - **Independently autoscale** node pools based on specific workload patterns (e.g., API servers, ML jobs, batch tasks).

---

## 🔧 How to Specify a Node Pool Type in Azure CLI

When creating node pools, specify whether it's a **System** or **User** pool using the `--mode` flag.

---

### 🎯 System Node Pool Example

```bash
az aks nodepool add \
  --resource-group myResourceGroup \
  --cluster-name myAKSCluster \
  --name systempool \
  --mode System \
  --node-count 1 \
  --node-vm-size Standard_DS2_v2
```

### 👩‍💻 User Node Pool Example
``` bash
az aks nodepool add \
  --resource-group myResourceGroup \
  --cluster-name myAKSCluster \
  --name userpool \
  --mode User \
  --node-count 3 \
  --node-vm-size Standard_D4s_v3 \
  --enable-cluster-autoscaler \
  --min-count 1 \
  --max-count 5

```
###💡 Use additional flags like --priority Spot for cost-optimized Spot instances in user pools.

---

## 💰 AKS Spot Instances for User Node Pools

---

### 🧠 Why Use Spot Instances?

**Spot VMs** use Azure’s unused compute capacity at **deeply discounted rates** — up to **90% cheaper** than regular VMs.

They're perfect for:
- 🧪 Non-critical dev/test environments
- 🧮 Batch jobs or CI/CD runners
- 🧠 ML training tasks
- 🔁 Event-driven workloads

---

### ⚠️ Spot VM Behavior

- 💸 **Cheaper**, but can be **evicted anytime** when Azure needs capacity.
- 🧘‍♂️ Best suited for **interruptible** or **stateless** workloads.
- 🚫 Not ideal for **mission-critical apps** requiring guaranteed uptime.

---

## 🔧 How to Add a Spot Node Pool in AKS (Azure CLI)

```bash
az aks nodepool add \
  --resource-group myRG \
  --cluster-name myAKSCluster \
  --name spotpool \
  --mode User \
  --priority Spot \
  --spot-max-price -1 \
  --eviction-policy Delete \
  --node-count 1 \
  --node-vm-size Standard_D4s_v3
```

---

## 🔍 Parameter Breakdown for AKS Spot Node Pools

| Parameter               | Description                                                                 |
|-------------------------|-----------------------------------------------------------------------------|
| `--priority Spot`       | Marks the node pool as **Spot**, using Azure’s unused capacity              |
| `--spot-max-price -1`   | Pay up to the **current market price** (or specify your own price limit)    |
| `--eviction-policy Delete` | When Azure evicts the node, it is **automatically deleted**                 |
| `--mode User`           | Ensures the node pool is for **user workloads**, not system components      |
| `--node-vm-size`        | Select VM size based on workload (e.g., `Standard_D4s_v3`, `D2s_v3`, etc.)  |

> ⚠️ `--eviction-policy` can **only** be set to `Delete` in AKS.  
> AKS **does not support `Deallocate`** for eviction policy.

---

✅ Example command using all of the above:

```bash
az aks nodepool add \
  --resource-group myRG \
  --cluster-name myAKSCluster \
  --name spotpool \
  --mode User \
  --priority Spot \
  --spot-max-price -1 \
  --eviction-policy Delete \
  --node-count 1 \
  --node-vm-size Standard_D4s_v3
