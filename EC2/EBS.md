* https://docs.aws.amazon.com/ebs/latest/userguide/ebs-encryption.html
* https://docs.aws.amazon.com/ebs/latest/userguide/ebs-fast-snapshot-restore.html

# **Create an EBS Volume**
**Steps:**
• Go to **EC2 Console → Elastic Block Storage → Volumes**
• Click **Create Volume**
• Choose:
* **Type:** gp2
* **Size:** 5 GB
* **AZ:** ap-south-1a (*must match instance AZ*)
  • Click **Create Volume**
(Do the same to create another volume in **ap-south-1b** — this is to demonstrate AZ restriction.)

---

# **Launch EC2 Instance (in Matching AZ)**

• Launch an EC2 instance
• AMI: **Ubuntu**
• Instance Type: **t2.micro**
• Edit Network → Select subnet of **ap-south-1a**
• Add an extra volume:
* **Size: 6GB**
  • Launch instance
Now, this instance has:
```
/dev/xvda → 8GB (root volume)
6GB → extra attached volume
```

---

# **Verify Attached Volumes**
Inside the EC2 instance, run:
```bash
lsblk
```
You will see:
```
xvda   8G
xvdb   6G
```

---

# **Attach Manually Created EBS Volume**
Remember:
**EBS can attach only if Instance AZ = Volume AZ**
So attach only the volume created in **ap-south-1a**.
**Steps:**
• EC2 → Volumes
• Select **5GB volume (ap-south-1a)**
• Actions → **Attach Volume**
• Select the Instance
• Attach

* **Inside the instance:**
```bash
lsblk
```
Now you see:
```
xvda → 8GB
xvdb → 6GB
xvdf → 5GB  ← newly attached
```
**Format the New Volume**
Format using EXT4 filesystem:
```bash
sudo mkfs.ext4 /dev/xvdf
```

**Create a Mount Point**
```bash
sudo mkdir /test
```

**Mount the Volume**
```bash
sudo mount /dev/xvdf /test
```
Verify:
```bash
mountpoint /test
```
If it says:
```
/test is a mountpoint
```
Then mount successful.

**Store Data on the EBS Volume**
```bash
cd /test
touch file1 file2 file3
echo "Hello AWS" > demo.txt
```
These files are stored **inside the EBS disk**, not on root disk.

**Unmount the Volume (Safe Removal)**
```bash
cd /
sudo umount /test
```
Check:
```bash
ls /test
```
(Empty — because EBS volume is removed from that directory.)

**Detach the Volume**
**Steps:**
• Go to **EC2 → Volumes**
• Select the 5GB volume
• Actions → **Detach Volume**
• Confirm
Inside instance:
```bash
lsblk
```
The 5GB volume disappears.


**Real-World Concept: Auto-Mount After Reboot**
You must add the volume to `/etc/fstab`:
This is your next task.
Tell me, and I will give the exact correct entry.

**Important: What Happens to Data After Detach?**
✔ Data stays inside the EBS volume
✔ You can attach this volume to ANY EC2 instance in the **same AZ**
✔ Your files will appear exactly the same
This is how AWS provides **persistent storage**.

**Summary Diagram (Easy Memory)**
```
Create EBS Volume
      ↓
Attach to EC2
      ↓
Format (mkfs.ext4)
      ↓
Mount to folder
      ↓
Store data
      ↓
Unmount
      ↓
Detach (safe)
```

**Detaching from EBS**
  * Data will be intect after detach and can mount EBS to other instance.
  * Check EBS have Filesystem or not
      ```bash
      sudo file -s /dev/xvdf
      /dev/xvdf: Linux filesystem (ext4)
      ```
      * If it have filesystem don't format it, your data will be lost.


##### **Resizing EBS**

* **STEP-1: Modify the EBS Volume Size (AWS Console)**
  ✔ No need to stop of detach from instance or even unmounting is not required.
  ✔ Go to: **EC2 → Elastic Block Store → Volumes**
  ✔ Select the EBS volume (example: 5GB)
  Click: **Actions → Modify Volume**
  Now:
  * You can **increase** size
  * You **cannot decrease** size
  Example:
  ```
  5 GB  →  8 GB   (allowed)
  5 GB  →  4 GB   (NOT allowed ❌)
  ```
  Click **Modify → Confirm**.
  After 10–15 seconds, AWS will update the volume.

* **STEP-2: Verify OS Still Shows Old Size**
  Connect to EC2 and run:
  ```bash
  lsblk
  ```
  Output will show something like:
  ```
  xvdf     8G   (correct new size)
  └─xvdf1  5G   (file system still old 5G)
  ```
  Meaning:
  ✔ Volume size changed
  ❌ File system NOT resized
  Now we must resize filesystem.


* **STEP-3: Resize the File System (Grow ext4)**
  Run the following:
  ```bash
  sudo resize2fs /dev/xvdf
  ```
  (Replace `xvdf` with your device name)
  This expands the ext4 filesystem to use full size.
  After resize:
  Run again:
  ```bash
  lsblk
  ```
  Now output will show:
  ```
  xvdf     8G
  └─xvdf1  8G   (filesystem expanded)
  ```

* **IMPORTANT: Why Was This Needed?**
  AWS only increases the **raw block device**.
  But the OS still sees old partition size unless you grow filesystem manually.
  That’s why **lsblk showed 8GB volume but only 5GB usable**.
  This fix is done by `resize2fs`.

* **What If You Need to Reduce Size? (Important)**
  AWS does **NOT** support decreasing EBS volume size.
  Why?
  Because decreasing can corrupt data.
  So the only safe method is:
  ✔ Create new smaller EBS volume
  ✔ Attach to EC2
  ✔ Copy the data manually (`rsync` or `cp`)
  ✔ Detach old large volume
  ✔ Attach and use the new smaller one
  This is the real industry **workaround**.

---

### Resize EC2 Root Volume (Increase OS Disk Size)

* **1️⃣ Modify Root EBS Volume from AWS Console**
✔ Go to **EC2 → Volumes**
✔ Select the **root volume (xvda)**
✔ Click **Actions → Modify Volume**
Example:
```
8 GB → 16 GB
```
Click **Modify → Confirm**
AWS will update the *raw block size*.

* **2️⃣ Verify Size Inside EC2**
SSH into EC2 and run:
```bash
lsblk
```
You will see:
```
xvda     16G   (volume changed)
└─xvda1   8G   (partition NOT changed yet)
```
✔ Volume = 16GB
❌ Partition = still 8GB
❌ File system = still 8GB

* **3️⃣ Check File System Type**
```bash
df -Th
file -s /dev/xvda1
```
If you see:
```
/dev/xvda1  ext4
```
→ Use `resize2fs`
If you see:
```
/dev/xvda1  xfs
```
→ Use `xfs_growfs`


* **4️⃣ Grow the Partition (VERY IMPORTANT)**
This step is required only for **root volumes**.
Run:
```bash
sudo growpart /dev/xvda 1
```
Where:
* `/dev/xvda` → device
* `1` → partition number
This expands the partition to full 16GB.
Check again:
```bash
lsblk
```
Now:
```
xvda     16G
└─xvda1  16G   (partition expanded)
```

* **5️⃣ Grow the File System**
**If filesystem = ext4**
Run:
```bash
sudo resize2fs /dev/xvda1
```
**If filesystem = xfs**
Run:
```bash
sudo xfs_growfs /
```
(`/` is the mount point of root volume)


* **6️⃣ Verify New Size**
```bash
df -h
```
Output will show:
```
/dev/xvda1   16G
```
 
* **IMPORTANT NOTES (Industry Use)**
  * You can **increase** root volume
  * You **cannot decrease** it
  * If you need a smaller root volume:
    * Create a new smaller volume
    * Copy filesystem
    * Create new AMI or attach volume manually

---

### EBS MULTI-ATTACH (Attach One EBS Volume to Multiple EC2 Instances)
* https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html#instance-hypervisor-type

**1️⃣ What is Multi-Attach?**
* Multi-Attach = One EBS volume attached to **multiple EC2 instances simultaneously**.
* Only for **io1 / io2** volumes
* Only on **Nitro-based EC2 instances** (T3, T4g, M5, C5, R5, etc.)
* Not available for GP2/GP3
* Not available for Xen-based instances (T2, M3, C3, etc.)


**2️⃣ Why Your First Attempt Failed? (Very Important)**
* You used **T2.micro**, which uses the **Xen Hypervisor**.
* Xen does NOT support Multi-Attach
* Multi-Attach works ONLY on **Nitro Hypervisor**
* So EBS returned this error:
```
"Multi-Attach is not supported for this instance type"
```

**3️⃣ How To Check Nitro Instances (AWS Official List)**
Any of these:
* T3 / T3a / T4g
* M5 / M6i
* C5 / C6i
* R5 / R6g
* m5d / c5d
* i3en
* etc.

Simple rule:
* **T3 and above supports Nitro**
* **T2 does not**


**4️⃣ Steps You Followed (Clean Version)**
* **Step 1 — Launch 2 EC2 Instances**
      * AMI: Ubuntu
      * Type: **T3.micro** (IMPORTANT – Nitro)
      * Both in **same Availability Zone (ap-south-1a)**

* **Step 2 — Create an EBS Volume**
      * Size: 10 GB
      * Type: **io2**
      * Enable: **Multi-Attach**

* **Step 3 — Attach Volume to First Instance**
      * AWS → EC2 → Volumes
      * Select volume → **Actions → Attach Volume**
      * Choose EC2 → Attach

* **Step 4 — Attach SAME volume to Second Instance**
Repeat:
```
Attach → Select 2nd EC2 → Attach
```
Now EBS volume is attached to **both EC2 machines**.


**5️⃣ Verify Inside EC2**
Run on both instances:
```bash
lsblk
```
You saw output like:
```
xvdf   10G
```
On BOTH servers — confirmed that Multi-Attach works.


**6️⃣ IMPORTANT WARNING — NEVER USE ext4/xfs WITH MULTI-ATTACH**
* Multi-Attach works ONLY with **cluster-aware file systems**:
      * GFS2
      * OCFS2
      * Lustre
      * IBM GPFS
      * Oracle ACFS
* Not:
      * ext4
      * xfs
      * btrfs
      * zfs
* If you mount EBS Multi-Attach volume with ext4 on two machines →  **100% data corruption**
* AWS clearly warns:
```
Use cluster-aware file systems only.
```
* Formating a volume with cluster aware filesystem
* https://aws.amazon.com/blogs/storage/clustered-storage-simplified-gfs2-on-amazon-ebs-multi-attach-enabled-volumes/

**7️⃣ Real Industry Use Cases**

* Shared Storage for HA Clusters
  Like:
      * Active-active application clusters
      * Database clusters using GFS2
      * Pacemaker/Corosync clusters

* High-performance parallel compute workloads (Low-latency access to same block device)

* Logging servers writing into same shared FS (using cluster FS)

---

### AWS EBS Snapshot – Full Concept (Clean Explanation)

**What is an EBS Snapshot?**
      * A **snapshot is a point-in-time backup** of an EBS volume.
      * AWS stores snapshots in **Amazon S3 (internally, not your bucket)**.
      * Snapshots are **region-specific** (cannot be used across regions without copying).
      * Think of it like a **photo of your disk** at a specific moment.

**Where do we use Snapshots in real life?**
      * Before doing risky changes (patching, upgrades)
      * Before installing new software
      * Before modifying files (example: `/etc/fstab`, `/etc/ssh` etc.)
      * If your EC2 disk gets corrupted
      * If someone deletes important files
      * For regular backups
      * For disaster recovery
      * To move volumes across Availability Zones


**Important property: Snapshots are Incremental**
  * Only the **first snapshot** is full.
  * Future snapshots store **only changed blocks**.
  * Example:

      | Day   | Volume Data Present | Snapshot Saved        |
      | ----- | ------------------- | --------------------- |
      | Day 1 | 50 GB               | 50 GB                 |
      | Day 3 | 60 GB               | Only 10 GB new blocks |
      | Day 5 | 62 GB               | Only 2 GB new blocks  |

  * So AWS **saves storage cost** by storing only changed data.


**What if you delete one snapshot?**

* Case 1: You delete the **first** snapshot
      * AWS moves any needed blocks into the next snapshot
      * NO DATA LOSS

* Case 2: You delete **middle snapshot**
      * Only unique blocks inside that snapshot will be copied to the next snapshot
      * NO DATA LOSS

* Case 3: You delete the **latest** snapshot
      * No impact on older snapshots
      * You only lose the newest backup
* AWS internally manages block mapping so your chain is never broken.


**Very important rule: Snapshots are Region-Specific**
      * Volume is created in **one Availability Zone**
      * Snapshot is stored in **full Region**
      * You can restore a volume in:
            * same AZ
            * another AZ in same region
            * OR copy snapshot to another region

**Why does AWS call it “Elastic Block Storage”?**
  Because:
      * Data is stored in **blocks**
      * You can expand storage
      * You can attach/detach storage
      * You can move data across AZs using snapshots

**How to Create an EBS Snapshot?**
```bash
AWS Console → EBS → Volumes → Select → Actions → Create Snapshot
```
You can also automate snapshots using:
* AWS Backup
* Data Lifecycle Manager (DLM)



**Restoring a Snapshot to Create Volume in any AZ**
      Steps:
      1. Go to **Snapshots**
      2. Select snapshot
      3. **Create Volume**
      4. Choose any **Availability Zone**
      5. Use volume in EC2

---

### All Snapshot Backup Strategies

**1. Full Snapshot Strategy**
      * Every backup = **complete data copy**
      * Most expensive (highest storage cost)
      * Slowest
      * Easiest to restore (only 1 snapshot needed)
      * Used when:
            * Very small datasets
            * Critical systems requiring simplest restore process


**2. Incremental Snapshot Strategy**
      (**AWS EBS uses this by default**)

      * First snapshot = Full
      * Future snapshots = only new/changed blocks
      * AWS handles block comparison
      * Lowest cost
      * Fastest backup
      * Restoration requires AWS to combine chain, done automatically
      * Used when:
            * Regular backups of EC2 EBS volume
            * Large and frequently changing data
            * Cost optimization needed

**3. Differential Snapshot Strategy**
      (Not used in AWS EBS, but used in databases & backup software)
      * First snapshot = Full
      * Future snapshots = changes **from last full** (not from last snapshot)
      * Restoring requires:
            * Full snapshot
            * Latest differential snapshot
      * Used when:
            * You want simpler restore
            * More frequent backups


**4. Synthetic Full Snapshot Strategy**
  * System creates a **virtual full snapshot** combining:
    * Previous full snapshot
    * Incremental changes
  * No need to re-copy full data
  * Looks like a full backup
  * Faster and cheaper than traditional full backup
  * Used when:
    * You want the speed of incremental + restore simplicity of full snapshot


**5. Multi-Region Snapshot Strategy**
  * Copy snapshot from Region A → Region B
  * For disaster recovery (DR)
  * Protects against region failure
  * Used when:
    * You need DR setup
    * You want volume in another region
    * Application needs high reliability

**6. Cross-AZ Snapshot Strategy**
  * Snapshot created in Region → volume can be restored in any AZ within that Region
  * Helps move EBS volumes across AZs
  * Used when:
    * Migrating EC2 to another AZ
    * Balancing load across AZs

---

#### Automate EBS Volume Backup Using EBS Lifecycle Manager
• EBS Lifecycle Manager (DLM) helps automate snapshot creation of EBS volumes without manual effort.
• Ideal for databases, critical applications, and regular backup schedules.
• **Snapshots support a Recycle Bin**
      * Deleted snapshots can be auto-retained for X number of days.

**🔹 Step 1: Create an EBS Volume**
• Create a new EBS volume (e.g., 5GB).
• Choose the correct Availability Zone.
• The volume does **not** need to be attached to an EC2 instance for automatic snapshots.

**🔹 Step 2: Add Tags to the Volume**
• Lifecycle Manager identifies volumes based on **tags**, not names.
• In production, common tagging strategy:
* `Name = <app-name>`
* `Tier = database` or `Tier = application`
  • Example tag for demo:
* `Name = test-vol`


**🔹 Step 3: Open EBS Lifecycle Manager**
• Navigate to:
**EC2 Console → Elastic Block Store → Lifecycle Manager**
• Click **Create lifecycle policy**
• Select **EBS Snapshot Policy**


**🔹 Step 4: Select Target Volumes Using Tags**
• Choose **Resource Type = Volume**
• Choose **Target Resources = Tags**
• Add the tag you configured earlier:
* `Name = test-vol`
• You can also apply multiple tag conditions.


**🔹 Step 5: Configure Snapshot Schedule**
You can configure how often snapshots are taken:
• **Hourly**
• **Daily**
• **Every X hours**
• **Weekly on selected days**
Example configuration:
• Frequency: **Daily**
• Time: **12:00 AM (Midnight)**


**🔹 Step 6: Configure Retention (How Many Snapshots to Keep)**
• Helps prevent too many snapshots from being stored.
• Example logic:
* 2 snapshots/day × 30 days = **60 snapshots**
* Set retention = **60**
• Demo example:
* Retention = **15**


**🔹 Step 7: Review & Create Policy**
• Review schedule, tags, retention.
• Click **Create Policy**.

**What Happens After Policy Creation?**
• Initially, there will be **zero snapshots**.
• At the next scheduled time, AWS **automatically creates a snapshot**.
• Snapshot description will show:
* “Created by policy: <policy-id>”
• Example from real usage:
* Schedule: 9:00 AM, every 2 hours
* Snapshot automatically created at 11:00 AM

---

#### Snapshot & AMI Recycle Bin in AWS

* **What Is Recycle Bin in AWS?**
  • The Recycle Bin is a safety feature for **EBS Snapshots** and **AMIs**.
  • If you **accidentally delete** a snapshot or AMI, it won’t be permanently removed immediately.
  • Instead, it is kept in the **Recycle Bin** for a defined **retention period** (1 day to 1 year).
  • After the retention period expires, AWS permanently deletes it.

* **Why Do We Need Recycle Bin?**
  • Prevents accidental data loss.
  • Works like the Windows Recycle Bin — deleted files are recoverable for some time.
  • Useful in production when:
      * A snapshot is wrongly deleted.
      * An AMI is removed by mistake.
      * Developers or automation scripts accidentally delete resources.


* **Creating a Recycle Bin Retention Rule**

  1. Open **Recycle Bin** from AWS console.
  2. Choose whether the rule applies to:
     * Snapshots
     * AMIs
  3. Choose **Apply to all resources** OR select via **Tags**.
  4. Set **Retention Period**:
     * Minimum: **1 day**
     * Maximum: **1 year**
     * Example: Many companies use **10 days** retention because:
       • Issues in applications often appear within 10 days
       • Allows recovery of older stable backups
  5. Click **Create Retention Rule**.


* **What Happens After Creating the Rule?**
  • Any **newly deleted snapshot or AMI** will move to the Recycle Bin.
  • It will NOT be permanently deleted until the retention period ends.

* **Testing the Recycle Bin**
To verify the rule:
  **1. Create a New Snapshot**
    • Go to **Volumes** → **Create Snapshot**
    • Give a name and create.
  **2. Delete the Snapshot**
    • Select snapshot → **Actions** → **Delete Snapshot**
  **3. Check the Recycle Bin**
    • Open **Recycle Bin**
    • You’ll see the deleted snapshot listed.
    • Details include:
      * Date deleted
      * Original ID
      * Days remaining before permanent deletion

* **Recovering a Snapshot or AMI**
  • Select the snapshot in Recycle Bin
  • Click **Recover Resources**
  • AWS restores the snapshot to its original state
  • You can see it again under **Snapshots**


**🔹 Important Notes for Real Environments**
  • Recycle Bin is extremely important for production:
      * Protects against human errors
      * Protects automated scripts from accidental mass deletion
      * Acts as a safety buffer before data is lost forever
  • Just creating EC2 + Security Groups is not enough for real infra.
You must also plan for:
      * Backup
      * Recovery
      * Retention
      * Disaster readiness
* Recycle Bin helps achieve safer and more resilient infrastructure.

---

#### Copy Snapshot Across Regions / Accounts in AWS

**🔹 Why Copy Snapshots Across Regions?**
Copying snapshots cross-region is useful for:
      • **Disaster Recovery (DR)**
      • **Multi-Region architecture**
      • **Migration of workloads**
      • **Creating backups in safer or cheaper regions**
      • **Sharing AMIs or data across accounts/teams**

**🔹 Before You Copy a Snapshot**
      • You **cannot directly copy an EBS Volume** to another region.
      • You must copy the **snapshot** of the volume.
      • Only snapshots can be moved or copied across regions/accounts.

**🔹 Step 1: Go to the Source Region**
Example:
• You are in **Mumbai (ap-south-1)**
• You want to copy the snapshot to **N. Virginia (us-east-1)**
Make sure you are in the region where the **snapshot currently exists**.

**🔹 Step 2: Select the Snapshot**
• Go to **EC2 → Snapshots**
• Select the snapshot you want to copy
You will notice:
• **Volumes have no “copy” option**
• Only **snapshots** show the **Copy** option

**🔹 Step 3: Copy the Snapshot**
Click:
**Actions → Copy Snapshot**
You will see:
• Description (optional)
• **Destination Region**
* Choose the region you want to copy the snapshot to
* Example: **us-east-1 (N. Virginia)**

**Important Setting: Encryption**
• If original snapshot is **unencrypted**, you can choose to **encrypt** it while copying.
• If snapshot is **encrypted**, any volume you create from it will also be encrypted.
➡ Encryption cannot be removed later — encrypted snapshots create only encrypted volumes.

**🔹 Step 4: Switch to Destination Region**
Now change region to the destination region, e.g. **N. Virginia (us-east-1)**.
Go to:
**EC2 → Snapshots**
You will see:
• The copied snapshot with status **pending → completed**
Once completed, it behaves like any normal snapshot.

**🔹 Step 5: Create a Volume from the Copied Snapshot**
Select the copied snapshot → click:
**Actions → Create Volume**
Choose:
• Availability Zone (e.g. us-east-1a)
• Volume type
• Size (>= snapshot size)
• Encryption (if needed)
Now you can:
• Attach this volume to any EC2 instance in that region
• Use it as normal storage

**🔹 Encryption Considerations**
• During cross-region copy, you can **add encryption**, even if the original snapshot was not encrypted.
• If you copy an **already encrypted snapshot**, you **must have KMS permissions**.
• Any volume created from an encrypted snapshot is **always encrypted**.

**🔹 Cross-Account Copy**
You can also copy a snapshot **to another AWS account**, but you must:
### **If snapshot is unencrypted:**
• Modify snapshot permissions
• Add the target account ID
• Then the other account can copy the snapshot into its region

### **If snapshot is encrypted:**
• You must share the **KMS key** with the target account
• Then grant snapshot access
• Then the other account can copy it

---

### EBS Volume Encryption

**🔹 1. What Happens When You Encrypt an EBS Volume?**
When you enable encryption on an EBS volume, AWS gives several built-in protections:

* **Data at Rest is Encrypted**
  • EBS volumes store data in AWS’s internal SAN (Storage Area Network).
  • Once encrypted, all data saved on the disk stays in **encrypted format**.

* **Data in Transit is Also Encrypted**
  • When EC2 reads/writes from EBS, the data traveling between EC2 and storage is **automatically encrypted**.
  • No manual configuration required.

AWS ensures:
```
EC2  ⇆  EBS Disk  
All traffic is encrypted.
```

<br>

**🔹 2. Creating Encrypted and Unencrypted Volumes**
You can create:
• One **Encrypted Volume**
• One **Unencrypted Volume**
Example:
```
Volume A → Encrypted
Volume B → Unencrypted
```
This helps demonstrate snapshot behavior.

<br>

**🔹 3. Snapshot Behavior With Encrypted & Unencrypted Volumes**
* Case 1: Snapshot of an Encrypted Volume**
  • If a volume is encrypted, its snapshot is **always encrypted**.
  • You cannot create an unencrypted snapshot from an encrypted volume.
* Case 2: Snapshot of an Unencrypted Volume**
  • Snapshot is **unencrypted** by default.
  • During volume creation from the snapshot, you can **choose to encrypt it**.

<br>

**🔹 4. Creating a Volume from a Snapshot**
* Case 1: Snapshot is Encrypted**
  • When you create a new volume from this snapshot:
  * Encryption is **mandatory**
  * The checkbox cannot be turned off
    • Resulting volume = **Encrypted**
* Case 2: Snapshot is Unencrypted**
  • While creating a new volume:
  * The **encryption checkbox is optional**
    • If you check the box → New volume becomes **encrypted**
    • If you don’t → New volume remains **unencrypted**

<br>

**🔹 5. AWS Claims: No Performance Impact**
  AWS documentation states:
  • **Encrypting or decrypting** EBS data has **almost zero performance impact**.
  • You can encrypt even production databases without worrying about performance loss.
  This is because:
  • Encryption/decryption happens in hardware (not software).
  • AWS Nitro System handles cryptographic operations efficiently.

<br>

**🔹 6. Why You Should Encrypt EBS Volumes**
  • Protects sensitive data
  • Industry compliance (ISO, HIPAA, PCI-DSS)
  • No performance overhead
  • No additional operational burden
  • Works for:
    * EBS volumes
    * Snapshots
    * AMIs
    * Instance store-backed volumes (via guest encryption)

<br>

* **🔹 7. Enforcing Default Encryption (Very Important)**
  * Often, engineers forget to check “Enable Encryption” when creating new volumes.
  * To avoid mistakes:
  * **Enable Default EBS Encryption**
    Go to:
    ```
    EC2 Console → Settings → EBS Encryption
    ```
    Then enable:
      ```
      ✔ Enable EBS Encryption by Default
      ```
  * **Effect**
    • All **new volumes** will be encrypted automatically
    • Users cannot accidentally create unencrypted volumes
    • Best practice for production and enterprise systems

---


#### FAST SNAPSHOT RESTORE (FSR)

**🔹 What is Fast Snapshot Restore?**
• All EBS snapshots are stored in **Amazon S3** internally.
• When you create a volume from a snapshot, data is **lazy-loaded** from S3 → EBS.
• Large snapshots take time to fully restore.

**Fast Snapshot Restore (FSR)** solves this.
* **✔ What FSR Does**
    • Pre-warms the snapshot
    • Ensures instant, full-speed data access
    • High-speed restore from S3 → EBS
    • Low latency
    • Removes initial slow I/O period

* **How to Enable**
    • Go to snapshot → Actions → **Fast Snapshot Restore**
    • Select Availability Zones
    • Enable FSR


