# 🚀 Why Autoscaling Based on CPU and Memory is Not Enough in Modern Microservices

In modern microservices architecture, relying solely on **CPU** and **Memory-based autoscaling** is often **not sufficient**. This is because:

- Many services are **I/O bound**, not CPU or memory bound.
- Latency issues in message queues or APIs might occur **before** CPU usage spikes.
- Background jobs and event-driven workloads don’t necessarily increase CPU usage when under load.

As a result, **traditional Horizontal Pod Autoscaler (HPA)** may fail to respond to real workload signals.

---
![image](https://github.com/user-attachments/assets/5895b39b-5689-4cd5-8457-c2d54c201aa4)

## 🔍 What is KEDA?

**KEDA** (Kubernetes-based Event-Driven Autoscaler) is an **open-source** component that brings **event-driven scaling** to Kubernetes. It:

- Supports autoscaling based on **custom metrics**, not just CPU/Memory.
- Integrates with various **event sources** like:
  - Kafka
  - RabbitMQ
  - Azure Service Bus
  - Prometheus
  - Redis
  - AWS SQS
  - And many more

> KEDA can scale **from zero to N** pods based on demand from external systems.

---

## 🛠️ Install KEDA

You can install KEDA using **Helm**:

```bash
helm repo add kedacore https://kedacore.github.io/charts
helm repo update
helm install keda kedacore/keda --namespace keda --create-namespace
kubectl get all -n keda
```

# 🚀 Outdated Autoscaling? Why You Need KEDA Now

Scaling based on **CPU and memory** is outdated in today's fast-paced, **event-driven microservices** world.

KEDA enables you to focus on what truly matters: **scaling based on real demand** such as:

- Message queue length
- HTTP request volume
- Database load
- Custom application metrics

If you're struggling with **inefficient autoscaling strategies**, consider exploring **KEDA**.  
It’s a **game-changer** for ensuring **reliability**, **scalability**, and **cost-effectiveness**.

---

## ✅ Step 1: Install Prometheus with ServiceMonitor Support

### 1.1 Create Namespace and Add Helm Repo

```bash
kubectl create namespace monitoring

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prom-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --set grafana.enabled=false
kubectl get pods -n monitoring

```
🧭 Step 2: Deploy Spring Boot App with Prometheus Annotations
https://github.com/Sumanth17-git/SRETraining/tree/main/springboot-microservice-logging
Update your Spring Boot deployment (springboot-app) and expose /actuator/prometheus.
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: springboot-app
  labels:
    app: springboot-app
spec:
  replicas: 2  # Updated replicas for high availability
  selector:
    matchLabels:
      app: springboot-app
  template:
    metadata:
      labels:
        app: springboot-app
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8881"  # Updated port
        prometheus.io/path: "/actuator/prometheus"
    spec:
      containers:
      - name: springboot-app
        image: sumanth17121988/springbootmetric:1
        ports:
        - name: metrics-port  # Named port for Prometheus
          containerPort: 8881  # Application container port
        resources:
          limits:
            cpu: "500m"
            memory: "256Mi"
          requests:
            cpu: "250m"
            memory: "128Mi"
        livenessProbe:
          httpGet:
            path: /actuator/health/liveness
            port: 8881
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /actuator/health/readiness
            port: 8881
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: springboot-app-service
  labels:
    prometheus: monitored  # Label to match ServiceMonitor
spec:
  selector:
    app: springboot-app
  ports:
    - name: metrics-port  # Named port for Prometheus
      protocol: TCP
      port: 8881  # Exposed service port
      targetPort: 8881  # Container port
  type: LoadBalancer  # Expose the service externally
---
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: springboot-app-monitor
  labels:
    release: prom-stack  # Label to match the Prometheus release name
spec:
  selector:
    matchLabels:
      prometheus: monitored  # Matches the label on the Service
  namespaceSelector:
    matchNames:
      - default  # Ensure this matches the namespace
  endpoints:
    - port: "metrics-port"  # Named port as a string
      path: /actuator/prometheus  # Path to scrape metrics
      interval: 30s  # Scraping interval
```
```bash
kubectl apply -f deployment_prometheus.yaml
http://<ipaddress>:8881/api/json
http://<ipaddress>:8881/actuator/prometheus
kubectl get svc -n monitoring prom-stack-kube-prometheus-prometheus
kubectl edit svc -n monitoring prom-stack-kube-prometheus-prometheus
change it to LoadBalancer.
```
![image](https://github.com/user-attachments/assets/81b314a6-f529-46fb-aebd-a858d43cbca6)

scaledobject.yaml
```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: springboot-keda-scaler
  namespace: default
spec:
  scaleTargetRef:
    name: springboot-app
  minReplicaCount: 1
  maxReplicaCount: 5
  pollingInterval: 30    # Poll every 30s
  cooldownPeriod: 60     # Wait 60s before scaling down
  triggers:
    - type: prometheus
      metadata:
        serverAddress: http://prom-stack-kube-prometheus-prometheus.monitoring.svc.cluster.local:9090
        metricName: api_json_requests_count_total
        query: |
          sum(rate(api_json_requests_count_total{application="SpringbootMicroservice"}[1m]))
        threshold: "1"
```
```bash
kubectl apply -f keda-scaler.yaml
kubectl get hpa
```
Step 6: Generate Load with k6
### 🧰 Step 1: Install k6 (if not already)
#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install -y gnupg software-properties-common
curl -s https://dl.k6.io/key.gpg | sudo apt-key add -
echo "deb https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt update
sudo apt install k6
```
### script.js
```bash
import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  vus: 10,           // 10 virtual users
  duration: '5m',    // Run for 5 minutes
};

export default function () {
  http.get('http://20.253.196.6:8881/api/json');
  sleep(1);  // Wait 1 second between requests
}
```
### Run the Load Test
k6 run script.js

```bash
kubectl get hpa
kubectl get pods -l app=springboot-app -o wide
kubectl get pods -w
kubectl logs -n keda -l app=keda-operator -f
kubectl get hpa -w

```
