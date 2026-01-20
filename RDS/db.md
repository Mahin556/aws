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
