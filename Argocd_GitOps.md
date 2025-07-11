# 🧠 What is GitOps?

**GitOps = Git + DevOps**

GitOps is a modern way to manage Kubernetes using **Git as the single source of truth**.

It means:

- 📁 You store all your Kubernetes configurations (YAML files) in a Git repository  
- ✅ Any change to your app, infra, or configuration is done by committing to Git  
- 🔁 A tool like **Argo CD** or **Flux** watches that Git repo and automatically applies changes to your cluster  
# 🧱 Core GitOps Principles (Easy Explanation)

| Principle                         | Explanation                                                                                             |
|----------------------------------|---------------------------------------------------------------------------------------------------------|
| ✅ Git as the single source of truth | All your Kubernetes YAMLs (deployments, services, config) live in Git. No changes made manually in the cluster. |
| 📦 Declarative infrastructure     | Everything you want in your cluster is described in files (e.g., `deployment.yaml`). Git becomes your blueprint. |
| 🔁 Automated delivery             | Tools like Argo CD automatically sync what’s in Git to your cluster.                                   |
| 🔍 Version control and audit     | Git tracks every change: who changed what, when, and why. Easy rollback with Git history.              |
| 🔐 Security and compliance       | No one needs direct access to the cluster — all changes go through Git (with review + approval).       |
| 🔧 Self-healing                  | If someone makes a manual change in the cluster, GitOps tools detect drift and fix it automatically.   |

# 🎯 Why Do We Need GitOps? (With Scenarios)

| ❌ Problem (Without GitOps)               | ✅ GitOps Solves It By                      | 🔍 Real-World Scenario                                                                                                                                                        |
|------------------------------------------|--------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Manual `kubectl apply` commands          | Automated sync from Git                    | A developer forgets to apply the latest YAML to staging; production behaves differently. With GitOps, once it's merged to `main`, Argo CD applies it — no human error.       |
| Drift between Git and cluster            | Reconciles cluster to match Git            | An engineer manually updates a replica count from 2 to 4 in the cluster. Git still says 2. Argo CD detects the mismatch and rolls back the drift — keeping it in sync.       |
| No change tracking                       | Every config change is versioned           | You're debugging a failure — but nobody knows who changed the env variable in the deployment YAML last week. With GitOps, every change is recorded in Git (with author).     |
| Risk of mistakes during live edits       | Safe, peer-reviewed changes via Git        | Someone applies a YAML with the wrong image tag in production. Oops! With GitOps, changes go through a Pull Request and review before being deployed.                        |
| Difficult rollbacks                      | Rollback with `git revert` or `git checkout` | A new deployment causes issues. No need to remember the last good YAML — just use `git revert` and Argo CD will restore the previous state automatically.                    |
| No team collaboration                    | Everyone works through Git (PRs, reviews)  | DevOps uses kubectl, Devs edit local files, SREs tweak things live. Chaos! With GitOps, everyone works from a shared Git repo — versioned, reviewed, and traceable.          |


# 🖼️ GitOps Architecture Diagram (Text View)

```text
Developer
   |
   | 1. Push YAML to Git (Deployment/Service/etc.)
   v
Git Repository  (e.g., GitHub)
   |
   | 2. Argo CD watches this repo
   v
Argo CD running in AKS
   |
   | 3. Reconciles desired state from Git
   v
AKS Cluster (actual state updated)

```
# 🚀 Step-by-Step GitOps Flow

---

### 🧑‍💻 Step 1: Developer Pushes YAML to Git

A developer makes a change (e.g., updates `deployment.yaml`) and pushes it to the **main branch** of a Git repository (e.g., GitHub, GitLab, Bitbucket).

---

### 🛰️ Step 2: Argo CD Watches Git Repository

- Argo CD is installed in your AKS cluster (via **Helm** or **Kubernetes manifest**)
- An **Argo CD Application** resource is configured to point to the Git repo and path
- Argo CD continuously polls the repository for changes

---

### 🔁 Step 3: Argo CD Syncs to AKS

- Argo CD detects the new Git commit
- It applies the changes to the cluster using the **Kubernetes API**
- Your workloads (Deployments, Services, ConfigMaps, etc.) are updated automatically

✅ No manual `kubectl apply`  
✅ Full audit/history in Git  
✅ Cluster always reflects Git = **Single Source of Truth**

# 🚀 Install Argo CD with Helm and Set Admin Password

This guide explains how to install Argo CD on a Kubernetes cluster using Helm and set a custom admin password securely.

---

## 📁 Step 0: Create Namespace for Argo CD

```bash
kubectl create namespace argocd
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
```
## 🔐 Step 1: Generate bcrypt Hash for `admin@123`

Install Apache utilities (for `htpasswd`) on Debian/Ubuntu:

```bash
sudo apt install apache2-utils
htpasswd -nbBC 10 "" admin@123 | tr -d ':\n' | sed 's/$2y/$2a/'
```
### 🛠 Step 2: Install Argo CD with Helm and set the password
```bash
helm install argocd argo/argo-cd \
  --namespace argocd \
  --create-namespace \
  --set server.service.type=LoadBalancer \
  --set configs.params.server.insecure=true \
  --set-string "configs.secret.argocdServerAdminPassword=\$2a\$10\$9NPKk3cEQczH8uqoN6YcDuwYjEkFZ5I6oncoRIyGjRt4bT47O4hfK"
```
-- 🔐 Replace the hashed password with the output from your htpasswd command.


