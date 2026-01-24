![Image](https://d2908q01vomqb2.cloudfront.net/972a67c48192728a34979d9a35164c1295401b71/2023/02/13/DBBLOG-2553_SolArch-1024x489.png)

![Image](https://d2908q01vomqb2.cloudfront.net/887309d048beef83ad3eabf2a79a64a389ab1c9f/2024/12/02/1_blog.png)

![Image](https://d2908q01vomqb2.cloudfront.net/887309d048beef83ad3eabf2a79a64a389ab1c9f/2021/07/21/DBBLOG-1488-image001.png)

* **Point-in-Time Recovery (PITR)**

  * DynamoDB feature to **restore a table to any second** in the past
  * Recovery window: **last 35 days**
  * Helps recover from:

    * Accidental deletes
    * Bad updates
    * Application bugs
    * Data corruption

* **How it works**

  * DynamoDB continuously keeps **incremental backups**
  * You choose:

    * A **specific timestamp**
    * Or **latest restorable time**
  * Restore always creates a **new table**
  * Original table is **not overwritten**

* **What gets restored**

  * Table data
  * Primary keys
  * Local Secondary Indexes (LSI)
  * Global Secondary Indexes (GSI)
  * Provisioned settings (can be changed after restore)

* **What does NOT get restored**

  * IAM policies
  * Alarms
  * Auto Scaling policies
  * Tags (you may need to reapply)

* **Consistency & safety**

  * Restore is **atomic and consistent**
  * No downtime for the original table
  * Works even if the table was **deleted** (within 35 days)

* **Enable / Disable**

  * Can be enabled or disabled **anytime**
  * Once enabled, backups are automatic
  * No performance impact on reads/writes

* **Cost**

  * Charged based on:

    * Table size
    * Duration PITR is enabled
  * No charge when PITR is disabled

* **Use cases**

  * Production safety net
  * Compliance requirements
  * Human error recovery
  * Safer schema / app changes

* **Difference from On-Demand Backup**

  * PITR:

    * Continuous
    * Second-level restore
    * Automatic
  * On-Demand Backup:

    * Manual
    * Single snapshot
    * User-initiated

* **Important limits**

  * Restore time depends on table size
  * Cannot restore only specific items (full table restore)
  * Restore creates a **new table name**

* **Interview one-liners**

  * “PITR allows restoring DynamoDB tables to any second in the last 35 days.”
  * “PITR restores data into a new table, not the existing one.”
  * “It protects against accidental deletes and bad writes.”
