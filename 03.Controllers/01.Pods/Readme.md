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
```
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
apiVersion: apps/v1
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

### 🧾 What Does the `metadata` Field Do?

The `metadata` field contains **identifying information** about the Kubernetes object.  
It helps Kubernetes **track, categorize, and manage** the resource.

#### 📋 It Includes:

- `name`: Unique name of the object.
- `namespace`: *(Optional)* The namespace where the object will be created.
- `labels`: Key-value pairs used for selection, grouping, and filtering.
- `annotations`: Additional metadata (not used for selection).

#### 🧠 Example:

```yaml
apiVersion: apps/v1
kind: Pod
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

### 📦 What Does the `spec` Field Do?

The `spec` field is where you tell Kubernetes **what to do** with your object.

It defines the **desired state**, such as:

✅ What containers should run? (for Pods)  
✅ How many replicas should run? (for Deployments)  
✅ How should a Service expose an application?

This is the core of the manifest that controls runtime behavior.

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

### 🔍 Explanation:

- 🎯 **Creates** a Pod named `nginx-pod`
- 🐳 **Runs** a single container using the official `nginx` image
- 🌐 **Exposes** port `80` inside the container


## 🌐 Kubernetes Service

A **Service** in Kubernetes is an abstraction that defines a logical set of Pods and a policy by which to access them — typically via a stable network endpoint (ClusterIP, NodePort, LoadBalancer, etc.).

---

### 📄 Sample YAML: LoadBalancer Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
  namespace: default
spec:
  selector:
    app: nginx  # Matches the Pod label
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: LoadBalancer  # Use "NodePort" if LoadBalancer is not available
 
 ### 🎯 What is a `selector` in Kubernetes?

The `selector` in a **Service** tells Kubernetes **which Pods it should route traffic to**.

It works by **matching labels** defined on Pods. This is how Kubernetes dynamically discovers which Pods belong to which Service, Deployment, ReplicaSet, etc.

---

### ✅ Selector Use Cases

| Question                                  | Answer                                                |
|-------------------------------------------|--------------------------------------------------------|
| Which Pods belong to this Service?        | Those with labels matching the selector value          |
| Which Pods should this Deployment manage? | Those matching the selector defined in the spec        |
| Can one Service serve multiple Pods?      | Yes, if the Pods share the same labels                 |

