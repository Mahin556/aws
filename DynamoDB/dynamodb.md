* **DynamoDB**
  * Fully managed NoSQL key–value and document database by AWS
  * Serverless (no servers to manage)
  * Automatically scales read/write capacity
  * Very low latency (single-digit milliseconds)
  * Used for high-traffic apps, microservices, gaming, IoT, logs

* **Partition Key**
  * Mandatory part of the primary key
  * Used to decide **which partition** the item is stored in
  * Items with same partition key are stored together
  * Must be **unique** if no sort key exists
  * Example: `user_id`

* **Sort Key**
  * Optional second part of the primary key
  * Used to **sort items** with the same partition key
  * Enables range queries (`=`, `<`, `>`, `BETWEEN`, `begins_with`)
  * Example: `order_date`

* **Primary Key**
  * Unique identifier for each item
  * Two types:
    * **Simple primary key** → Partition key only
    * **Composite primary key** → Partition key + Sort key

* **Composite Key**
  * Combination of partition key and sort key
  * Partition key can repeat
  * Partition key + sort key together must be unique
  * Example:
    * Partition key: `user_id`
    * Sort key: `timestamp`

* **Item Max Size**
  * Maximum size of **one item = 400 KB**
  * Includes:
    * Attribute names
    * Attribute values
    * Data types

* **Max Items**
  * No fixed limit on number of items in a table
  * Limited only by:
    * Partition key design
    * Account limits
    * Throughput settings

* **Type of Items**
  * Each row in DynamoDB is called an **item**
  * Items can have different attributes (schema-less)
  * Example:
    * Item 1 → `user_id`, `name`, `email`
    * Item 2 → `user_id`, `name`, `phone`, `address`

* **Attributes**
  * Attributes are key-value pairs inside an item
  * Attributes do NOT need to be the same across items
  * Data types:
    * String (S)
    * Number (N)
    * Binary (B)
    * Boolean (BOOL)
    * Null (NULL)
    * List (L)
    * Map (M)
    * String Set (SS)
    * Number Set (NS)
    * Binary Set (BS)

* **Scan**
  * Reads **entire table** or index
  * Very slow and expensive for large tables
  * Does not use keys efficiently
  * Filtering happens **after** reading data
  * Use only for:
    * Small tables
    * One-time admin tasks

* **Query**
  * Reads data using **partition key**
  * Much faster and cheaper than Scan
  * Can filter using sort key conditions
  * Example:
    * Get all orders for `user_id = 101`
    * Get orders between two dates

* **CRUD Operations on Items**
  * **Create**
    * `PutItem`
    * Inserts new item or overwrites existing one
  * **Read**
    * `GetItem` → Get single item using primary key
    * `Query` → Multiple items with same partition key
    * `Scan` → Full table scan
  * **Update**
    * `UpdateItem`
    * Update specific attributes without replacing whole item
  * **Delete**
    * `DeleteItem`
    * Deletes item using primary key

* **Creating Sort Key After Creating Table**
  * ❌ **Not possible**
  * Primary key (partition key + sort key) is **immutable**
  * You cannot add or modify sort key later
  * Workarounds:
    * Create a **new table** with required sort key
    * Migrate data using:
      * DynamoDB Streams
      * Data Pipeline
      * Custom script (Lambda / SDK)
