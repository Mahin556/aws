What is Amazon EKS
• EKS stands for **Elastic Kubernetes Service**
• It is AWS’s **managed Kubernetes service**
• AWS manages the **control plane**, you manage the **worker nodes**

Control plane includes:
• Kubernetes API Server
• Scheduler
• Controller Manager
• etcd

AWS responsibilities:
• Provision control plane
• Maintain and patch master nodes
• High availability of control plane
• Scaling and backups

Your responsibility:
• Worker nodes
• Application workloads

---

Why use EKS (or any managed Kubernetes service)
Problems with self-managed Kubernetes:
• Very complex to install
• Hard to operate and scale
• Requires deep Kubernetes expertise
• Security and patching is manual

Benefits of EKS:
• No control plane management
• AWS handles security best practices
• Highly available by default
• Easy integration with AWS services:

* IAM
* Load Balancers
* S3
* Secrets Manager
  • Production-ready Kubernetes

---

EKS Architecture (High-level)

• Control Plane → Managed by AWS
• Worker Nodes → Managed by you (or partially by AWS)
• Kubernetes API → Exposed securely
• Applications run only on worker nodes

---

Worker Node Options in EKS

There are **3 ways** to run worker nodes.

---

1. Self-managed worker nodes

What it means:
• You create EC2 instances manually
• You install Kubernetes components yourself

You must manage:
• kubelet
• kube-proxy
• container runtime
• OS updates
• Security patches
• Node registration to cluster

Pros:
• Full control

Cons:
• High operational overhead
• Not recommended for beginners

---

2. Managed Node Groups (Most common)

What AWS does:
• Creates EC2 instances for you
• Uses EKS-optimized AMI
• Manages lifecycle of nodes

What you control:
• Instance type
• Min / max / desired capacity --> asg  ->auto scale based on the load
• Scaling

Key points:
• Nodes are part of Auto Scaling Group
• Easy upgrades and replacements
• Balanced control + convenience

Recommended for:
• Most production workloads

---

3. AWS Fargate (Serverless Kubernetes)

What it means:
• No EC2 instances to manage
• Pods run on-demand
• AWS creates nodes automatically

Advantages:
• No server management
• Pay only for what you use
• Automatic scaling
• Optimal instance selection

Disadvantages:
• Less control
• Not suitable for all workloads

Best for:
• Microservices
• Short-lived workloads
• Teams that don’t want infra management

---

What is eksctl

• eksctl is a **command-line tool**
• Created by **Weaveworks**
• Simplifies EKS cluster creation
• Automates:

* VPC
* Subnets
* Node groups
* IAM roles
* kubeconfig setup

Without eksctl:
• Manual console setup
• Very long and error-prone

With eksctl:
• One command = full cluster

---

Ways to create an EKS cluster

1. AWS Console
   • Manual
   • Time-consuming
   • Not scalable

2. eksctl
   • Fast
   • Simple
   • Recommended for learning and POCs

3. Infrastructure as Code (Terraform / Pulumi)
   • Best for production
   • Version controlled
   • Fully automated

This tutorial focuses on **eksctl**

---

Install eksctl

Follow official AWS documentation based on OS:
• Linux
• macOS
• Windows

Verify installation:

```
eksctl version
```

If version prints → installation successful

---

AWS Authentication Setup (Required)

eksctl uses AWS APIs
You must configure AWS credentials

Steps:
• Create IAM user
• Generate Access Key and Secret Key

Two ways to configure:

Option 1: Using AWS CLI

```
aws configure
```

Provide:
• Access key
• Secret key
• Region
• Output format

Option 2: Manually create files

`~/.aws/credentials`

```
[default]
aws_access_key_id=XXXX
aws_secret_access_key=YYYY
```

`~/.aws/config`

```
[default]
region=us-east-1
output=json
```

After this:
• eksctl can talk to AWS

---

Explore eksctl commands

View help:

```
eksctl --help
```

Main commands:
• eksctl create
• eksctl delete

Cluster-specific help:

```
eksctl create cluster --help
```

---

Important eksctl flags

• --name → Cluster name
• --region → AWS region
• --zones → Availability Zones (minimum 2)
• --node-type → EC2 instance type
• --nodes → Number of worker nodes
• --nodegroup-name → Node group name
• --fargate → Use Fargate instead of EC2

---

Create an EKS cluster using eksctl

Example command:

```
eksctl create cluster \
  --name cluster-one \
  --nodegroup-name nodegroup-one \
  --region us-east-1 \
  --node-type t2.micro \
  --nodes 2
```

What happens internally:
• VPC is created
• Public and private subnets created
• Internet Gateway attached
• Routing tables configured
• Control plane created
• Node group created
• EC2 instances launched
• kubeconfig updated automatically

Cluster creation takes several minutes

---

Verify resources in AWS Console

VPC:
• New VPC prefixed with `eksctl`
• 2 public subnets
• 2 private subnets

EKS:
• Cluster status = Active
• Kubernetes version visible

Compute:
• Node group created
• Desired nodes = 2

EC2:
• Two EC2 instances running
• Instance type matches command

---

kubectl configuration (Automatic)

eksctl automatically updates kubeconfig

Verify:

```
kubectl config view
```

Check nodes:

```
kubectl get nodes
```

If nodes appear:
• Cluster is ready
• kubectl is connected successfully

---

Delete EKS cluster (Cleanup)

Command:

```
eksctl delete cluster --name cluster-one
```

What gets deleted:
• EKS cluster
• Node groups
• EC2 instances
• VPC
• Subnets
• Load balancers
• IAM resources created by eksctl

Always delete clusters to avoid AWS charges

---

Key interview points

• EKS is managed Kubernetes
• AWS manages control plane
• Worker nodes can be:

* Self-managed
* Managed node groups
* Fargate
  • eksctl simplifies cluster creation
  • One command can provision full infrastructure
  • kubeconfig is auto-configured
  • eksctl is ideal for fast setups
  • Terraform is preferred for production

---

If you want next:
• eksctl vs Terraform comparison
• EKS architecture diagram
• eksctl YAML-based cluster creation
• Real-world EKS interview questions
• Common EKS mistakes and fixes

Just tell me.
