#### AMI (Amazon Machine Image)
**What is an AMI?**
A **template** or **image** used to launch EC2 instances.
**AMI contains:**
  • Operating System
  • Application code
  • Configurations
  • Installed packages
  • Security hardening
  • Custom environment

---

**Simple Example to Understand AMI**
* **Example 1: ISO File**
  • Just like you install Ubuntu/Windows from an ISO file
  • You can create multiple systems from the same ISO
  • AMI works the same way for EC2
* **Example 2: House Blueprint**
  • Many houses → one common map
  • Many EC2 instances → one AMI

---

**Why Use AMIs?**
* **Faster deployments**
  * No need to install packages again and again.
* **Consistent environments**
  * Every instance created from the AMI is identical.
* **Golden Images**
  * A pre-configured image with:
    • OS
    • Security patches
    • Applications
    • Monitoring
    • Agents
    • Custom configs
  * Ideal for enterprise deployment.

**Creating an AMI (Step-by-Step)**
* **Step 1: Launch a Base EC2 Instance**
  Example:
  • Ubuntu AMI
  • Install nginx
  • Put your application inside `/var/www/html`
  • Verify that application is running
    ```bash
    sudo apt update
    sudo apt install nginx
    echo "Welcome to LearningMotion.com" > /var/www/html/index.html
    ```

* **Step 2: (Optional) Ensure Services Auto-Start**
  If nginx should run after reboot:
    ```bash
    sudo systemctl enable nginx
    ```
  This was the step missed in the video (and later added via userdata).


* **Step 3: Create the AMI**
  Two methods:
  **Method 1: Direct from EC2 instance**
    * EC2 → Select Instance → Actions → Image & Templates → **Create Image**
  **Method 2: Using a Snapshot**
    • Create snapshot of root volume
    • Snapshot → Actions → **Create Image**

* **Step 4: Wait for AMI Creation**
  * AMI creation takes **10–20 minutes**.
  * AMI creates:
    • An AMI entry
    • One or more snapshots (backend)

---

**Launching an Instance From Your AMI**
    • Go to EC2 → Launch Instance
    • Select your **Custom AMI**
    • Choose instance type
    • Add security group rules
    • Add user data only if required
    • Launch the instance
    * When the instance starts:
        • Your application is already installed
        • No need for bootstrap scripts
        • No delay in deployment

**Behind the Scenes (Very Important)**
  * **When you create an AMI:**
    AWS automatically:
    1. Takes a **snapshot** of your instance’s root volume  
    2. Registers an **AMI** that points to this snapshot
  In snapshots:
  • You can see: “Created by CreateImage” 
  • This is the backend snapshot used by the AMI

---

**Where AMIs Are Used in Industry**

**1. Auto Scaling Groups (ASG)**
    ASG requires a **Launch Template** that usually uses a **custom AMI**.

**2. Golden AMIs**
  For large companies:
  • OS updates
  • Security patches
  • Application pre-installed
  • Monitoring agents
  • Logging agents
All baked into the AMI.

**3. Faster Deployment Pipelines**
  CI/CD often builds AMIs automatically.
  Tools used:
  • **Packer**
  • Jenkins
  • GitHub Actions
  • AWS CodeBuild / CodePipeline


---

## **🔹 1. Before Deleting AMI – Clean Up Other Resources**

Before managing or deleting an AMI, always:
• Delete EC2 instances
• Delete EBS volumes
• Delete unnecessary snapshots

This ensures no resource is still using the AMI.

---

#### SHARING AN AMI
* Share an AMI With Another AWS Account
* Steps:
  1. Go to **EC2 → AMIs**
  2. Select your custom AMI
  3. Click: **Actions → Edit AMI Permissions**
  4. Options:
     * **Share with specific AWS Account IDs**
     * **Make AMI Public** (any account can use it)
* Important:
  * If AMI is **encrypted**, you must also share the **KMS key**.
  * If AMI is unencrypted → no KMS needed.

---

#### COPY AMI TO ANOTHER REGION
* Deploy same OS + app setup in multiple regions
* Avoid redoing configuration in each region
* Disaster Recovery (DR)
* Create golden images usable globally

**How to Copy an AMI**
  1. Select AMI
  2. Actions → **Copy AMI**
  3. Select destination region
  4. Click **Copy**

* Destination region will receive a **new AMI version**, identical to the source.

---

#### HOW TO DELETE (DEREGISTER) AN AMI
* AMI cannot be “deleted” directly.
* Instead, it must be **deregistered**.
* **What Deregistering Does**
  • Removes the AMI from the AMI list
  • But **does NOT delete the snapshot**
  • Snapshot must be removed separately
* **🔹 Deregister AMI**
  1. EC2 → AMIs
  2. Select AMI
  3. Actions → **Deregister AMI**
  4. Confirm
  After this, AMI disappears from AMI list.

* **DELETE THE SNAPSHOT ASSOCIATED WITH AMI**
  Behind the scenes:
  • When you create an AMI from an instance
  • AWS creates a **snapshot** of the root volume
  • AMI only *points* to this snapshot
  So after deregistering:
    1. Go to **Snapshots**
    2. Identify snapshot with description:
     * “Created by CreateImage”
    3. Actions → **Delete Snapshot**
  Now AMI is completely deleted.

---

**Understanding the Behind-the-Scenes Behaviour**
* **When You Create an AMI:**
  AWS automatically:
  1. Takes **snapshot** of root volume
  2. Registers an **AMI** that uses that snapshot
  3. Stores metadata (kernel ID, architecture, block device mapping)

* **When You Delete an AMI:**
  • AMI entry removed (deregistered)
  • Snapshot still exists → must delete manually
  • If snapshot stays, storage cost continues

---