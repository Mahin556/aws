### References:
- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-groups.html

---

* In **Amazon Web Services**, a Placement Group is a logical grouping of **Amazon EC2 instances**
* It controls **how EC2 instances are physically placed on hardware inside a data center**
* You don’t see the hardware, but AWS decides:
  * Which rack
  * Which host
  * Which network path
* Goal = optimize for:
  * Performance
  * High availability
  * Fault isolation

• **Why Placement Groups exist**
* Normally, AWS spreads instances randomly
* But some workloads need:
  * Ultra-low latency (HPC, big data)
  * Protection from rack failure
  * Isolation between nodes
* Placement Groups give you **control over failure domains**

---

**There are 3 types (VERY important)**

**1️⃣ Cluster Placement Group — Performance First**

![Image](https://miro.medium.com/v2/da%3Atrue/resize%3Afit%3A1200/0%2AnaAV6WjdHzYuFc3-)

![Image](https://miro.medium.com/v2/resize%3Afit%3A1200/1%2AYMoQbPQ0iQzRP0j2G8KmwA.png)

* Instances are placed:
  * **Very close together**
  * Often in the **same rack**
* Provides:
  * **Low network latency**
  * **High network throughput (10/25/100 Gbps depending on instance)**
* Best for:
  * HPC workloads
  * Machine learning clusters
  * Big data (Spark, Hadoop)
  * Financial trading systems

**BUT RISKY ⚠️**
* If that rack fails → many instances go down together
* So:
  * ❌ Not ideal for critical HA apps
  * ✅ Best for performance-heavy, parallel jobs

---

**2️⃣ Spread Placement Group — Maximum Safety**

* Instances are placed on:
  * **Different hardware**
  * Different racks
  * Separate failure domains
* AWS guarantees:
  * Each instance is on distinct underlying hardware

**Use case**
* Small number of critical servers:
  * Domain controllers
  * Database primary & standby
  * Licensing servers

**Limitations**
* Max **7 instances per AZ per spread group**
* Not for large clusters

---

**3️⃣ Partition Placement Group — For Big Distributed Systems**

* AWS divides instances into **partitions**
* Each partition:
  * Different rack set
  * Separate power/network
* Failure of one partition **does NOT affect others**

**Perfect for:**
* Hadoop
* Cassandra
* Kafka
* Large Kubernetes worker pools

You can have:
* Up to **7 partitions per AZ**
* Many instances per partition

This is **balance of performance + fault isolation**

---

• **Quick Comparison**

| Feature        | Cluster     | Spread           | Partition            |
| -------------- | ----------- | ---------------- | -------------------- |
| Focus          | Performance | Fault isolation  | Large-scale HA       |
| Distance       | Very close  | Very far         | Grouped into sets    |
| Failure impact | High        | Very low         | Limited to partition |
| Max instances  | High        | 7 per AZ         | Large                |
| Example        | HPC, ML     | Critical servers | Big data clusters    |

---

• **Important Rules**

* You can’t:
  * Merge groups
  * Change type after creation
* Some instance types may fail to launch if:
  * Not enough capacity in that placement style

---

• **How to create (CLI)**

```bash
aws ec2 create-placement-group \
  --group-name my-cluster-group \
  --strategy cluster
```

Other strategies:

* `spread`
* `partition`

---

• **When YOU should use what**

* Doing **DevOps / Kubernetes clusters** → use **Partition**
* Running **ML training** → use **Cluster**
* Running **production DB primary + standby** → use **Spread**
