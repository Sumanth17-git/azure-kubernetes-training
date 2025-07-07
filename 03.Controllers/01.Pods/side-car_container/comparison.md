# 🔍 Comparing Init Containers vs Sidecar Containers in Kubernetes

Kubernetes allows you to use **multiple containers** within a single pod. Among them, **Init Containers** and **Sidecar Containers** serve two distinct but complementary purposes.

This table compares them side-by-side for better understanding and practical use in real-world deployments.

---

## 🧮 Feature Comparison: Init Container vs Sidecar Container

| 🔧 Feature         | 🚦 **Init Containers**                                                                 | 🔄 **Sidecar Containers**                                                                  |
|-------------------|----------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| **Lifecycle**      | Run **once** before the main containers start; **terminate** after completion          | Run **alongside** main containers during the entire pod lifecycle                          |
| **Execution Order**| Run **sequentially** (one after another) **before** app containers start               | Start **in parallel** with the main containers and run **concurrently**                    |
| **Purpose**        | Perform **setup/preparation** tasks like downloading config, waiting for DB, etc.      | Provide **ongoing support** like logging, monitoring, proxying, or syncing                 |
| **Container Status**| **Exit** after finishing their task                                                   | Remain **running** as long as the pod is alive                                             |
| **Probes Supported**| ❌ **Not supported** (no liveness, readiness, or startup probes)                       | ✅ Fully supports **liveness**, **readiness**, and **startup probes**                      |
| **Interaction**    | Do **not interact** with the main containers once they're running                      | Often **interact continuously** with main containers (e.g., share logs, sync config)       |
| **Failure Impact** | Pod will **fail to start** if any init container fails                                | Pod may continue running even if a sidecar crashes (depends on restart policy)            |
| **Use Cases**      | Wait for services, clone Git repos, fix permissions, perform migrations                | Log shipping, metrics scraping, config syncing, service mesh proxies                      |

---

## 🧠 When to Use What?

| Use This Pattern For           | Recommended Container Type |
|-------------------------------|-----------------------------|
| Waiting for a database         | ✅ Init Container           |
| Running a database migration   | ✅ Init Container           |
| Sending logs to Azure Monitor  | ✅ Sidecar Container        |
| Prometheus metrics exporter    | ✅ Sidecar Container        |
| Pulling secrets from Key Vault | ✅ Init Container or Sidecar (depends on lifecycle) |

---

## 📚 Learn More

- [Kubernetes Init Containers](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/)
- [Kubernetes Multi-Container Pods](https://kubernetes.io/docs/concepts/workloads/pods/#multi-container-pods)
- [Sidecar Pattern - Microsoft](https://learn.microsoft.com/en-us/azure/architecture/patterns/sidecar)

---

## 💡 Pro Tip

In production environments:
- Use **Init Containers** to make sure everything is ready **before** the app runs.
- Use **Sidecars** for **real-time interactions** and operational support like logging, tracing, and security agents.

