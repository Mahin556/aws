* **Scan**
  * Reads **every item** in the table or index
  * Does **not require** partition key
  * Very **slow** for large tables
  * High **RCU cost** because all data is read
  * Filters are applied **after** reading all items
  * Used when:
    * You don’t know the partition key
    * Table is very small
    * One-time admin/debug tasks
  * Example:
    * Get all users whose `age > 30` (no key condition)

* **Query**
  * Reads items using **partition key (mandatory)**
  * Much **faster** and **cheaper**
  * Reads only matching partition
  * Can use **sort key conditions**
    * `=`, `<`, `>`, `BETWEEN`, `begins_with`
  * Filters applied **after** key condition
  * Used when:
    * You know the partition key
    * High-performance production queries
  * Example:
    * Get all orders for `user_id = 101`
    * Get orders between two dates for a user

* **Key Differences (Quick Comparison)**
  * Scan
    * Access pattern: Full table
    * Partition key: Not required
    * Performance: Slow
    * Cost: High
    * Scalability: Poor
    * Best for: Small tables, testing
  * Query
    * Access pattern: Partition-based
    * Partition key: Required
    * Performance: Fast
    * Cost: Low
    * Scalability: Excellent
    * Best for: Production workloads

* **Interview One-Line Answer**
  * Scan checks **everything**
  * Query checks **only what you ask for using keys**

