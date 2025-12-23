*Imagine you have a website hosted on a server in the USA, but users are accessing it from India, Nepal, Bangladesh and other regions. Every time a user in India tries to load even a small image or webpage:
* The request must travel from India → USA
* The response must travel back from USA → India


```bash
Your browser → sends request → USA web server
USA web server → sends response → back to India
```

* Even with high-speed fiber internet, crossing continents creates:
  * delay
  * slow loading
  * poor user experience
* Users far from the origin server always experience more delay.
* For example:
* Access speed comparison:

    | User Location    | Server in USA | Experience |
    | ---------------- | ------------- | ---------- |
    | USA user         | very fast     | ✔ great    |
    | India user       | slow          | ✘ delay    |
    | Nepal/Bangladesh | slow          | ✘ delay    |
    | Singapore        | moderate      | ✔ ok       |
    | Europe           | slow          | ✘ delay    |

* Even though internet speed is fast, physical distance always creates latency.
* This is because distance = latency.
* This is the exact “problem statement” CloudFront solves.

* What is Amazon CloudFront? (Simple Explanation)
    * Amazon CloudFront is a Global CDN (Content Delivery Network).
    * Simple Definition:
        * CloudFront caches and delivers your website’s:
            * images
            * videos
            * HTML pages
            * CSS/JS files
            * API responses
            * downloads
            * dynamic content
        * from the nearest AWS Edge Location, not from the main server.

---

* Edge Locations (The Key Idea of CloudFront)
  * AWS has hundreds of Edge Locations worldwide.
  * Think of an Edge Location as a mini AWS data center placed very close to users.
  * For example:
    * India has edge locations in:
      * Delhi
      * Mumbai
      * Hyderabad
      * Chennai (in some regions)
    * USA, Europe, Singapore, Dubai, Australia…
    * Everywhere there are multiple edge locations.
  * CloudFront uses these edge nodes to store copies of your content.

---

* Without CloudFront
```bash
User (India)
   |
   | long-distance request
   v
Origin Server (USA)
   |
   | long-distance response
   v
User
```

* Diagram – With CloudFront
```bash
User (India)
   |
   | short-distance request
   v
Nearest Edge Location (Delhi/Mumbai)
   |
   | fast high-speed AWS internal network
   v
Origin Server (USA)
```
* After first request:
```bash
User (India)
   |
   | request
   v
Edge Location (Delhi)
   |
   | returns cached copy instantly
   v
User
```

* **Explanation:**
* User visits the website
    * Request goes to Delhi Edge Location
    * Delhi checks: “Do I already have this file cached?”
    * If not cached → Delhi forwards the request to USA
    * USA sends the content to Delhi
    * Delhi forwards it to the user
    * Delhi stores a cached copy for next time
    * This first request is called a MISS FROM CLOUDFRONT.
    * Requests after first request is called a HIT FROM CLOUDFRONT.

---

* **Cache HIT vs MISS**

  * **CACHE MISS**
    * When the Edge Location does NOT have the file and must fetch it from the origin.
    * Occurs when:
        * First user accesses a file
        * Cache expired (TTL ended)
        * File never cached before
        * Cache invalidated
        * New version of file uploaded

```bash
User
 ↓
Edge Location → MISS → fetch from Origin
 ↓
Return to User + Cache it
```
* CloudFront response header:
```bash
X-Cache: Miss from cloudfront
```

  * **CACHE HIT**
    * When the Edge Location already has the content and returns it instantly.

```bash
User
 ↓
Edge Location → HIT → returns immediately
 ↓
User (fast)
```
Response header:
```bash
X-Cache: Hit from cloudfront
```
This is super fast because:
    * No round trip to USA
    * Response served from a server inside India
    * Latency becomes extremely low

---

* **Static Content vs Dynamic Content in CloudFront**
* CloudFront supports both:
    * Static content
    * Dynamic content

* Static Content Examples:
    * Images (PNG, JPG)
    * Videos
    * Audio
    * CSS
    * JavaScript
    * HTML files
    * PDFs
    * Documents
  * Static content benefits the most because caching improves performance.

* Dynamic Content Examples:
    * API calls
    * Personalized HTML
    * Login responses
    * User-specific content
    * Payment responses

* CloudFront doesn't always cache dynamic responses, but it still reduces latency because:
* CloudFront keeps a connection to the origin open
* Global AWS backbone is faster than public internet
* Even dynamic content is faster through CloudFront.

---

* **Large File Delivery Explained**
* When a large file (e.g., 1 GB) is stored in the Origin (USA) and a user in India requests it for the first time CloudFront does not wait for the complete file. As soon as the first few kilobytes arrive at the Edge, CloudFront immediately starts forwarding those bytes to the user.

* CloudFront streams the file in real-time:

```bash
Origin → Edge → User 
(Streaming simultaneously)
```

* Next user gets the same file instantly from Edge (HIT)

* First request (MISS)
```bash
X-Cache: Miss from cloudfront
```

* Second request (HIT)
```bash
X-Cache: Hit from cloudfront
```

---

* **How CloudFront Helps in SEO**
* Google prioritizes fast-loading websites in search results/rankings.
* Fast website = Better ranking = More traffic = More conversions.
* Google’s ranking signals include:
    * Largest Contentful Paint (LCP)
    * First Input Delay (FID)
    * Time To First Byte (TTFB)
    * Core Web Vitals Score

* CloudFront dramatically improves all of them.
    * Users receive content from nearest edge
    * Decreased latency
    * Faster load time
    * Faster cached responses
    * No waiting for distance between continents

* Therefore CloudFront is critical for:
    * Blogs
    * News websites
    * Affiliate marketing sites
    * Portfolio sites
    * Corporate websites
    * E-commerce sites

---

* **REAL-WORLD USE CASES FOR AMAZON CLOUDFRONT**
* CloudFront is not only for images. It accelerates websites, APIs, videos, downloads, and large-scale applications.
* The CDN reduces latency by serving content from the nearest edge.
* CloudFront is used in:
  - Static websites
  - Dynamic APIs
  - Video streaming
  - E-commerce
  - E-learning
  - Image-heavy sites
  - Large file distribution
* A versatile CDN for global performance.

```bash

# 1️⃣ STATIC WEBSITE ACCELERATION
# • Speeds up HTML, CSS, JS, images
# • Extremely low cost
# • Instant loading worldwide
# Ideal for: blogs, portfolios, business sites


# 2️⃣ DYNAMIC API ACCELERATION
# CloudFront also accelerates backend APIs.
#
# Useful for:
# • Login & authentication APIs
# • Payment APIs
# • Mobile app backends
# • ML / AI inference APIs
#
# Lower latency = smoother API experience.


# 3️⃣ VIDEO STREAMING (HUGE USE CASE)
# CloudFront supports:
# • On-demand video (like courses)
# • Live streaming
# • HLS / DASH protocols
#
# Perfect for:
# • Online classes
# • Webinars
# • OTT applications
# • Tutorials and training content


# 4️⃣ E-COMMERCE WEBSITES
# • Faster product image loading
# • Lower cart abandonment
# • Reduced server and DB load
#
# Speed directly increases sales.


# 5️⃣ E-LEARNING PLATFORMS  
# Example:
# • Students in US, Europe, India
# • Origin server in Delhi
# Without CDN → buffering
# With CloudFront → smooth playback
#
# Global students get equal performance.


# 6️⃣ IMAGE-HEAVY OR STATIC-HEAVY WEBSITES
# Photography, art, graphics, wallpapers.
# CloudFront is ideal for fast global delivery
# of static assets.


# 7️⃣ SOFTWARE DOWNLOADS
# Delivers large files quickly:
# • ZIP
# • EXE
# • APK
# • ISO
#
# Reduces server load and speeds up user downloads.

```
---

####  **Create Your First CloudFront Distribution (With EC2 Origin)**

###### **Step 1 — Prepare EC2 Web Server**

Launch an EC2 instance (Amazon Linux 2 / Ubuntu).
Install a web server (example: Nginx).

**Ubuntu commands:**
```bash
sudo apt update
sudo apt install nginx -y
```
Test in browser:
```
http://<EC2-Public-DNS>
```
You should see the default Nginx welcome page.

###### **Step 2 — Configure Security Group**
Allow inbound rules:

| Port | Protocol | Source    | Purpose                 |
| ---- | -------- | --------- | ----------------------- |
| 80   | HTTP     | 0.0.0.0/0 | Required for CloudFront |
| 443  | HTTPS    | 0.0.0.0/0 | Optional (if using SSL) |

CloudFront must be able to reach the EC2 web server.

## **Step 3 — Copy Your EC2 Public DNS**
Example:
```
ec2-13-233-122-45.ap-south-1.compute.amazonaws.com
```
**Important:**
Do **not** include `http://` or `https://`.
CloudFront accepts only the hostname.

## **Step 4 — Create CloudFront Distribution**
Navigate in AWS Console:
```
CloudFront → Create Distribution
```
### **Origin Settings**
Fill in the fields as follows:

| Field              | Value / Explanation                      |
| ------------------ | ---------------------------------------- |
| Origin Domain Name | Paste EC2 Public DNS                     |
| Protocol           | HTTP (if your server does not have SSL)  |
| Origin Path        | Optional (prefix to forward requests to) |
| Name               | Auto-filled or custom                    |

### **Understanding “Origin Path”**
If you set:
```
/gaurav
```
Then a CloudFront request:
```
https://xxxxx.cloudfront.net/dogs.txt
```
forwards internally to:
```
http://<EC2-DNS>/gaurav/dogs.txt
```

### **Custom Headers (Optional Security Feature)**
You can add a custom header to secure your origin:
Example:

| Header Name         | Header Value |
| ------------------- | ------------ |
| X-CloudFront-Secret | abc123       |

Your backend application (Node/Django/Spring Boot/etc.) should validate this header.

If a direct request hits EC2 without the secret header → reject the request.

(A complete origin security section is covered in later chapters.)


## **Step 5 — Cache Policy**
You may choose:
* AWS managed cache policy
  or
* A custom cache policy (used in the transcript example)

### **TTL Settings**
TTL values are always in **seconds**.
| TTL Type    | Meaning                                     |
| ----------- | ------------------------------------------- |
| Minimum TTL | Cache must exist for at least this duration |
| Default TTL | Typical caching duration                    |
| Maximum TTL | Cache will never exceed this duration       |

Example:
```
Default TTL: 3600   # 1 hour
```
This means CloudFront stores cached objects for one hour unless overridden by origin headers.


## **Step 6 — Web Application Firewall (Optional)**

WAF is optional.
It can be enabled later if security rules are needed.


## **Step 7 — Create the Distribution**

Click:
```
Create Distribution
```
You will see status:
```
Deploying
```
This means CloudFront is propagating the configuration to all edge locations globally.
Typical propagation time:
```
5–15 minutes
```
Once status becomes **Enabled**, your CloudFront distribution is live.

---

* **Why CloudFront Deployment Takes Time**
* AWS has 400+ edge locations globally.
* Your distribution settings must be copied to ALL of them.
```bash
Your settings
     ↓
AWS Global Control Plane
     ↓
Distributed to all CloudFront Edge Locations worldwide
```
* This replication takes time, but after that, your CDN is live everywhere.

---

#### **Testing Your CloudFront Distribution**
After your distribution shows:
```
Last Modified: <timestamp>
Status: Deployed
```
your CloudFront CDN is fully active.

###### **Step 1 — Copy the CloudFront URL**

Example:

```
https://d3j8ja8sa.cloudfront.net
```
Open this URL in your browser.

###### **Step 2 — Observe Response Headers**

* **First Request (Cache MISS)**
CloudFront does *not* have the object cached yet.
Response header:
```
X-Cache: Miss from cloudfront
```
This indicates:
    * CloudFront forwarded the request to your origin
    * Fetched the object
    * Delivered it to the user
    * Cached it at the edge location


###### **Second Request (Cache HIT)**
Now the object is already cached at the edge.
Response header:
```
X-Cache: Hit from cloudfront
```
This means:
    * CloudFront served the object instantly from the edge cache
    * No request was sent to the origin
    * Load time is much faster
    * Origin server load is reduced

---

#### **Understanding TTL (Time To Live) in CloudFront**
* TTL (Time To Live) controls **how long CloudFront keeps an object cached** at an edge location.
Every cached object has a lifetime, measured in **seconds**.
* CloudFront supports three TTL types:

###### **1. Minimum TTL**
* The **minimum duration** CloudFront must keep the object cached.
* CloudFront will *not* remove or refresh the object before this time, even if the origin marks it as expired.
* **Example:**
    ```
    Minimum TTL = 60 seconds
    ```
* For the first 60 seconds, CloudFront **must** serve the cached copy.
* No revalidation with the origin during this time.

###### **2. Default TTL**
* Used when the origin **does not specify** any cache-control headers.
* This is the **most important TTL** in CloudFront.
* **Example:**
    ```
    Default TTL = 3600   # 1 hour
    ```
* If the origin does not provide caching headers,
* CloudFront will store the object for **1 hour**,
* And serve it directly from cache during that time.

###### **3. Maximum TTL**
* The **upper limit** for how long CloudFront is allowed to keep an object.
* Even if the origin says:
    ```
    Cache-Control: max-age=864000
    ```
* CloudFront will **not** exceed your Maximum TTL.
* **Example:**
    ```
    Maximum TTL = 86400   # 24 hours
    ```
* Edge locations will never keep the object longer than 24 hours.
* After this time expires → CloudFront refetches from origin.

###### **How TTL Works Internally**
    ```
    Origin  ───→  Edge Cache  ───→  User
    1. Origin sends object to Edge.
    2. Edge stores it for TTL duration.
    3. Users are served directly from Edge.
    4. After TTL expires:
        Next request = MISS → object refetched from origin.
    ```

---

#### **Custom Cache Policy — Deep Explanation**
* A **Cache Policy** in CloudFront defines *how CloudFront should cache your content*.
* It decides exactly **what variations of a file** should be stored at the edge.
* A Cache Policy controls:
    * What headers CloudFront should cache based on
    * What cookies matter to caching
    * What query parameters affect caching
    * TTL rules
    * How dynamic/static content behaves at Edge

###### **Parameters of a Cache Policy**

| Setting           | Meaning                                                  |
| ----------------- | -------------------------------------------------------- |
| **TTL values**    | Controls how long objects stay cached                    |
| **Headers**       | Cache separate versions based on selected headers        |
| **Query Strings** | Cache different versions for different query parameters  |
| **Cookies**       | Cache different versions based on selected cookie values |

* Each parameter can drastically change how CloudFront serves or differentiates content.

###### **Caching Based on Query Parameters**
* Query parameters can change the meaning of a URL.
    ```
    example.com/products?id=10
    example.com/products?id=11
    ```
* If each ID corresponds to a **different product**, then CloudFront must treat them as **different cache keys**.
* **So you enable:**
```
Cache Based on Query Strings → Yes
Forward selected strings → id
```
* This ensures:
    * Each product page is cached separately
    * No cross-product mixing
* **Best for:** product pages, filters, searches, category pages.

###### **Caching Based on Headers**
* Headers change how content should be displayed.

* **Common headers used in cache keys:**
    * `Accept-Language`
    * `User-Agent`
    * `Authorization`

* **Example use cases:**

**1. Caching based on language**
    ```
    Accept-Language: en-US
    Accept-Language: fr-FR
    ```
* CloudFront stores **two versions** of the same URL:
    * English version
    * French version

**2. Caching based on device**
    ```
    User-Agent: Mobile Safari
    User-Agent: Chrome Desktop
    ```
* Used when you serve different layouts for mobile vs desktop.

**3. Caching based on Authorization**
* Only used when you have **public but personalized** objects.


###### **Caching Based on Cookies**
* Cookies often represent user-specific or session-specific data.
* Examples:
    * Country or region cookie
    * Theme preference (dark/light mode)
    * A/B testing cookie
    * Logged-in status cookie
* If your backend changes content based on a cookie,
CloudFront must cache per cookie value.
* **Example:**
    ```
    Cookie: theme=dark
    Cookie: theme=light
    ```
* CloudFront stores two separate cached versions.

---

#### **CloudFront for Dynamic Content**
* CloudFront is not only for static files.
* It also **accelerates dynamic content**, even when the content is **not cached**.

###### **How CloudFront Handles Dynamic Data**
* CloudFront does **not** cache all dynamic responses by default.
* However, it still speeds up dynamic traffic significantly.
* This means:
    * API calls
    * Login requests
    * Personalized pages
    * Search results
* can all become faster—even without caching.

###### **Why Dynamic Content Becomes Faster With CloudFront**
* Dynamic content is faster because of three core optimizations:

**1. Persistent Connections (Edge → Origin)**
* CloudFront maintains long-lived, persistent TCP connections to your origin.
* This eliminates slow TCP handshakes for every request.

**2. AWS Global Backbone Network**
* Requests travel over the AWS ultrafast global network instead of the public Internet.

**3. Reduced TTFB (Time to First Byte)**
* Even uncached dynamic responses show lower latency.
* Your APIs and dynamic pages respond faster for users worldwide.

###### **Dynamic Caching Is Also Possible**
* CloudFront can cache selected dynamic content by adjusting:
    * **Cache Policy**
    * **Allowed Headers**
    * **Allowed Cookies**
    * **Allowed Query Parameters**
* This allows caching of:
    * Product lists
    * Search results
    * API responses
    * Pre-rendered pages
    * Filtered data
* This is an advanced setup and must be configured carefully to avoid caching personal or user-specific content.

---

#### **How to Prevent Users from Accessing EC2 Directly (Very Important)**
  * A critical CloudFront + EC2 architecture requirement is:
  * **Users must NOT access EC2 directly.**
  * **Only CloudFront should be able to reach the EC2 origin.**
  * Example of what should be blocked:
    ```
    http://ec2-13-112-88-22.compute.amazonaws.com
    ```
  * This endpoint must *not* be publicly reachable by end users.

###### **Why This Matters**
  * Prevents bypassing CloudFront
  * Stops DDoS, brute force, bots from hitting EC2 directly
  * Protects origin from overload
  * Ensures caching works properly
  * Required in real interviews and production setups


###### **Solution 1 — Restrict EC2 to CloudFront IP Ranges (Best Practice)**
  * CloudFront uses specific AWS IP ranges for edge traffic.
  * AWS publishes all IP ranges here:
    ```
    https://ip-ranges.amazonaws.com/ip-ranges.json
    ```
  * Filter entries where:
    ```
    "service": "CLOUDFRONT"
    ```
  * **Steps**
    1. Open EC2 Security Group
    2. Remove this rule:
       ```
       HTTP 80 → 0.0.0.0/0     # REMOVE THIS
       ```
    3. Add inbound rules only for CloudFront CIDR blocks:
       Example:
       ```
       HTTP 80 → 54.182.0.0/16
       HTTP 80 → 204.246.164.0/22
       HTTP 80 → 70.132.0.0/18
       ...
       ```
       (You must add all CloudFront IPv4 ranges.)
  * **Result**

    | Source              | Allowed? |
    | ------------------- | -------- |
    | User → EC2 directly | ❌ No     |
    | CloudFront → EC2    | ✔ Yes    |
    | CDN works normally  | ✔ Yes    |

  * This is the **most recommended** production solution.

###### **Solution 2 — Custom Header Authentication (Simple & Effective)**
  * CloudFront lets you send a secret header to the origin.
  * **Step 1 — Add a custom header in CloudFront Origin Settings**
    * Example:
        ```
        Header Name: X-Origin-Secret
        Header Value: abcd1234
        ```
    * CloudFront sends this header with every request to EC2.

  * **Step 2 — Validate the header in your backend**
    * Pseudo-code:
        ```python
        if request.headers.get("X-Origin-Secret") != "abcd1234":
            return "Access Denied", 403
        ```
  * **Result**

    | Request Source      | Has Secret Header? | Outcome    |
    | ------------------- | ------------------ | ---------- |
    | User → EC2 directly | No                 | ❌ Rejected |
    | CloudFront → EC2    | Yes                | ✔ Allowed  |

  * This is extremely common in interviews.


###### **Solution 3 — Put EC2 in a Private Subnet (Highly Secure)**
* Enterprise-grade architecture:
    1. Move EC2 into a **private subnet**
    2. Remove the public IP
    3. Place an **Application Load Balancer (ALB)** in a public subnet
    4. Attach ALB → CloudFront as the origin
    5. EC2 is reachable only via ALB
    6. ALB Security Group only allows CloudFront IP ranges

* **Result**
  * EC2 is **not reachable** from the Internet
  * All traffic goes:
    ```
    User → CloudFront → ALB → EC2 (private subnet)
    ```
  * This is the **most secure** method.

---


#### **CloudFront Request/Response Headers**
  * CloudFront adds special HTTP headers to help you understand **how a request was processed**, whether it came from cache, and how old the cached object is.
  * These headers are extremely important for debugging and for interviews.

###### **1. `X-Cache` (Most Important Header)**
  * This tells you whether CloudFront served the object from cache or had to fetch it from the origin.
  * **Possible Values**

    | Value                        | Meaning                                                  |
    | ---------------------------- | -------------------------------------------------------- |
    | `Hit from cloudfront`        | Served directly from edge cache (very fast)              |
    | `Miss from cloudfront`       | Edge did not have object → fetched from origin → cached  |
    | `RefreshHit from cloudfront` | Cache was stale → revalidated with origin → served again |

  * **Examples**
  
    * **First request:**
        ```bash
        X-Cache: Miss from cloudfront
        ```
    * **Second request:**
        ```bash
        X-Cache: Hit from cloudfront
        ```

###### **2. `Via` Header**
  * Shows CloudFront edge processing path.
  * Example:
    ```bash
    Via: 1.1 abcdef.cloudfront.net (CloudFront)
    ```
  * Meaning:
    * The request passed through CloudFront
    * `abcdef` is the edge location identifier
    * Used for tracing and diagnosis

###### **3. `Age` Header**
  * Shows how long (in seconds) the object has been cached at the edge location.
  * Example:
    ```
    Age: 45
    ```
  * Meaning:
    * CloudFront cached this object **45 seconds ago**
    * Can be compared with TTL to understand expiry time

---

* **What is Origin Shield?**
* An additional centralized caching layer that reduces load on origin and increases cache HIT ratio.

---


---

#### Make EC2 / ALB Accessible Only from CloudFront

* Problem
    * Anyone on the internet can access your EC2/ALB directly even cloudfront placed in front of it.
    * This breaks security, caching, cost optimization

* Outcome
    * Only CloudFront should access EC2/ALB
    * Direct browser access must be blocked

* Edge locations
  * https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/LocationsOfEdgeServers.html
  * https://ip-ranges.amazonaws.com/ip-ranges.json
  * https://docs.aws.amazon.com/vpc/latest/userguide/working-with-aws-managed-prefix-lists.html#available-aws-managed-prefix-lists

* There are 2,000+ CloudFront IP ranges
* Put them into Security Groups
* They change every week
* You cannot maintain it manually
* Terraform/Ansible scripts will run repeatedly

* Other approaches
    * Terrform
    * Scripting
    * Python
    * Ansible

* Best approaches
    * Use AWS-Managed Prefix List: "com.amazonaws.global.cloudfront.origin-facing".
    * AWS internally maintains a PREFIX LIST containing all CloudFront IP ranges managed by AWS..
    * It is always up-to-date.
    * You simply attach this prefix list to your EC2/ALB security group.

    ```bash
    AWS Console → VPC → Prefix Lists
    ```
    ```bash
    com.amazonaws.global.cloudfront.origin-facing
    ```
    Copy the Prefix List ID, e.g.:
    ```bash
    pl-1234567890abcdef
    ```

    Go to EC2 security group:
    ```bash
    sg-mywebserver
    ```
    Add this in inbound rules
    Do same with ALB SG

    Remove Existing “ALLOW 0.0.0.0/0” Rule

    CLEAR CLOUDFRONT CACHE
    ```bash
    CloudFront → Distribution → Invalidations → Create Invalidation
    ```
    ```bash
    /*
    ```

    Test direct access (blocked)
    Test CloudFront access (working)

```bash
           +----------------+
Client --> | CloudFront CDN | ---> Allowed IPs Only ----> EC2/ALB
           +----------------+
                    |
                Allowed
                    |
       +--------------------------------+
       | Prefix List: CloudFront IP Set |
       +--------------------------------+

Direct Access:
Client ----X----> EC2      (BLOCKED)
Client ----X----> ALB      (BLOCKED)
```