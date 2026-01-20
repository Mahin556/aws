### READ REPLICAS

• Read Replica is a copy of the primary database used only for **read operations**
• Write operations (INSERT, UPDATE, DELETE) always happen on the **primary database**
• Read operations (SELECT) can be offloaded to Read Replicas
• Example application: **E-commerce website**
    – Users place orders → write operations
    – Users view order history → read operations
• As the application grows:
    – Large volume of orders accumulates
    – Search data, cart data, and user behavior data increases
• Analytics requires:
    – Running heavy read queries
    – Scanning large datasets
    – Frequent SELECT operations
• Running analytics on the primary database:
    – Increases database load
    – Slows down query response
    – Affects production users
• Solution:
    – Create a **Read Replica**
    – Run analytics and reporting on the Read Replica
    – Keep the production database performance stable
• Read Replicas are useful for:
    – Analytics and reporting
    – Debugging production issues safely
    – Handling read-heavy workloads
    – Reducing load on the primary database
• Real-life debugging use case:
    – Production database cannot be touched
    – Read Replica is used to run queries and debug
    – Replica can be deleted after use
• Creating a Read Replica in AWS RDS:
    – Select the primary database
    – Go to **Actions**
    – Click **Create Read Replica**
• AWS handles replication automatically:
    – No manual MySQL/PostgreSQL replication setup
    – Fully managed by AWS
• Cross-region Read Replicas:
    – Replica can be created in another AWS region
    – Improves availability and disaster recovery
    – Helps serve users closer to their location
• Each Read Replica has:
    – A separate endpoint
    – Independent instance size and storage
    – Independent configuration options
• Instance size of Read Replicas can be increased:
    – Useful for heavy analytics workloads
• Read Replicas support:
    – IPv4, IPv6, and dual stack
    – Public or private accessibility
    – Password-based or IAM authentication
    – Encryption (enabled by default)
• Data replication behavior:
    – Any data written to the primary DB appears in the Read Replica
    – Read Replicas do not allow write operations
    – Attempting to write causes permission errors
• Read traffic can be distributed:
    – Application servers write to primary DB
    – Analytics tools read from Read Replicas
• Important limitation:
    – Read Replicas do NOT solve Availability Zone failures
    – If the primary DB is single-AZ and that AZ goes down, DB becomes unavailable
• Read Replicas are for:
    – Performance
    – Scalability
    – Analytics
• Read Replicas are NOT for:
    – High availability failover
• High availability is handled using **Multi-AZ deployments** 
