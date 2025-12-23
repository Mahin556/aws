# ⭐ **What is an Instance Profile?**

➡️ **An Instance Profile is a “container” that holds exactly ONE IAM Role**, and it is used to **attach that role to an EC2 instance**.

AWS EC2 **cannot use an IAM Role directly**.
It can only use an **Instance Profile**, which internally contains that IAM Role.

Think of it like this:

```
IAM Role  →  placed inside  →  Instance Profile  →  attached to EC2
```

---

# ⭐ **Why Do We Need an Instance Profile?**

Because **EC2 does not understand IAM roles**, but it DOES understand instance profiles.

The instance profile gives EC2:

✔ Temporary AWS credentials
✔ Automatically rotated credentials
✔ Permissions to call AWS APIs
✔ Secure access without storing keys

Example use cases:

* EC2 needs to access S3
* EC2 needs to send logs to CloudWatch
* EC2 needs to be managed by SSM
* EC2 needs to interact with DynamoDB
* EC2 needs Secrets Manager access

Without an instance profile, your EC2 **cannot** talk to AWS securely.

---

# ⭐ **Easy Example (Real-Life Analogy)**

* **IAM Role** = Job role (ex: “S3AccessRole”)
* **Instance Profile** = ID card holder
* **EC2 Instance** = Employee

An employee (EC2) cannot receive a job role (IAM Role) unless the role is put inside an ID card holder (Instance Profile).

---

# ⭐ **Terraform Example: Create IAM Role + Instance Profile**

### 1️⃣ Create an IAM Role

This role grants EC2 the permissions:

```hcl
resource "aws_iam_role" "ssm_role" {
  name = "ec2-ssm-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
      Action = "sts:AssumeRole"
    }]
  })
}
```

### 2️⃣ Attach Permissions (SSM, Logs, etc.)

```hcl
resource "aws_iam_role_policy_attachment" "ssm" {
  role       = aws_iam_role.ssm_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}
```

### 3️⃣ Create the Instance Profile

This wraps the IAM role:

```hcl
resource "aws_iam_instance_profile" "ssm_profile" {
  name = "ssm-instance-profile"
  role = aws_iam_role.ssm_role.name
}
```

### 4️⃣ Attach Instance Profile to EC2

```hcl
resource "aws_instance" "example" {
  ami                    = "ami-xyz"
  instance_type          = "t3.micro"
  iam_instance_profile   = aws_iam_instance_profile.ssm_profile.name
}
```

Now the EC2 instance has the permissions defined in the IAM role.

---

# ⭐ **What Happens Inside EC2?**

Once EC2 has an instance profile:

* It receives **temporary AWS credentials** via **Instance Metadata Service (IMDSv2)**
* Credentials are automatically rotated by AWS
* They are stored in the EC2 metadata endpoint:

```
http://169.254.169.254/latest/meta-data/iam/security-credentials/<role-name>
```

Applications inside EC2 can now call AWS APIs like:

* `aws s3 ls`
* `aws logs put-log-events`
* `aws ec2 describe-instances`

without storing any passwords or keys.

---

# ⭐ **Why It’s More Secure Than AWS Keys**

| Method                      | Secure? | Reason                                               |
| --------------------------- | ------- | ---------------------------------------------------- |
| Storing AWS access keys     | ❌       | Keys can be leaked, stolen, or forgotten             |
| IAM Role + Instance Profile | ✔✔✔     | Temporary credentials, auto-rotated, least privilege |

Instance profiles **eliminate the need for hardcoded AWS keys**.

---

# ⭐ **Common Interview Question**

❓ *What is the difference between an IAM Role and an Instance Profile?*

✔ IAM Role = permission set
✔ Instance Profile = wrapper that allows EC2 to use that role

---

