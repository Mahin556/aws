* **Local Secondary Index (LSI)**
  * Secondary index in **DynamoDB**
  * Uses the **same Partition Key** as the base table
  * Uses a **different Sort Key**
  * Helps query data in **multiple sort orders**
  * Created **only at table creation time**

* **Key Structure**
  * Partition Key → **Same as table**
  * Sort Key → **Different**
  * Example:
    * Table PK: `user_id`
    * Table SK: `order_date`
    * LSI SK: `order_amount`

* **Why LSI is Used**
  * Query same data with **different sorting/filtering**
  * Avoid full table scans
  * Improve query flexibility

* **Read Consistency**
  * Supports **Strongly Consistent Reads**
  * Supports **Eventually Consistent Reads**

* **Storage**
  * LSI shares **same partition storage** as base table
  * Size limit applies:
    * **10 GB per partition key value** (table + all LSIs)

* **Projection Types**
  * KEYS_ONLY
  * INCLUDE (specific attributes)
  * ALL

* **Limits**
  * Max **5 LSIs per table**(soft limit)
  * Cannot add or delete LSI after table creation
  * Cannot modify LSI later

* **When to Use LSI**
  * When you:
    * Need strong consistency
    * Want multiple sort keys
    * Have predictable access patterns

* **LSI vs GSI (One-liner)**
  * LSI → Same PK, different SK, strong consistency, create at table creation
  * GSI → Different PK, optional SK, eventual consistency only, can be added anytime

* **Interview One-Liners**
  * “LSI uses the same partition key but a different sort key.”
  * “LSI must be created at table creation time.”
