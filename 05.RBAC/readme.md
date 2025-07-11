# 🔐 What is RBAC in Kubernetes?

**RBAC (Role-Based Access Control)** controls **who can do what** within your Kubernetes cluster.

RBAC defines access based on:

- **Who** (subjects)  
- **Can do what** (verbs)  
- **On which resources**  
- **In what namespace**

This enables fine-grained access control over Kubernetes resources by assigning roles to users or groups and specifying their permissions within a namespace or cluster-wide.

# 🔧 STEP-BY-STEP IMPLEMENTATION: Kubernetes RBAC Without AD

## 1. Create a Namespace

```bash
kubectl create namespace demo-rbac
```
## 2. Create a Service Account

We use a dummy Kubernetes-native identity to simulate a user.

**`service-account.yaml`**
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: dummy-user
  namespace: demo-rbac
```
Apply the Service Account with:
```bash
kubectl apply -f service-account.yaml
```
## 3. Create a Role

This Role allows access to Pods within the `demo-rbac` namespace.

**`role.yaml`**
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: demo-rbac
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
```
```bash
kubectl apply -f role.yaml
```
4. Bind Role to Service Account
```yaml
# rolebinding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods-binding
  namespace: demo-rbac
subjects:
- kind: ServiceAccount
  name: dummy-user
  namespace: demo-rbac
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io

```
```bash
kubectl apply -f rolebinding.yaml
```




```yaml
# clusterrole-readonly.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cluster-read-only
rules:
- apiGroups: ["", "apps", "batch", "extensions"]
  resources: ["pods", "services", "deployments", "replicasets", "nodes", "namespaces", "events"]
  verbs: ["get", "list", "watch"]
  
```

