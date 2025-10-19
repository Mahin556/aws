### References:
- https://aws.amazon.com/organizations/faqs/
- https://docs.aws.amazon.com/cli/latest/reference/organizations/

## 🧩 **What Is AWS Organizations**

* **AWS Organizations** is a **centralized account management service** that lets you manage multiple AWS accounts **from a single place**.
* It allows you to **group accounts**, apply **policies**, manage **billing**, and **delegate administrative control** — all under one structure.
* It’s designed for organizations with **multiple teams, environments, or projects**, giving them strong isolation and centralized governance.
* Organizations helps you to programmatically create new accounts.
* Simplify billing by setting up a single payment method for all of your accounts.
* create groups of accounts to organize your workflows
* Apply policies to these groups for governance.
* AWS Organizations is integrated with other AWS services so you can define central configurations, security mechanisms, and resource sharing across accounts in your organization and logging.
* Global Service.
* If accessed through the API the endpoint would be in the US East(N. Virginia)
* You can also attach policies to entities such as administrative roots, organizational units (OUs), or accounts within your organization.

---

## ⚙️ **How It Works — High-Level Overview**

1. You create or enable **AWS Organizations** from one AWS account.
   → That account becomes the **Management Account** (formerly “Master Account”).

2. The management account can:

   * **Create new AWS accounts** (using AWS Organizations API or console).
   * **Invite existing accounts** to join.
   * **Group accounts** into **Organizational Units (OUs)**.
   * **Attach Service Control Policies (SCPs)** to these OUs or individual accounts.
   * **Enable consolidated billing** to simplify cost management.

3. Member accounts continue to operate independently but remain governed by:

   * The **policies** applied by the management account.
   * The **billing** structure defined by the organization.

---

## 🧱 **Core Components**

### **Organization**
* You need to create a organization from any of the account(this account called a master account)

### 1. **Management Account**

* The first and top-level account in your organization.
* Has **full permissions** to:

  * Manage other accounts.
  * Control access using SCPs.
  * Handle consolidated billing.
* Should not run workloads — used only for governance and billing.

---

### 2. **Member Accounts**

* AWS accounts that belong to the organization but are **controlled by the management account**.
* centraly manage multiple accounts
* Can be:

  * **Created** from within the organization(very easy account creation then the traditional process), aws provide certial api call to create a account using organization service
  * **Invited** from outside (existing AWS account joins the organization).
* Operate independently but **cannot leave or modify policies** unless allowed.
* The management account is the ultimate owner of the organization, having final control over security, infrastructure, and finance policies. This account has the role of a payer account and is responsible for paying all charges accrued by the accounts in its organization. You cannot change which account in your organization is the management account.
* Each account get it's own root account

---

### 3. **Organization Root**

* The **starting point** of your organization’s hierarchy .
* It’s the **default container** for all your AWS accounts and organizational units.
* You can attach **Service Control Policies (SCPs)** directly to the root to affect **every account** in the organization.

![](/images/introduction-to-aws-organizations.webp)

---

### 4. **Organizational Units (OUs)**

* **Logical groupings** of AWS accounts under the organization.
* You can **nest OUs** (create OUs within OUs) to mirror your company’s structure.
* SCPs attached to an OU apply to all **accounts inside** that OU.
* You can go upto 5 in heirarchy(root,OUs,account)

Example structure:

```
Root
 ├── OU: Security
 │     ├── Account: SecurityAudit
 │     └── Account: Logging
 │
 ├── OU: Production
 │     ├── Account: Prod-App
 │     └── Account: Prod-DB
 │
 └── OU: Development
       ├── Account: Dev-Team1
       └── Account: Dev-Team2
```

---

### 5. **Service Control Policies (SCPs)**

* **Organization-level IAM-like policies** that define the **maximum permissions** an account can have.
* SCPs do **not grant permissions** — they **limit/max** what IAM policies can do.
* Even if a user in an account has `AdministratorAccess`, an SCP can **deny** specific actions globally.
* Permission policy that is specified at organization and applied to account,OUs,Root level
* If we assign a SCP that deny any thing even the root account can't perform that action.
* We need to enable service control policy first.
* How aws find that user can perform action or not:
![](/images/image.png)

Example SCP:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Action": "s3:DeleteBucket",
      "Resource": "*"
    }
  ]
}
```

This prevents **any account** in the OU from deleting an S3 bucket — even if IAM allows it.

---

## 💰 **Consolidated Billing**

* AWS Organizations provides **centralized billing** for all accounts in the organization.
* All charges from member accounts roll up to the **management account**.
* Instead of each account baying it own bill separately the management account used to pay collective bill(with discounts)
* Benefits:

  * **Single payment** for all accounts.
  * **Shared volume discounts** (e.g., EC2, S3, data transfer).
  * **Cost visibility** — you can track cost per account or OU.
* Member accounts **do not see** each other’s data but **management account can view everything** via **Cost Explorer** and **Billing console**.

---

## 🧾 **Policy Types in AWS Organizations**

AWS Organizations supports multiple policy types, each for specific governance functions.

| Policy Type                         | Purpose                                                  |
| ----------------------------------- | -------------------------------------------------------- |
| **Service Control Policies (SCPs)** | Set permission boundaries for accounts                   |
| **Tag Policies**                    | Enforce consistent tagging across accounts               |
| **Backup Policies**                 | Centralize and automate AWS Backup configurations        |
| **AI Services Opt-Out Policies**    | Control access to AWS AI/ML services for privacy reasons |

---

## 🔐 **Delegated Administrator**

* Instead of letting the management account handle every service, you can **delegate specific AWS services** to a **member account**.
* Example:
  Delegate the **Security Account** as the **administrator** for AWS Config or GuardDuty.

Benefits:

* Reduces workload on the management account.
* Distributes management responsibilities securely.

---

## 🔁 **Account Creation and Invitations**

You can add accounts to an organization in two ways:

### 1. **Create a new account**

* Using the management account:

  ```bash
  aws organizations create-account --email dev@example.com --account-name DevAccount
  ```
* The new account is automatically linked and governed.

### 2. **Invite an existing account**

* You send an **invitation** to another AWS account’s email or account ID.
* Once accepted, that account becomes a **member**.

---

## 🚫 **Service Control Flow**

When an IAM user or role makes a request:

1. The request is evaluated by **SCPs** first.
2. Then IAM policies within the account.
3. Then resource-based policies.
4. Then any service-specific policies (like S3 bucket policies).

If any SCP denies an action, it’s denied globally, even if IAM allows it.

---

## 🧠 **Best Practices**

* **Keep management account clean:**
  Use it only for billing and org management.
* **Use separate accounts for environments:**
  e.g., `Dev`, `Test`, `Prod`, `Security`.
* **Apply SCPs carefully:**
  Start with *allow list* policies (`DenyAllExcept...`) to strictly control permissions.
* **Enable CloudTrail organization trail:**
  For unified logging across all accounts.
* **Use AWS Control Tower:**
  Simplifies setup and enforces governance automatically on top of Organizations.
* **Tag accounts and OUs** for visibility in cost reports.

---

## 📊 **Integration with Other AWS Services**

| Service                          | Integration Purpose                                          |
| -------------------------------- | ------------------------------------------------------------ |
| **AWS IAM**                      | Enforces permissions within each account, bounded by SCPs    |
| **AWS CloudTrail**               | Can create organization-wide audit trails                    |
| **AWS Config**                   | Can track configuration compliance across accounts           |
| **AWS Control Tower**            | Automates best-practice setup for multi-account environments |
| **AWS Cost Explorer & Budgets**  | Analyze costs per account or OU                              |
| **AWS GuardDuty / Security Hub** | Centralized security monitoring across accounts              |

---

## 🏗️ **Example Real-World Setup**

**Company: TechCorp**

```
Root
 ├── OU: Security
 │     ├── Account: SecurityAudit
 │     └── Account: Logging
 │
 ├── OU: Infrastructure
 │     ├── Account: Networking
 │     ├── Account: SharedServices
 │
 ├── OU: Production
 │     ├── Account: Prod-Web
 │     └── Account: Prod-DB
 │
 └── OU: Development
       ├── Account: Dev-Team1
       └── Account: Dev-Team2
```

SCP examples:

* Security OU: Deny all except GuardDuty, CloudTrail, S3 (for logs)
* Prod OU: Deny IAM role modifications
* Dev OU: Allow most services but deny expensive instance types

---

# Benefits of central management

* **Single point of control**
  • Centralized management allows you to manage multiple AWS accounts from a single management (root) account.
  • You can apply policies, control billing, and monitor resources across all accounts from one place, without logging into each account individually.

* **Consolidated billing**
  • AWS Organizations supports consolidated billing, where all member accounts share a single payment method.
  • This simplifies financial management and gives volume discounts or savings plans across accounts collectively.
  • You get a single bill for the entire organization, making cost tracking easier.

* **Centralized policy enforcement (Service Control Policies)**
  • Administrators can create **Service Control Policies (SCPs)** at the organizational unit (OU) or account level.
  • SCPs define what actions are allowed or denied, regardless of permissions granted in IAM policies.
  • Ensures consistent security posture and compliance across all accounts.

* **Improved security and compliance**
  • Security baselines can be enforced across accounts — for example, denying IAM user creation or enforcing MFA.
  • Centralized logging and monitoring can be set up to collect logs from all accounts into one security account (e.g., CloudTrail, GuardDuty, Security Hub).

* **Separation of workloads and environments**
  • Each account can be isolated for different purposes — development, staging, production, or by business unit.
  • This isolation limits blast radius if one account is compromised or misconfigured.
  • Still, management policies and permissions are controlled centrally.

* **Delegated administration**
  • You can assign specific AWS services’ administrative rights (like AWS Config or Service Catalog) to designated member accounts.
  • This improves flexibility while keeping centralized governance.

* **Scalability and automation**
  • Organizations can programmatically create new accounts using **AWS Control Tower** or **Organizations APIs**.
  • Automatically apply guardrails, SCPs, IAM roles, and baseline configurations to new accounts.
  • Scales easily as your organization grows.

* **Centralized access management**
  • Using AWS Single Sign-On (SSO) or IAM Identity Center, you can centrally control user access to multiple AWS accounts and applications.
  • Reduces the complexity of managing credentials separately in each account.

* **Cost visibility and optimization**
  • You can use **AWS Cost Explorer** and **AWS Budgets** at the organizational level.
  • Provides visibility into which accounts or OUs are driving costs.
  • Enables chargeback or cost allocation per team or project.

* **Simplified compliance auditing**
  • Centralized logs and uniform access policies make auditing easier.
  • Compliance checks (e.g., PCI, HIPAA, ISO) can be done at the organization level rather than account-by-account.

* **Resource sharing**
  • Using **AWS Resource Access Manager (RAM)**, centrally managed accounts can share resources like subnets, transit gateways, and license configurations across accounts securely.


### Example
* Organization creation
  * AWS console
  * AWS organization service
  * Create organization
  * Add account
    * Create
      * Unique and valid email.
      * send confermation email.
      * forgot password
      * use thing like ID,debit/credit card from the master account.
    * Add already created account.
      * email or account id
      * Verification email send
      * account need to accept invite.
  * The account used to create Organization is become a management account(master account)
  * create a OU and move account from root level to that OU level.
  * Account only belogn to one OU
  * One OU can belong to Other OU aswell
  * One OU can have multiple accounts