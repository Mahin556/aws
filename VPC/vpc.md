## **1. What is a VPC?**
• A **Virtual Private Cloud (VPC)** is your own private network inside AWS.
• You use it to organize and secure your EC2 instances, databases, and other services.
• Just like a company creates different LAN networks in its office, AWS gives you VPC to build your cloud network.

---

## **2. Default VPC**
• Every AWS region comes with a **default VPC** that has all necessary components pre-configured.
• If you launch an EC2 without specifying a VPC, it goes into the default VPC automatically.
• A VPC is **regional**, meaning a VPC in Mumbai region cannot be used in the Virginia region.

---

## **3. VPC CIDR (IP Range)**
• When you create a VPC, you must choose an **IP range** using private IP blocks:
* `10.0.0.0/8`
* `172.16.0.0/12`
* `192.168.0.0/16`

• These IP ranges do **not** route on the public internet.
• CIDR notation (`/16`, `/24`) defines how many total IPs your network will have:

* `/16` → around 65,000 IPs
* `/24` → around 256 IPs

---

## **4. Why 0–255 in IP Addressing?**

• An IPv4 address has **4 octets** (8 bits each).
• Each octet has values from **00000000 (0)** to **11111111 (255)**.
• Therefore each block ranges from **0 to 255**.

---

## **5. Subnetting (Creating Smaller Networks)**

• Once a VPC is created, you divide the large IP range into smaller networks called **subnets**.
• Subnets make your architecture more organized, secure, and manageable.
• Example subnets inside a `/16` VPC:

* `192.168.1.0/24`
* `192.168.2.0/24`
* `192.168.3.0/24`
* Each subnet belongs to **a specific AZ** (ap-south-1a, ap-south-1b, etc.).

---

## **6. Public vs Private Subnets**

**Public Subnet:**
• A subnet becomes public if its route table contains:

```
0.0.0.0/0 → Internet Gateway (IGW)
```

• Instances in this subnet receive **public IPs** and can be accessed from the internet.

**Private Subnet:**
• A subnet is private if it has **no route to the Internet Gateway**.
• Instances get only private IPs and cannot be accessed directly from the internet.
• Used for databases, backend servers, internal services.

---

## **7. Security Groups (SGs)**

• Work at the **instance level**.
• Are **stateful** — if inbound is allowed, response outbound is automatically allowed.
• Can only **ALLOW** traffic — cannot block.
• Belong to a **specific VPC**.

---

## **8. Network ACLs (NACLs)**

• Work at the **subnet level**.
• Are **stateless** — inbound and outbound rules must be configured separately.
• Can **ALLOW or DENY** specific traffic.
• Rule priority depends on rule number (lower number is checked first).
• Default NACL → allows everything.
• Custom NACL → denies everything unless rules are added.

Example use case:
• Blocking specific IPs attacking your server.

---

## **9. Accessing Private EC2 Instances**

A private EC2 cannot be accessed directly because it has:

• No public IP
• No internet route
• No external connectivity

To access it, we use a:

### **Bastion Host (Jump Server)**

• A public EC2 instance used as a gateway.
• You first SSH into the bastion host → then SSH into the private EC2 using its private IP.
• This is widely used in production environments for secure private-server access.

---

## **10. Internet for Private Instances**

Private instances cannot run:

• `yum update`
• `apt-get update`
• `curl https://...`

Because they do not have internet connectivity.

To give them internet only for **outbound** traffic, you use:

---

## **11. NAT Instance vs NAT Gateway**

### **NAT Instance (Old Method – Not Recommended)**

• A special EC2 instance used to forward traffic.
• Problems:

* You must manage OS updates
* Not scalable
* Performance limits
* Single point of failure
* Must disable source/destination check

### **NAT Gateway (Recommended by AWS)**

• Fully managed by AWS
• Automatically scales
• Highly available and fast
• No maintenance
• Best choice for production workloads

Private subnet route table must contain:

```
0.0.0.0/0 → NAT Gateway
```

This gives **outgoing** internet access while still keeping the instance private.

---

## **12. How NAT Works Internally**

• Private instance sends traffic → NAT replaces private IP with its own public IP.
• Internet responds to NAT’s public IP.
• NAT forwards response back to the private instance.

This keeps private IPs hidden from the internet.

---

## **13. When to Use Public Subnets**

Use public subnets for:

• Load balancers
• Bastion hosts
• NAT gateways
• Reverse proxies
• Web servers (if directly public)

---

## **14. When to Use Private Subnets**

Use private subnets for:

• Databases (RDS, MySQL, PostgreSQL)
• Application servers
• Internal microservices
• Backend APIs
• Internal tools
• Batch processing systems

Keeping databases and application servers private improves **security**, **performance**, and **is industry best practice**.

---

### NACL vs SG

| Scenario                              | Use SG   | Use NACL              |
| ------------------------------------- | -------- | --------------------- |
| Control access to EC2                 | ✔ Yes    | ❌ No                  |
| Control access to RDS                 | ✔ Yes    | ❌ No                  |
| ALB → EC2 rules                       | ✔ Yes    | ❌ No                  |
| EKS worker nodes                      | ✔ Yes    | ❌ No                  |
| Private → NAT routing                 | ✔ Yes    | ❌ No                  |
| Need DENY rule                        | ❌ No     | ✔ Yes                 |
| Block entire CIDR ranges              | ❌ No     | ✔ Yes                 |
| Block a country / bad IP list         | ❌ No     | ✔ Yes                 |
| Extra layer of defence (PCI, Gov)     | Optional | ✔ Yes                 |
| Subnet-level isolation                | ❌ No     | ✔ Yes                 |
| Handling return traffic automatically | ✔ Yes    | ❌ No                  |
| Want simple firewall                  | ✔ Yes    | ❌ No                  |
| Want coarse subnet firewall           | ❌ No     | ✔ Yes                 |
| High security hardened VPC            | ✔ Yes    | ✔ Yes (both together) |


| Topic / Situation                  | **Security Group (SG)**                             | **Network ACL (NACL)**                                                     |
| ---------------------------------- | --------------------------------------------------- | -------------------------------------------------------------------------- |
| **Type**                           | Instance-level firewall                             | Subnet-level firewall                                                      |
| **Stateful?**                      | ✔ Yes (return traffic auto-allowed)                 | ❌ No (must allow return traffic manually)                                  |
| **Default behavior**               | Inbound deny / Outbound allow                       | Allow all                                                                  |
| **Rule ordering**                  | No rule order                                       | Rules evaluated lowest → highest                                           |
| **Can DENY traffic?**              | ❌ No                                                | ✔ Yes                                                                      |
| **Use in modern AWS**              | Mandatory                                           | Optional                                                                   |
| **Best for**                       | Controlling EC2/RDS/ALB/EKS access                  | Blocking subnets, CIDR ranges, additional filtering                        |
| **Typical usage frequency**        | 99% of cases                                        | Rare                                                                       |
| **When EC2 needs Internet**        | Best choice — handles ephemeral ports automatically | Not recommended — must manually allow 1024–65535                           |
| **When private instance uses NAT** | Works perfectly                                     | Often causes issues (forgotten ephemeral ports)                            |
| **Blocking bad IP ranges**         | Not possible                                        | ✔ Easy using deny rules                                                    |
| **Isolating subnets**              | Not possible (no deny)                              | ✔ Used for subnet isolation                                                |
| **Complexity**                     | Simple                                              | Complex (stateless + rule numbers)                                         |
| **Performance**                    | High                                                | Slight overhead                                                            |
| **Example use cases**              | SSH from bastion, App → DB, ALB → EC2, EC2 → RDS    | PCI-DSS hardening, blocking countries, blocking CIDR, extra security layer |
| **When NOT to use**                | Almost never                                        | EC2 → Internet, dynamic ports, NAT traffic                                 |
| **Who recommends it**              | AWS recommends SG as primary firewall               | AWS recommends leaving NACL default OPEN unless needed                     |
| **Inbound return traffic**         | Auto allowed                                        | Must be explicitly allowed using ephemeral ports                           |
| **Outbound return traffic**        | Auto allowed                                        | Must be explicitly allowed                                                 |


---

### NAT Gateway
* required elastic ip
* region or zonal association
* should be in public subnet
* connectivity type --> public,private

---

### NIC
* subnet
* private ip --> custom,auto-assign
* tag
* security group

---

### NAT instance
* Used to enable a communication from instance in private subnet to the internet
* need to be in public subnet
* enable auto assigne public ip
* attach a elastic public ip
* route rule --> route all traffic to nat instance in the route tabel of private instance subnet
* disbale the source/destination check in nat instace so nat instance do not discard the incomming packets from the interten(responces)(check destination ip in the packet)
* not recommended to use
* limitations
    * scalable ---> route limited traffinc with the instacne type or NIC
    * single point of failure
    * patching --> security
* allow all traffic in the sg of it

---

### SG(Security group)
* Statefull
* Only allow
* Instance level firewall
* 

---

### NACL(network access control list)
* stateless
* allow/deny traffic ---> IP
* subnet level firewall
* rule number
* keep deny rule on top.
* options --> rule number, type, protocol, port range, source, allow/deny
* Created within a VPC
* All VPC have there default NACL
* Associate with multiple subnets
* Subnet can't be associated with the multiple NACLs.
* By default all subnets associated with the default NACL of the VPC.
* Subnets always need to be associated with any of the NACL
* Default NACL ---> default all inbound/outbound traffic allow
* Custom NACL ---> default all inboud/outbound traffic deny 
* ipv4,ipv6
* port range


---
### elastic ip
* allocate
* associate
* Static, public IPv4 address you can allocate to your account.
* Offering a consistent internet endpoint for cloud resources like EC2 instances, unlike default dynamic IPs that change on restart. EIPs provide fault tolerance by allowing quick remapping to a healthy instance during outages, ensuring service availability, and can be associated with network interfaces for flexibility, though you're charged for unassociated EIPs to encourage efficient use. 
* Costs:
    * Free when associated with a running instance.
    * Charged if allocated but not associated (to prevent hoarding). 

---

### VPC Peering
* CIDR blocks must not overlap
* Peering is non-transitive (A↔B and B↔C does NOT mean A↔C) no traffic redirection
* No edge-to-edge routing (VPN / Direct Connect cannot pass through peering)
* Security groups and route tables must be explicitly updated
* Can be:
    * VPC peering (same account, same region)
    * VPC peering (same account, different regions)
    * VPC peering (different accounts, same region)
    * VPC peering (different accounts, different regions)
* There is only one-to-one communication between 2 VPCs
* Longest Prefix Match (LPM) is a routing rule used by routers to decide where to send a packet. When a destination IP address matches more than one route in the routing table, the router chooses the most specific route, meaning the one with the longest subnet mask (more matching bits). For example, if a destination IP matches both 192.85.0.0/16 and 192.85.15.0/24, the router will choose /24 because it is more specific.
* In simple terms:
    * Routers compare the destination IP with all routes.
    * Multiple routes may match.
    * The route with more matching bits (longer prefix) wins.
    * This ensures packets take the most accurate path.
* LPM(longest prefix matching) - 
    If a packet is destined for 172.16.0.10, which route is chosen -
    172.16.0.0/12 (only 12 bits match)
    172.16.0.0/16 (only match, 16 bits)
    172.16.0.10/32 (best match, 32 bits)
    The router chooses 172.16.0.10/32 because it has the longest prefix (32 bits).
* VPC peering allows only direct, one-to-one communication between resources in the peered VPCs. Each VPC must have its own internet gateway or outbound access mechanism to reach the internet independently.

---

### Transit Gateway and Transit Gateway Attachments
* To connect some VPC with each other we can use VPC peering but to connect multiple(10,20,50 etc) VPC with each other we should use transit gateway to easly manage them.
* The other solution then transit gateway is creating a multiple VPC and make all those VPC peering with one common VPC and create a instance on that on VPC use that instance to access other VPC
* Transit gateway is automatically scaled based on traffic.
* Traffic flow within AWS internal network(Communication is encrypted and never goes over the public internet)
* Process to create:
    * Create a VPCs + subnets
    * Create a transit gateway in VPC
* We can connect VPCs, VPCs peerings, Customer connect, VPN through Transit Gateway.
* It work as a central hub
    * all vpc connected to it
    * all VPCs subnets route tables route traffic for all other VPC/subents towards the Transit Gateway.
* Connect VPC, private subnets, public subnets, on-premise networks.
* In the route table we route traffic toward the Transit gateway attachment.
* All instance from different VPC can communicate with each other.
* Security groups must allow the required traffic.
* Transit gateway also connect the VPC of diff regions or VPC of diff accounts.
* While deleting a transit gateway --> first delete a transit gateway attachements one by one
* Involve 
    * Transit gateway attachment
    * Transit gateway route table
* Allow all ICMP traffic if want to check using `ping`

---

### VPC Flow Logs

In simple terms, VPC Flow Logs help you monitor network traffic.
Flow Logs at different levels
    • VPC Flow Log → captures all VPC traffic
    • Subnet Flow Log → captures subnet-level traffic
    • ENI Flow Log → captures traffic for a specific instance
    • EC2 instance → Flow Logs via its network interface (ENI)
Wherever you see the Flow Logs option, you can enable it.


If you enable Flow Logs on a VPC, AWS records:
    • Which IP addresses are sending traffic
    • Which packets are ACCEPTED
    • Which packets are REJECTED

This information is extremely useful when you face connectivity issues.
* For example:
    • You launched an EC2 instance
    • You installed a web server
    • But you cannot access it
* Flow Logs help you understand:
    • Where the traffic reached
    • Where it was blocked
    • Whether security groups or NACLs are causing the issue

This is one of the **best use cases** of VPC Flow Logs.

Where can Flow Logs send data?
* Flow Logs can be delivered to:
    • Amazon S3
    • Amazon CloudWatch Logs
    • Amazon Kinesis Data Firehose
    • Even to another AWS account

How Flow Logs work (example with S3)
    • Click **Create Flow Log**
    • Choose the resource (VPC / Subnet / ENI)
    • Select traffic type:
    - ACCEPT
    - REJECT
    - ALL
    • Choose aggregation interval (1 minute or 10 minutes)
    • Select destination → S3 bucket
    • Provide the S3 bucket ARN
    • Choose log format (default or custom)
    • Select time-based partitioning if logs are high-volume
Once created, logs automatically start getting stored in the S3 bucket.

Multiple Flow Logs
* You can create **multiple Flow Logs** for the same resource.
    * Example:
        • One Flow Log → S3
        • One Flow Log → CloudWatch
        • One Flow Log → Kinesis

---

### VPC Endpoint

**What problem do VPC Endpoints solve? (Simple Story)**
* Imagine you and your brother are sitting next to each other at home, connected to the same Wi-Fi.
* If you send him a WhatsApp message, it goes:    `Phone → Router → Internet → WhatsApp servers → Internet → Router → Brother’s phone`
* Even though he is sitting right next to you, the message still goes outside to the internet.
* Now imagine a system where the message does NOT leave your house.
* The router directly delivers the message internally.
* That’s exactly what **VPC Endpoints** do.
    * Another example:
        Inside a hotel, if you want to call another room, you just dial the room number.
        The call never goes outside the hotel — it stays internal.

**Relating this to AWS**
    Suppose:
    • Your EC2 instance is inside a VPC  
    • Your S3 bucket is also part of AWS infrastructure  
    By default, when EC2 accesses S3, the traffic goes **via public AWS endpoints (internet)**.
    With a **VPC Endpoint**, EC2 can access S3 **privately**, without using the internet.

**Infrastructure Setup**
    • One VPC  
    • One private subnet  
    • Private subnet route table has only a local route  
    • One public EC2 (bastion host)  
    • One private EC2 (application server)  
    * The private EC2:
        • Has no public IP  
        • Has no internet access  
        • Cannot ping 8.8.8.8  
        • Cannot reach google.com  

**Problem Statement**
    The private EC2 needs to upload objects to S3.
    Even after attaching an IAM role with **S3 Full Access**, the command: `aws s3 ls` does not work.
    Why?
    Because AWS CLI tries to reach S3 using a public URL,
    and the private instance has no internet connectivity.

**Solution: VPC Endpoint**
    We create a **VPC Endpoint for S3**.
    Steps:
    • Go to VPC → Endpoints  
    • Click Create Endpoint  
    • Select Service: S3  
    • Endpoint Type: **Gateway**  
    • Select the VPC  
    • Select the **private route table**  
    • Create endpoint  

**What happens after creating a Gateway Endpoint?**
    AWS automatically adds a new route to the selected route table.
    This route uses an **AWS-managed prefix list** for S3.
    Meaning:
        Any traffic whose destination is S3 will be routed internally
        through the VPC Endpoint — not through the internet.

**Verification**
    From the private EC2:
        • Ping to 8.8.8.8 → still fails  
        • Internet access → still blocked  
        • aws s3 ls → SUCCESS  
    This confirms:
        • No internet access  
        • But private access to S3 is working via VPC Endpoint  
    You can now:
        • List buckets  
        • Upload objects  
        • Download objects  
        • Fully use S3 privately  

**Important Notes**
    • VPC Endpoints can be created at:
        - VPC level
        - Subnet level
        - Network Interface (ENI) level
    • You can create multiple endpoints for the same VPC.
    • AWS supports **many services** (100+ depending on region) via VPC Endpoints.
    • Two endpoint types exist:
        - Gateway Endpoint (S3, DynamoDB)
        - Interface Endpoint (most other AWS services)


**Create an Interface VPC Endpoint**
Now we create an **Interface Endpoint** for S3.
Steps:
• Go to VPC → Endpoints  
• Click Create Endpoint  
• Select service → S3  
• Endpoint type → **Interface**  
• Select the VPC  
Unlike Gateway endpoints, this time AWS asks for:
• Subnet selection  
• Security Group selection  
Why?
Because Interface Endpoints work by creating a **network interface (ENI)** inside your subnet.
Important Settings for Interface Endpoints
    • Select the **private subnet**
    • Address type → IPv4
    • Attach a **security group** that allows:
    - Port 443 (HTTPS)
    • Enable **DNS name resolution** (very important)
Also ensure that your VPC has:
    • DNS Resolution = enabled  
    • DNS Hostnames = enabled  
If these are disabled in a custom VPC, the Interface Endpoint will not work properly.
What happens after creation?
    • A new **Elastic Network Interface (ENI)** is created
    • The ENI is attached to the selected subnet
    • It gets a **private IP address**
    • Traffic to S3 is routed via this interface — not via the internet
    You can verify this by going to:
    EC2 → Network Interfaces  
    You’ll see an extra interface created for the VPC Endpoint.
Verification
    From the private EC2 instance:
    • Internet access is still blocked
    • Ping to 8.8.8.8 fails
    • But running:
    aws s3 ls
    now works successfully
    This confirms that S3 is accessed **privately via the Interface Endpoint**.

**Gateway Endpoint vs Interface Endpoint**
    **Gateway Endpoint:**
        • Works using **route table changes**
        • No network interface is created
        • No security group involved
        • Free (no hourly cost)
        • Supported only for **S3 and DynamoDB**

    **Interface Endpoint:**
        • Works using a **network interface (ENI)**
        • Requires subnet and security group
        • Uses PrivateLink
        • Supports **most AWS services**
        • Has **hourly and data processing cost**

**Important Recommendation**
    Whenever possible, prefer **Gateway Endpoints** (S3, DynamoDB):
    • Simpler
    • Cheaper
    • No ENI cost
    Use **Interface Endpoints** when:
    • Gateway endpoints are not supported
    • You need private access to services like:
    - SSM
    - ECR
    - CloudWatch
    - STS
    - Secrets Manager

---

### Egress-Only Internet Gateway
An Egress-Only Internet Gateway is similar to a **NAT Gateway**, but it is used **only for IPv6 traffic**.

Key points:
• It allows **outbound-only** internet access
• It works **only with IPv6**
• Inbound traffic from the internet is blocked
• It prevents unsolicited inbound connections

Important:
Do NOT compare an Egress-Only Internet Gateway with an Internet Gateway.
You should compare it with a **NAT Gateway**.

• IPv4 outbound access → **NAT Gateway**
• IPv6 outbound-only access → **Egress-Only Internet Gateway**
* https://docs.aws.amazon.com/vpc/latest/userguide/egress-only-internet-gateway.html

Steps:
• Go to VPC → Egress-Only Internet Gateways
• Click Create Egress-Only Internet Gateway
• Provide a name
• Select the VPC
• Click Create

After creating it, you use it **exactly like a NAT Gateway**:
• Add a route in the private subnet’s route table
• Destination → IPv6 (::/0)
• Target → Egress-Only Internet Gateway

This allows private instances to access the internet over IPv6
while still blocking inbound connections.