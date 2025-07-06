# 🧱 Multi-Container Pod in Kubernetes (NGINX + Tomcat Example)

## 🎯 What is a Multi-Container Pod?

A **multi-container pod** is a Kubernetes pod that runs **two or more containers**, sharing:

- 🧠 The **same network namespace** (same IP address)
- 💾 The **same volumes**
- 📡 Communication via `localhost`

> Think of it like **roommates in the same apartment**:
> - Sharing a **kitchen** (volume)
> - Same **address** (IP)
> - They can talk freely via **localhost**

---

## 🧠 Real-Life Analogy

Imagine a **shared hostel room** (the Pod) with **two roommates**:

| Roommate | Role                   |
|----------|------------------------|
| NGINX    | The **front desk** manager |
| Tomcat   | The **backend** engineer   |

They:
- Live at the **same address (IP)**
- Share **common space** (volume + network)
- Can **talk directly using `localhost`**

---

## ✅ What We Want to Achieve

We want to deploy a **Kubernetes pod** with two containers:

- 🚪 NGINX: Listens on **port 80** and acts as a **reverse proxy**
- 🔧 Tomcat: Listens on **port 8080** and serves the actual Java app
- 🔁 NGINX forwards requests to **Tomcat via `localhost:8080`**
- 🧳 Both containers **run inside the same pod**

---

## 🧬 How It Works Internally

| Element         | Behavior                                                       |
|----------------|----------------------------------------------------------------|
| **Tomcat**      | Runs inside the pod and listens on port `8080`                 |
| **NGINX**       | Runs inside the pod, listens on port `80`, proxies to `localhost:8080` |
| **Network**     | Both containers share the **same IP address** and `localhost`  |
| **Volumes**     | Shared config can be injected using **volumes + ConfigMap**    |
| **Pod IP**      | One IP exposed via a **Kubernetes Service**                    |

---
To test this pods separately , login into new container

Kubectl exec -it <pod name> -- sh

curl http://podip:8080
curl http://podip:80



