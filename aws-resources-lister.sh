#!/bin/bash

#################################################################################
# This script lists all AWS resources in the current account and region.
# Auther: Mahin Raza
# Version: 0.0.1

# Following are the AWS services that are supported by this script
# 1. EC2
# 2. S3
# 3. RDS
# 4. DynamoDB
# 5. Lambda
# 6. EBS
# 7. ELB
# 8. CloudFront
# 9. CloudWatch
# 10. SNS
# 11. SQS
# 12. Route53
# 13. VPC
# 14. CloudFormation
# 15. IAM

# Usage: ./aws-resource-lister.sh <region> <service-name>
# Example: ./aws-resource-lister.sh ap-south-1 EC2
##################################################################################

# Validating if the required no of argument passed or not
if [[ $# -ne 2 ]];then
    echo "Usage: $0 <region> <service-name>"
    echo "Example: $0 ap-south-1 EC2"
    exit 1
fi

aws_region=$1
aws_service=$2

# Verify AWS CLI Installed
if ! command -v aws &> /dev/null;then
    echo "AWS CLI is not installed. Please Install AWS CLI First and try again"
    exit 1
fi

# Check is AWS CLI is configured or not
if [[ ! -d ~/.aws ]];then
    echo "AWS CLI is not configured. Please configure it and try again"
    exit 1
fi

# Execute the CLI command based on the service name
case $aws_service in
    EC2)
        echo "Listing EC2 instances in region $aws_region..."
        aws ec2 describe-instances --region $aws_region --output table 
        ;;
    S3)
        echo "Listing S3 buckets in region $aws_region..."
        aws s3 ls --region $aws_region
        ;;
    RDS)
        echo "Listing RDS instances in region $aws_region..."
        aws rds describe-db-instances --region $aws_region --output table
        ;;
    DynamoDB)
        echo "Listing DynamoDB tables in region $aws_region..."
        aws dynamodb list-tables --region $aws_region --output table
        ;;
    Lambda)
        echo "Listing Lambda functions in region $aws_region..."
        aws lambda list-functions --region $aws_region --output table
        ;;
    EBS)
        echo "Listing EBS volumes in region $aws_region..."
        aws ec2 describe-volumes --region $aws_region --output table
        ;;
    ELB)
        echo "Listing ELB load balancers in region $aws_region..."
        aws elbv2 describe-load-balancers --region $aws_region --output table
        ;;
    CloudFront)
        echo "Listing CloudFront distributions in region $aws_region..."
        aws cloudfront list-distributions --region $aws_region --output table
        ;;
    CloudWatch)
        echo "Listing CloudWatch metrics in region $aws_region..."
        aws cloudwatch list-metrics --region $aws_region --output table
        ;;
    SNS)
        echo "Listing SNS topics in region $aws_region..."
        aws sns list-topics --region $aws_region --output table
        ;;
    SQS)
        echo "Listing SQS queues in region $aws_region..."
        aws sqs list-queues --region $aws_region --output table
        ;;
    Route53)
        echo "Listing Route53 hosted zones in region $aws_region..."
        aws route53 list-hosted-zones --region $aws_region --output table
        ;;
    VPC)
        echo "Listing VPCs in region $aws_region..."
        aws ec2 describe-vpcs --region $aws_region --output table
        ;;
    CloudFormation)
        echo "Listing CloudFormation stacks in region $aws_region..."
        aws cloudformation list-stacks --region $aws_region --output table
        ;;
    IAM)
        echo "Listing IAM users in region $aws_region..."
        aws iam list-users --region $aws_region --output table
        ;;
    *)
        echo "Invalid service name. Please provide a valid AWS service name."
        exit 1
esac