```bash
kubectl create namespace demo-rbac
kubectl apply -f service-account.yaml

kubectl apply -f role.yaml
kubectl apply -f rolebinding.yaml
kubectl get serviceaccount dummy-user -n demo-rbac
kubectl apply -f test-pod.yaml
kubectl run nginx --image=nginx -n dev
kubectl exec -n demo-rbac -it rbac-test -- /bin/sh
kubectl run testpod --image=nginx --restart=Never -n demo-rbac
kubectl get pods -n demo-rbac
kubectl get secrets -n demo-rbac
kubectl get pods -n demo-rbac
kubectl delete pod testpod -n demo-rbac
kubectl run anotherpod --image=nginx --restart=Never -n default
verbs: ["get", "list", "watch"]  # Remove create/delete
```

```yaml
# role-full-access.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: demo-rbac
  name: full-access
rules:
- apiGroups: ["*"]         # All API groups
  resources: ["*"]         # All resource types
  verbs: ["*"]             # All actions (get, list, create, delete, etc.)
```
```yaml
## Full Permission
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: full-access
  namespace: demo-rbac
rules:
- apiGroups: [""]  # Core group
  resources: [
    "pods", "services", "endpoints",
    "persistentvolumeclaims", "configmaps",
    "secrets", "serviceaccounts", "events"
  ]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]

- apiGroups: ["apps"]
  resources: [
    "deployments", "daemonsets",
    "replicasets", "statefulsets"
  ]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]

- apiGroups: ["batch"]
  resources: ["jobs", "cronjobs"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]

- apiGroups: ["networking.k8s.io"]
  resources: ["networkpolicies", "ingresses"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]

- apiGroups: ["policy"]
  resources: ["poddisruptionbudgets"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]

# Optional - for Role/RoleBinding management
- apiGroups: ["rbac.authorization.k8s.io"]
  resources: ["roles", "rolebindings"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
```
