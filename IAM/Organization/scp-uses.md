### References:- 
- https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html

### 🔹 1. Understand the Role of SCPs

* SCPs are **“permission boundaries”** for accounts, not permission providers.
* They define **what IAM users and roles *can never exceed***, even if their IAM policy says otherwise.
* Always think of SCPs as **guardrails**, not access grants.

---

### 🔹 2. Start with “Allow Everything,” Then Restrict

* By default, AWS Organizations includes a **FullAWSAccess SCP**, which allows everything (`"Action": "*"`) for all accounts.
* Keep this attached at the root to avoid unintentionally blocking services when starting out.
* Then, **create restrictive SCPs for OUs or accounts** that need boundaries (e.g., dev/test).

Example:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "*",
      "Resource": "*"
    }
  ]
}
```

→ Keep this at root for safety while you develop specific restrictions.

---

### 🔹 3. Use SCPs to Enforce Organizational Security Guardrails

* Restrict actions that could **weaken security or cause compliance issues**.
* Examples:

  * Prevent disabling CloudTrail:

    ```json
    {
      "Effect": "Deny",
      "Action": [
        "cloudtrail:StopLogging",
        "cloudtrail:DeleteTrail"
      ],
      "Resource": "*"
    }
    ```
  * Prevent deleting encryption keys:

    ```json
    {
      "Effect": "Deny",
      "Action": "kms:ScheduleKeyDeletion",
      "Resource": "*"
    }
    ```
  * Block IAM privilege escalation:

    ```json
    {
      "Effect": "Deny",
      "Action": [
        "iam:CreatePolicyVersion",
        "iam:SetDefaultPolicyVersion"
      ],
      "Resource": "*"
    }
    ```

---

### 🔹 4. Use OU Structure Strategically

* Design your OU hierarchy to match your organization’s environments and risk levels.
* Apply SCPs at the OU level, not per account, to simplify management.

Example OU design:

```
Root
├── Security (no restrictions)
├── Infrastructure (moderate restrictions)
├── Dev (restricted to cost control)
└── Sandbox (heavily restricted)
```

Then:

* Apply **broad SCPs** at higher levels (e.g., Root or Infrastructure)
* Apply **tighter, environment-specific SCPs** at lower levels (e.g., Dev or Sandbox)

---

### 🔹 5. Deny Specific Risky Services

You can use SCPs to block entire services that shouldn’t be used in certain environments.

Example – block expensive or risky services in Dev:

```json
{
  "Effect": "Deny",
  "Action": [
    "ec2:RunInstances",
    "rds:*",
    "redshift:*"
  ],
  "Resource": "*"
}
```

→ Developers can still view resources but not launch new ones.

---

### 🔹 6. Enforce Region Restrictions

* Control which AWS Regions are allowed to use resources.
* Helps with compliance and cost management.

Example – allow only `us-east-1` and `us-west-2`:

```json
{
  "Effect": "Deny",
  "Action": "*",
  "Resource": "*",
  "Condition": {
    "StringNotEquals": {
      "aws:RequestedRegion": ["us-east-1", "us-west-2"]
    }
  }
}
```

---

### 🔹 7. Deny Root User Access (Strongly Recommended)

* Block root user from performing sensitive operations.

Example:

```json
{
  "Effect": "Deny",
  "Action": "*",
  "Resource": "*",
  "Condition": {
    "StringLike": {
      "aws:PrincipalArn": "arn:aws:iam::*:root"
    }
  }
}
```

---

### 🔹 8. Combine “Allow Lists” and “Deny Lists” Thoughtfully

* **Deny list strategy:** Start with `FullAWSAccess` and add SCPs that *deny* risky actions or services.

  * Easier to maintain.
  * Common for large enterprises.
* **Allow list strategy:** Start with `Deny All` and explicitly *allow* only required services.

  * More restrictive, harder to manage.
  * Useful for high-security or compliance environments (e.g., GovCloud).

---

### 🔹 9. Test SCPs Safely Before Rolling Out

* Always test new SCPs in a **sandbox OU** before applying them organization-wide.
* Misconfigured SCPs can **lock out administrators** from critical operations.
* Tip: keep an emergency account in a **separate OU with minimal SCPs** to regain access if needed.

---

### 🔹 10. Combine SCPs with Other Controls

SCPs are powerful but not enough alone. Combine with:

* **IAM policies** → for granular access control
* **AWS Config** → to detect and report violations
* **CloudTrail + GuardDuty** → for monitoring actions
* **Service Quotas** → to prevent cost overruns

---

### 🔹 11. Document and Version-Control SCPs

* Keep SCP JSON files in Git for version control.
* Use meaningful names like:

  * `scp-deny-expensive-services.json`
  * `scp-enforce-region-restrictions.json`
* Add comments in documentation explaining **why** each policy exists.

---

### 🔹 12. Monitor SCP Effectiveness

* Use **AWS CloudTrail** to verify if SCPs are working as expected.
* Watch for `AccessDenied` events caused by SCPs.
* AWS Console → *Organizations → Policies → Service control policies* → Check which accounts they’re attached to.

---

### 🔹 13. Don’t Overuse SCPs

* Too many SCPs can make troubleshooting difficult.
* Use OU-level policies instead of per-account policies whenever possible.
* Keep them **simple, few, and clear**.

---

### 🔹 14. Always Include an Emergency “Break-Glass” Account

* Keep one admin account in a **separate OU** with **FullAWSAccess SCP** attached.
* It serves as a fallback if SCPs accidentally restrict critical admin access.

---

### 🔹 15. Summary Table

| Strategy              | Description                             | Example                                |
| --------------------- | --------------------------------------- | -------------------------------------- |
| Deny list             | Allow everything, deny specific actions | Deny `iam:DeleteUser`                  |
| Allow list            | Deny everything, allow specific actions | Allow only `s3:*`                      |
| Region restriction    | Limit AWS regions                       | Deny `aws:RequestedRegion` not in list |
| Environment isolation | Separate OUs for prod/test/dev          | Different SCPs per OU                  |
| Security enforcement  | Prevent disabling logging/encryption    | Deny CloudTrail deletion               |
| Root block            | Prevent use of root account             | Deny actions for `arn:aws:iam::*:root` |




Here’s a **detailed example** of a **Service Control Policy (SCP)** that allows users in an AWS account (for example, in the **Dev OU**) to **create VPCs and Internet Gateways (IGWs)**, but **blocks the ability to attach the IGW to the VPC**.

---

### 🧩 **SCP Policy Example**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowVPCCreation",
      "Effect": "Allow",
      "Action": [
        "ec2:CreateVpc",
        "ec2:DescribeVpcs",
        "ec2:DeleteVpc"
      ],
      "Resource": "*"
    },
    {
      "Sid": "AllowIGWCreation",
      "Effect": "Allow",
      "Action": [
        "ec2:CreateInternetGateway",
        "ec2:DescribeInternetGateways",
        "ec2:DeleteInternetGateway"
      ],
      "Resource": "*"
    },
    {
      "Sid": "DenyAttachIGW",
      "Effect": "Deny",
      "Action": "ec2:AttachInternetGateway",
      "Resource": "*"
    }
  ]
}
```

---

### 🧠 **Detailed Explanation**

* **`Version`** → Defines the policy language version (always `"2012-10-17"` for SCPs).
* **`Statement`** → Contains one or more permission rules.

#### 1️⃣ **AllowVPCCreation**

* Grants permissions to create, describe, and delete **VPCs**.
* These actions are required so users can manage their own VPCs.

#### 2️⃣ **AllowIGWCreation**

* Grants permissions to create, describe, and delete **Internet Gateways**.
* So users can provision IGWs but not necessarily attach them.

#### 3️⃣ **DenyAttachIGW**

* Explicitly **denies** the ability to attach an Internet Gateway to any VPC (`ec2:AttachInternetGateway`).
* Since **SCPs are evaluated with “explicit deny” precedence**, even if an IAM policy allows this action, the SCP will override it and block the action.

---

### ⚙️ **How Evaluation Works**

* SCPs define the *maximum* permissions an account’s IAM policies can grant.
* When both are evaluated:

  * **IAM Policy allows** → but **SCP denies** → **Action is denied.**
  * **IAM Policy allows** → **SCP allows** → **Action is allowed.**
  * **SCP denies** → no IAM policy can override it.

---

### 🧭 **Practical Scenario**

* You attach this SCP to the **Dev OU**.
* Users in that OU can:

  * Create and delete VPCs.
  * Create and delete Internet Gateways.
* But they **cannot attach** the Internet Gateway to any VPC (network isolation enforced).

---

### ✅ **Verification**

To test:

```bash
aws ec2 create-vpc --cidr-block 10.0.0.0/16
aws ec2 create-internet-gateway
aws ec2 attach-internet-gateway --vpc-id vpc-xxxx --internet-gateway-id igw-xxxx
```

* The first two commands will **succeed**.
* The last one (attach) will **fail** with an **“explicit deny by service control policy”** error.

