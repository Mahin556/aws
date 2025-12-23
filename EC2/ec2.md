* EC2 stands for: Elastic Compute Cloud
* It basically gives you servers on rent from AWS on temperory bases.
* Used to get computational power on cloud.
* Used case:
    * Suppose you need a powerful machine (64GB RAM) for a 1-month project.
    * Training AI models
    * Hosting applications
    * Running backend APIs
    * Deploying microservices
    * CI/CD agents
    * Batch jobs
    * Hosting databases
    * Jump servers / Bastion hosts
* EC2 server/instance == VM created using a Type1 hypervisor(HyperV,Zen hypervisor).
* AWS keeps powerful servers in its datacenters.
* You create a machine remotely and access it via SSH or RDP.
* Region specific
* In free tier we can run instance 750HR/month.

* What Can You Configure in EC2 instance?
    * Operating System (Ubuntu, Amazon Linux, Windows, etc.)
    * Instance type: `t2.micro (Free Tier)`
        * Compute power (CPU cores)
        * vCPU
        * Memory (RAM size)
    * Storage (EBS volume size)
        * Root Volume
        * Default: 8 GB
        * Volume Size (8GB, 30GB, 100GB, etc.)
        * Volume Type (gp3, gp2, io2, etc.)
    * Network speed
    * Network configuration
        * VPC
        * Subnet
        * Auto-assign Public IP
    * Create Key Pair
        * Download .pem or .ppk key file.
        * This key will be used later to SSH into the instance.
        * In case of Windows we uses a RDP.
        * Public Key → stored inside EC2
        * Private Key (.pem/.ppk) → stays with you
Used for SSH authentication.
    * Security Group (what traffic can enter or leave the server)
        * Inbound Rules (incoming)
        * Outbound Rules (outgoing)
    * Bootstrap Script (User Data)

* instance status check 
    * 2/2

* **User Data(Bootstrap Script)
    → A script that runs automatically when the server launches
    * Helps automate:
        * Software installation
        * Configuration
        * Application deployment
        * Registering machine in DNS
        * Starting services
    ```bash
    #!/bin/bash
    apt update -y
    apt install nginx -y
    echo "Welcome to learningmotion.com" > /var/www/html/index.html
    systemctl start nginx
    ```
    * User Data always runs as root user, so you do not need `sudo`.


* **Important commands**
    ```bash
    ip a
    cat /etc/os-release
    df -h
    lscpu
    free -h
    ```

* **Accessing instance**
    * CMD --> if ssh installed
    * GitBash
    * Putty
    * Terminal (Linux/MacOS)
    * RDP Connect --> Windows
    * EC2 Instance connect

* **Root Volume**
    * Install OS of instance
    * While creating instance if `Delete on termination` ---> Yes root volume deleted when instance deleted. 

* **EC2 Lifecycle Options**
```bash
• Start
• Stop
• Reboot
• Hibernate
• Terminate
```

* **Boot Options**
```bash
• Boot from EBS
• Boot from instance store
• Boot via custom AMI
• Boot using encrypted root volume
```

* **Special EC2 Modes**
    ```bash
    * On-demand instance
    • Spot instances
    • Reserved instances
    • Savings plans
    • Dedicated hosts
    • Dedicated instances
    • Capacity reservations
    • EFA (Elastic Fabric Adapter)
    • Elastic GPUs / GPGPU
    ```

* **Instance Attributes (Describe-Instances)**
```bash
aws ec2 describe-instances
```
You can see:
  * Launch time
  * Root device type
  * virtualization type
  * hypervisor
  * CPU options
  * ENIs
  * Elastic IPs
  * Placement group
  * Monitoring state
  * Hibernation support
  * Capacity reservation
  * Billing type (spot/on-demand/reserved)

* **AWS Availability Zones are NOT identical for each user**
    * Your ap-south-1a ≠ My ap-south-1a
    * AWS maps AZ names differently for load balancing.
    * If 1000 new users create EC2 without changing anything, AWS distributes them across real hardware — that’s why AZ naming is randomized per account.

* **Fingerprint verification**
```bash
The authenticity of host 'ec2-X-X-X-X.compute.amazonaws.com' can't be established.
ECDSA key fingerprint is SHA256:xxxxxxxxxxxxxxxxxxx
Are you sure you want to continue connecting (yes/no)?
```
* Verify Using EC2 Instance Connect (BEST)


---

These are **all the fields** you can configure at launch time.

**1. Name & Tags**
    ```
    • Name
    • Key = Value tags
    ```
    Tags are used for:
        * Billing
        * Organization
        * Automation
        * Ownership

**2. Application & OS Images (AMI)**
Choose an AMI:
    ```
    • Amazon Linux 2 / 2023
    • Ubuntu
    • RHEL / CentOS
    • SUSE
    • Windows
    • Custom AMI
    • Marketplace AMI
    ```
Options:
    * 64-bit (x86)
    * 64-bit (ARM)
    * Kernel ID
    * RAM disk ID (legacy)


**3. Instance Type**
Defines CPU + RAM + Network + Storage capabilities.
Families:
    ```
    • t-family (general)
    • m-family (general)
    • c-family (compute)
    • r-family (memory)
    • i / d (storage optimized)
    • g / p / inferentia (GPU / ML)
    ```
Each type defines:
    ```
    • vCPUs
    • RAM (GiB)
    • EBS bandwidth
    • Network bandwidth
    • IPv6/IPv4 support
    ```

**4. Key Pair (SSH Login)**
Options:
```
• Create new key pair
• Use existing key pair
• No key pair (NOT recommended)
```
Types:
```
• RSA
• ED25519
```

**5. Network Settings**
* VPC Selection:
```
• Choose VPC
• Default VPC
```

* Subnet Selection:
```
• Public subnet
• Private subnet
```

* Auto-assign Public IP:
```
• Enable
• Disable
```

* Firewall / Security Group:
```
• Create new SG
• Use existing SG
• Allow SSH (22)
• Allow HTTP (80)
• Allow HTTPS (443)
• Custom TCP/UDP rules
```

* Advanced Network Options:
```
• Primary IPv4 address (manual)
• Secondary IPv4 addresses
• IPv6 addresses
• ENI (Elastic Network Interface) selection
• ENI attachments
```

**6. Storage Configuration (EBS)**
Each volume supports:
```
• Volume type:
    gp2
    gp3
    io1 / io2
    st1
    sc1
• Size (GiB)
• IOPS (if io1/io2)
• Throughput (gp3)
• Encryption:
    AWS-managed
    KMS key
• DeleteOnTermination:
    true / false
• Volume attachment:
    /dev/xvda or /dev/sda1
```
Add multiple EBS volumes as needed.


**7. Advanced Settings**

**A. IAM Role**
Attach IAM instance profile:
```
• FullAccess
• S3Access
• SystemsManagerAccess
• Custom IAM roles
```

**B. Shutdown Behavior**
```
• Stop
• Terminate
```

**C. Stop Protection**
```
Enable / Disable
```

**D. Termination Protection**
```
Enable / Disable
```
Prevents accidental termination.


**E. Monitoring**
```
• Enable detailed monitoring (1 minute metrics)
• Disable (default 5 min)
```

**F. Tenancy**
```
• Shared (default)
• Dedicated host
• Dedicated instance
```

**G. Capacity Reservation**
```
• Open
• Targeted
```

**H. Placement Group**
```
• Cluster
• Spread
• Partition
```

**I. Credit Specification (for T-family)**
```
• Standard
• Unlimited
```

**J. Elastic GPU (legacy)**
**K. Kernel ID (for legacy PV AMIs)**
**L. Nitro Enclaves Support**
```
Enable / Disable
```

**M. Metadata Service (IMDS)**
```
• IMDSv1
• IMDSv2 (recommended)
• Hop limit
• Token requirement
```

**N. User Data (Boot Script)**
```
#!/bin/bash
apt update -y
apt install nginx -y
echo "Hello" > /var/www/html/index.html
```
User Data types:
```
• Shell script
• Cloud-init
• MIME Multipart
```
Always runs as **root**.

