### References:- 
- https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html

### 🔹 Scenario Setup

You have:

* **Root** of the AWS Organization
* **Organizational Unit (OU)** named `dev`
* **Member Account** inside the `dev` OU

And:

* You attach **one SCP at the Root** level
* You attach **another SCP at the Dev OU** level

Now you want to know:
➡️ *What happens to the effective permissions of the account inside the Dev OU?*

---

### 🔹 Step 1: What SCPs Actually Do

* **SCPs (Service Control Policies)** define the **maximum permissions boundary** for accounts.
* They **don’t grant permissions** themselves — they only **restrict** what IAM policies *can* grant.
* Think of them as **“guardrails”** for all IAM users and roles within an account.

In other words:

> IAM policies tell you *what you can do*
> SCPs tell you *the most you are allowed to do, even if IAM allows more*

---

### 🔹 Step 2: SCP Inheritance Behavior

* SCPs are **inherited down the hierarchy**.
* Every account’s **effective permission boundary** is determined by the **intersection** of all SCPs that apply from:

  * The **Root**
  * The **OU(s)** above it
  * The **Account itself**

So:

> Effective permissions = intersection of (Root SCP ∩ OU SCP ∩ Account SCP ∩ IAM permissions)

---

### 🔹 Step 3: Example

Let’s make it concrete 👇

#### SCP attached to Root

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "ec2:*",
      "Resource": "*"
    }
  ]
}
```

→ This means:
All accounts under the Root can only ever use EC2 — **no other service** (S3, RDS, IAM, etc.) will work, even if IAM allows it.

#### SCP attached to Dev OU

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "ec2:Describe*",
      "Resource": "*"
    }
  ]
}
```

→ This further restricts EC2 actions to only “Describe” operations (no Start/Stop/Create).

---

### 🔹 Step 4: Combine the Two SCPs

The **Root SCP** says:

> Allow EC2 actions only.

The **Dev OU SCP** says:

> Allow only EC2 “Describe*” actions.

The **Effective SCP** for the Dev account = intersection of both
✅ `ec2:Describe*` (allowed)
❌ All other EC2 actions (blocked)
❌ All other AWS services (blocked)

So, even though Root allows EC2:*, the OU narrows it further.

---

### 🔹 Step 5: Important Rules of Evaluation

* SCPs are **cumulative “AND” restrictions**, not additive “OR” permissions.
* If any higher-level SCP **denies** something (explicit or implicit), lower ones **cannot override** it.
* **Explicit Deny** in any SCP always wins.
* If no SCP allows an action anywhere in the chain → that action is denied by default.
* Even if a higher-level SCP allows, if a lower-level SCP denies, that action is still denied.

---

### 🔹 Step 6: If You Add Another SCP at Account Level

You can also attach an SCP directly to the **member account**.

Let’s say:

```json
{
  "Effect": "Allow",
  "Action": "s3:*",
  "Resource": "*"
}
```

Would it work?

❌ No, because Root already limits all accounts to EC2-only.
So S3 actions are blocked higher up — the Account-level SCP cannot expand that.

---

### 🔹 Step 7: IAM Policy Interaction

Even if your IAM user has this:

```json
{
  "Effect": "Allow",
  "Action": "ec2:StartInstances",
  "Resource": "*"
}
```

That user **still cannot** start EC2 instances because:

* SCP at OU level only allows `Describe*`
* SCPs override IAM permissions.

---

### 🔹 Step 8: Visualization

```
Organization Root
│
├── SCP: Allow EC2:*      ← applies to everyone
│
└── OU: Dev
     ├── SCP: Allow EC2:Describe*
     └── Account: Dev-Account
          └── IAM Policy: Allow EC2:*
```

**Effective Permission:** EC2:Describe* only ✅
Everything else ❌

---

### 🔹 Step 9: Key Takeaways

* SCPs are **guardrails**, not permission-granters.
* SCPs **cascade downward** (Root → OU → Account).
* The **final effective permissions** are the **intersection** of all applicable SCPs and IAM policies.
* **Explicit deny** anywhere wins.
* If the Root SCP blocks something, no lower SCP or IAM can allow it.
* Always start with a **broad “Allow” SCP at Root** (like `Allow *`) and restrict more specifically at lower levels (e.g., `Dev`, `Prod` OUs).
