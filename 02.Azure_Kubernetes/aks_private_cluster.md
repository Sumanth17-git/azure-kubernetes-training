# 🔒 Azure Kubernetes Service (AKS) – Private Cluster Access Guide

A **Private AKS Cluster** ensures your control plane is **not exposed to the public internet**, increasing security and compliance.

---

## 🧱 Step 1: Create a Private VM (Jumpbox)

Use a VM inside the same virtual network as the AKS cluster. This acts as a **jumpbox** for internal access.

```bash
az vm create \
  --resource-group MC_internal-training_aks-training_westus \
  --name aks-jumpbox \
  --image Ubuntu2202 \
  --admin-username azureuser \
  --authentication-type ssh \
  --generate-ssh-keys \
  --vnet-name aks-vnet-17585922 \
  --subnet aks-subnet \
  --public-ip-address "" \
  --nsg "" \
  --output table

---

## ✅ Key Points: Jumpbox VM for AKS Private Cluster

| Feature                | Description                                           |
|------------------------|-------------------------------------------------------|
| 🚫 No Public IP        | VM is fully private inside the VNet                   |
| 🔐 AKS VNet Bound      | Only accessible within the same VNet or peered VNet   |
| 🛡️ Secure SSH Disabled | Use **Azure Bastion** for access instead              |

---

## 🚀 Step 2: Connect to Private AKS Cluster

Once your AKS is private, you **can't run `kubectl` from your local machine** unless you're in the same private network.  
Azure provides multiple **secure ways** to interact with the cluster:

---

### ✅ Option 1: Use `az aks command invoke` (Recommended)

This is the **simplest and safest way** to interact with a private AKS cluster **without Bastion or SSH**.  
It lets you run any `kubectl` command remotely using Azure control plane APIs.

> 🧠 Behind the scenes, Azure injects your command into the cluster via an internal control channel and returns the result.

---

### 📦 Example Commands

#### 🔹 Get all pods in all namespaces
```bash
az aks command invoke (No Need for SSH or Jumpbox)
az aks command invoke \
  --resource-group <rg-name> \
  --name <aks-cluster-name> \
  --command "kubectl get pods -A"

az aks command invoke \
  --resource-group <rg-name> \
  --name <aks-cluster-name> \
  --command "kubectl run nginx --image=nginx"

az aks command invoke \
  --resource-group <rg-name> \
  --name <aks-cluster-name> \
  --command "kubectl get pods"

az aks command invoke \
  --resource-group <resource-group-name> \
  --name <aks-cluster-name> \
  --file ./nginx-deployment.yaml
```

---

## 🔐 Option 2: Create a Jumpbox VM Inside the Same VNet (Private AKS Access)

If your AKS cluster is private (no public API endpoint), you **cannot connect from your local machine**.  
To manage it, you need a **Jumpbox VM** inside the **same VNet** or a **peered VNet**.

---

### 🧠 Why You Need a Jumpbox

- AKS Private clusters **disable public API access**
- You must connect from **within the same VNet** or via **VPN/ExpressRoute**
- A **Jumpbox** is a VM deployed in the same subnet, allowing you to:
  - SSH into it
  - Install Azure CLI + `kubectl`
  - Connect securely to the AKS control plane

---

## 🔧 Step-by-Step: Create and Use a Jumpbox for AKS Access

---

### 🧱 Step 1: Get AKS Node Resource Group and VNet Details

Run the following command to get the AKS node resource group:

```bash
az aks show \
  --resource-group internal-training \
  --name aks-training \
  --query "nodeResourceGroup" \
  -o tsv
  
az network vnet list \
  --resource-group MC_internal-training_aks-training_westus \
  -o table

Get the subnet details:
az network vnet subnet list \
  --resource-group MC_internal-training_aks-training_westus \
  --vnet-name aks-vnet-17585922 \
  -o table

```
### 🖥️ Step 2: Create the Jumpbox VM (Ubuntu Linux)
```bash
az vm create \
  --resource-group MC_internal-training_aks-training_westus \
  --name aks-jumpbox \
  --image Ubuntu22.04 \
  --admin-username azureuser \
  --authentication-type ssh \
  --generate-ssh-keys \
  --vnet-name aks-vnet-17585922 \
  --subnet aks-subnet \
  --public-ip-address "" \
  --nsg "" \
  --output table
```
This creates a private VM (no public IP), secured. You’ll access it using Azure Bastion
This creates a private VM inside the AKS VNet/subnet.


### 🌐 Step 3: Enable Azure Bastion (🔒 Optional but Recommended)

If your Jumpbox VM does **not** have a public IP (as per best practice), you'll need **Azure Bastion** to access it securely from your browser — **no need for SSH keys or IP exposure**.

---

#### 🧱 What Is Azure Bastion?

Azure Bastion is a fully managed PaaS service that provides **secure and seamless RDP/SSH** connectivity to VMs directly through the **Azure Portal**, using TLS over HTTPS — **without exposing the VM to the public internet**.


### 🔧 Create Azure Bastion

```bash
az network bastion create \
  --name aks-bastion \
  --resource-group MC_internal-training_azurecluster_westus \
  --vnet-name aks-vnet-17585922 \
  --public-ip-address aks-bastion-ip \
  --location westus \
  --sku Basic
```
#### Then go to VM → Connect → Bastion in portal and login with azureuser.

---

### 🔧 Step 4: Install Azure CLI + kubectl on the Jumpbox

Once you're connected to the Jumpbox VM (via Azure Bastion):

#### 📦 Install Azure CLI

```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
az aks install-cli
az login

az aks get-credentials \
  --resource-group internal-training \
  --name aks-training
This merges your AKS credentials into ~/.kube/config.
kubectl get nodes
kubectl get pods -A
```
---

## 🔧 Section 1: Install Azure CLI

Azure CLI is essential for managing your AKS cluster, including authentication and configuration tasks.

---

### 📍 On Windows (Using PowerShell as Administrator)

```powershell
Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi
Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'
Remove-Item .\AzureCLI.msi
az version
```

---

## 🔐 Section 2: Configure SSH Permissions (Windows Only)

When using SSH from Windows (via PowerShell, OpenSSH, or Azure Bastion), your **PEM key file must have strict permissions**.  
If the key is accessible by system or administrator groups, SSH may reject it for security reasons.

---

### 📍 Step 1: Open PowerShell in Your SSH Key Directory

Navigate to the directory where your `.pem` key file is stored:

```powershell
cd "C:\04.Kubernetes\Azure\"

📍 Restrict PEM File Permissions:
icacls .\azurejump-server_key.pem /inheritance:r
icacls .\first-vm_key.pem /grant:r "${env:USERNAME}:R"

# Remove inheritance (if not already done)
icacls "C:\04.Kubernetes\Azure\first-vm_key.pem" /inheritance:r

# Remove overly permissive groups
icacls "C:\04.Kubernetes\Azure\first-vm_key.pem" /remove "BUILTIN\Administrators"
icacls "C:\04.Kubernetes\Azure\first-vm_key.pem" /remove "NT AUTHORITY\SYSTEM"
icacls "C:\04.Kubernetes\Azure\first-vm_key.pem" /remove "NT AUTHORITY\Authenticated Users"

# Grant read access to only your current user
icacls .\first-vm_key.pem /grant:r "${env:USERNAME}:R"
```
---

### ✅ This Will:

- 🔐 Remove inherited permissions from the PEM file
- 🔒 Strip overly permissive access groups
- 👤 Allow only **your user account** to read the key file

> This is required for OpenSSH to accept the PEM key on Windows.

---

## 🚀 Section 3: SSH into the Azure VM (from Windows)

Once your key permissions are secured, you can SSH into your **Azure Linux VM** directly using PowerShell or a terminal that supports OpenSSH.

---

### 📍 SSH Command Example

```powershell
ssh -i .\azurejump-server_key.pem azureuser@135.13.13.230
```
---

## ☁️ Section 4: Azure CLI Authentication and Subscription Setup

Once you have SSH access to your **Jumpbox VM**, you’ll use the Azure CLI (`az`) to authenticate and set your desired subscription context.

---

### 📍 Step 1: Login to Azure

#### 👤 Option 1: Standard Login (if browser access is available)

```bash
az login
az login --use-device-code
az account show --output table
az account set --subscription "24c4fb07-0fb5-4b37-bc45-5cb7e6e95520"
```
### 🧰 Section 5: Clone Your Repository and Run Setup Scripts
📍 Clone Git Repository:
```bash
sudo su
apt update -y
apt install git -y
git clone https://github.com/Sumanth17-git/APMTrianing.git
cd APMTraining

📍 Make Scripts Executable:
chmod +x *

📍 Run Setup Scripts:
./setup_ubuntu.sh
./setup_kubectl.sh

```
### ☸️ Section 6: Connect to AKS Cluster
```bash
📍 Get AKS credentials:
az aks get-credentials --resource-group internal-training --name aks-training --overwrite-existing

📍 Verify AKS access:
kubectl get deployments --all-namespaces=true
kubectl get pods --all-namespaces=true
```

