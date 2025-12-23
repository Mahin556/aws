```
# Check which AWS identity you are using
aws sts get-caller-identity


# Check kubeconfig exists
ls -l ~/.kube/config


# Update kubeconfig for EKS (most important)
aws eks update-kubeconfig \
  --region <region> \
  --name <cluster-name>


# Example
aws eks update-kubeconfig \
  --region ap-south-1 \
  --name demo-cluster


# Verify kubectl context
kubectl config get-contexts
kubectl config current-context


# (Old method) Check aws-auth ConfigMap
kubectl get configmap aws-auth -n kube-system


# EC2-specific fix (kubeconfig created as root)
sudo cp -r /root/.kube /home/ec2-user/
sudo chown -R ec2-user:ec2-user /home/ec2-user/.kube


# Quick verification after fix
kubectl get nodes
kubectl get pods -A



```