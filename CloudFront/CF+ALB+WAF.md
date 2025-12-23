Here is your content rewritten in **clean, clear, GitHub-ready Markdown**, with full explanation for both architectures:

---

# **CloudFront + ALB (Application Load Balancer)**

**Origin = EC2 (behind ALB)**

This is one of the most common production architectures.

```
User → CloudFront → ALB → EC2 instances
```

### **Why use ALB behind CloudFront?**

* ALB handles **path-based routing**, **host-based routing**
* ALB distributes traffic across multiple EC2 instances
* ALB supports **auto-scaling groups**
* CloudFront provides **global caching + security**

### **Benefits**

✔ Global CDN
✔ Reduced latency
✔ Caching for static & dynamic assets
✔ SSL termination at CloudFront
✔ ALB load balances traffic inside your VPC
✔ EC2 runs in private subnets (no public IPs needed)
✔ Security improved — users never hit EC2 directly

### **Typical Architecture**

```
                  +------------------------+
                  |        CloudFront      |
                  |  (CDN + global cache)  |
                  +-----------+------------+
                              |
                     HTTPS (OAC optional)
                              |
                  +-----------v------------+
                  |     Application LB     |
                  | (path/host routing)    |
                  +-----------+------------+
                              |
                     Auto Scaling Group
                              |
                 +-------------+-------------+
                 |       EC2 Instances       |
                 |     (private subnets)     |
                 +---------------------------+
```

---

# **CloudFront + WAF (Web Application Firewall)**

🔸 **Blocking countries, bots, IP ranges**

AWS WAF integrates directly with CloudFront.

```
User → CloudFront → WAF → Allowed traffic → Origin
```

### **Why use WAF with CloudFront?**

WAF can block:

* Entire countries
* Bad bots
* Anonymous proxies
* Known attack IPs
* SQL injection attempts
* XSS, LFI/RFI attacks
* Rate limiting (throttle users)

### **Common WAF Rules**

| Rule Type         | Purpose                                                     |
| ----------------- | ----------------------------------------------------------- |
| Block Country     | Block traffic from specific countries (e.g., China, Russia) |
| Bot Control       | Block scraper bots / crawlers                               |
| Rate-Based Rule   | Limit requests like 100 per IP in 5 minutes                 |
| Block IP Sets     | Maintain blacklist/whitelist                                |
| SQLi / XSS Rules  | Block OWASP Top 10 attacks                                  |
| AWS Managed Rules | Prebuilt protection packages                                |

### **Example Setup**

1. Create Web ACL in WAF
2. Add rules (GeoBlocking, Bot Control, Rate Limit)
3. Attach Web ACL to CloudFront distribution

Result:

* Bad traffic blocked **at edge** before reaching ALB/EC2
* Saves bandwidth
* Reduces load
* Protects backend

---

# **Combined Architecture: CloudFront + WAF + ALB + EC2**

```
                +-----------------------------+
                |         CloudFront          |
                | (CDN + HTTPS + OAC + Cache) |
                +---------------+-------------+
                                |
                        +-------v--------+
                        |      WAF       |
                        | (security layer)|
                        +-------+--------+
                                |
                        +-------v--------+
                        |      ALB       |
                        | (load balancing)|
                        +-------+--------+
                                |
               +----------------+-----------------+
               |                |                 |
         +-----v----+     +----v-----+      +----v-----+
         |   EC2    |     |   EC2    |      |   EC2    |
         | Private  |     | Private  |      | Private  |
         +----------+     +----------+      +----------+
```

### **Benefits of Full Stack**

✔ Global CDN performance
✔ Secure access to origin
✔ Country and bot blocking
✔ Auto-scaling backend
✔ Zero direct EC2 exposure
✔ Production-grade security & speed

---

If you want, I can also create:

✅ A chapter-style explanation
✅ Step-by-step setup guide for CloudFront → ALB
✅ Full WAF rule examples
✅ CloudFront + ALB + WAF **hands-on lab**
Just tell me!
