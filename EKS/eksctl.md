* https://github.com/eksctl-io/eksctl
* https://docs.aws.amazon.com/eks/latest/eksctl/installation.html

* https://devopscube.com/create-aws-eks-cluster-eksctl/
* https://subbaramireddyk.medium.com/amazon-eks-cluster-setup-using-eksctl-c582915a4e2f

* https://docs.aws.amazon.com/eks/latest/userguide/automode-get-started-eksctl.html
* https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html
* https://docs.aws.amazon.com/eks/latest/eksctl/what-is-eksctl.html

eksctl is a CLI tool that creates an EKS cluster, VPC, IAM roles, and managed node groups automatically using a single command.

```bash
# Prerequisites
aws --version
kubectl version --client
eksctl version
aws sts get-caller-identity

#Configure AWS credentials (one-time)
aws configure
# Provide:
# Access Key
# Secret Key
# Region (e.g. ap-south-1)
# Output format (json)

# Step 2: Create EKS cluster with managed node group (single command)
eksctl create cluster \
  --name demo-eks \
  --region ap-south-1 \
  --version 1.28 \
  --nodegroup-name demo-ng \
  --node-type t3.medium \
  --nodes 2 \
  --nodes-min 1 \
  --nodes-max 3 \
  --managed
  
# What eksctl does automatically
# - Creates VPC
# - Creates public & private subnets
# - Creates IAM roles
# - Creates control plane
# - Creates managed node group
# - Updates kubeconfig


# Step 3: Verify cluster and nodes
kubectl config get-contexts
kubectl get nodes
kubectl get pods -A


# Step 4: Check eksctl-managed resources
eksctl get cluster
eksctl get nodegroup --cluster demo-eks


# Step 5: (Optional) Create cluster using Fargate
eksctl create cluster \
  --name demo-eks-fargate \
  --region ap-south-1 \
  --fargate


# Step 6: (Optional) Deploy test workload
kubectl create deployment nginx --image=nginx
kubectl get pods


# Step 7: Delete cluster (cleanup)
eksctl delete cluster \
  --name demo-eks \
  --region ap-south-1
```