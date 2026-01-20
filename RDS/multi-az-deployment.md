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
