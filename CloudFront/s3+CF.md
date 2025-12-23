* Block Public access.
* Private bucket.
* Making S3 accessible only through CloudFront.
* Using Origin Access Identity (OAI)
* Using Origin Access Control (OAC) – latest AWS recommended method
* Signed URLs / Signed Cookies
* Permissions, caching, invalidations
* CloudFront only must have permission to fetch objects
* Users must never get S3 URLs directly

* Problems with Public S3:
  * Anyone can access the bucket directly
  * High latency for users far from AWS region
  * No caching → slow repeated requests
  * No security layer
  * No geographic acceleration

* CloudFront fixes everything:
  * Caches S3 content in global edge locations
  * Reduces latency drastically
  * Keeps S3 private
  * Only CloudFront can fetch objects
  * S3 is hidden from public

* Architecture
    ```bash
    Client → CloudFront → S3 (private)
    ```

#### Steps

* **CREATE S3 BUCKET (PRIVATE)**
    * Disable public access
    * Don’t create any public bucket policy
    * Don’t enable static website hosting (CloudFront handles the website)
    * Upload files normally (images, HTML, JS, videos, PDFs)

* **CREATE CLOUDFRONT DISTRIBUTION**
    * Select origin --> S3 bucket
    
* **ENABLE OAC (Origin Access Control)**
    * Securely allow CloudFront to access your S3 bucket – recommended for all new CloudFront distributions.
    * OAC is the new and improved way to securely connect CloudFront to an Amazon S3 bucket.
    * It replaces the older Origin Access Identity (OAI) method.
    * With OAC:
        * Your S3 bucket is private
        * Users cannot directly access S3 URLs
        * Only CloudFront is allowed to access objects
        * CloudFront signs requests using AWS Signature Version 4 (SigV4)
        * This ensures maximum security and prevents bypassing CloudFront.
    ```bash
    -> CloudFront Console 
    -> Create Distribution 
    -> Choose Origin Access → “Origin Access Control (OAC)”
    -> You will see an option:
         • Public
         • Origin Access Control (recommended)
    -> Create control setting
        Fill:
        * Name → e.g., my-oac
        * Signing Protocol → SigV4
        * Signing Behavior → Sign requests
    -> This tells CloudFront:
        * Every request to S3 must be authenticated
        * CloudFront signs each request using SigV4
        * Your bucket will accept only signed requests
    -> Click Create.
    ```

* **Attach OAC to Your Origin**
  * After creating the OAC, select it in:
    ```bash
    Origin Access → OAC
    ```
  * You will now see the OAC name attached to your S3 origin.
  * After attaching the OAC:
    * CloudFront will now automatically sign all requests
    * S3 bucket will accept only requests signed by CloudFront
  * Click Create Distribution.


* **What Happens Internally When OAC is Enabled?**
  * When CloudFront accesses S3:
    * CloudFront creates a SigV4-signed request
    * S3 verifies the signature
    * S3 checks the bucket policy
    * If signature + policy are valid → object is returned
    * If not valid → 403 Access Denied
  * This ensures:
    * Users cannot access S3 URLs directly
    * Only CloudFront can retrieve objects

* **You MUST Update the S3 Bucket Policy**
  * After enabling OAC, CloudFront shows a message:
    ```bash
    Update your S3 bucket policy to allow CloudFront OAC access.
    ```
  * It also provides a JSON policy like:
    ```json
    {
    "Version": "2012-10-17",
    "Statement": [
        {
        "Sid": "AllowCloudFrontServicePrincipalReadOnly",
        "Effect": "Allow",
        "Principal": {
            "Service": "cloudfront.amazonaws.com"
        },
        "Action": "s3:GetObject",
        "Resource": "arn:aws:s3:::my-bucket/*",
        "Condition": {
            "StringEquals": {
            "AWS:SourceArn": "arn:aws:cloudfront::123456789012:distribution/EXAMPLEID"
            }
        }
        }
    ]
    }
    ```
    ```bash
    S3 Bucket → Permissions → Bucket Policy
    ```
 
* **TEST ACCESS**
    ```bash
    #Direct S3 URL:
    https://mybucket.s3.amazonaws.com/image.png
    #You get:
    #Access Denied

    #CloudFront URL:
    https://d123abcd.cloudfront.net/image.png
    #Works perfectly.
    ```

---

```
my-demo-site/
│
├── index.html
├── style.css
│
├── images/
│     └── demo.jpg
│
└── videos/
      └── sample.mp4

```
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>S3 Demo Website</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <h1>Welcome to My S3 Demo Website</h1>
    <p>This website is hosted on Amazon S3.</p>

    <h2>Demo Image</h2>
    <img src="images/demo.jpg" alt="Demo Image" width="500">

    <h2>Demo Video</h2>
    <video width="600" controls>
        <source src="videos/sample.mp4" type="video/mp4">
        Your browser does not support HTML5 video.
    </video>

</body>
</html>
```
```css
body {
    font-family: Arial, sans-serif;
    max-width: 800px;
    margin: 40px auto;
    padding: 20px;
    text-align: center;
}

img {
    margin-top: 10px;
    border-radius: 8px;
    border: 2px solid #ddd;
}

video {
    margin-top: 10px;
    border: 2px solid #ccc;
    border-radius: 8px;
}
```
```
images/demo.jpg
videos/sample.mp4
```