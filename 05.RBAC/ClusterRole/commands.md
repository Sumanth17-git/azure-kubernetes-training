```bash
kubectl create serviceaccount testuser -n demo-rbac
```
```yaml
# clusterrole.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: pod-admin
rules:
- apiGroups: ["", "apis", "batch", "extensions"]
  resources: ["pods", "deployments", "services", "secrets"]
  verbs: ["get", "watch", "list", "create", "delete"]
```
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: pod-admin-binding
subjects:
- kind: ServiceAccount
  name: testuser
  namespace: demo-rbac
roleRef:
  kind: ClusterRole
  name: pod-admin
  apiGroup: rbac.authorization.k8s.io
```
```bash
kubectl apply -f clusterrole.yaml
kubectl apply -f clusterrolebinding.yaml
kubectl describe clusterrole pod-admin
kubectl describe clusterrolebinding pod-admin-binding
kubectl get serviceaccounts -n demo-rbac
kubectl get roles -n demo-rbac
kubectl get rolebindings -n demo-rbac

```
