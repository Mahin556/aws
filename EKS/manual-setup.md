* https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/

• The overall flow followed was:
    * Review VPC setup
    * Create IAM role for EKS cluster
    * Create IAM role for worker nodes
    * Create EKS cluster
    * Create node group (worker nodes)
    * Assign IAM user access to the cluster
    * Connect to the cluster using kubectl
    * Deploy and verify an application

• First step was **IAM role creation**, because EKS needs permissions to work
    * Two IAM roles are required
    * One role is for the **EKS control plane (cluster role)**
    * Second role is for **worker nodes (node group role)**

• Cluster IAM role creation:
    * IAM → Roles → Create role
    * Trusted entity: AWS service
    * Use case: EKS → EKS Cluster
    * Policy automatically attached: `AmazonEKSClusterPolicy`
    * Role name example: `eks-cluster-role`
    * This role allows AWS to manage Kubernetes control plane

• Node group IAM role creation:
    * IAM → Roles → Create role
    * Trusted entity: EC2 (because worker nodes are EC2 instances)
    * Required policies:
        * `AmazonEKSWorkerNodePolicy`
        * `AmazonEKS_CNI_Policy`
        * `AmazonEC2ContainerRegistryReadOnly`
    * Role name example: `eks-nodegroup-role`
    * This role allows worker nodes to:
        * Join the cluster
        * Pull images from ECR
        * Use networking (CNI plugin)

• VPC review:
    * Custom VPC used with CIDR like `10.0.0.0/16`
    * Two private subnets
    * One public subnet
    * EKS worker nodes placed in **private subnets**
    * NAT Gateway configured so private instances can access the internet
    * Internet Gateway only attached to public subnet
    * No inbound internet traffic directly reaches private instances

• EKS cluster creation via console:
    * AWS Console → EKS → Add cluster → Create
    * Cluster name example: `demo-cluster`
    * Kubernetes version selected (default was 1.28)
    * Cluster IAM role selected (created earlier)
    * Authentication mode: EKS API + ConfigMap
    * VPC selected
    * Only **private subnets** selected
    * Default security group selected
    * Logging optional (can be enabled)
    * Core add-ons selected:
        * CoreDNS
        * kube-proxy
        * Amazon VPC CNI
        * EKS Pod Identity Agent
    * Latest versions selected for add-ons
    * Cluster creation takes around 10–15 minutes

• Node group (worker nodes) creation:
    * EKS → Cluster → Compute → Add node group
    * Node group name provided
    * Node IAM role selected (created earlier)
    * Capacity type: On-Demand
    * Instance type: `t3.medium`
    * Desired nodes: 2
    * Private subnets selected
    * Node group creation takes 2–3 minutes

• IAM user access to EKS cluster:
    * Existing IAM user: `demo-user`
    * EKS → Cluster → Access → Create access entry
    * Principal: IAM user `demo-user`
    * Access type: Standard
    * Policy attached:
        * Cluster Administrator
    * This allows the IAM user to run kubectl commands

• Connecting to EKS from EC2 instance:
    * EC2 instance used has **only private IP**
    * Connected using bastion or internal access method
    * AWS CLI and kubectl already installed on the instance

• Update kubeconfig:
    * Command used:
        ```
        aws eks update-kubeconfig --name demo-cluster --region us-east-1
        ```
    * This updates kubeconfig so kubectl can talk to EKS

• Verifying cluster:
    * `kubectl get pods` → no pods in default namespace
    * `kubectl get pods -n kube-system` → all system pods running
    * Confirms cluster and node group are healthy

• Deploying a test application:
    * Created an nginx deployment:
        ```
        kubectl create deployment nginx --image=nginx
        ```
    * Verified pods:
        ```
        kubectl get pods
        ```
    * Checked logs:
        ```
        kubectl logs <pod-name>
        ```
    * nginx pod running successfully

