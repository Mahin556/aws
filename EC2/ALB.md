# **Application Load Balancer (ALB) — Complete Clean Notes**

1. **What Is ALB & How It Differs from Classic Load Balancer**

**Classic Load Balancer (CLB)**
  * You directly attach **EC2 instances** to the load balancer.
  * LB distributes traffic straight to EC2s.

**Application Load Balancer (ALB)**
  * ALB **does NOT attach EC2s directly**.
  * Instead, it sends traffic to a **Target Group (TG)**.
  * ALB works at **Layer 7 (Application Layer)** → understands HTTP/HTTPS.

2. **Target Groups (The Core of ALB)**
A **Target Group** is a collection of backend targets where ALB forwards requests.
Target types:
  * EC2 instances
  * IP addresses
  * Lambda functions
  * Another ALB

You can create:
  * A single target group
  * Multiple target groups (blue/green deployment, mobile vs desktop, API splits, etc.)

Why Target Groups?
They allow **flexible and powerful routing**, such as:
* `learningmotion.com` → Blue TG
* `student.learningmotion.com` → Green TG
* `/tutorials` → TG-A
* `/q` → TG-B
* Mobile users → Mobile TG
* Laptop users → Desktop TG

3. **Why ALB Is Powerful (Layer 7 Intelligence)**
Because ALB operates at **Application Layer**, it understands:
* URL Paths (`/api`, `/test`, `/student`)
* HTTP Headers
* HTTP Methods (GET, POST)
* Query Parameters (`?search=Gaurav`)
* Cookies
* Hostnames (`student.example.com`)

This enables **advanced routing**:

| Type         | Example               | Use Case       |
| ------------ | --------------------- | -------------- |
| Path-based   | `/api`, `/test`       | Microservices  |
| Host-based   | `student.example.com` | Multi-domain   |
| Query-based  | `?platform=mobile`    | API versioning |
| Header-based | `device=mobile`       | Device routing |
| Method-based | GET/POST              | API control    |
| Source-IP    | IP ranges             | Internal apps  |


4. **Creating a Target Group (Steps)**
1. Go to **EC2 → Target Groups**
2. Click **Create Target Group**
3. Select **Instances**
4. Name your TG
5. Configure **health checks**
6. Select your EC2 instances
7. Add them to the TG

Target group is READY — waiting to be attached to ALB.


5. **Creating an Application Load Balancer**
1. Go to **Load Balancers → Create Load Balancer**
2. Choose **Application Load Balancer**
3. Select **HTTP / HTTPS**
4. Select **Availability Zones**
5. Choose a **Security Group**
   * Should allow only ALB → EC2 communication
6. Attach your Target Group
7. Create ALB
After a few seconds → **ALB is Active**.


6. **Routing Examples with ALB**
### Path-based
* `myapp.com/` → TG-A
* `myapp.com/api` → TG-B
* `myapp.com/student` → TG-C

### Host-based
* `api.myapp.com` → API TG
* `auth.myapp.com` → Auth TG

### Query-based
* `?platform=mobile` → Mobile TG
* `?server=test` → Test TG


7. **Why EC2 Cannot See Real Client IP Through ALB**
When EC2 is accessed through ALB:
```
Client → ALB → EC2
```
* ALB **terminates** the original TCP connection.
* ALB opens a **new TCP connection** to EC2.
* Therefore, EC2 sees **ALB’s private IP**, not the real client IP.

Solution → Use `X-Forwarded-For` header
ALB adds the original client IP into:
```
X-Forwarded-For: <Real-IP>, <ALB-IP>
```

But by default, Nginx does NOT log this header → you only see ALB IP.

8. **How to Log Real Client IP in Nginx (Clean Guide)**
Step 1: Add custom log format
```
log_format custom '$http_x_forwarded_for - $remote_user [$time_local] '
                  '"$request" $status $body_bytes_sent '
                  '"$http_referer" "$http_user_agent"';
```

Step 2: Apply log format

```
access_log /var/log/nginx/access.log custom;
```

Step 3: Reload Nginx
```
sudo systemctl reload nginx
```
Now logs show real IP:
```
106.78.19.55 - - [timestamp] "GET /test" 200
```

9. **Why You Should NOT Expose EC2 Instances Publicly**
When EC2 has a public IP:
* Users can bypass the ALB
* ALB features (rules, SSL, WAF, headers) are bypassed
* Security risks increase

Correct approach:
**EC2 should only allow traffic from ALB security group**, not the internet.

How to fix:
Security Group Inbound:
```
Type: HTTP
Source: <ALB Security Group>
```

This ensures:
* No direct user access
* All requests go through ALB
* Health checks work
* Secure architecture

10. **Listener Rules (Custom Routing & Custom Responses)**
Inside ALB → Listeners → View/Edit Rules
Example you created:
```
IF path == /error
THEN return fixed-response 503
```
ALB directly returns 503 without touching EC2.
Useful for:
* Maintenance mode
* Custom error pages
* Blocking paths

11. **Stickiness (Session Affinity)**
What is stickiness?
Keeps a user on the **same EC2 instance** by setting a cookie.

Why?
For session-based apps:
* Shopping cart
* Login sessions
* Stateful apps

How it works:
* First request → EC2 instance A
* ALB sets cookie: `AWSALB=xyz123`
* All future requests → same EC2 instance

Why not always use it?
* Can cause uneven load
* One instance may overload
* Reduces load balancing fairness

12. **Cross-Zone Load Balancing**
Enabled by default in ALB
When Enabled:
* Traffic is balanced **across all instances in all AZs**.
When Disabled:
* Traffic stays within same AZ → unbalanced distribution
Example:
* AZ-1 has 5 instances
* AZ-2 has 2 instances
  → AZ-1 gets more traffic
Cross-zone LB fixes this.

13. **HTTPS / SSL Termination**
Browser shows **"Not Secure"** when using HTTP.
To enable HTTPS:
1. Add Listener on **443**
2. Attach certificate from ACM or upload manually
3. ALB decrypts HTTPS, forwards HTTP to EC2
Benefits:
* Secure communication
* Centralized certificate management
* Works perfectly with routing rules

14. **Important ALB Features (Production Level)**
✔ Access Logs
* ALB pushes logs to S3
* Use Athena for analysis

✔ Remove Invalid Headers
* Prevents malformed or malicious client headers

✔ Custom Header Injection
* Add info like environment, microservice name

✔ Connection Draining (Deregistration Delay)
* Allows active requests to complete before removing an instance
* Prevents broken sessions

