* **Eventually Consistent Read**
  * Default read behavior in DynamoDB
  * Data **may not be immediately updated** across all replicas
  * Usually becomes consistent **within milliseconds**
  * **Cheapest** read option
  * 1 RCU = **2 reads of 4 KB**
  * Best for:
    * Caching
    * Analytics
    * Non-critical reads
    * High-read throughput apps

* **Strongly Consistent Read**
  * Always returns the **latest committed value**
  * Reads from **leader replica**
  * Slightly **higher latency**
  * **More expensive**
  * 1 RCU = **1 read of 4 KB**
  * Not supported on:
    * Global Secondary Index (GSI)
  * Best for:
    * Banking balances
    * Inventory count
    * User profile after update

* **Transactional Consistency**
  * Uses DynamoDB **Transactions**
  * Provides **ACID guarantees**
    * Atomicity
    * Consistency
    * Isolation
    * Durability
  * Multiple items (up to **25 items or 4 MB**) updated together
  * All succeed or **all fail**
  * Strongest consistency model
  * Higher latency & higher cost
  * Operations:
    * `TransactGetItems`
    * `TransactWriteItems`

* **Transactional Read**
  * Always **strongly consistent**
  * Reads multiple items atomically
  * Ensures **no partial data**

* **Transactional Write**
  * Multiple writes as a **single unit**
  * Supports:
    * Put
    * Update
    * Delete
    * Condition checks
  * Used when **data integrity is critical**

* **Quick Comparison**
  * Eventually Consistent
    * May return stale data
    * Lowest cost
    * Highest throughput
  * Strongly Consistent
    * Always latest data
    * Higher cost
    * Lower throughput
  * Transactional
    * ACID compliant
    * Highest cost
    * Strict consistency
    * Multiple-item operations

* **Important Limits**
  * Transactions:
    * Max **25 items**
    * Max **4 MB total**
  * Not ideal for high-frequency simple reads

* **Interview One-Liners**
  * Eventually consistent → *Fast & cheap, may be stale*
  * Strongly consistent → *Always latest*
  * Transactional → *All-or-nothing ACID*
