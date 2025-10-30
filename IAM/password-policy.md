### 🧩 **What Is an IAM Password Policy?**

* A **password policy** in AWS IAM defines the rules for passwords used by IAM users in your AWS account.

* Go to IAM ---> Account settings

* It ensures that passwords meet your organization’s **security requirements** (like complexity, length, and expiration).

* You can configure it through the **AWS Management Console**, **AWS CLI**, or **IAM API**.


### ⚙️ **Options Explained in Detail**

#### 1. **Default Password Policy**

* This is the AWS default:

  * Minimum length = 8 characters
  * No complexity requirements (upper/lower/number/special not enforced)
* Simple but **not secure** for production environments.
* Recommended only for testing or temporary accounts.

---

#### 2. **Custom Password Policy**

* You can **customize all rules** to match your company’s security standards.
* AWS strongly recommends enabling complexity and expiration.

---

#### 3. **Password Minimum Length**

* Range: **6–128 characters**
* Default is **8**.
* Increasing to **12–16+** is a common enterprise best practice for better security.
* Example: `Minimum length = 12`

---

#### 4. **Password Strength Requirements**

You can enforce one or more of the following:

* ✅ **Require at least one uppercase letter (A–Z)**
  Prevents weak, all-lowercase passwords.
* ✅ **Require at least one lowercase letter (a–z)**
  Ensures variation in case.
* ✅ **Require at least one number (0–9)**
  Adds numeric complexity.
* ✅ **Require at least one non-alphanumeric character (!@#$%^&*)**
  Increases password entropy, making brute-force attacks harder.

**Example:**
Password `Admin@123` meets all requirements.

---

#### 5. **Other Requirements**

* **Turn on password expiration**

  * Forces IAM users to change their passwords regularly (e.g., every 90 days).
  * Default: Off.
  * Best practice: On for production accounts.
  * Helps prevent long-term credential compromise.

* **Password expiration requires administrator reset**

  * If enabled, when passwords expire, users cannot reset them themselves.
  * An admin must set a new one.
  * Used in highly secure or regulated environments.

* **Allow users to change their own password**

  * When **enabled**, users can change their own password via the AWS console or CLI.
  * Highly recommended so users can rotate passwords themselves.

* **Prevent password reuse**

  * AWS lets you specify how many previous passwords can’t be reused (up to 24).
  * Prevents users from cycling between the same few passwords.

---

### 🔐 **Example of a Strong Password Policy**

| Setting                   | Recommended Value |
| ------------------------- | ----------------- |
| Minimum length            | 12                |
| Require uppercase         | ✅                 |
| Require lowercase         | ✅                 |
| Require number            | ✅                 |
| Require special character | ✅                 |
| Password expiration       | 90 days           |
| Allow user change         | ✅                 |
| Prevent reuse             | Last 5 passwords  |

**Result:**
Strong passwords like `S3cur3@Cloud2025` would be required.

---

### 🧰 **Configure via AWS CLI**

Example command:

```bash
aws iam update-account-password-policy \
  --minimum-password-length 12 \
  --require-symbols \
  --require-numbers \
  --require-uppercase-characters \
  --require-lowercase-characters \
  --allow-users-to-change-password \
  --max-password-age 90 \
  --password-reuse-prevention 5
```

To view the current policy:

```bash
aws iam get-account-password-policy
```

---

### 🧠 **Key Points**

* Password policies apply **only to IAM users**, not to root accounts or federated users (SSO, Cognito, etc.).
* For organizations using **AWS Organizations + IAM Identity Center (SSO)**, password policies are managed separately at the **Identity Center** level.
* Strong password policies are a basic layer of protection — they should be combined with **MFA (Multi-Factor Authentication)** for real security.
