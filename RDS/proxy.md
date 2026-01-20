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
