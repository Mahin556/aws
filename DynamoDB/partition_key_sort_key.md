* **DynamoDB overview**
  * DynamoDB is a **serverless NoSQL database** managed by AWS
  * AWS handles:
    * Scaling
    * Infrastructure
    * Storage
  * Data is stored on **SSDs** in AWS data centers

* **What is a DynamoDB partition**
  * DynamoDB stores data in **partitions**
  * A partition is a chunk of data stored on **one SSD**
  * Partitions are created and managed automatically by AWS

* **Role of the Partition Key**
  * Partition key decides **which partition** an item goes to
  * All items with the **same partition key value**:
    * Are grouped together
    * Live in the **same partition**
  * Optional **Sort Key**:
    * Organizes items **within the same partition**

* **Example (Good vs Bad design)**
  * Movies table:
    * Partition Key: `actor`
    * Sort Key: `movie_title`
    * All movies of the same actor go into one partition
  * Pets table (bad design):
    * Partition Key: `animal` (dog, cat)
    * Problem:
      * Huge number of items under `dog`
      * One very large partition
      * Causes throttling
  * Better design:
    * Partition Key: `breed`
    * Data spreads across many partitions
    * Better performance

* **High Cardinality (VERY IMPORTANT)**
  * High cardinality = **many unique partition key values**
  * Low cardinality = **few repeated values**
  * You should always design partition keys with **high cardinality**
  * This keeps partitions:
    * Smaller
    * Balanced
    * Faster

* **Hot Partition problem**
  * Happens when:
    * One partition receives much more traffic than others
  * Results in:
    * Throttling
    * Performance issues

* **Hard limits per partition**
  * **3,000 Read Capacity Units (RCUs) per second**
  * **1,000 Write Capacity Units (WCUs) per second**
  * These limits are **fixed and cannot be exceeded**
  * Even if your table has more total capacity

* **Provisioned capacity & partitions**
  * In Provisioned mode:
    * Total RCUs/WCUs are **distributed across partitions**
  * Example:
    * 4 partitions
    * 40 RCUs total
    * Each partition gets ~10 RCUs
  * DynamoDB can **rebalance capacity automatically**
  * But **hard per-partition limits still apply**

* **Automatic partition balancing**
  * AWS automatically:
    * Spreads partitions across SSDs
    * Groups small partitions together
    * Balances data and traffic
  * You do NOT need to manage this manually

* **What you MUST think about as a developer**
  * Choose a good partition key
  * Avoid low-cardinality keys
  * Avoid hot partitions
  * Keep partitions small and evenly used

* **Key takeaways (Interview-ready)**
  * “Partition key determines data distribution.”
  * “All items with the same partition key live in the same partition.”
  * “Each partition has a hard limit of 3,000 RCUs and 1,000 WCUs per second.”
  * “High-cardinality partition keys prevent throttling.”
  * “AWS automatically balances partitions, but key design is our responsibility.”
