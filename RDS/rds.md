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

