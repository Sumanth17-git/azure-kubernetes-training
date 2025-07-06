# 🐳 Container Runtime in AKS: containerd (Not Docker)

## 📌 Summary

As of recent AKS versions, **containerd** is the default container runtime replacing Docker. It is lightweight, optimized for Kubernetes, and fully compatible with the **CRI (Container Runtime Interface)** used by Kubernetes.

You can verify the container runtime on your AKS nodes using:

```bash
kubectl get nodes -o wide
## 🛠️ Using `crictl` to Inspect Containers

When you're using **containerd** as the container runtime (the default in AKS), Docker CLI commands like `docker ps` won’t work.

Instead, use [`crictl`](https://kubernetes.io/docs/tasks/debug/debug-cluster/crictl/), a CLI tool for working with **CRI-compatible** runtimes like `containerd` and `CRI-O`.

### 🔍 Why `crictl`?

Kubernetes no longer requires Docker as a runtime. Tools like `crictl` are now essential for low-level container inspection when using CRI-compliant runtimes.

---

### 🔧 Install `crictl`

You can download it from the GitHub releases:

```bash
# Example for Linux
VERSION="v1.28.0"
curl -LO https://github.com/kubernetes-sigs/cri-tools/releases/download/$VERSION/crictl-$VERSION-linux-amd64.tar.gz
sudo tar -C /usr/local/bin -xzf crictl-$VERSION-linux-amd64.tar.gz

```


## 📦 Common `crictl` Commands

`crictl` is the CLI tool for container runtime debugging and management on CRI-compatible runtimes like `containerd` or `CRI-O`.

| Command                        | Description                                |
|-------------------------------|--------------------------------------------|
| `crictl ps`                   | List all **running containers**            |
| `crictl ps -a`                | List **all containers**, including stopped |
| `crictl pods`                 | Show all **pods** known to the runtime     |
| `crictl inspect <container_id>` | View **detailed info** about a container  |
| `crictl logs <container_id>`    | Show **logs** of a container              |
| `crictl exec -it <container_id>` | **Exec** into a running container       |
| `crictl stats`               | View **resource usage** stats              |

> 🧠 Tip: You must be connected to the host node (e.g., via `kubectl debug node/...` and `chroot /host`) to use `crictl`.

---

### ✅ Example

```bash
# List all containers
crictl ps -a

# Inspect a container
crictl inspect <container_id>

# View logs
crictl logs <container_id>

# Exec into container
crictl exec -it <container_id> sh
```

# 🔧 Access AKS Cluster Nodes for Maintenance or Troubleshooting

In Azure Kubernetes Service (AKS), direct access to cluster nodes is **restricted by design** for security and stability. However, certain maintenance or troubleshooting tasks (e.g., log collection, runtime debugging) require node-level access.

---

## 🧱 Why Can't You SSH Directly?

- AKS nodes **do not have public IPs** by default.
- Managed nodes in a **Virtual Machine Scale Set (VMSS)** are part of the AKS control plane.
- Instead of SSH, **Kubernetes-native APIs** are the recommended way to inspect nodes.

---

## 🚀 Option 1: Access Nodes Using `kubectl debug`

You can access the node using a temporary debug pod and a container image (like BusyBox or Mariner).

### 🧪 Step-by-Step: Access a Node

1. **List Nodes**
```bash
kubectl get nodes -o wide

kubectl debug node/aks-workerpool-47159840-vmss000000 -it --image=mcr.microsoft.com/cbl-mariner/busybox:2.0

chroot /host
## 🧑‍💻 Interacting with the Node via `kubectl debug`

Once you've started a debug session using:

```bash
kubectl debug node/<node-name> -it --image=mcr.microsoft.com/cbl-mariner/busybox:2.0
chroot /host

crictl ps
crictl logs <container_id>
top
df -h
journalctl -u kubelet
crictl ps
crictl logs <container_id>
kubectl delete pod <debug-pod-name>
