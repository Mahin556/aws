### References:-
- [Day-10 | AWS CLI Deep Dive | Concept + Installation + Demo](https://youtu.be/TiDSwf8gydk?si=HBvyBMFyuJYljsuk)
- [Day 5- AWS CLI Tutorial with Commands | Learn AWS CLI commands with Notes](https://youtu.be/mPqzf1oIXu8?si=IicZlAS_hjrnOGRe)
- [AWS Tutorials - 55 - How to use AWS CLI - AWS Configure - How to Create AWS Instance Using CLI - AWS](https://youtu.be/nooY45x12Qw?si=n70cCV0e5cqmBt8v)
- [AWS Tutorials - 56 - AWS CLI Handle Multiple AWS Accounts - How to use AWS CLI In Linux -AWS(Hindi)](https://youtu.be/tcQFWVcWBTY?si=vcYG0EC2DQRsOUnD)
- [Master AWS CLI | Installation, Configuration & Hands-On Demo](https://youtu.be/mxpw-yfZnCQ?si=p9a-YP_N0i-PPHJj)
- [AWS CLI for Beginners: The Complete Guide](https://youtu.be/PWAnY-w1SGQ?si=5seZ_Dgzvh03JPtd)

### Imp links
- https://docs.aws.amazon.com/cli/latest/

* 2 ways to interact with aws
    * console(GUI)
    * programmatically(api)
* Command line interface
    * AWS CLI(python programm, prarameter, json, token, keys, http call)
    * It is a python program, when you run a `aws` command it translate the command into api call and send it to API. 
    * Provide abstraction over complicated API call.
    * EX: `aws s3 ls`
* IAC
    * Terraform
    * CloudFormation
    * CDK

* SDK
* Providion a resources on the aws(cloud)
* Scripting
* Automation friendly
* Can create a 10 VPC instantly
* `aws cli` allow to interact with Aws APIs.
* API ---> Application prof
* `aws` cli required python installed
* Requiredment(aws-cli, IAM user, Access-keys)
* Don't use it for complex login use it for quick refrences.
* What problem it solve
  * Create multiple VPC
  * Download data from S3
  * any operation that need some kind of loop

* When you run aws s3 ls, the CLI sends this HTTPS GET request:
```bash
GET / HTTP/1.1
Host: s3.amazonaws.com
Authorization: AWS4-HMAC-SHA256 Credential=<AccessKey>/...
x-amz-date: 20251030T082000Z
User-Agent: aws-cli/2.x.x Python/3.x
```
* API Response Example(S3 responds with an XML payload that lists your buckets)
```xml
<ListAllMyBucketsResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
  <Owner>
    <ID>1234567890abcdef</ID>
    <DisplayName>mahin</DisplayName>
  </Owner>
  <Buckets>
    <Bucket>
      <Name>my-first-bucket</Name>
      <CreationDate>2025-01-15T10:23:00.000Z</CreationDate>
    </Bucket>
    <Bucket>
      <Name>backup-data</Name>
      <CreationDate>2025-02-10T14:52:00.000Z</CreationDate>
    </Bucket>
  </Buckets>
</ListAllMyBucketsResult>
```
* API Endpoint
    * Depending on your region and endpoint configuration:
        ```bash
        https://s3.amazonaws.com/
        ```
    * or for specific region:
        ```bash
        https://s3.<region>.amazonaws.com/
        ```

```bash
aws --version
aws configure

AWS Access Key ID [None]: AKIA************
AWS Secret Access Key [None]: ***************
Default region name [None]: ap-south-1
Default output format [None]: json

aws s3 ls
aws help
aws s3 help
aws ec2 describe-instances --region ap-south-1
aws ec2 run-instances --region ap-south-1 --image-id=<id> --instance-type=<type>
```
```bash
echo $PATH
/usr/local/bin/aws --versioon
```
```bash
aws configure --profile account1
aws configure --profile account2
aws s3 ls --profile dev
aws ec2 describe-instances --region ap-south-1 --profile=account1 #To use a different profile temporarily

export AWS_PROFILE="your_profile_name" #Set default profile

#~/.aws/credentials → contains access keys
#~/.aws/config → contains region, output format, etc.
#[default] mention default profile under it

# ~/.aws/credentials
[default]
aws_access_key_id = AKIA*************
aws_secret_access_key = ***************

# ~/.aws/config
[default]
region = ap-south-1
output = json



aws configure list #list active profiles

echo $AWS_PROFILE

aws ec2 describe-instances --output table,json,text,yaml
aws ec2 describe-instances --output table > demo.txt

```
* storing a `aws_access_key_id` and `aws_secret_access_key` on EC2 instance is not secure so use role here.

```bash
aws ec2 describe-instances #Retrieves details about one or more EC2 instances.
$ aws ec2 describe-instances --instance-ids i-1234567890abcdef0

aws ec2 start-instances --instance-ids <instance-id> #Starts a stopped EC2 instance.
$ aws ec2 start-instances --instance-ids i-1234567890abcdef0

aws ec2 stop-instances --instance-ids <instance-id> #Stops a running EC2 instance.
$ aws ec2 stop-instances --instance-ids i-1234567890abcdef0

aws ec2 terminate-instances --instance-ids <instance-id> #Terminates an EC2 instance.
$ aws ec2 terminate-instances --instance-ids i-1234567890abcdef0

aws ec2 create-key-pair --key-name <key-name> #Creates a new SSH key pair.
$ aws ec2 create-key-pair --key-name MyKeyPair --query 'KeyMaterial' --output text > MyKeyPair.pem

aws ec2 create-security-group --group-name <group-name> --description "<description>" #Creates a new security group.
$ aws ec2 create-security-group --group-name MySecurityGroup --description "My security group"

aws ec2 authorize-security-group-ingress --group-name <group-name> --protocol <tcp|udp|icmp> --port <port> --cidr <ip-range> #Adds a rule to a security group to allow inbound traffic.
$ aws ec2 authorize-security-group-ingress --group-name MySecurityGroup --protocol tcp --port 22 --cidr 0.0.0.0/0

aws s3 mb s3://<bucket-name> #Creates a new S3 bucket.
$ aws s3 mb s3://my-bucket-name

aws s3 cp <local-file> s3://<bucket-name>/ #Uploads a file to a specified S3 bucket.
$ aws s3 cp myfile.txt s3://my-bucket-name/

aws s3 cp s3://<bucket-name>/<file-name> <local-destination> #Downloads a file from S3 to your local machine.
$ aws s3 cp s3://my-bucket-name/myfile.txt ./myfile.txt

aws s3 sync <local-dir> s3://<bucket-name>/ #Syncs a local directory to an S3 bucket.
$ aws s3 sync ./my-folder s3://my-bucket-name/

aws s3 rb s3://<bucket-name> --force #Deletes an S3 bucket and its contents.
$ aws s3 rb s3://my-bucket-name --force

aws iam list-users #Lists all IAM users in your account.
$ aws iam list-users

aws iam create-user --user-name <user-name> #Creates a new IAM user.
$ aws iam create-user --user-name DevUser

aws iam attach-user-policy --user-name <user-name> --policy-arn <policy-arn> #Attaches a managed policy to an IAM user.
$ aws iam attach-user-policy --user-name DevUser --policy-arn arn:aws:iam::aws:policy/AdministratorAccess

aws iam create-role --role-name <role-name> --assume-role-policy-document file://<policy-document> #Creates a new IAM role with a specified trust policy.
$ aws iam create-role --role-name MyRole --assume-role-policy-document file://trust-policy.json

aws iam list-roles #Lists all IAM roles in your account.
$ aws iam list-roles

aws lambda list-functions #Lists all Lambda functions in your account.
$ aws lambda list-functions

aws lambda invoke --function-name <function-name> <output-file> #Invokes a Lambda function and outputs the response to a file.
$ aws lambda invoke --function-name MyFunction result.txt

aws lambda update-function-code --function-name <function-name> --zip-file fileb://<zip-file> #Updates the code of an existing Lambda function.
$ aws lambda update-function-code --function-name MyFunction --zip-file fileb://my-function.zip

aws cloudformation create-stack --stack-name <stack-name> --template-body file://<template-file> #Creates a new CloudFormation stack based on a template file.
$ aws cloudformation create-stack --stack-name MyStack --template-body file://template.json

aws cloudformation update-stack --stack-name <stack-name> --template-body file://<template-file> #Updates an existing CloudFormation stack with a new template.
$ aws cloudformation update-stack --stack-name MyStack --template-body file://template.json

aws cloudformation delete-stack --stack-name <stack-name> #Deletes an existing CloudFormation stack.
$ aws cloudformation delete-stack --stack-name MyStack

aws eks list-clusters #Lists all EKS clusters in your account.
$ aws eks list-clusters

aws eks describe-cluster --name <cluster-name> #- Provides details about an EKS cluster.
$ aws eks describe-cluster --name MyCluster

aws eks create-cluster --name <cluster-name> --role-arn <role-arn> --resources-vpc-config <vpc-config> #Creates a new EKS cluster with the specified configuration.
$ aws eks create-cluster --name MyCluster --role-arn arn:aws:iam::123456789012:role/EKSRole --resources-vpc-config subnetIds=subnet-abc123,subnet-def456,securityGroupIds=sg-123456

aws rds describe-db-instances #Lists all RDS DB instances.
$ aws rds describe-db-instances

aws rds create-db-instance --db-instance-identifier <identifier> --db-instance-class <instance-class> --engine <engine> --allocated-storage <storage-size> --master-username <username> --master-user-password <password> #Creates a new RDS DB instance.
$ aws rds create-db-instance --db-instance-identifier MyDBInstance --db-instance-class db.t2.micro --engine mysql --allocated-storage 20 --master-username admin --master-user-password secretpassword

aws rds delete-db-instance --db-instance-identifier <identifier> --skip-final-snapshot #Deletes an RDS DB instance.
$ aws rds delete-db-instance --db-instance-identifier MyDBInstance --skip-final-snapshot

aws route53 list-hosted-zones #Lists all Route 53 hosted zones in your account.
$ aws route53 list-hosted-zones

aws route53 create-hosted-zone --name <domain-name> --caller-reference <unique-string> #Creates a new Route 53 hosted zone for a domain.
$ aws route53 create-hosted-zone --name example.com --caller-reference "unique-string-123"

aws cloudwatch describe-alarms #Lists all CloudWatch alarms.
$ aws cloudwatch describe-alarms

aws cloudwatch put-metric-alarm --alarm-name <alarm-name> --metric-name <metric-name> --namespace <namespace> --statistic <statistic> --period <seconds> --threshold <value> --comparison-operator <operator> --evaluation-periods <count> #Creates a new CloudWatch alarm based on a specified metric.
$ aws cloudwatch put-metric-alarm --alarm-name HighCPUAlarm --metric-name CPUUtilization --namespace AWS/EC2 --statistic Average --period 300 --threshold 80 --comparison-operator GreaterThanThreshold --evaluation-periods 1