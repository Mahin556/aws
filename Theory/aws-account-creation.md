### 🌐 **1. What Is an AWS Account**

* An **AWS account** is your **personal or organizational identity** used to access and manage all AWS cloud services.
* Each account has:

  * A unique **account ID (12 digits)**
  * A **root user** (the original email used to sign up)
  * **IAM users and roles** created for daily operations
* You use this account to:

  * Create and manage cloud resources (EC2, S3, RDS, etc.)
  * Track usage and billing
  * Set permissions and security policies
  * Manage multiple environments via **AWS Organizations**

---

### 🧾 **2. Prerequisites Before You Start**

* A **valid email address** (not used for any other AWS account).
* A **strong password** (minimum 8 characters, mix of letters, numbers, and symbols).
* A **credit/debit card** (international cards supported; required for identity verification even if using the Free Tier).
* A **valid phone number** for SMS or voice call verification.
* **Internet browser** (latest version of Chrome, Firefox, or Edge recommended).

---

### 🏁 **3. Step-by-Step AWS Account Creation Process**

#### **Step 1: Visit AWS Signup Page**

* Go to the official AWS signup page:
  🔗 [https://aws.amazon.com/](https://aws.amazon.com/)
  Click **“Create an AWS Account.”**

---

#### **Step 2: Enter Account Information**

* **Root user email address:**
  Enter your primary email (this will be your AWS login ID).
* **Password:**
  Create a strong password (AWS will require a mix of uppercase, lowercase, numbers, and special characters).
* **AWS Account Name:**
  Choose a recognizable name (e.g., `MahinRaza-DevAccount` or `MyCompany-AWS`).

Click **“Continue”**.

---

#### **Step 3: Contact Information**

* Choose the **Account type:**

  * **Personal** (for individual use)
  * **Professional** (for a company or organization)
* Fill in details:

  * Full name
  * Address
  * City, State, Postal code
  * Country
  * Phone number
* Accept the **AWS Customer Agreement** and continue.

---

#### **Step 4: Payment Information**

* Enter your **credit or debit card details**:

  * Card number, expiry date, and name on card.
* AWS will perform a **temporary authorization charge** (usually ₹2 or $1) to verify your card.
  This amount is refunded automatically within a few days.

Click **“Verify and Continue.”**

---

#### **Step 5: Identity Verification**

* AWS will now **verify your identity** via **phone call or SMS**:

  * Choose **Text message (SMS)** or **Voice call**.
  * Enter your **phone number**.
  * You’ll receive a **6-digit code**.
  * Enter it to complete verification.

---

#### **Step 6: Select a Support Plan**

* AWS offers multiple support plans:

  * **Basic (Free)** – for all users, includes 24×7 access to documentation and forums.
  * **Developer ($29/month)** – for non-production workloads.
  * **Business ($100/month)** – for production support.
  * **Enterprise ($15,000/month)** – for mission-critical systems.
* For beginners, choose **Basic Support – Free** and click **Continue**.

---

#### **Step 7: Account Activation**

* AWS will send an **activation confirmation email** (can take up to 5–10 minutes).
* Once received, click the link to verify your email.
* Your AWS account is now **active**.

You’ll see a message like:

> “Welcome to Amazon Web Services. Your account has been successfully activated.”

---

### 🔑 **4. Logging into the AWS Console**

* Go to: [https://aws.amazon.com/console/](https://aws.amazon.com/console/)
* Click **“Sign in to the Console.”**
* Select **Root User** (since you’re the account owner).
* Enter:

  * The **email address** used during signup.
  * The **password** you created.
* You’ll be redirected to the **AWS Management Console**.

---

### 🧩 **5. Initial Configuration After Login**

Once inside your AWS Console, perform these **initial setup steps** to secure and organize your account:

#### a) **Enable Multi-Factor Authentication (MFA)**

* Go to **IAM > Users > Security Credentials**.
* Under “Multi-factor authentication (MFA),” click **Activate MFA**.
* Choose **Virtual MFA device** (e.g., Google Authenticator, Authy).
* Scan the QR code and confirm codes.
* This protects your root account from unauthorized access.

#### b) **Create an IAM Admin User**

* Go to **IAM > Users > Add user**.
* Username: `admin`
* Check **AWS Management Console access**.
* Set a password.
* Assign permissions → Attach policy **AdministratorAccess**.
* Save the credentials.
* Use this **IAM user** for all daily operations — not the root user.

#### c) **Enable Billing Alerts**

* Go to **Billing Dashboard > Budgets**.
* Create a **Cost Budget** (e.g., ₹500 or $10).
* Set email alerts to get notified before exceeding your budget.

#### d) **Set a Default Region**

* Click the top-right corner (region selector).
* Choose a region near you (for India → `Asia Pacific (Mumbai) – ap-south-1`).

---

### 🧮 **6. AWS Free Tier**

* When you create a new account, you automatically get **AWS Free Tier benefits** for 12 months.
* Examples of free usage:

  * **EC2:** 750 hours/month (t2.micro or t3.micro)
  * **S3:** 5 GB storage
  * **RDS:** 750 hours/month of db.t2.micro
  * **Lambda:** 1 million requests/month
  * **CloudFront:** 50 GB data transfer
* After 12 months, you’re charged per usage, but **Free Tier–eligible services** remain available.

---

### 💳 **7. Billing and Cost Management**

* Access **Billing Dashboard** via your account dropdown.
* You can:

  * View invoices
  * Track monthly usage
  * Check Free Tier usage
  * Configure payment methods
* Use **Cost Explorer** to visualize where your money is spent.
* Always check:

  * **Service charges per region**
  * **Free Tier usage limits**

---

### 🛡️ **8. Best Security Practices (Right After Creation)**

* **Don’t use root user** except for billing and initial setup.
* **Enable MFA** on root and admin IAM users.
* **Delete access keys** for the root account.
* **Set strong password policies** for all IAM users.
* **Use IAM roles** for EC2 instead of embedding credentials.
* **Turn on CloudTrail** to log all API activity.
* **Activate AWS Config** to track resource changes.

---

### 🧱 **9. Optional: AWS Organizations (for Multi-Account Setup)**

If you plan to manage multiple AWS environments (e.g., Dev, Test, Prod):

* Use **AWS Organizations** to:

  * Create multiple accounts under one master account.
  * Apply **Service Control Policies (SCPs)** for centralized governance.
  * Consolidate billing for all accounts.
* Example setup:

  * Master Account → Billing and governance
  * Child Accounts → Separate workloads per team/environment

---

### 📞 **10. AWS Account Support**

If your account creation fails or payment verification is stuck:

* Visit the **AWS Support Center**: [https://console.aws.amazon.com/support](https://console.aws.amazon.com/support)
* Choose **“Account and Billing Support”**
* AWS offers **24×7 chat and email support** even on the free plan.

---

### 🧭 **11. Quick Recap Table**

| Step | Action                                  | Purpose                                   |
| ---- | --------------------------------------- | ----------------------------------------- |
| 1    | Go to AWS signup page                   | Start account creation                    |
| 2    | Enter email, password, and account name | Create root credentials                   |
| 3    | Add contact info                        | Identify account type (personal/business) |
| 4    | Add payment method                      | Verify identity                           |
| 5    | Verify phone                            | Confirm user authenticity                 |
| 6    | Select support plan                     | Choose Basic (Free)                       |
| 7    | Activate account                        | Begin using AWS                           |
| 8    | Enable MFA                              | Secure root account                       |
| 9    | Create IAM user                         | Use for daily AWS access                  |
| 10   | Set billing alerts                      | Monitor Free Tier and costs               |
