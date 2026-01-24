* **DynamoDB Capacity Calculator (Simple & Exam-Friendly)**

* **Step 1: Identify operation type**
  * Read or Write
  * Strongly consistent read / Eventually consistent read
  * Item size (in KB)
  * Requests per second (RPS)
 
* **Read Capacity Unit (RCU) Calculation**
  * 1 RCU =
    * 1 **strongly consistent read** of **4 KB**
    * OR 2 **eventually consistent reads** of **4 KB**
  * Formula:
    * `RCU = (Item Size in KB / 4 KB) × Reads per second`
  * Round **up** always

* **Write Capacity Unit (WCU) Calculation**
  * 1 WCU = **1 KB write per second**
  * Formula:
    * `WCU = (Item Size in KB / 1 KB) × Writes per second`
  * Round **up** always

* **Example 1 (Read)**
  * Item size = 8 KB
  * Reads = 100 per second
  * Consistency = Strong
  * Calculation:
    * 8 KB / 4 KB = 2 RCUs per read
    * 2 × 100 = **200 RCUs**

* **Example 2 (Write)**
  * Item size = 3 KB
  * Writes = 50 per second
  * Calculation:
    * 3 KB / 1 KB = 3 WCUs per write
    * 3 × 50 = **150 WCUs**

* **Eventually Consistent Read Example**
  * Item size = 4 KB
  * Reads = 100 per second
  * Calculation:
    * 1 RCU supports 2 reads
    * 100 / 2 = **50 RCUs**

* **On-Demand Mode Calculation (Conceptual)**
  * No need to calculate RCUs/WCUs beforehand
  * DynamoDB internally still uses same math
  * You are charged **per request**
  * Capacity planning not required

* **Provisioned Mode Calculation (Important for exams & design)**
  * You MUST calculate RCUs/WCUs
  * Under-provision → throttling
  * Over-provision → extra cost

* **Golden Rules**
  * Always **round up**
  * Item size matters a lot
  * Query is cheaper than Scan
  * On-Demand = convenience
  * Provisioned = cost-efficient for steady load

* **One-line Interview Answer**
  * “RCU/WCU depends on item size, consistency model, and requests per second.”
