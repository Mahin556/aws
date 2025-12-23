### References:-
- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html

---

# 🧠 **1️⃣ What is IMDS (Instance Metadata Service)?**

* The **Instance Metadata Service (IMDS)** is a special local web service that **runs inside every EC2 instance**.
* It’s available only to applications running **inside the instance**.
* Purpose → Provide metadata about the instance and **temporary AWS credentials** for the IAM role attached to that EC2.

---

# 🌐 **IMDS Endpoint**

```
http://169.254.169.254/
```

✅ This is a **non-routable IP** (link-local), accessible only within the EC2 instance.

---

# 📦 **2️⃣ Why AWS Introduced IMDSv2**

Earlier, AWS had **IMDSv1**, where:

* Any process inside EC2 could access metadata using simple HTTP GET requests.
* Example:

  ```bash
  curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
  ```
* This made EC2 instances vulnerable to **SSRF (Server-Side Request Forgery)** attacks.

An attacker could trick an app into fetching metadata → stealing IAM credentials.

---

# 🔒 **IMDSv2 — The Secure Version**

AWS released **IMDSv2** to mitigate SSRF and similar attacks.

It introduces:
✅ **Session-based authentication**
✅ **PUT requests with session tokens**
✅ **Time-limited tokens (TTL)**

---

# ⚙️ **3️⃣ How IMDSv2 Works (Step-by-Step)**

---

### 🧩 Step 1: Get a Session Token

```bash
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
```

* Method: `PUT`
* Header: `X-aws-ec2-metadata-token-ttl-seconds` sets how long (in seconds) the token is valid.
* Example above: 21,600 seconds = 6 hours

✅ Response: A session token string

---

### 🧩 Step 2: Use That Token to Get Metadata Securely

```bash
curl -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/iam/security-credentials/
```

✅ Now you get the IAM role name, safely.
Example output:

```
MyEC2Role
```

---

### 🧩 Step 3: Retrieve Temporary Credentials

```bash
curl -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/iam/security-credentials/MyEC2Role
```

✅ Output:

```json
{
  "Code": "Success",
  "LastUpdated": "2025-11-12T06:00:00Z",
  "Type": "AWS-HMAC",
  "AccessKeyId": "ASIAxxxxxxxxxxxx",
  "SecretAccessKey": "xxxxxxxxxxxxxxxxxxxxx",
  "Token": "IQoJb3JpZ2luX2VjE...",
  "Expiration": "2025-11-12T12:00:00Z"
}
```

---

# 🧩 Step 4: AWS CLI / SDK Automatically Handles IMDSv2

✅ The AWS CLI and SDKs (Boto3, Java SDK, etc.) automatically use IMDSv2 under the hood.
You don’t need to add tokens manually.

They:

1. Request token
2. Cache it
3. Refresh when expired

---

# ✅ **4️⃣ Advantages of IMDSv2**

| Advantage                              | Description                                                  |
| -------------------------------------- | ------------------------------------------------------------ |
| 🔐 **Protects from SSRF attacks**      | External attacker can’t trick instance to reveal credentials |
| 🧾 **Uses session tokens**             | Temporary access with TTL                                    |
| 🕒 **Token expiration control**        | You can define how long it remains valid                     |
| 🚫 **Blocks unauthenticated requests** | IMDSv1-style (GET) requests fail when IMDSv2 enforced        |
| 🧠 **Automatic support in SDKs**       | No code changes needed in modern SDKs                        |

---

# ⚠️ **5️⃣ IMDSv1 vs IMDSv2 Comparison**

| Feature            | IMDSv1 | IMDSv2             |
| ------------------ | ------ | ------------------ |
| Authentication     | None   | Token-based        |
| Request Type       | GET    | PUT + GET          |
| Vulnerable to SSRF | ✅ Yes  | ❌ No               |
| Token Expiry       | ❌ None | ✅ TTL (default 6h) |
| SDK Support        | Legacy | Default since 2020 |
| Security           | Low    | High (Recommended) |

---

# ⚙️ **6️⃣ How to Enforce IMDSv2 on an Instance**

You can enforce IMDSv2 so that **IMDSv1 requests are rejected**.

### ✅ Option 1: Using AWS CLI

```bash
aws ec2 modify-instance-metadata-options \
  --instance-id i-0abcd1234efgh5678 \
  --http-tokens required \
  --http-endpoint enabled
```

✅ This enforces:

* `http-tokens = required` → IMDSv2 only
* `http-endpoint = enabled` → metadata service remains accessible

---

### ✅ Option 2: When Launching a New Instance

Under **Advanced Details → Metadata Options**:

* Metadata accessible? → *Enabled*
* Require IMDSv2? → *Yes*

---

# 🔍 **7️⃣ Verify Current IMDS Setting**

```bash
aws ec2 describe-instances \
  --instance-id i-0abcd1234efgh5678 \
  --query "Reservations[*].Instances[*].MetadataOptions"
```

Example output:

```json
[
  {
    "State": "applied",
    "HttpTokens": "required",
    "HttpEndpoint": "enabled",
    "HttpPutResponseHopLimit": 1
  }
]
```

✅ `HttpTokens: required` → means IMDSv2 enforced.

---

# 🔒 **8️⃣ Security Best Practices**

✅ Always **enable IMDSv2** (AWS recommends it).
✅ Disable IMDSv1 (`HttpTokens=required`).
✅ Set `HttpPutResponseHopLimit=1` to prevent container-level access (e.g., in ECS or K8s).
✅ Never expose `169.254.169.254` to external network routes.
✅ Audit instance settings using AWS Config or Security Hub.

---

# 🧾 **9️⃣ How AWS CLI / SDK Uses It Internally**

When the AWS CLI runs on EC2:

1. It first sends a `PUT` request to get a token from IMDSv2.
2. It includes that token in all future metadata requests (e.g., fetching credentials).
3. It caches the token and automatically renews it.
4. All credentials fetched are **temporary** IAM role credentials.

So AWS CLI commands like:

```bash
aws s3 ls
```

→ Work automatically and securely with IMDSv2, no manual configuration required.

---

# ✅ **10️⃣ Summary Table**

| Feature                 | IMDSv1                | IMDSv2                             |
| ----------------------- | --------------------- | ---------------------------------- |
| Access Type             | GET requests          | PUT (get token) → GET (with token) |
| Authentication          | None                  | Token required                     |
| Protection Against SSRF | ❌ No                  | ✅ Yes                              |
| Default in New EC2s     | Optional              | Enabled                            |
| Enforce via             | `HttpTokens=required` | —                                  |
| SDK/CLI Support         | Legacy                | Fully supported                    |

---

# ✅ **In Simple Words**

> IMDSv2 is a secure way for EC2 instances to get metadata and IAM credentials using a **temporary token-based session**, protecting against **credential theft** and **SSRF attacks**.

---

If you want, I can show next:
✅ how to test IMDSv2 token manually inside EC2,
✅ how IMDSv2 interacts with containers (ECS/EKS), or
✅ IAM role credential rotation under IMDSv2.

Would you like that?


---


Excellent question ✅ — this is a **core concept** in AWS security and automation.
Let’s go step-by-step through **how an AWS CLI running inside an EC2 instance automatically gets its credentials from an IAM role** — without you ever typing `aws configure`.

---

# 🧠 **Concept Overview**

When you launch an **EC2 instance with an IAM Role attached**,
that role provides **temporary security credentials** to the instance — via the **Instance Metadata Service (IMDS)**.

The **AWS CLI** automatically retrieves these credentials when you make any AWS API call.

So the flow is:

```
IAM Role → EC2 Instance Metadata → AWS CLI / SDK → AWS API
```

---

# ✅ **1️⃣ IAM Role Attached to EC2**

* You attach an **IAM Role** to your EC2 instance (when launching it or afterward).
* The role has an **IAM Policy** that grants specific permissions.

Example role policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:*"],
      "Resource": "*"
    }
  ]
}
```

---

# ✅ **2️⃣ Temporary Credentials Provided via Instance Metadata Service (IMDS)**

AWS runs a **metadata service** locally on every EC2 instance.

It’s available only inside the instance at this link:

```
http://169.254.169.254/
```

This service provides information about:

* Instance details (ID, region, etc.)
* IAM role credentials

---

# ✅ **3️⃣ CLI Automatically Contacts IMDS**

When you run a command inside EC2:

```bash
aws s3 ls
```

The **AWS CLI** automatically:

1. Checks for credentials in environment variables (`AWS_ACCESS_KEY_ID`, etc.)
2. If none → looks in `~/.aws/credentials`
3. If none → contacts **IMDS (169.254.169.254)** to get **temporary credentials** for the attached IAM role.

You don’t need to do anything.

---

# ✅ **4️⃣ What’s Inside the Metadata (Example)**

You can view them manually:

```bash
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
```

Example output:

```
MyEC2Role
```

Then get credentials for that role:

```bash
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/MyEC2Role
```

Example JSON:

```json
{
  "Code": "Success",
  "LastUpdated": "2025-11-12T06:00:00Z",
  "Type": "AWS-HMAC",
  "AccessKeyId": "ASIAxxxxxxxxxxxx",
  "SecretAccessKey": "xxxxxxxxxxxxxxxxxxxxx",
  "Token": "IQoJb3JpZ2luX2VjE...",
  "Expiration": "2025-11-12T12:00:00Z"
}
```

✅ These are **temporary credentials** valid typically for **6 hours**.

---

# ✅ **5️⃣ AWS CLI Automatically Uses These Credentials**

* AWS CLI includes an internal “credential provider chain.”
* One of the sources is **Instance Metadata Service (IMDS)**.
* So, when running inside EC2, CLI automatically:

  * Retrieves these credentials
  * Uses them to sign requests
  * Refreshes them automatically before expiration

✅ No need to store access keys or run `aws configure`.

---

# ✅ **6️⃣ IMDSv2 (Improved Security)**

AWS now uses **IMDSv2**, which requires a **session token**.

### Fetch manually (for understanding):

```bash
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")

curl -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/iam/security-credentials/
```

✅ This protects metadata from SSRF (Server-Side Request Forgery) attacks.

---

# ✅ **7️⃣ Expiration and Rotation**

* Credentials automatically **rotate** before they expire.
* The AWS CLI or SDK transparently refreshes them.
* You don’t need to manage rotation or re-authentication.

---

# ✅ **8️⃣ Example Flow Summary**

| Step | Component                        | Function                                 |
| ---- | -------------------------------- | ---------------------------------------- |
| 1    | IAM Role                         | Defines what actions EC2 can perform     |
| 2    | Instance Metadata Service (IMDS) | Provides temporary credentials           |
| 3    | AWS CLI / SDK                    | Requests credentials from IMDS           |
| 4    | AWS API                          | Uses signed request to perform operation |
| 5    | AWS                              | Verifies role + token + signature        |

---

# ✅ **9️⃣ Example Real-Life Use**

If your EC2 instance has a role like:

```
EC2_S3_ReadOnlyRole
```

with permission:

```json
{
  "Effect": "Allow",
  "Action": "s3:GetObject",
  "Resource": "*"
}
```

Then from inside that EC2:

```bash
aws s3 ls s3://mybucket/
```

✅ Works without any access keys configured — CLI fetches credentials from IMDS automatically.

---

# ✅ **10️⃣ Security Best Practices**

* Never use long-term access keys inside EC2.
* Always use IAM Roles for EC2 for automatic short-lived credentials.
* Use IMDSv2 (default now).
* Restrict role permissions (least privilege).
* Monitor CloudTrail for `GetSessionToken` or unexpected role assumption.
* Rotate roles instead of static keys.

---

# ✅ **In Simple Words**

> The AWS CLI on EC2 gets its credentials automatically from the **Instance Metadata Service (IMDS)** using the **IAM Role** attached to that instance.
> No manual key configuration needed — AWS handles it automatically and securely.

---

If you want, I can also show:
✅ how to test IAM role permissions from EC2,
✅ how to verify IMDSv2 is enabled, or
✅ how Lambda and ECS use similar role-based credential systems.

Would you like that?

---

The AWS Instance Metadata Service (IMDS) endpoint for retrieving IAM role credentials from within an EC2 instance is a local, non-routable IP address. 
IMDSv1 and IMDSv2 Endpoints: 

• IPv4: 169.254.169.254 
• IPv6 (for Nitro instances): fd00:ec2::254 

How to access IAM role credentials using IMDSv2 (recommended): 

• Request a session token: Send an HTTP PUT request to the IMDS endpoint with the X-aws-ec2-metadata-token-ttl-seconds header, specifying the desired token duration (e.g., 21600 seconds for 6 hours). 

    TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")

• Retrieve credentials using the token: Send an HTTP GET request to the credentials path, including the X-aws-ec2-metadata-token header with the retrieved token. 

    curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/iam/security-credentials/YOUR_IAM_ROLE_NAME

Replace YOUR_IAM_ROLE_NAME with the actual name of the IAM role attached to your EC2 instance. 
Note: While IMDSv1 is still available, IMDSv2 is recommended for its enhanced security features, including the use of session tokens for authenticated access. AWS SDKs typically try IMDSv2 first and fall back to IMDSv1 if necessary, but you can configure the SDKs to exclusively use IMDSv2 for increased security. 

AI responses may include mistakes.


---

# 🟦 **SECTION 2 — FULL EC2 INSTANCE METADATA (IMDSv2)**

Available via:

```
http://169.254.169.254/latest/meta-data/
```

Below is the **complete list**.

---

# 🔵 **1. Identity Information**

```
/instance-id
/ami-id
/instance-type
/hostname
/local-hostname
/public-hostname
```

---

# 🔵 **2. Network Metadata**

```
/local-ipv4
/public-ipv4
/network/interfaces/macs/
/security-groups
/vpc-id
/subnet-id
```

---

# 🔵 **3. Placement Metadata**

```
/placement/availability-zone
/placement/region
/placement/group-name
```

---

# 🔵 **4. EBS Metadata**

```
/block-device-mapping/
/ebs/
/elastic-inference/
/elastic-gpu/
```

---

# 🔵 **5. IAM Metadata**

```
/iam/info
/iam/security-credentials/<role-name>
```

Contains:

```
AccessKey
SecretKey
Token
Expiration
```

---

# 🔵 **6. User Data**

```
http://169.254.169.254/latest/user-data
```

You can retrieve the same script passed at launch.

---

# 🔵 **7. Tags (Readable from Instance Only with IAM Policy)**

```
/tags/instance/<tag-key>
```

---

# 🔵 **8. Events & Maintenance**

```
/events/maintenance/
/events/recommendations/
/events/spot/
/events/scheduled/
/events/rebalance/
```

---

# 🔵 **9. System Information**

```
/kernel-id
/ramdisk-id
/architecture
```

---

# 🔵 **10. IMDS Config**

```
/meta-data/instance-life-cycle
/meta-data/services/
/meta-data/profile/
/meta-data/mac/
/meta-data/hypervisor/
```

---

### Why Metadata Is Important (Real Industry Use Case)

* You use metadata inside User-Data scripts.
* Example:
  * Your user-data wants to write instance-id to a file:
    ```bash
    INSTANCE_ID=$(curl -s 169.254.169.254/latest/meta-data/instance-id)
    echo $INSTANCE_ID > /var/log/my-instance-id.txt
    ```
  * If you want public IP for your application:
    ```bash
    PUBLIC_IP=$(curl -s 169.254.169.254/latest/meta-data/public-ipv4)
    echo "Server public IP = $PUBLIC_IP"
    ```

* This is extremely useful for:
  * Auto-configuration
  * Auto-registration
  * Logging
  * Bootstrapping applications
  * DevOps automations