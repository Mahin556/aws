### What is Database?
* Programs lose data when they exit unless the data is stored permanently

• Storing data in files allows persistence but file read/write operations are slow and inefficient

• As applications grow, file-based storage is not scalable or suitable for large data

• Databases are used to store data efficiently and permanently

• Relational databases store data in tables and allow relationships between tables

• Examples of relational databases: MySQL, MariaDB, PostgreSQL, SQL Server, Oracle

• Databases can be installed locally, but this creates problems like uptime, connectivity, security, and scalability

• Running databases on EC2 solves some issues but adds operational overhead

• Managing OS patches, security, backups, and replication manually is complex 

• High traffic applications need features like read replicas and multi-AZ availability

---

### RDS 
• Amazon RDS provides a managed relational database service
* Fully managed
• AWS handles OS management, patching, monitoring, backups, and scaling
• Read replicas and multi-AZ setups are easy with RDS

• RDS reduces manual work compared to self-managed databases

• Amazon RDS falls under **Platform as a Service (PaaS)**

• Before creating RDS, requirements must be clarified:
– Which database engine is needed (MySQL, MariaDB, PostgreSQL, Oracle, SQL Server, DB2)
– Which database the application supports


• A **database identifier** is required so the database can be easily recognized later

• A **username and password** must be set for database access

• Public access is disabled:
– The database is kept **private**
– It will be accessed only from an EC2 instance in the same subnet

• Availability Zone is selected explicitly for simplicity

• Password-based authentication is enabled

• Database creation goes through states like **Creating**, **Backing up**, and finally **Available**

• Different database engines show **different configuration options** in the UI
• There is no single fixed configuration for all databases:
– Options change based on the selected engine
– Features like Single DB, Multi-AZ, and clusters depend on the database type

• AWS admins should always coordinate with **database administrators** to choose correct options

* RDS have Security group(enable database port)

* Endpoint  and port

* we need to install a mysql client to interact with the database `mysql -h <db_endpoint> -u <user> -p<password>
* quories
    `SHOW databases`
    `CREATE database demo`

```bash
┌──────────────────────────────┬──────────────────────────────┬──────────────────────────────┐
│        ON-PREMISES           │          AMAZON EC2          │          AMAZON RDS          │
├──────────────────────────────┼──────────────────────────────┼──────────────────────────────┤
│ App Optimization   (User)    │ App Optimization   (User)    │ App Optimization   (User)    │
│ Scaling            (User)    │ Scaling            (User)    │ Scaling            (AWS)     │
│ High Availability  (User)    │ High Availability  (User)    │ High Availability  (AWS)     │
│ DB Backups         (User)    │ DB Backups         (User)    │ DB Backups         (AWS)     │
│ DB Software Patch  (User)    │ DB Software Patch  (User)    │ DB Software Patch  (AWS)     │
│ DB Installation    (User)    │ DB Installation    (User)    │ DB Installation    (AWS)     │
│ OS Patching        (User)    │ OS Patching        (User)    │ OS Patching        (AWS)     │
│ OS Installation    (User)    │ OS Installation    (User)    │ OS Installation    (AWS)     │
│ Server Maintenance (User)    │ Server Maintenance (AWS)     │ Server Maintenance (AWS)     │
│ Rack & Stack       (User)    │ Rack & Stack       (AWS)     │ Rack & Stack       (AWS)     │
│ Power & Network    (User)    │ Power & Network    (AWS)     │ Power & Network    (AWS)     │
└──────────────────────────────┴──────────────────────────────┴──────────────────────────────┘
```
```bash
┌──────────────────────── HOW TO UNDERSTAND THIS DIAGRAM ────────────────────────┐
│                                                                                 │
│  ON-PREMISES                                                                    │
│  • You manage everything                                                        │
│  • Power, networking, servers, OS, database, backups, HA                        │
│  • Full control but highest operational overhead                                 │
│                                                                                 │
│  AMAZON EC2                                                                     │
│  • AWS manages the physical infrastructure                                      │
│  • You still manage:                                                            │
│      - Operating System                                                         │
│      - Database installation                                                    │
│      - Backups                                                                  │
│      - High availability                                                        │
│  • Medium operational effort                                                     │
│                                                                                 │
│  AMAZON RDS                                                                     │
│  • AWS manages:                                                                 │
│      - Infrastructure                                                          │
│      - Operating System                                                         │
│      - Database installation                                                    │
│      - Patching                                                                 │
│      - Backups                                                                  │
│      - High availability                                                        │
│  • You focus only on:                                                           │
│      - Application logic                                                        │
│      - Query optimization                                                       │
│      - Schema design                                                            │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```
```bash
┌────────────────────────── RDS CONCEPTS & TERMINOLOGY ──────────────────────────┐
│                                                                                 │
│                                  USER / APP                                     │
│                                      │                                          │
│                                 Read / Write                                   │
│                                      │                                          │
│                                   ┌───▼───┐                                    │
│                                   │  VPC  │                                    │
│                                   └───┬───┘                                    │
│                                       │                                        │
│        ┌──────────────────────────────┴──────────────────────────────┐        │
│        │                              REGION                            │        │
│        │                                                                │        │
│        │   ┌───────────────────────┐        ┌───────────────────────┐  │        │
│        │   │   AVAILABILITY ZONE A  │        │   AVAILABILITY ZONE B  │  │        │
│        │   │                       │        │                       │  │        │
│        │   │   ┌──────────────┐    │        │   ┌──────────────┐    │  │        │
│        │   │   │  PRIMARY DB  │    │        │   │ READ REPLICA │    │  │        │
│        │   │   │ (MASTER)     │────┼────────▶   │  (READ ONLY) │    │  │        │
│        │   │   │ Read/Write   │    │ Replication│   │            │    │  │        │
│        │   │   └──────────────┘    │        │   └──────────────┘    │  │        │
│        │   │                       │        │                       │  │        │
│        │   │   (Standby for Multi-AZ)       │                       │  │        │
│        │   └───────────────────────┘        └───────────────────────┘  │        │
│        │                                                                │        │
│        └────────────────────────────────────────────────────────────────┘        │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```
```bash
┌──────────────────────────── EXPLANATION (SIMPLE) ──────────────────────────────┐
│                                                                                 │
│ MULTI-AZ                                                                        │
│ • Provides high availability and disaster recovery                              │
│ • Automatically fails over to standby instance                                  │
│ • Used for fault tolerance, not read scaling                                     │
│                                                                                 │
│ PRIMARY HOST                                                                    │
│ • Main database instance                                                         │
│ • Handles both READ and WRITE operations                                         │
│ • Application always connects to this endpoint                                   │
│                                                                                 │
│ SECONDARY HOST (STANDBY)                                                         │
│ • Used only in Multi-AZ                                                          │
│ • Does not serve traffic unless failover happens                                 │
│ • Automatically promoted if primary fails                                        │
│                                                                                 │
│ READ REPLICA                                                                    │
│ • Read-only copy of primary database                                             │
│ • Used for read scaling and performance                                          │
│ • Can be in another AZ or another Region                                         │
│ • Does NOT provide automatic failover                                            │
│                                                                                 │
│ IMPORTANT DIFFERENCE                                                            │
│ • Multi-AZ  → High Availability (Failover)                                      │
│ • Read Replica → Performance & Read Scaling                                     │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```
```bash
┌────────────────────── SYNCHRONOUS vs ASYNCHRONOUS REPLICATION ──────────────────────┐
│                                                                                      │
│ SYNCHRONOUS REPLICATION                                                              │
│ • Write operation is sent to PRIMARY and STANDBY at the same time                    │
│ • PRIMARY waits for confirmation from STANDBY                                       │
│ • Only after both confirm, write is marked as SUCCESS                                │
│ • Data is always consistent between instances                                        │
│ • Slightly higher write latency                                                      │
│ • Used for HIGH AVAILABILITY                                                         │
│ • Example: RDS Multi-AZ                                                              │
│                                                                                      │
│ Write Flow:                                                                          │
│ App → Primary DB → Standby DB → ACK → App                                            │
│                                                                                      │
│                                                                                      │
│ ASYNCHRONOUS REPLICATION                                                             │
│ • Write is committed on PRIMARY first                                                │
│ • PRIMARY does NOT wait for replica confirmation                                     │
│ • Data is copied to replica with a delay                                             │
│ • Replica may lag behind primary                                                     │
│ • Faster write performance                                                           │
│ • Used for READ SCALING and PERFORMANCE                                              │
│ • Example: RDS Read Replica                                                          │
│                                                                                      │
│ Write Flow:                                                                          │
│ App → Primary DB → ACK → App                                                         │
│               └─── Replication happens later ───▶ Read Replica                       │
│                                                                                      │
│                                                                                      │
│ KEY DIFFERENCE SUMMARY                                                               │
│ • Synchronous  → Safety first (no data loss)                                         │
│ • Asynchronous → Speed first (possible lag)                                          │
│                                                                                      │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

```bash
┌──────────────────────── AVAILABILITY & DURABILITY (RDS OPTIONS) ────────────────────────┐
│                                                                                           │
│ MULTI-AZ DB CLUSTER DEPLOYMENT (3 INSTANCES)                                              │
│ • 1 Primary instance + 2 Readable Standby instances                                       │
│ • Standbys are in different Availability Zones                                            │
│ • Readable standbys have their own reader endpoints                                        │
│ • Supports READ and WRITE scaling                                                         │
│ • Provides ~99.995% uptime                                                                │
│ • High availability + disaster recovery + read performance                                │
│ • Uses synchronous replication                                                            │
│ • Best for mission-critical production workloads                                          │
│                                                                                           │
│ Architecture Flow                                                                         │
│ App → Write/Read Endpoint → Primary (AZ1)                                                  │
│ App → Reader Endpoint → Standby (AZ2 / AZ3)                                                │
│                                                                                           │
│                                                                                           │
│ MULTI-AZ DB INSTANCE DEPLOYMENT (2 INSTANCES)                                              │
│ • 1 Primary instance + 1 Standby instance                                                  │
│ • Standby is in a different Availability Zone                                              │
│ • Standby has NO endpoint (not readable)                                                   │
│ • Used only for failover                                                                  │
│ • Provides ~99.95% uptime                                                                 │
│ • High availability but NO read scaling                                                    │
│ • Uses synchronous replication                                                            │
│                                                                                           │
│ Architecture Flow                                                                         │
│ App → Write/Read Endpoint → Primary (AZ1)                                                  │
│                          ↳ Standby (AZ2) [Failover only]                                  │
│                                                                                           │
│                                                                                           │
│ SINGLE-AZ DB INSTANCE DEPLOYMENT (1 INSTANCE)                                              │
│ • Only 1 Primary database instance                                                         │
│ • No standby instance                                                                     │
│ • No automatic failover                                                                   │
│ • No data redundancy                                                                     │
│ • Provides ~99.5% uptime                                                                  │
│ • Lowest cost                                                                             │
│ • Suitable for dev/test or non-critical workloads                                         │
│                                                                                           │
│ Architecture Flow                                                                         │
│ App → Write/Read Endpoint → Primary (AZ1)                                                  │
│                                                                                           │
│                                                                                           │
│ KEY DIFFERENCE SUMMARY                                                                    │
│ • Single-AZ        → Low cost, no HA                                                       │
│ • Multi-AZ (2)     → High availability, failover only                                     │
│ • Multi-AZ Cluster → HA + Read scaling + highest durability                                │
│                                                                                           │
└───────────────────────────────────────────────────────────────────────────────────────────┘
```

---

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



---

### Multi AZ in RDS - High Availability with Multi-AZ deployment
* If the AWS Region or a specific Availability Zone (AZ) goes down accidentally,
* The database instance will go down,
* And when the database goes down, the application will not behave as expected.
* Because of this issue, the application may fail, stop responding, or show incorrect behavior.
* The database engine selected was MariaDB.
* After selecting MariaDB, the Free Tier option was chosen.
    * In the Free Tier, the option “Availability and Durability – Multi-AZ Deployment” is disabled.
    * This is because Multi-AZ is not supported in the Free Tier.
    * To enable high availability, the Dev/Test option is selected instead of Free Tier.
    * Once Dev/Test is selected, the Multi-AZ deployment option becomes available.
* The Multi-AZ deployment option allows creating a standby database instance.
* A standby instance means:
    * AWS automatically creates another copy of the primary database in a different Availability Zone.
    * This standby instance is not used for reads or writes during normal operation.
    * All application requests (queries) continue to go to the primary database.
    * The standby instance remains synchronized via replication, so data is always the same on both instances.
    * If the primary database instance fails, AWS automatically performs a failover.
* During failover:
    * The standby instance becomes the new active (primary) database.
    * All incoming queries are redirected to the standby instance automatically.
    * The application does not need to change the database endpoint manually.
* A real-world analogy is used to explain this:
    * Just like a President and Vice President,
    * If the President is unavailable, the Vice President takes over responsibilities.
    * Similarly, if the primary database is unavailable, the standby instance takes over.
* The standby instance handles:
    * All incoming queries
    * All responses to the application
    * Since replication is always active, data consistency is maintained, and no data loss occurs.
* The situations when the primary database can go down:
    * Operating System (OS) patching
    * Security updates
    * Temporary OS unresponsiveness
    * Network connectivity loss
    * Storage volume becoming full
    * In all these cases: The standby instance continues to handle database operations.
* The Multi-AZ can be enabled:
    * While creating a new database
    * Or by modifying an existing database instance
        * The database is modified by selecting:
            * Apply immediately
            * Convert to Multi-AZ
            * After applying changes, the database status changes to Modifying.
            * Once modification is complete, the database status becomes Available.
            * The Multi-AZ value changes from False to True, confirming successful configuration.
* The database endpoint:
    * The endpoint of the database does not change.
    * The application always connects using the same endpoint.
    * AWS manages backend changes without impacting the application.

* To demonstrate failover:
    * DNS lookup (nslookup) on the database endpoint.
    * The nslookup command is used to: Resolve the endpoint to an IP address
    * Initially, nslookup returns an IP address pointing to the primary database instance.
    * To simulate a failure:
        * The primary database instance is selected.
        * Reboot with failover option is chosen.
        * This forces AWS to:
            * Reboot the primary instance
        * Trigger a failover to the standby instance
        * During the reboot:
            * The primary instance stops responding to queries.
        * AWS detects the failure immediately.
            * Runs nslookup during this process.
        * After failover starts:
            * The same database endpoint now resolves to a different IP address.
            * This new IP belongs to the standby instance, which is now active.
            * AWS automatically updates the DNS record behind the scenes.
            * This behavior is similar to:
                * Route 53 health checks
                * DNS-based failover policies
                * The endpoint remains the same, but the IP address changes dynamically.
            * All new queries are routed to the standby instance.
            * The application continues to work without any manual intervention.
            * The standby instance remains fully operational and responsive.
        * Even if:
            * One Availability Zone goes down
            * Or the primary database fails completely
            * The second Availability Zone continues serving database requests.
            * This ensures:
                * High availability
                * Fault tolerance
                * Minimal downtime
* Multi-AZ is not for scaling reads
    * It is strictly for high availability and disaster recovery
    * Read Replicas are used for:
        * Read scaling
        * Performance improvement
    * Multi-AZ is used for:
        * Automatic failover
        * Business continuity


---

### Proxy in RDS

```bash
+--------------------+
|   Client / App     |
| (EC2 / Lambda /    |
|  ECS / EKS)        |
+----------+---------+
           |
           | SQL Requests
           v
+-----------------------------+
|        RDS PROXY            |
|-----------------------------|
|  • Connection Pooling       |
|  • Auth via Secrets Manager |
|  • Fast Failover Handling   |
|  • IAM / DB Auth            |
+--------------+--------------+
               |
               | Optimized DB Connections
               v
+-----------------------------+
|        RDS DATABASE         |
|-----------------------------|
|  Primary DB (Writer)        |
|  Standby DB (Multi-AZ)      |
+--------------+--------------+
               |
               | Automatic Replication
               v
+-----------------------------+
|      Standby Instance       |
|   (Different AZ – HA)       |
+-----------------------------+
```

* Improving application performance and speed.
* A basic query such as `SHOW DATABASES` is executed on an RDS instance.
    * Even though this query looks very small and simple, **many background operations happen behind the scenes**.
    * These operations happen between:
        * The **application server (EC2 instance)**
        * And the **RDS database instance**
    * When an application runs a query, the following internal steps occur:
        * The database driver (for example, MySQL client) initiates a connection.
        * A **network socket** is opened at the operating system level.
        * Authentication is performed using:
            * Username
            * Password
        * The database validates whether the credentials are correct.
        * After successful authentication, the query is executed.
        * The query result is returned to the application.
        * The database connection is closed.
        * The network socket is also closed.
    * Even for a single query, **multiple OS-level operations** are involved.
    * This is not a problem when:
      * Only a few queries are executed.
    * A problem starts when:
        * Requests increase to thousands or millions.
        * Example explained:
            * If 1 lakh (100,000) requests come in.
            * Each request triggers around 5 backend operations.
            * Total backend operations become around **5 lakh operations**.
        * This leads to:
            * High CPU utilization
            * High memory utilization
            * Increased load on the database
        * This situation becomes a **performance bottleneck**.
        * This is the main **problem statement** RDS Proxy solves.

* The proxy sits between:
  * The application server
  * And the RDS database
* This proxy maintains **persistent database connections**.
* RDS Proxy works by:
    * Keeping a set of database connections **already open**
    * These connections are called **connection pools**
    * When a new request arrives:
        * The proxy reuses an existing open connection
        * It does not create a new connection every time
        * Because connections are already open:
            * Authentication is already done
            * Network sockets are already established
            * The query is executed immediately.
        * This significantly reduces:
            * CPU usage
            * Memory usage
            * Connection overhead
        * Only query execution happens at request time.
* RDS Proxy:
  * Reuses existing connection pools
  * Avoids repeated open/close operations
  * Returns query results efficiently

* The proxy always sits **between the client application and the database**.
* The application never talks directly to the database.
* All communication goes through the proxy.
* But the core benefit is **performance optimization**.

* Inside the RDS database section:
    * The proxy count initially shows **zero proxies**.
    * The option **Create Proxy** is selected.
    * AWS RDS Proxy supports only specific database engines:
        * MySQL
        * MariaDB
        * PostgreSQL
        * SQL Server
    * Some databases (like DB2) are not supported.
    * While creating the proxy:
        * Proxy identification details are configured.
        * Connection pool timeout is configured.
        * Connection pool idle timeout to **30 minutes**.
        * Target group configuration is explained:
            * It defines which database the proxy will forward requests to.
            * The specific MariaDB database is selected.
    * Maximum connections setting:
        * You can define how many DB connections the proxy can manage.
        * AWS allows up to **5000 connections** depending on configuration.
    * IAM authentication:
        * Can be enabled for additional security.
    * TLS encryption option:
        * Can be enabled for secure connections.
        * Optional but recommended for production environments.
    * AWS Secrets Manager is used:
        * Database credentials are stored securely.
        * A new secret is created.
        * Credentials are saved without hardcoding them in the application.
    * After completing configuration:
        * The **Create Proxy** button is clicked.
    * Once available:
        * Proxy endpoint details are visible.
        * Idle connection timeout shows **30 minutes**.
        * Multiple endpoints can be created for a single proxy if needed.
    * To connects to the database using:
        * MySQL client
        * Proxy endpoint URL instead of direct DB endpoint
    * After connection:
        * All queries are successfully executed.
        * Queries flow through the proxy to the database.
    * Authentication is done using proxy-managed credentials.

* Extra benefits of proxy usage are highlighted:
    * Request handling optimization
    * Connection lifecycle management
    * Security improvements
    * Reduced database stress

* secure RDS in such a way that:
    * Only RDS Proxy can access the database.
    * No EC2 instance can access the database directly.

---

