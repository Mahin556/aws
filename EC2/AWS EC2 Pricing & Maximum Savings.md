**1. ON-DEMAND INSTANCES (Most Expensive, Most Flexible)**
* What are On-Demand instances?
  You simply say to AWS:
  > “I need an EC2 instance right now.”
* AWS instantly gives it to you — **no commitment**, no upfront cost.
* Because of this convenience, on-demand instances cost the most.

* **Billing Rules**
* Linux / Windows Instances
    ```
    First 1 minute → Fully charged  
    After that → per-second billing
    ```
    * Example:

        | Usage time | You pay for   |
        | ---------- | ------------- |
        | 20 seconds | Full 1 minute |
        | 80 seconds | 80 seconds    |

* Other operating systems (RHEL, SUSE, etc.)
    * Billed per hour

* **When to use On-Demand**
    * Short-term workloads
    * Development, testing, learning
    * When workload is unpredictable
    * Urgent ad-hoc server needs
* This is the **highest convenience**, but **highest cost** option.

---

**2. RESERVED INSTANCES (RI) — Save up to 72%**
* Reserved Instances are AWS’s classic, long-term cost-saving option.
* When to use?
  * When your workload is:
    * Predictable
    * Long-running
    * Always needed (e.g., a website, database)
* Example:
    * Your company knows it will need minimum 3 servers for the next 3 years → Use RIs.

* **How is the RI discount calculated?**
* Discount depends on **4 factors**:
  * OS Type
    * Linux is cheaper than Windows.
  * Region
    * Different regions = different pricing.
  * Instance Type
    * (t2.micro, t3.medium, m5.large, r6g, etc.)
  * Commitment Term
        ```
        1 year → Medium savings  
        3 years → Maximum savings
        ```
  * Payment Method
        ```
        All upfront → Highest discount  
        Partial upfront → Medium  
        No upfront → Lowest
        ```
  * Best combination gives up to **72% discount**.


* **Convertible vs Non-Convertible RIs**
    * **Non-Convertible RI**
        * Cannot change instance type
        * Highest savings (up to 72%)
    * **Convertible RI**
        * You CAN change:
          * instance type
          * instance family
          * OS
          * tenancy
        * Lower savings (~65%)
        * If you upgrade instance size →
            * AWS only charges the **difference**, not full price.
            * This is extremely fair and clean billing.

---

**3. SPOT INSTANCES — Save up to 90%**
*(AWS's Cheapest Option)*
Spot = Unused AWS capacity sold at huge discounts.

**Hotel Room Analogy**
  Hotel has 25 rooms
  20 are booked
  5 are empty
  Normal price: ₹1000
  You say:
  > “I can pay only ₹100.”
  Manager says:
  > “Okay, stay…
  > But the moment a full-paying customer comes,
  > **you must leave instantly.**”
  This is exactly how Spot Instances work.

**Spot Instance Characteristics**
  * Up to **90% cheaper**
  * Can be terminated anytime (2-minute warning)
  * Best for **interruptible workloads**

**Best Use Cases**
  * Batch jobs
  * Data processing pipelines
  * Video rendering
  * ML model training
  * Test automation
  * Background workers
  * Containers (EKS/ECS tasks)

If interruption does not matter → Spot is the best.

---

**4. DEDICATED INSTANCES & HOSTS**
Dedicated = The entire physical hardware belongs only to you.

* When to use?
    * Compliance or regulators require isolation
    * When you bring your own software license
    (Oracle, SQL Server, SAP, etc.)
    * Strict security environments
    * Government, Health, Finance workloads
This is the **most expensive** option.

---

**5. SAVINGS PLANS (Modern Replacement of RIs)**
*(Most used by real companies)*
Savings Plans = Similar discounts as RIs but more flexible.

* Key difference:
  * Reserved Instance → You commit to a **specific instance**
  * Savings Plan → You commit to **a spending amount per hour**

Example:
```
I promise to spend $10 per hour for the next 1–3 years.
```
AWS then automatically applies discounts to:
* EC2 (any instance, any region)
* Lambda
* Fargate

Discount
Up to **72%**, same as RIs.
This is the **best mix of flexibility + saving**.

---

* **Comparison Table**

| Option             | Savings          | Flexibility   | Interruption | Use Case                      |
| ------------------ | ---------------- | ------------- | ------------ | ----------------------------- |
| On-Demand          | ❌ Low            | ⭐ High        | ❌ No         | Short-term, unpredictable     |
| Reserved Instances | ⭐⭐ Up to 72%     | Medium        | ❌ No         | Long-term stable workloads    |
| Convertible RIs    | ⭐⭐ 60–65%        | ⭐⭐ High       | ❌ No         | Long-term but may change type |
| Spot Instances     | ⭐⭐⭐ Up to 90%    | Medium        | ✔ Yes        | Batch, ML, rendering, tests   |
| Savings Plans      | ⭐⭐⭐ Up to 72%    | ⭐⭐⭐ Very High | ❌ No         | Flexible mixed workloads      |
| Dedicated Hosts    | ❌ Very expensive | Medium        | ❌ No         | Compliance, licensing         |

---

* **Ultimate Summary**

* **On-Demand** → Maximum flexibility, maximum cost
* **Reserved Instances** → Best savings for stable workloads
* **Convertible RI** → Flexibility + moderate savings
* **Spot Instances** → Highest savings, lowest reliability
* **Savings Plan** → Best for mixed workloads, flexible
* **Dedicated** → Needed for special licensing or isolation

