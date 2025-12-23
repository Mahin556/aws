#### CloudFront Invalidation (Complete Guide)
  * CloudFront is a global CDN.
  * It caches your content at **edge locations** worldwide for fast delivery.
  * But sometimes:
    * You update/change a file on your EC2/S3 origin
    * CloudFront **still shows the OLD version**
    * Because CloudFront is serving the **cached copy** from edge
  * This is normal caching behavior.
  * To remove or refresh this old content/cache from all AWS edge locations, we can use **CloudFront Invalidation**

* **Why Invalidation Is Needed? (Simple Example)**

1. Your EC2 server page originally showed:
```
Welcome to nginx
```

2. You updated your EC2 HTML file using:
```bash
echo "This is Gaurav Sharma" > /var/www/html/index.html
```

3. Accessing EC2 directly → shows the **new** content:
```
This is Gaurav Sharma
```

4. But accessing CloudFront URL → still shows **old** content:
```
Welcome to nginx
```

And response header is:
```
X-Cache: Hit from cloudfront
```
This means:
* CloudFront Edge Location still has the **old cached copy**
* Even though origin has been updated
* This scenario is extremely common in real-world environments.

* **How CloudFront Caching Creates This Problem**
* CloudFront caches content for a specific period (TTL).
* When CloudFront receives a request:
```
Edge Location:
   If it has cached content → return it (HIT)
   If not → fetch from origin → cache → return (MISS)
```
* If the content already exists in cache (HIT), CloudFront will **NOT** fetch the updated version from EC2 until:
  * The TTL expires, OR
  * Origin instructs new caching headers, OR
  * **You manually invalidate the cache**

* **What Is CloudFront Invalidation? (Perfect Definition)**
* Invalidation removes outdated cached objects from all CloudFront edge locations immediately.
* After invalidation:
  * Next request is forced to go to origin (EC2/S3)
  * Fresh updated content is fetched
  * Edge stores the updated copy again

* **How to Perform CloudFront Invalidation (Step-by-Step)**

* Step 1 – Open CloudFront Console
Go to:
```
AWS Console → CloudFront → Distributions
```
Select your CloudFront Distribution.

* Step 2 – Click on “Invalidations” Tab
You will see a section like:
```
Invalidations
Create Invalidation
```

* Step 3 – Create a New Invalidation
Click:
```
Create Invalidation
```
You will see a field asking:
```
Enter paths
```
This tells CloudFront which files to remove from cache.

* **Most Important Part: What Path Should You Enter?**
* CloudFront invalidates **paths**, not files.
    * Invalidate EVERYTHING
        ```
        /*
        ```
    * This will delete **all** files cached at all edge locations.
        * Recommended after major deploy
        * Clears entire CDN cache
        * Fast and simple

    * Invalidate only specific folder
    * Example: only `images/` folder changed:
    `    ```
        /images/*
        ````

    * Invalidate only one file
    * Example: index.html updated:
        ```
        /index.html
        ```
        Or:
        ```
        /app/home.css
        ```
        * CloudFront invalidation allows up to:
            * 1,000 paths free per month
            * After that: small cost


* Step 4 – Create Invalidation
    Click:
    ```
    Invalidate
    ```
    You will see the status:
    ```
    In Progress
    ```
    After some time:
    ```
    Completed
    ```
    Invalidation is now complete.


* **What Happens Internally During Invalidation?**
  * When you invalidate `/index.html` or `/*`:
  * CloudFront Marks Cached Object As “Expired”
        ```
        Edge Location:
        Mark /index.html = STALE
        ```
  * On next request:
        ```
        User → Edge
        Edge → detects object is invalidated
        Edge → sends request to Origin (EC2)
        EC2 → returns updated version
        Edge → caches new version
        User → receives new content
        ```

  * The next request will show:
        ```
        X-Cache: Miss from cloudfront
        ```
  * Then second request will show:
        ```
        X-Cache: Hit from cloudfront
        ```

 
* **Cost of Invalidation**
    AWS provides:
    * **1,000 invalidation paths free per month**
    After that:
    * **$0.005 per path**
    Using `/*` counts as **1 path**.
    This is why many companies use `/*`—cheap and simple.
