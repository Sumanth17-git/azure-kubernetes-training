# 📦 Introduction to Kubernetes Objects and Pod YAML Structure

## 🧠 What are Kubernetes Objects?

Kubernetes **objects** are like instructions or blueprints that tell Kubernetes **how to manage your application and resources**. These objects define:

- ✅ What to run (app, service, job, etc.)
- 📦 How many copies should run
- 🔗 How it connects to other services
- 💾 How data is stored and persisted

> Think of Kubernetes objects as **declarative blueprints** that define your desired state.

---
## 🧱 Why Pods, Not Just Containers?

Kubernetes doesn't manage containers directly. Instead, it manages **Pods**, which are the **smallest deployable unit** in Kubernetes.

### 🗳️ What is a Pod?

A **Pod** is like a **box** that can hold one or more containers. It includes:
- Containers (e.g., NGINX, app, logger)
- Storage (volumes)
- Network configuration (IP, ports)

```bash
# Command to create a Pod manually
kubectl run nginx --image=nginx:latest
Example: A Pod might contain a web app container and a log forwarder sidecar container — both working together.

## 🧭 Choosing the Right `apiVersion`

Different Kubernetes objects are managed under different **API groups**, and each uses a specific `apiVersion`.

This field tells Kubernetes which **versioned API** to use for validating and interpreting the object.

---

### 📘 Common `apiVersion` Mappings

| 🧩 **Object Type**        | 🔢 **apiVersion Example** |
|---------------------------|---------------------------|
| Pod, Service, ConfigMap   | `v1`                      |
| Deployment, StatefulSet   | `apps/v1`                 |
| Job, CronJob              | `batch/v1`                |

---

### 🔗 Reference:

For a complete and up-to-date guide on Kubernetes API versions:
👉 [Kubernetes API Version Guide – Matthew Palmer](https://matthewpalmer.net/kubernetes-app-developer/articles/kubernetes-apiversion-definition-guide.html)

---

> ✅ Tip: Always check your Kubernetes cluster version to ensure the object `apiVersion` is supported.

## 📌 Fields Explained: Anatomy of a Kubernetes YAML File

Every Kubernetes YAML file follows a structured format. Let’s break down the **four core fields** used in almost all Kubernetes resource definitions.

---
### 1️⃣ `apiVersion`

The `apiVersion` field specifies **which version of the Kubernetes API** should be used to create and manage the object.

This helps Kubernetes determine:
- 🛠️ What features are supported
- ⚠️ Which validations apply
- 🔄 How to process the object

#### ✅ Common Values:

| Kubernetes Object Type           | `apiVersion`   |
|----------------------------------|----------------|
| Pod, Service, ConfigMap          | `v1`           |
| Deployment, ReplicaSet, StatefulSet | `apps/v1`      |
| Job, CronJob                     | `batch/v1`     |

#### 🧠 Example:

```bash
apiVersion: apps/v1
```
### 2️⃣ `kind`

The `kind` field defines the **type of Kubernetes object** you are creating — such as a `Pod`, `Service`, or `Deployment`.

This tells Kubernetes **what** the YAML file is intended to manage or deploy.

---

#### 🧠 Syntax Example:

```yaml
kind: Pod
```
#### 📘 Common `kind` Examples

| Kubernetes Object Type | Description                                          |
|------------------------|------------------------------------------------------|
| `Pod`                  | A basic containerized unit                           |
| `Deployment`           | Scalable, self-healing application management        |
| `Service`              | Exposes your application to the network              |
| `ConfigMap`            | Stores non-sensitive configuration data              |


### 3️⃣ `metadata`

The `metadata` field contains identifying information about the Kubernetes object. This helps Kubernetes track, categorize, and manage the resource.
•	Contains details about the object, such as: 
o	name: Unique name of the object.
o	namespace: (Optional) Defines the namespace where the object will be created.
o	labels: Key-value pairs used for identification and selection.
o	annotations: Additional metadata (not used for selection).


#### 🧠 Example:

```yaml
metadata:
  name: my-nginx-pod
  namespace: default
  labels:
    app: nginx
    environment: dev
  annotations:
    description: "This is an NGINX pod"
    createdBy: "Admin"
```
#### 📋 Metadata Field Breakdown

| Field        | Purpose                                                                |
|--------------|------------------------------------------------------------------------|
| `name`       | Unique name of the object within the namespace                         |
| `namespace`  | (Optional) Logical grouping; separates resources into environments     |
| `labels`     | Key-value pairs used for selection, grouping, and filtering            |
| `annotations`| Key-value pairs for attaching extra metadata (not used in selection)   |

### 4️⃣ `spec`

The `spec` (short for **specification**) defines the **desired state** of the Kubernetes object.

This is where you tell Kubernetes **what to do**, such as what containers to run, what ports to expose, how many replicas to maintain, or how to mount volumes.
✅ How many replicas should run? (for Deployments)
✅ What containers should run? (for Pods)
✅ How should a Service expose an application?

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-nginx-pod
  namespace: default
  labels:
    app: nginx
    environment: dev
  annotations:
    description: "This is an Nginx pod"
    createdBy: "Admin"
spec:
  containers:
    - name: nginx
      image: nginx:latest
      ports:
        - containerPort: 80

```

📌 Explanation:
•	Creates a Pod named nginx-pod.
•	Runs a single container using the nginx image.
•	Opens port 80 inside the container.
