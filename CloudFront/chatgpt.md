Great — I’ll continue with the **practical, production-ready next part** you asked for. Below you’ll find:

* Terraform automation to create **S3 (private) + CloudFront distribution with Origin Access Control (OAC)** and the **bucket policy** that allows CloudFront only.
* How to create **CloudFront Signed URLs / Signed Cookies** (concept + step-by-step + code snippets to generate signed URLs).
* Example **AWS WAF** rules to attach to CloudFront (common protections).
* How to wire **CloudFront → ALB → ECS/EC2** for hybrid apps (architecture + settings).
* Short checklist & testing steps.

I keep things clear and copy-paste ready. If you want any of these as Terraform modules, CloudFormation, or a runnable script, tell me and I’ll produce it.

---

# 1) Terraform: Private S3 + CloudFront (OAC) + Bucket Policy

This example assumes AWS provider v4+ (Terraform). It creates:

* private S3 bucket (no public access),
* CloudFront Origin Access Control (OAC),
* CloudFront distribution using that OAC,
* bucket policy to allow only that CloudFront distribution.

Save as `main.tf`. **Update** `region`, `account_id`, `certificate_arn` (if you want HTTPS custom domain), and `allowed_cnames` as needed.

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"        # CloudFront control-plane region can be any; S3 bucket region can differ.
}

# 1. Create private S3 bucket
resource "aws_s3_bucket" "site" {
  bucket = "my-private-site-bucket-12345"  # choose globally unique name
  acl    = "private"

  versioning {
    enabled = false
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

# Block all public access
resource "aws_s3_bucket_public_access_block" "site" {
  bucket = aws_s3_bucket.site.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# 2. Create CloudFront Origin Access Control (OAC)
resource "aws_cloudfront_origin_access_control" "oac" {
  name                      = "oac-s3-access"
  description               = "OAC for CloudFront -> S3 private bucket"
  origin_access_control_origin_type = "s3"
  signing_behavior         = "always"      # sign requests
  signing_protocol         = "sigv4"
}

# 3. Create CloudFront distribution
# NOTE: For production you will want behaviours, logging, WAF, certificate etc.
resource "aws_cloudfront_distribution" "cdn" {
  enabled = true

  origin {
    domain_name = aws_s3_bucket.site.bucket_regional_domain_name
    origin_id   = "s3-${aws_s3_bucket.site.id}"

    s3_origin_config {
      # empty for OAC usage
    }

    origin_access_control_id = aws_cloudfront_origin_access_control.oac.id
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "s3-${aws_s3_bucket.site.id}"

    viewer_protocol_policy = "redirect-to-https"

    # use managed caching policy or define your own
    cache_policy_id = "658327ea-f89d-4fab-a63d-7e88639e58f6" # Managed-CachingOptimized
    # OR create custom response/header/policy resources and reference IDs

    # forward nothing unless required (minimize cache fragmentation)
    origin_request_policy_id = "216adef6-5c7f-47e4-b989-5492eafa" # Managed-AllViewerExceptHostHeader
  }

  price_class = "PriceClass_100" # choose price class
  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
    # For custom domain use acm_certificate_arn and ssl_support_method = "sni-only"
    # acm_certificate_arn = var.certificate_arn
    # ssl_support_method = "sni-only"
  }

  # Optional: default root object
  default_root_object = "index.html"

  tags = {
    Project = "PrivateS3WithCloudFront"
  }
}

# 4. Bucket policy allowing CloudFront OAC (only this distribution)
data "aws_caller_identity" "me" {}

resource "aws_s3_bucket_policy" "allow_cloudfront" {
  bucket = aws_s3_bucket.site.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid = "AllowCloudFrontServicePrincipal"
        Effect = "Allow"
        Principal = {
          Service = "cloudfront.amazonaws.com"
        }
        Action = "s3:GetObject"
        Resource = "${aws_s3_bucket.site.arn}/*"
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = aws_cloudfront_distribution.cdn.arn
          }
        }
      }
    ]
  })
}
```

Notes & tips:

* Terraform `aws_cloudfront_origin_access_control` resource creates OAC which signs requests with SigV4.
* The bucket policy uses `AWS:SourceArn` to restrict to that CloudFront distribution only.
* If you use a custom domain, add `viewer_certificate` with ACM cert (in us-east-1 for CloudFront).
* After apply, upload files to the S3 bucket (private). Access via CloudFront domain, not S3 URL.
* If CloudFront returns `AccessDenied`, check the bucket policy `SourceArn` vs distribution ARN and that the distribution is deployed.

---

# 2) Generating CloudFront Signed URLs and Signed Cookies

Use cases:

* Private/premium content (videos, downloads)
* Time-limited access to specific users

Important concepts:

* You create a CloudFront key pair / public key & private key (or use Key Groups).
* You embed a signature and expiry in the URL (signed URL) or set it in cookies (signed cookies).
* CloudFront verifies signature and expiry before forwarding to origin.

## High-level steps (console)

1. Create a **CloudFront key pair** for signing (older method: AWS account key pair; newer: CloudFront Key Group with public key).
2. Create a Key Group and associate the public key.
3. Attach the Key Group to CloudFront behavior (Trusted Key Groups) for the paths that require signed access.
4. Generate signed URLs (server-side) using the private key. Return signed URL to user.

## Recommended (modern) approach: Key Group + Public Key

* Create **CloudFront Public Key** (upload your public key).
* Create **Key Group** which includes that public key.
* In CloudFront behavior, set **Trusted Key Groups** and require signed URLs.

## Example: Generate a signed URL (Node.js example using `aws-cloudfront-sign` npm package)

Install: `npm install aws-cloudfront-sign`

```js
const { getSignedUrl } = require("aws-cloudfront-sign");

// path to your private key PEM (generated with openssl)
const privateKey = require('fs').readFileSync('./private_key.pem', 'utf8');

const policy = {
  Statement: [
    {
      Resource: "https://d111111abcdef8.cloudfront.net/private/*",
      Condition: {
        DateLessThan: { "AWS:EpochTime": Math.floor(Date.now()/1000) + 60*60 } // 1 hour
      }
    }
  ]
};

const options = {
  keypairId: "APKAXXXXXXX",   // Key Pair ID or CloudFront key id (for old method)
  privateKeyString: privateKey,
  policy: JSON.stringify(policy)
};

const signedUrl = getSignedUrl("https://d111111abcdef8.cloudfront.net/private/video.mp4", options);
console.log("Signed URL:", signedUrl);
```

Notes:

* The exact library and API may differ; the concept is: sign a policy or canned policy with your private key and return the tokenized URL.
* For production, issue on server side (not client); set short expiry and optionally IP restriction.

## Signed Cookies

* Use signed cookies when you must authorize user to access multiple files (e.g., all URLs under `/videos/*`).
* Generate cookies (CloudFront-Key-Pair-Id, CloudFront-Policy or CloudFront-Signature) and set them in the browser for the domain. CloudFront checks the cookie for each request.

---

# 3) AWS WAF + CloudFront (recommended protections)

Attach a WAF Web ACL to your CloudFront distribution to protect against common attacks. You can create managed rules and custom rules.

Example protections:

* AWS Managed Rules (Bot Control, Known Bad Inputs)
* Geo blocking (block entire countries)
* Rate limiting (requests per minute)
* SQLi / XSS detection

## Sample Terraform snippet for WAFv2 (basic)

```hcl
resource "aws_wafv2_web_acl" "cloudfront_acl" {
  name        = "cloudfront-acl"
  description = "Basic WAF for CloudFront"
  scope       = "CLOUDFRONT"

  default_action {
    allow {}
  }

  rule {
    name     = "AWS-AWSManagedRulesCommonRuleSet"
    priority = 1

    override_action {
      none {}
    }

    statement {
      managed_rule_group_statement {
        name = "AWSManagedRulesCommonRuleSet"
        vendor_name = "AWS"
      }
    }
    visibility_config {
      cloudwatch_metrics_enabled = true
      sampled_requests_enabled   = true
      metric_name                = "AWSManagedRulesCommonRuleSet"
    }
  }

  # Example rate limit rule
  rule {
    name     = "rate-limit"
    priority = 10
    action {
      block {}
    }
    statement {
      rate_based_statement {
        limit = 2000
        aggregate_key_type = "IP"
      }
    }
    visibility_config {
      cloudwatch_metrics_enabled = true
      sampled_requests_enabled   = true
      metric_name = "rate-limit"
    }
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    sampled_requests_enabled   = true
    metric_name                = "cloudfront-acl"
  }
}
```

Attach to CloudFront by referencing the WAF arn in the CloudFront distribution configuration (`web_acl_id`).

---

# 4) CloudFront + ALB (Origin) — Architecture & key settings

Use this when your origin is dynamic (ECS, EC2, Kubernetes) or you want TLS at ALB and route-based behaviours.

Architecture:

```
User
  ↓
CloudFront (Behaviors + WAF)
  ↓
ALB (HTTPS)
  ↓
ECS / EC2 (app servers)
```

Key points:

* Use **HTTPS** between CloudFront and ALB (viewer_protocol_policy: redirect-to-https; origin protocol policy: https only).
* ALB should **allow traffic only from CloudFront** — use Prefix List `com.amazonaws.global.cloudfront.origin-facing` in the ALB Security Group inbound rule (or prefix-list ID).
* For ALB origin, set CloudFront Origin Domain Name to ALB DNS (no `http://`).
* Use stickiness / session if needed at ALB/ECS.
* If different paths need to bypass cache (`/api/*`) create a CloudFront behavior for `/api/*` with `CachePolicy: CachingDisabled` (forward all headers and cookies) and `origin_request_policy` to forward necessary headers.

Example CloudFront behavior:

* Behavior `/static/*`: cache long TTL, compress, serve from S3
* Behavior `Default (*)`: forward to ALB, cached minimally or not at all
* Behavior `/api/*`: CachePolicy = CachingDisabled; OriginRequestPolicy to forward Authorization header

Security recommendations:

* ALB in private subnets with no public IPs, ALB fronted by CloudFront. If ALB must be public, restrict inbound SG to CloudFront prefix list.
* Use TLS termination at ALB, mutual TLS if required.

---

# 5) Invalidation Automation & CI/CD

* On deploy (CI pipeline), after uploading new assets to S3, run a CloudFront invalidation for changed paths or use versioned filenames to avoid invalidation. Invalidation can be automated via AWS CLI:

Example CLI:

```bash
# invalidate everything (counts as 1 path)
aws cloudfront create-invalidation --distribution-id E123ABCD --paths "/*"

# invalidate specific file(s)
aws cloudfront create-invalidation --distribution-id E123ABCD --paths "/index.html" "/css/app.css"
```

* Prefer **cache-busting** (file name contains hash) in front-end builds so you avoid many invalidations and get better cache efficiency.

---

# 6) Testing & Troubleshooting Checklist

* After deploy + invalidation:

  * Curl CloudFront URL with headers:

    ```bash
    curl -I https://d111111abcdef8.cloudfront.net/index.html
    ```

    Check `X-Cache` header (Miss → then Hit).
* If `AccessDenied`:

  * Check S3 bucket policy `AWS:SourceArn` matches distribution ARN.
  * Confirm OAC created and distribution `origin_access_control_id` is set.
* If direct S3 URL still accessible:

  * Confirm S3 public access block settings & no public bucket policy/ACL; test anonymous request.
* For only CloudFront access to ALB/EC2:

  * Confirm SG inbound allows only CloudFront prefix list (use AWS-managed prefix list ID), not `0.0.0.0/0`.
* For signed URLs failing:

  * Ensure KeyGroup/PublicKey is attached as trusted key group in CloudFront behavior.
  * Private key used to sign must match public key in CloudFront.

---

# 7) Short Best-Practices Summary

* Keep S3 buckets private; use CloudFront OAC (SigV4).
* Avoid `/*` invalidations frequently — use asset versioning.
* Use Key Group + signed URLs for paid/protected content.
* Use AWS-managed prefix list for CloudFront origin-facing access in SG rules — don’t hardcode IPs.
* Attach WAF to CloudFront for production-grade protection.
* Use separate CloudFront behaviors for static (long TTL) and dynamic (no cache) content.
* Always use HTTPS viewer and origin protocol for production.

---

If you want, I’ll now:

* produce a **ready-to-run Terraform module** that includes CloudFront OAC, S3, WAF + sample ALB origin and CI invalidation hook; **or**
* produce **Node.js** and **Python** code examples for generating signed CloudFront URLs (complete with key generation and usage); **or**
* draw **detailed ASCII or PNG diagrams** for each architecture (CloudFront+S3, CloudFront+ALB, CloudFront+Signed-URLs).

Which of those should I do next?


---

Below is a **complete, crystal-clear, production-ready guide** on **CloudFront Path-Based Routing with Multiple Origins** — including theory, diagrams, best practices, and **full YAML + Terraform examples** so you can implement it immediately.

---

# ✅ **What Is CloudFront Path-Based Routing?**

CloudFront allows you to create **multiple origins** (S3, EC2, ALB, API Gateway, MediaStore, etc.) and **route traffic to each origin based on URL path patterns**.

Examples:

| Path Pattern  | Origin Target |
| ------------- | ------------- |
| `/static/*`   | S3 bucket     |
| `/app/*`      | EC2/ALB       |
| `/api/*`      | API Gateway   |
| `/video/*`    | MediaStore    |
| `*` (default) | EC2 backend   |

CloudFront checks incoming requests → matches the **longest / most specific path rule** → forwards to correct origin.

---

# 📘 **How It Works (Simple Diagram)**

```
                 🌍 Users 
                     |
                CloudFront
         ┌──────────┼──────────┐
         │          │           │
   /static/*     /api/*       /*
     (S3)       (API GW)    (ALB)
```

CloudFront Behavior Engine:

1. Match **longest pattern**
2. Apply viewer request policy (headers, cookies)
3. Decide cache or not
4. Forward to chosen origin

---

# 🎯 **Typical Real-World Use Case**

### **E-commerce site**

* Static UI → served from S3
* APIs → served from ALB/ECS or API Gateway
* Images → served from another S3 bucket
* Video → CloudFront MediaPackage

### **DevOps/Platform**

* Route `/docs/*` → S3 Docs bucket
* Route `/app/*` → Backend microservice
* Route `/auth/*` → Cognito hosted UI

---

# 🔥 **FULL STEP-BY-STEP WORKING EXAMPLE**

We will create:

* **Origin #1 → S3 bucket** (static files)
* **Origin #2 → ALB** (application backend)
* **Origin #3 → API Gateway** (REST API)

Routing rules:

| Path                   | Origin |
| ---------------------- | ------ |
| `/static/*` → S3       |        |
| `/api/*` → API Gateway |        |
| Default `/*` → ALB     |        |

---

# ☑️ **CloudFront Console: Steps**

### **Step 1: Create All Origins**

In CloudFront > Distribution > Origins:

#### Origin 1: S3

```
S3 bucket: my-static-assets
Origin ID: S3-static
```

#### Origin 2: ALB

```
Domain: myapp-alb-123.us-east-1.elb.amazonaws.com
Origin ID: ALB-app
Protocol: HTTPS only
```

#### Origin 3: API Gateway

```
Domain: abc123.execute-api.us-east-1.amazonaws.com
Origin ID: API-gateway
Origin Path: /prod
```

---

### **Step 2: Create Behaviors (Routing Rules)**

#### Behavior 1 → `/static/*`

```
Path Pattern: /static/*
Origin: S3-static
Cache Policy: CachingOptimized
```

#### Behavior 2 → `/api/*`

```
Path Pattern: /api/*
Origin: API-gateway
Cache Policy: CachingDisabled
Forward all headers/cookies
```

#### Behavior 3 → Default (`*`)

```
Path Pattern: *
Origin: ALB-app
Cache Policy: CachingDisabled
```

---

# 🧨 **VERY IMPORTANT — ORDER MATTERS**

CloudFront matches rules **top → down**, longest first.

Correct order:

```
1 → /static/*
2 → /api/*
3 → *
```

Incorrect order:

```
* on top breaks routing
```

---

# ✔️ FULL TERRAFORM EXAMPLE

(You can copy-paste and deploy)

This Terraform configuration uses 3 origins and 3 behaviors.

---

### **Terraform: Multiple Origins + Path-Based Routing**

```hcl
resource "aws_cloudfront_distribution" "multi" {
  enabled = true
  default_root_object = "index.html"

  # ------------------------
  # ORIGIN 1 - S3 (Static)
  # ------------------------
  origin {
    domain_name = aws_s3_bucket.static.bucket_regional_domain_name
    origin_id   = "S3-Static"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.oai.cloudfront_access_identity_path
    }
  }

  # ------------------------
  # ORIGIN 2 - ALB Backend
  # ------------------------
  origin {
    domain_name = aws_lb.app_dns_name
    origin_id   = "ALB-App"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
    }
  }

  # ------------------------
  # ORIGIN 3 - API Gateway
  # ------------------------
  origin {
    domain_name = aws_api_gateway_rest_api.api.execution_arn
    origin_id   = "API-GW"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
    }

    origin_path = "/prod"
  }

  # -------------------------------
  # BEHAVIOR 1: /static/*
  # -------------------------------
  ordered_cache_behavior {
    path_pattern     = "/static/*"
    target_origin_id = "S3-Static"

    viewer_protocol_policy = "redirect-to-https"
    cache_policy_id        = "658327ea-f89d-4fab-a63d-7e88639e58f6" # CachingOptimized
  }

  # -------------------------------
  # BEHAVIOR 2: /api/*
  # -------------------------------
  ordered_cache_behavior {
    path_pattern     = "/api/*"
    target_origin_id = "API-GW"

    viewer_protocol_policy = "redirect-to-https"
    cache_policy_id        = "413f12a3-34f8-4e7e-9f95-58e37e249003" # CachingDisabled
  }

  # -------------------------------
  # BEHAVIOR 3: DEFAULT (*)
  # -------------------------------
  default_cache_behavior {
    target_origin_id       = "ALB-App"
    viewer_protocol_policy = "redirect-to-https"
    cache_policy_id        = "413f12a3-34f8-4e7e-9f95-58e37e249003"
  }

  price_class = "PriceClass_100"

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}
```

---

# ⭐ Best Practices (VERY IMPORTANT)

✔ **Always create specific paths before wildcard**
CloudFront matches longest path.

✔ **Do not cache APIs**
APIs must have:

* CachePolicy: `CachingDisabled`
* OriginRequestPolicy: forward Authorization headers

✔ **Use S3 + OAC for `/static/*`**
OAC = latest secure method replacing OAI.

✔ **Enable compression**
Serve Gzip/Brotli.

✔ **Use different origins for dynamic & static**
This reduces latency and cost.

✔ **For React/Angular/Vue SPAs**
Route everything to S3 except `/api/*`.

✔ **For security**

* Attach WAF to CloudFront
* Restrict ALB to CloudFront prefix list
* Make S3 bucket private

---

# 🧪 Testing Commands (CLI)

```
curl -I https://d123.cloudfront.net/static/logo.png
→ should come from S3

curl -I https://d123.cloudfront.net/api/health
→ should hit API Gateway

curl -I https://d123.cloudfront.net/dashboard
→ should go to ALB
```

---

# 🎁 Want More?

I can also provide:

✅ **Architecture Diagrams (PNG/ASCII)**
✅ **Terraform Module for Multiple Origins**
✅ **Complete Project: React UI (S3) + Node API (ALB) + Auth API (API Gateway)**
✅ **Signed URLs for specific origin paths only**
✅ **CloudFront + Lambda@Edge + Rewrite/Redirect rules**
✅ **Kubernetes (EKS) backend behind CloudFront**

Just tell me **"Give me complete architecture example"**, and I’ll generate everything.


---

Below is the **complete, detailed explanation** of the transcript you gave — **CloudFront Path-Based Routing with Multiple Origins (S3 + EC2)** — in very simple English, but extremely deep and production-level.

This covers exactly what Gaurav explains in his video:
✔ Why path-based routing
✔ How CloudFront behaves
✔ How to configure it (step-by-step)
✔ How S3 & EC2 origins work
✔ Behaviour rules
✔ Cache interactions
✔ Edge-case warnings
✔ Full working example
✔ Debugging behavior
✔ Final validation & testing

---

# ✅ **Concept: CloudFront Path-Based Routing With Multiple Origins**

CloudFront allows you to:

* Create **multiple origins** inside ONE distribution.
* Send requests to **different origins** based on the URL path pattern.

✔ Example logic from video:

```
If URL starts with /s3      → go to S3 bucket  
If URL starts with /api     → go to EC2 instance  
Everything else (*)         → go to EC2 instance (default origin)
```

This is called:

### 🟢 **Path-Based Routing (Behavior Rules)**

Where CloudFront checks:

1. Request URL
2. Matches against path rules
3. Sends request to correct origin

---

# ⭐ Why CloudFront Needs Multiple Origins?

Typical real-world use case:

* **Static files** stored in S3
* **APIs** served from EC2 or ALB
* **Images & media** stored in S3
* **Dynamic HTML / backend** served from EC2

CloudFront helps combine all of them behind a **single CDN URL**.

---

# 🚀 Step-by-Step Guide (Exactly like in the video)

Below is the **entire logic explained line-by-line**.

---

# STEP 1️⃣ — Create CloudFront Distribution (with first origin)

When creating a new distribution from console, CloudFront forces you to add only **one origin** during creation.

Gaurav added:

* **Origin #1 → EC2 instance**
* Protocol: HTTP only (because EC2 is not using SSL)

CloudFront URL will look like:

```
d12345.cloudfront.net
```

If you visit:

```
https://d12345.cloudfront.net
```

CloudFront takes that request → sends to EC2 instance.

This is the **default behavior**.

---

# STEP 2️⃣ — Add Second Origin (S3 Bucket)

After distribution is created → go to:

**CloudFront → Distribution → Origins → Add Origin**

Select:

```
Origin Type: S3 bucket
Bucket: your-private-bucket
```

Because S3 bucket is **private**, CloudFront forces you to use:

### ✔ OAC (Origin Access Control)

This ensures:

* Nobody from public internet can access S3
* Only CloudFront can access S3
* Zero public bucket access

CloudFront generates a policy → you copy it.

Paste this into:

```
S3 → Permissions → Bucket Policy
```

Now CloudFront can read your S3 files.

---

# STEP 3️⃣ — Create Path-Based Behaviors

Now go to:

**Behaviors → Create Behavior**

### Behavior 1

```
Path Pattern: /api/*
Origin: EC2 instance
```

This means:

```
d123.cloudfront.net/api/index.html
→ goes to EC2 instance
```

### Behavior 2

```
Path Pattern: /images/*
Origin: S3 bucket
```

So:

```
d123.cloudfront.net/images/1.png
→ served from S3 bucket
```

### Default Behavior

```
Path Pattern: *
Origin: EC2 instance
```

This catches every request that does not match other rule.

---

# 🧠 Why Order Matters?

CloudFront processes behaviors in **priority order**:

1. Longest pattern first
2. Then specific prefixes
3. Wildcard (*) is last

Example (correct):

```
/api/* → EC2
/s3/* → S3
*     → EC2
```

If `*` is at top → every request goes to EC2 → routing breaks.

---

# STEP 4️⃣ — Deploy + Wait

CloudFront takes 5–10 minutes to deploy globally because:

* Config is replicated to **all edge locations** around the world.
* Cache rules + security + origins must propagate.

CloudFront shows:

```
Status: Deploying
Status: Enabled (deployment finished)
```

---

# STEP 5️⃣ — Test Routing

Now test:

### Test EC2 origin

```
https://d123.cloudfront.net/api/index.html
```

➡ CloudFront forwards to EC2
➡ Response is from EC2

### Test S3 origin

```
https://d123.cloudfront.net/images/1.png
```

➡ CloudFront sends to S3 bucket
➡ Response is from S3

You can confirm by checking:

* Response headers

  * `Miss from CloudFront` (cache miss)
  * `Hit from CloudFront` (cache hit)

---

# 🔥 Behind the Scenes (VERY IMPORTANT)

### ✔ CloudFront does NOT download files first

CloudFront behavior:

* If object is in cache → serves from edge.
* If object not in cache → fetch from origin in **chunks**, while streaming to user.

This is why:

* First request is slower (MISS)
* Next requests are instant (HIT)

---

# 📌 Why your /api/index.html didn’t work initially?

Because the EC2 instance **did not have** `/var/www/html/api/index.html`.

You created it manually via SSH:

```
/var/www/html
  └── api/
       └── index.html
```

After that, CloudFront could successfully serve the file.

---

# 🧨 Key Points Gaurav Explained

### ✔ CloudFront can have MANY origins

You added 2:

* EC2 → for API path
* S3 → for static path

### ✔ CloudFront matches URL patterns

Not file extensions.

### ✔ S3 bucket remains PRIVATE

Only CloudFront accesses it.

### ✔ You can route to:

* S3
* EC2
* ALB
* API Gateway
* MediaPackage
* Any custom origin

### ✔ Cache TTL controlled by Behaviors

Example:

```
default TTL: 86400 (1 day)
min TTL: 0
max TTL: 31536000 (1 year)
```

---

# 💡 Where Path Based Routing is Used?

### 🟢 Single website but multiple backends

* `/api/*` → EC2
* `/static/*` → S3
* `/*` → React/Angular/Vue app

### 🟢 Microservices

* `/auth/*` → Cognito
* `/images/*` → S3
* `/backend/*` → ALB

### 🟢 Video streaming sites

* `/video/*` → MediaStore
* `/assets/*` → S3

### 🟢 Real-time apps

* `/socket/*` → API Gateway WebSocket
* `/api/*` → Lambda (REST)

---

# 🎁 Want me to create full working setup for you?

I can generate:

### ✔ S3 + EC2 + CloudFront path-routing

### ✔ Full Terraform code

### ✔ Complete AWS diagram

### ✔ Production-grade security setup

### ✔ Signed URLs + OAC + WAF

### ✔ SPA routing (React/Vue)

### ✔ Lambda@Edge rewrite rules

Just tell me:

👉 **“Give full architecture example”**

or

👉 **“Give full Terraform setup”**

I will deliver everything.


---


Nice — I’ll give you a **ready-to-run, production-minded Terraform module** that implements:

* Private **S3** bucket (no public access) for static files
* **Origin Access Control (OAC)** so CloudFront signs requests to S3 (recommended)
* An **ALB + simple EC2 target** as an application origin (for `/api/*` or default)
* A **CloudFront distribution** with **path-based routing** (ordered behaviors):

  * `/static/*` → S3 origin (cached)
  * `/api/*` → ALB origin (no cache / forwarded)
  * default `*` → ALB origin
* Security group that **allows ALB only from CloudFront origin-facing prefix list** (managed AWS prefix list)
* Bucket policy restricting S3 to that CloudFront distribution (via `AWS:SourceArn`)
* Optional: attach WAF by setting `var.waf_web_acl_arn` if you have one
* Example outputs, testing steps, and notes about invalidations / cache-busting

Read the code, fill the variables at top (or supply via `terraform.tfvars`), then run `terraform init` → `terraform apply`.

---

## Important notes before you run

* Replace example names/values (bucket name, key-pair, AMI, domain/cert) with your own.
* CloudFront distributions take several minutes to deploy.
* Terraform `aws_cloudfront_origin_access_control` and `origin_access_control_id` require a recent AWS provider (>= 4.x). Use latest provider if possible.
* The script uses the AWS-managed prefix list `com.amazonaws.global.cloudfront.origin-facing` via `data "aws_prefix_list"`.

---

## Files — single `main.tf` (copy & paste)

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
  }
  required_version = ">= 1.0"
}

provider "aws" {
  region = var.region
}

########################
# VARIABLES (simple) ###
########################
variable "region" {
  type    = string
  default = "us-east-1"
}

variable "project" {
  type    = string
  default = "cf-multi-origin"
}

variable "bucket_name" {
  type    = string
  description = "Globally unique S3 bucket name"
}

variable "vpc_id" { type = string }
variable "public_subnet_ids" { type = list(string) }   # ALB subnets (public)
variable "private_subnet_ids" { type = list(string) }  # EC2 subnets
variable "key_pair_name" { type = string }
variable "instance_ami" { type = string }  # e.g. Amazon Linux 2 AMI id
variable "instance_type" { type = string, default = "t3.micro" }

# Optional WAF
variable "waf_web_acl_arn" { type = string, default = "" }

########################
# S3 Private Bucket ####
########################
resource "aws_s3_bucket" "static" {
  bucket = var.bucket_name
  acl    = "private"

  tags = {
    Name    = "${var.project}-static-bucket"
    Project = var.project
  }
}

resource "aws_s3_bucket_public_access_block" "static" {
  bucket = aws_s3_bucket.static.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# server-side encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "static" {
  bucket = aws_s3_bucket.static.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

########################
# Simple ALB + EC2 #####
########################
# Security group for ALB (inbound ports 80 from CloudFront prefix list)
resource "aws_security_group" "alb_sg" {
  name        = "${var.project}-alb-sg"
  description = "ALB SG - allow HTTP from CloudFront prefix list only"
  vpc_id      = var.vpc_id
}

# allow port 80 from CloudFront prefix list (data source)
data "aws_prefix_list" "cloudfront_origin" {
  name = "com.amazonaws.global.cloudfront.origin-facing"
}

resource "aws_security_group_rule" "allow_cf_to_alb" {
  type                     = "ingress"
  from_port                = 80
  to_port                  = 80
  protocol                 = "tcp"
  security_group_id        = aws_security_group.alb_sg.id
  source_prefix_list_id    = data.aws_prefix_list.cloudfront_origin.id
  description              = "Allow CloudFront origin-facing IPs to ALB"
}

# Allow inbound SSH from your IP (adjust or remove in prod)
resource "aws_security_group_rule" "allow_ssh_from_me" {
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"] # replace with your IP for security
  security_group_id = aws_security_group.alb_sg.id
  description       = "SSH (replace with your IP in production)"
}

# ALB
resource "aws_lb" "app" {
  name               = "${var.project}-alb"
  internal           = false
  load_balancer_type = "application"
  subnets            = var.public_subnet_ids
  security_groups    = [aws_security_group.alb_sg.id]
  enable_deletion_protection = false
}

resource "aws_lb_target_group" "app_tg" {
  name     = "${var.project}-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id
  health_check {
    path                = "/"
    protocol            = "HTTP"
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    interval            = 30
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.app.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "forward"
    target_group_arn = aws_lb_target_group.app_tg.arn
  }
}

# Simple EC2 instance to register to ALB (for demo)
resource "aws_security_group" "ec2_sg" {
  name        = "${var.project}-ec2-sg"
  description = "Allow traffic from ALB"
  vpc_id      = var.vpc_id
}

resource "aws_security_group_rule" "allow_alb_to_ec2" {
  type              = "ingress"
  from_port         = 80
  to_port           = 80
  protocol          = "tcp"
  security_group_id = aws_security_group.ec2_sg.id
  source_security_group_id = aws_security_group.alb_sg.id
}

resource "aws_instance" "app" {
  ami           = var.instance_ami
  instance_type = var.instance_type
  key_name      = var.key_pair_name
  subnet_id     = element(var.private_subnet_ids, 0)
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]

  tags = {
    Name = "${var.project}-app-instance"
  }

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y httpd
              systemctl enable httpd
              systemctl start httpd
              echo "<html><body><h1>API from EC2 - $(hostname -f)</h1></body></html>" > /var/www/html/index.html
              mkdir -p /var/www/html/api
              echo "<html><body><h1>API index from EC2</h1></body></html>" > /var/www/html/api/index.html
              EOF
}

resource "aws_lb_target_group_attachment" "app_attach" {
  target_group_arn = aws_lb_target_group.app_tg.arn
  target_id        = aws_instance.app.id
  port             = 80
}

########################
# CloudFront OAC (new)
########################
resource "aws_cloudfront_origin_access_control" "oac" {
  name                              = "${var.project}-oac"
  description                       = "OAC for CloudFront -> S3"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

########################
# CloudFront Distribution
########################
resource "aws_cloudfront_distribution" "cdn" {
  enabled = true
  comment = "CloudFront distribution with multiple origins (S3 + ALB)"

  origin {
    domain_name = aws_s3_bucket.static.bucket_regional_domain_name
    origin_id   = "s3-static-origin"

    s3_origin_config {}
    origin_access_control_id = aws_cloudfront_origin_access_control.oac.id
  }

  origin {
    domain_name = aws_lb.app.dns_name
    origin_id   = "alb-origin"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  # Default behavior -> ALB
  default_cache_behavior {
    target_origin_id = "alb-origin"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods  = ["GET","HEAD","OPTIONS","PUT","POST","PATCH","DELETE"]
    cached_methods   = ["GET","HEAD"]
    cache_policy_id  = "413f12a3-34f8-4e7e-9f95-58e37e249003" # CachingDisabled managed
    origin_request_policy_id = "88a5eaf4-2fd4-4709-b370-b4c650ea3fcf" # AllViewer
    compress = true
  }

  # Ordered behavior for /static/* -> S3
  ordered_cache_behavior {
    path_pattern = "/static/*"
    target_origin_id = "s3-static-origin"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods = ["GET","HEAD","OPTIONS"]
    cached_methods  = ["GET","HEAD"]
    cache_policy_id = "658327ea-f89d-4fab-a63d-7e88639e58f6" # CachingOptimized
    origin_request_policy_id = "216adef6-5c7f-47e4-b989-5492eafa" # AllViewerExceptHostHeader
    compress = true
  }

  # Ordered behavior for /api/* -> ALB (no cache)
  ordered_cache_behavior {
    path_pattern = "/api/*"
    target_origin_id = "alb-origin"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods  = ["GET","HEAD","OPTIONS","POST","PUT","PATCH","DELETE"]
    cached_methods   = ["GET","HEAD"]
    cache_policy_id  = "413f12a3-34f8-4e7e-9f95-58e37e249003" # CachingDisabled
    origin_request_policy_id = "88a5eaf4-2fd4-4709-b370-b4c650ea3fcf" # AllViewer
    compress = true
  }

  price_class = "PriceClass_100"  # change to suit

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  # Optional WAF
  dynamic "web_acl_id" {
    for_each = var.waf_web_acl_arn != "" ? [var.waf_web_acl_arn] : []
    content {
      web_acl_id = web_acl_id.value
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  default_root_object = "index.html"

  tags = {
    Project = var.project
  }
}

########################
# S3 bucket policy to allow only the CloudFront distribution (SourceArn)
########################
resource "aws_s3_bucket_policy" "allow_cloudfront" {
  bucket = aws_s3_bucket.static.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid    = "AllowCloudFrontServicePrincipal",
        Effect = "Allow",
        Principal = { Service = "cloudfront.amazonaws.com" },
        Action    = "s3:GetObject",
        Resource  = "${aws_s3_bucket.static.arn}/*",
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = aws_cloudfront_distribution.cdn.arn
          }
        }
      }
    ]
  })
}

########################
# Upload a small test static file (using local_file + s3_object for demo)
########################
resource "local_file" "index_html" {
  content  = "<html><body><h1>Static from S3</h1></body></html>"
  filename = "${path.module}/index.html"
}

resource "aws_s3_object" "static_index" {
  bucket = aws_s3_bucket.static.id
  key    = "static/index.html"
  source = local_file.index_html.filename
  etag   = filemd5(local_file.index_html.filename)
  content_type = "text/html"
}

########################
# Outputs
########################
output "cloudfront_domain" {
  value = aws_cloudfront_distribution.cdn.domain_name
}

output "alb_dns_name" {
  value = aws_lb.app.dns_name
}

output "s3_bucket_name" {
  value = aws_s3_bucket.static.bucket
}
```

---

## How to use this (quick start)

1. Create a `terraform.tfvars` file in same folder with required variables:

```hcl
bucket_name       = "your-unique-bucket-name-12345"
vpc_id            = "vpc-0abcd1234"
public_subnet_ids = ["subnet-aaa","subnet-bbb"]
private_subnet_ids= ["subnet-ccc","subnet-ddd"]
key_pair_name     = "my-keypair"
instance_ami      = "ami-0c02fb55956c7d316" # example Amazon Linux 2 (replace region-specific)
instance_type     = "t3.micro"
region            = "us-east-1"
project           = "cf-multi-origin-demo"
```

2. Initialize & apply:

```bash
terraform init
terraform apply
# confirm and wait
```

3. After apply: note outputs:

* `cloudfront_domain` (e.g. dxxxxx.cloudfront.net)
* `alb_dns_name`
* `s3_bucket_name`

4. Test:

* `curl -I https://<cloudfront_domain>/static/index.html` → first should show `X-Cache: Miss from cloudfront`.
* `curl -I https://<cloudfront_domain>/static/index.html` again → `X-Cache: Hit from cloudfront`.
* `curl -I https://<cloudfront_domain>/api/index.html` → served by ALB/EC2 backend (Miss/Hit from CloudFront depending on behavior).

5. If you update S3 content, either:

* Upload new object with new name (cache-busting), or
* Run invalidation:

  ```bash
  aws cloudfront create-invalidation --distribution-id <dist-id> --paths "/static/*"
  ```

---

## Security & production tips (short)

* Replace the broad SSH `0.0.0.0/0` rule with your IP CIDR.
* Use ACM certificate + custom domain (add `viewer_certificate` with `acm_certificate_arn` and `aliases`).
* Use `PriceClass` that matches your needs (PriceClass_100, 200, All).
* Attach WAF (`web_acl_id`) for bot/attack protection.
* For S3, prefer versioned object uploads and hashed filenames for static assets to avoid invalidations frequently.
* For ALB in prod, put it in private subnets + use internal ALB if you can, then expose via CloudFront and restrict SG to CloudFront prefix list (already done).
* Consider using CloudFront **Origin Shield** for higher cache hit aggregation.

---

If you want I can:

* Convert this into **CloudFormation** or a modular **Terraform module** with variables and outputs split into files (`variables.tf`, `outputs.tf`, `main.tf`)
* Add **ACM certificate + custom domain** + Route53 record to this flow
* Add a **WAF rule set** example and attach it automatically
* Provide **CI/CD pipeline snippet** (GitHub Actions) that uploads static files to S3 and invalidates changed paths

Which one would you like me to generate next?



---


Here is the **full CloudFront Custom Error Page explanation again — in clear English**, structured exactly like the video.

---

# ✅ **CloudFront Custom Error Page – Full Explanation (English Version)**

This video teaches how to configure a **Custom Error Page** inside CloudFront.
The previous video had:

* A CloudFront distribution
* **Two origins**:

  * `/api` → EC2 instance
  * `/images` → S3 bucket

Now he teaches **how to show your own custom 404 page** instead of CloudFront’s default error message.

---

# 🔥 **1. Upload a Custom Error Page in S3**

The instructor creates a custom HTML file:

`404.html`

Then uploads it to S3 bucket:

```
images/
 ├── 1.png
 └── 404.html     ← Custom error page
```

This bucket is PRIVATE (very important).

---

# 🔥 **2. Configure the Custom Error Page in CloudFront**

Go to:

CloudFront → Your Distribution → **Error Pages** →
**Create Custom Error Response**

Then configure:

```
HTTP Error Code: 404
Customize Error Response: YES
Response Page Path: /images/404.html
HTTP Response Code: 404
Error Caching Minimum TTL: (any value)
```

Meaning:

* Whenever CloudFront receives **404 (Not Found)**
* It should NOT show the default ugly XML error
* Instead, it should show **your 404.html file stored in S3**

---

# 🔥 **3. CloudFront Deployment**

After clicking **Create**, CloudFront will show:

```
Status: Deploying
```

CloudFront takes time to propagate the configuration to **every Edge Location** in the world.

You must wait until:

```
Status: Deployed
```

---

# 🔥 **4. Testing the Custom Error Page**

Now the instructor tests different URLs.

---

### **✔ Valid EC2 Page**

`https://xxxxx.cloudfront.net/index.html`

Works normally → served from EC2.

---

### **✔ Valid S3 Image**

`https://xxxxx.cloudfront.net/images/1.png`

Served from S3.

---

### ❌ **Invalid Image**

`https://xxxxx.cloudfront.net/images/notfound.jpg`

Since the file does not exist, CloudFront gets **404** from origin.
So CloudFront shows your custom error page:

```
This page is not available
```

---

### ❌ **Invalid API Path**

`https://xxxxx.cloudfront.net/api/anything.html`

Same behavior → custom 404.html is returned.

---

# 🎯 **Key Points You Learned**

✔ CloudFront supports **Custom Error Responses**
✔ You can replace CloudFront’s default error page with your own HTML
✔ Works across **all origins**:

* EC2
* S3
* ALB
* API Gateway

✔ Works with **Path-Based Routing**
✔ S3 bucket remains **private**
✔ Custom error pages are cached on Edge Locations

---

# ⭐ Why Custom Error Pages Are Important

* Better UX (no ugly XML errors)
* Consistent branding
* For SPAs / React / Angular → required for routing
* Prevents users from seeing origin-level information
* Helps SEO

---

# 🎁 If you want, I can also provide:

### ✓ Full CloudFront architecture diagram

### ✓ CloudFront config + Custom Errors (YAML/Terraform)

### ✓ Example 404.html page (professional)

### ✓ Multi-origin CloudFront setup for real project

Just say: **“Give me the full CloudFront setup with code.”**


---

Here is a **clear, complete, and practical explanation** of **How to Control Access to Your CloudFront Content Based on Country** — exactly how it works in AWS, step-by-step, with theory + realtime example.

---

# 🌍 **CloudFront Geo-Restriction (Country-Based Block/Allow)**

CloudFront lets you **allow or block access** to your content **based on the viewer’s country**.

This feature works because CloudFront knows **the country of every request** based on:

* The request’s IP address
* Geo-IP databases AWS maintains

CloudFront adds headers like:

```
CloudFront-Viewer-Country: IN
CloudFront-Viewer-Country-Name: India
```

Based on this, CloudFront can automatically:

* **BLOCK** a country
* **ALLOW ONLY** selected countries
* Return a custom error page if blocked
* Redirect users to a different region

---

# 🧠 **Two Ways to Control Access by Country**

## **1️⃣ Geo Restriction (Built-in CloudFront feature) — Easiest Method**

This works at the **distribution level**.

You can choose:

### ✔ Block specific countries

(Example: Block China, Russia, Pakistan)

### ✔ Allow only specific countries

(Example: Allow only India, UK, USA)

CloudFront will block BEFORE reaching your origin → your EC2/S3 is protected.

---

# 🛠 **How to Configure Geo Restriction**

### Step 1: Go to CloudFront

AWS Console → CloudFront → Your Distribution

### Step 2: Open **Restrictions**

Left-side → **Restrictions** → **Edit**

### Step 3: Configure Geo Restriction

#### Option A — **Blacklist** (Block specific countries)

Choose:

```
Restriction Type: Blacklist
Countries: CN, PK
```

This means:

* Block China & Pakistan
* Allow everyone else

#### Option B — **Whitelist** (Allow only specific countries)

```
Restriction Type: Whitelist
Countries: IN, US, CA
```

This means:

* Only India, USA, and Canada can access
* Everyone else receives “Access Denied”

### Step 4: Save & Deploy

CloudFront will update all edge locations.

---

# 🔥 What Happens When a Blocked Country Tries to Access?

CloudFront returns:

```
HTTP 403 – Access Denied
```

You can override this with a **Custom Error Page** (from previous lesson).

Example:

```
Sorry, this content is not available in your region.
```

---

# 🧪 **Testing Country Restrictions**

To verify:

### ✔ Use VPN

Connect to different countries
Check whether your CloudFront URL is accessible

### ✔ Check CloudFront headers

In browser DevTools → Network:

```
CloudFront-Viewer-Country: SG
```

---

# 🧠 **2️⃣ Country-Based Access Control Using CloudFront Functions / Lambda@Edge**

This is a more advanced method when you want:

* Country-based **redirects**
* Country-based **different content**
* Country-based **AB testing**
* More dynamic rules

Example (Function):

```js
function handler(event) {
  const country = event.request.headers['cloudfront-viewer-country'].value;

  if (country !== 'IN') {
    return {
      statusCode: 403,
      statusDescription: 'Forbidden',
      body: 'Not available in your country',
    };
  }

  return event.request;
}
```

Attach this to **Viewer Request**.

---

# 🔥 **Comparing the Two Methods**

| Feature                       | Geo Restriction | Lambda@Edge / CloudFront Function |
| ----------------------------- | --------------- | --------------------------------- |
| Easy to use                   | ✅ Yes           | ❌ Needs coding                    |
| Block countries               | ✅ Yes           | ✅ Yes                             |
| Allow only selected           | ✅ Yes           | ❌ Must code                       |
| Custom logic                  | ❌ Limited       | ✅ Full control                    |
| Redirect users                | ❌ No            | ✅ Yes                             |
| Different content per country | ❌ No            | ✅ Yes                             |

---

# 🎯 **Real-World Example Use Cases**

### ✔ Block IPs from hacker-heavy regions

Only allow from India/US/UK.

### ✔ OTT / Streaming content

Block countries that don’t have licensing rights.

### ✔ E-commerce business

Allow only countries where shipping is available.

### ✔ Multilingual sites

Redirect India → English/Hindi version
Redirect UAE → Arabic version

---

# 🚀 **Summary (In Simple Words)**

* CloudFront can detect your country automatically
* You can BLOCK or ALLOW countries
* You can show a **custom error page** for blocked countries
* Or use **CloudFront Functions** for advanced logic
* Your EC2/S3 stays protected

---

# 📥 Want Practical Demo Next?

I can give you:

### ✔ 1. CloudFront Geo-Restriction Full Steps with screenshots

### ✔ 2. CloudFront Function code to block countries

### ✔ 3. How to redirect different countries to different pages

### ✔ 4. How to debug which edge location is serving your request

Just say **“Continue”** or tell me which part you want.



---

Here is the **FULL, CLEAN, CLEAR, PROFESSIONAL ENGLISH EXPLANATION** of the entire transcript you shared about **CloudFront Geo-Restriction (Country Blocking / Allowing)** — rewritten exactly like Gaurav explains but in perfect English.

---

# ⭐ **CloudFront Geo-Restriction Explained (Block/Allow Countries)**

CloudFront allows you to control which countries can access your content.
This is useful for:

* Licensing restrictions
* Security controls
* Reducing unwanted traffic
* Serving content only to target markets

In this video, Gaurav explains how CloudFront identifies countries using **IP Address Ranges**, and how you can **Allow** or **Block** traffic.

Let’s convert everything to English step-by-step.

---

# 🔍 **Concept: How CloudFront Knows the Viewer’s Country**

Every internet IP belongs to a geographic region.

Example:
“India IP ranges”

These IP ranges belong to Indian ISPs.
CloudFront maintains an internal database that maps:

```
IP Address → Country
```

So CloudFront can determine:

```
If viewer's IP is from India → Country = IN  
If viewer's IP is from USA → Country = US
```

CloudFront adds this header to every request:

```
CloudFront-Viewer-Country: IN
```

This country code is used for restrictions.

---

# 🛠 **Geo Restriction in CloudFront**

You can configure CloudFront in two ways:

1. **Whitelist (Allowed Countries)** – only selected countries can access
2. **Blacklist (Blocked Countries)** – block specific countries, allow all others

---

# 🧪 **LIVE EXAMPLE FROM THE VIDEO — IN ENGLISH**

### ▶ Scenario

Two machines:

* **Laptop in India**
* **EC2 instance in USA (us-east-1)**

CloudFront distribution is created in front of an API:

```
/api/index.html
```

When accessed normally:

### ✔ From India → Works

### ✔ From EC2 (USA) → Works

---

# 🧩 **Step 1: Apply Geo Restriction**

Go to:

CloudFront → Select Distribution → **Restrictions → Edit**

### Choose:

```
Restriction Type: Whitelist (Allow only)
Allowed Countries: United States (US)
```

This means:

* Only USA users can access
* Everyone else (India, UK, Singapore, etc.) will be **blocked**

---

# 🧪 **Test After Applying Rule**

### ✔ Test from the **USA EC2 instance**

Command:

```
curl <cloudfront-url>/api/index.html
```

Output:

```
This is index.html from API
```

→ Works because the request came from USA.

---

### ❌ Test from **India Laptop**

Browser:

```
https://d12345abcd.cloudfront.net/api/index.html
```

Result:

```
Access Denied — your country is blocked
```

CloudFront automatically blocks Indian IPs because of geo restriction.

---

# 🔄 **Step 2: Reverse the Rule**

Now configure:

```
Restriction Type: Blacklist
Blocked Country: United States (US)
```

Now CloudFront blocks **USA**, allows everyone else.

### ❌ From USA EC2 → Blocked

### ✔ From India → Works

Browser in India now loads successfully:

```
This is index.html
```

This confirms geo restrictions are working.

---

# 🤖 **Why does CloudFront take 2–3 minutes to update?**

(Gaurav asked this in the video)

Because CloudFront must replicate your new configuration to **every Edge Location in the world**.

CloudFront has:

* hundreds of POPs globally
* each one must receive updated rules

This replication takes **2-3 minutes**.

That’s why:

```
Status = Deploying
```

After propagation:

```
Status = Deployed
```

---

# 🏁 **Final Summary (Clean English Version)**

* CloudFront can block or allow access by country using IP-to-country mapping
* Two modes: **Whitelist** (Allow-only) and **Blacklist** (Block-specific)
* Restrictions are enforced **before** requests reach the origin
* Testing is done via:

  * Browser from different countries
  * EC2 instances in different regions
  * VPN
  * curl
* Changes take a few minutes to propagate due to global edge replication

---

If you want, I can now give you:

### ✔ Step-by-Step Screenshots (in text format)

### ✔ CloudFront Function (Serverless JavaScript) to block countries

### ✔ Redirect specific countries to specific pages

### ✔ Custom “Blocked Country” HTML error page

Just reply **“continue”**.


---


Below is the **clean, clear, professional English explanation** of the SAME video content you shared — rewritten in simple technical English but preserving the same meaning and flow.

---

# ⭐ **Deploying a Dynamic API Application on EC2 Before Connecting to CloudFront**

(This is the English version of your Hindi transcript)

---

## **🎯 What You Learned in the Previous Video**

* You deleted all CloudFront distributions.
* In this video, you will:

  * Deploy a **Node.js API application** using **Docker** on EC2.
  * Understand how CloudFront behaves with **dynamic pages / APIs**.
  * Learn what CloudFront does by default for API responses.
  * Learn how to control or override CloudFront's behavior.

This video prepares the backend API so you can attach CloudFront in the next part.

---

# ⭐ **Step 1 — Launch an EC2 Ubuntu Server**

1. Go to **EC2 → Launch Instance**
2. Instance Name:
   `youtube-sample-demo-server`
3. AMI: **Ubuntu**
4. Instance type: **t2.micro**
5. Key pair: Select existing
6. Security group:

   * Allow **HTTP (80)**
   * Allow **SSH (22)**

Click **Launch Instance**.

---

# ⭐ **Step 2 — Connect to EC2 and Install Docker**

Run these commands on Ubuntu:

```bash
sudo apt-get update
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

Add Docker’s official repo:

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list
```

Install Docker:

```bash
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
```

Verify:

```bash
docker version
```

---

# ⭐ **Step 3 — Pull the Pre-built API Docker Image**

The API code is available in GitHub, and you already bundled it into a Docker image.

Pull image:

```bash
docker pull <your-image-url>
```

---

# ⭐ **Step 4 — Run the Application Container**

Run the container on **port 3000**:

```bash
docker run -d -p 3000:3000 <your-image-url>
```

* `-d` → run in background
* `-p 3000:3000` → map container port 3000 to host port 3000

Check container:

```bash
docker ps
```

---

# ⭐ **Step 5 — Test the API in Browser / Postman**

Open:

```
http://<EC2-Public-IP>:3000
```

You will see:

```
This is API response
```

---

# ⭐ **Step 6 — Understanding All API Endpoints**

Your Node.js application has multiple APIs:

### **1️⃣ /1m**

Returns output with a cache header:

```
Cache-Control: max-age=60
```

Meaning:
Browser/CloudFront can cache this response for **60 seconds**

---

### **2️⃣ /2m**

Same as above but:

```
Cache-Control: max-age=120
```

---

### **3️⃣ /users**

Returns paginated user list.

Examples:

#### Default:

```
/users
```

Gives:

* page = 1
* size = 5

#### With Query Parameters:

```
/users?page=1&size=2
```

#### Get 3rd page, 5 users:

```
/users?page=3&size=5
```

---

### **4️⃣ /custom-header**

This is protected.

Your app checks header:

```
learning_ocean_header: test-value
```

If header is missing, user gets:

```
You cannot access this application directly
```

---

# ⭐ **Step 7 — Code Explanation (index.js)**

Inside Node.js app:

* Every response includes a dynamic `UUID`
* Cache headers are set using `max-age`
* Pagination logic for `/users`
* Custom security logic for `/custom-header`
* Application listens on **port 3000**

---

# ⭐ **Why This Setup? (Very Important)**

Because CloudFront behaves differently for:

* **Static content** (cache aggressively)
* **Dynamic content / APIs** (cache may not work correctly)
* **Custom headers** (CloudFront may remove them unless configured)
* **UUID changes cause cache misses**
* **Cache-Control headers directly influence CloudFront behavior**

In the NEXT video you will configure CloudFront so that:

* `/users` does **not** get cached unexpectedly
* `/1m` and `/2m` follow cache header from backend
* `/custom-header` works only when CloudFront attaches the special header
* `/api` or `/images` get routed to different origins

This entire setup will help you understand **real production-grade CloudFront + API** behavior.

---

# 📌 If you want, I can also convert this into:

✔ Full step-by-step **CloudFront setup with this backend**
✔ Explanation of **caching policies for APIs**
✔ Behavior overrides
✔ Path-based routing
✔ OAC/OAI behavior
✔ Security (custom headers, whitelisting, blocking direct access)

Just say **“continue”**.



---


Below is a **clean, production-ready, CloudFront-friendly Python Flask application** that matches EXACTLY the behavior of the Node.js app you used in the tutorial.

It includes:

✔ API endpoints: `/1m`, `/2m`, `/users`, `/custom-header`
✔ Cache-Control headers
✔ Pagination
✔ UUID generation
✔ Custom security header
✔ Perfect for CloudFront behavior testing
✔ Simple to deploy with Gunicorn / Docker

---

# ⭐ **Flask Application (app.py)**

Copy-paste this as `app.py`.

```python
from flask import Flask, jsonify, request, make_response
import uuid
import math

app = Flask(__name__)

# -------------------------------
#  Dummy User Data (22 users)
# -------------------------------
users_data = [
    {"id": i, "name": f"User-{i}"} for i in range(1, 23)
]

# -------------------------------
# 1️⃣  /1m → Cache for 60 seconds
# -------------------------------
@app.route("/1m")
def one_minute():
    response = make_response({
        "message": "1-minute cached response",
        "uuid": str(uuid.uuid4())
    })
    response.headers["Cache-Control"] = "max-age=60"
    response.headers["learning_ocean_header"] = "test-value"
    return response


# -------------------------------
# 2️⃣  /2m → Cache for 120 seconds
# -------------------------------
@app.route("/2m")
def two_minutes():
    response = make_response({
        "message": "2-minute cached response",
        "uuid": str(uuid.uuid4())
    })
    response.headers["Cache-Control"] = "max-age=120"
    response.headers["learning_ocean_header"] = "test-value"
    return response


# -------------------------------
# 3️⃣  /users → Pagination Enabled
# -------------------------------
@app.route("/users")
def users():
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 5))

    total_users = len(users_data)
    total_pages = math.ceil(total_users / size)

    start = (page - 1) * size
    end = start + size
    paginated_users = users_data[start:end]

    response = {
        "page": page,
        "size": size,
        "total": total_users,
        "total_pages": total_pages,
        "uuid": str(uuid.uuid4()),
        "users": paginated_users,
    }

    output = make_response(jsonify(response))
    output.headers["learning_ocean_header"] = "test-value"
    output.headers["Cache-Control"] = "no-cache"       # APIs usually shouldn’t cache
    return output


# -------------------------------
# 4️⃣  /custom-header → Security Layer
# -------------------------------
@app.route("/custom-header")
def protected_api():

    incoming_header = request.headers.get("learning_ocean_header")

    if incoming_header != "cloudfront":
        return jsonify({"error": "You cannot access this application directly"}), 403

    response = make_response({
        "message": "Authorized Access",
        "uuid": str(uuid.uuid4())
    })
    response.headers["Cache-Control"] = "no-store"
    return response


# -------------------------------
#  Root endpoint
# -------------------------------
@app.route("/")
def home():
    return jsonify({"msg": "Flask API running", "uuid": str(uuid.uuid4())})


# -------------------------------
# Run Server
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
```

---

# ⭐ **Behavior Explanation (Matches CloudFront Tutorial)**

### ✔ `/1m`

* Cache-Control: 60 seconds
* CloudFront will cache it for 1 minute
* UUID changes on every backend request

### ✔ `/2m`

* Cache 2 minutes

### ✔ `/users`

* Pagination
* No caching
* Always fresh data
* Good for API workloads

### ✔ `/custom-header`

* Requires:

```
learning_ocean_header: cloudfront
```

* CloudFront must be configured to **forward this custom header**
* Direct browser access will fail

### ✔ `/`

* Simple health check

---

# ⭐ **Dockerfile (Optional, if you want Docker deployment)**

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY app.py .

RUN pip install flask

EXPOSE 3000

CMD ["python", "app.py"]
```

Build image:

```bash
docker build -t flask-demo .
```

Run:

```bash
docker run -d -p 3000:3000 flask-demo
```

---

# ⭐ **CloudFront Notes**

When attaching to CloudFront:

* For `/1m` and `/2m` → CloudFront should **cache based on headers**
* For `/users` → CloudFront should **not cache**
* For `/custom-header` →
  You must configure **CloudFront behavior → Add custom header:**

```
learning_ocean_header = cloudfront
```

This allows ONLY CloudFront to call your EC2 API.

---

# ⭐ Want the FULL CloudFront Setup for This Flask App?

I can give you:

✔ CloudFront distribution
✔ Behavior rules
✔ Path-based routing
✔ OAC/OAI
✔ Security
✔ Cache policies
✔ Header forwarding
✔ Terraform version (optional)

Just say **“continue with CloudFront setup”**.


---

Below is a **clean, production-ready, CloudFront-friendly Python Flask application** that matches EXACTLY the behavior of the Node.js app you used in the tutorial.

It includes:

✔ API endpoints: `/1m`, `/2m`, `/users`, `/custom-header`
✔ Cache-Control headers
✔ Pagination
✔ UUID generation
✔ Custom security header
✔ Perfect for CloudFront behavior testing
✔ Simple to deploy with Gunicorn / Docker

---

# ⭐ **Flask Application (app.py)**

Copy-paste this as `app.py`.

```python
from flask import Flask, jsonify, request, make_response
import uuid
import math

app = Flask(__name__)

# -------------------------------
#  Dummy User Data (22 users)
# -------------------------------
users_data = [
    {"id": i, "name": f"User-{i}"} for i in range(1, 23)
]

# -------------------------------
# 1️⃣  /1m → Cache for 60 seconds
# -------------------------------
@app.route("/1m")
def one_minute():
    response = make_response({
        "message": "1-minute cached response",
        "uuid": str(uuid.uuid4())
    })
    response.headers["Cache-Control"] = "max-age=60"
    response.headers["learning_ocean_header"] = "test-value"
    return response


# -------------------------------
# 2️⃣  /2m → Cache for 120 seconds
# -------------------------------
@app.route("/2m")
def two_minutes():
    response = make_response({
        "message": "2-minute cached response",
        "uuid": str(uuid.uuid4())
    })
    response.headers["Cache-Control"] = "max-age=120"
    response.headers["learning_ocean_header"] = "test-value"
    return response


# -------------------------------
# 3️⃣  /users → Pagination Enabled
# -------------------------------
@app.route("/users")
def users():
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 5))

    total_users = len(users_data)
    total_pages = math.ceil(total_users / size)

    start = (page - 1) * size
    end = start + size
    paginated_users = users_data[start:end]

    response = {
        "page": page,
        "size": size,
        "total": total_users,
        "total_pages": total_pages,
        "uuid": str(uuid.uuid4()),
        "users": paginated_users,
    }

    output = make_response(jsonify(response))
    output.headers["learning_ocean_header"] = "test-value"
    output.headers["Cache-Control"] = "no-cache"       # APIs usually shouldn’t cache
    return output


# -------------------------------
# 4️⃣  /custom-header → Security Layer
# -------------------------------
@app.route("/custom-header")
def protected_api():

    incoming_header = request.headers.get("learning_ocean_header")

    if incoming_header != "cloudfront":
        return jsonify({"error": "You cannot access this application directly"}), 403

    response = make_response({
        "message": "Authorized Access",
        "uuid": str(uuid.uuid4())
    })
    response.headers["Cache-Control"] = "no-store"
    return response


# -------------------------------
#  Root endpoint
# -------------------------------
@app.route("/")
def home():
    return jsonify({"msg": "Flask API running", "uuid": str(uuid.uuid4())})


# -------------------------------
# Run Server
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
```

---

# ⭐ **Behavior Explanation (Matches CloudFront Tutorial)**

### ✔ `/1m`

* Cache-Control: 60 seconds
* CloudFront will cache it for 1 minute
* UUID changes on every backend request

### ✔ `/2m`

* Cache 2 minutes

### ✔ `/users`

* Pagination
* No caching
* Always fresh data
* Good for API workloads

### ✔ `/custom-header`

* Requires:

```
learning_ocean_header: cloudfront
```

* CloudFront must be configured to **forward this custom header**
* Direct browser access will fail

### ✔ `/`

* Simple health check

---

# ⭐ **Dockerfile (Optional, if you want Docker deployment)**

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY app.py .

RUN pip install flask

EXPOSE 3000

CMD ["python", "app.py"]
```

Build image:

```bash
docker build -t flask-demo .
```

Run:

```bash
docker run -d -p 3000:3000 flask-demo
```

---

# ⭐ **CloudFront Notes**

When attaching to CloudFront:

* For `/1m` and `/2m` → CloudFront should **cache based on headers**
* For `/users` → CloudFront should **not cache**
* For `/custom-header` →
  You must configure **CloudFront behavior → Add custom header:**

```
learning_ocean_header = cloudfront
```

This allows ONLY CloudFront to call your EC2 API.

---

# ⭐ Want the FULL CloudFront Setup for This Flask App?

I can give you:

✔ CloudFront distribution
✔ Behavior rules
✔ Path-based routing
✔ OAC/OAI
✔ Security
✔ Cache policies
✔ Header forwarding
✔ Terraform version (optional)

Just say **“continue with CloudFront setup”**.


---


Below is **the full detailed explanation in clean English**, covering **every concept** shown in your Hindi transcript — **CloudFront + EC2 application + caching + headers + query string issue + solution**.
This is written in a **clear training-style format**, just like a professional AWS instructor.

---

# ✅ **Full CloudFront + EC2 Concepts Explained (English Version)**

*(Everything in your transcript explained step-by-step in a clean structured way)*

---

# ⭐ **PART 1 — Application Behavior Without CloudFront**

Your EC2 instance is running an API application (Node.js / Flask / etc.).

Examples:

* `/1m` → cached for 1 minute
* `/2m` → cached for 2 minutes
* `/users` → paginated API
* `/custom-header` → requires a special header
* `/` → returns a UUID that changes every refresh

When you hit the EC2 public IP directly:

```
http://<public-ip>/1m
```

You get **new UUID every time** because the request goes **directly** to the server.

---

# ⭐ **PART 2 — When Accessing via CloudFront**

When you call:

```
https://abc123.cloudfront.net/1m
```

CloudFront **caches** the response.

So instead of new UUID, you get:

* The **same cached UUID** (until cache expires)
* Response says → `Hit from CloudFront`
* After TTL expires → `Miss from CloudFront`

This is correct CloudFront behavior.

---

# ⭐ **PART 3 — Understanding Why CloudFront Misbehaves for APIs**

Example misbehavior:

Direct EC2 output:

```
curl http://<public-ip>/users?page=3&size=2
```

Correct JSON response.

But CloudFront output:

```
curl https://abc123.cloudfront.net/users?page=3&size=2
```

Gives **wrong response** (data of page=1, size=5).

## ❗ Why CloudFront breaks pagination?

Because CloudFront’s cache **key** only includes:

```
/users
```

NOT:

```
/users?page=3&size=2
```

So CloudFront stores:

```
Key: /users
Value: (response of first call)
```

All future calls — even `/users?page=3&size=2` — return the **same cached page**.

---

# ⭐ **PART 4 — FIX for CloudFront Pagination Issue**

We must **include query strings** in CloudFront cache key.

Steps:

### 1. Open CloudFront → Behavior → Edit

### 2. Go to **Cache key settings / Cache policy**

### 3. Edit cache policy:

Enable:

```
Include Query Strings: Yes
```

You can choose:

* **"All Query Strings"** → recommended
* or specific keys (page, size)

After enabling this:

CloudFront builds cache keys like:

```
/users?page=1&size=5
/users?page=3&size=2
/users?page=1&size=10
```

✔ Each query combination is cached separately
✔ Correct API pagination works
✔ Problem solved

---

# ⭐ **PART 5 — TTL (Time To Live) Explanation**

Cache TTL controls how long CloudFront keeps the response.

Three TTL values:

* **Default TTL** – used when origin response has no caching headers
* **Minimum TTL** – lower boundary (CloudFront will not cache for less)
* **Maximum TTL** – upper boundary (CloudFront will not cache for more)

Example:

If your server sends:

```
Cache-Control: public, max-age=7200
```

But CloudFront’s **max TTL = 3600**

Then CloudFront will cache only for **3600 seconds**, not 7200.

---

# ⭐ **PART 6 — Adding Extra Security (Allow Only CloudFront)**

Backend should reject direct access:

```
403 – You cannot access this application directly
```

How?

### Step 1: Add a custom header from CloudFront to EC2

CloudFront Origin → Edit → Add Header:

```
Header Name: request-from
Value: cloudfront-edge
```

### Step 2: Application checks header

In Node.js / Flask, check:

```python
if request.headers.get("request-from") != "cloudfront-edge":
    return "You cannot access this application directly", 403
```

✔ Now **only CloudFront** can access EC2
✔ Direct access from browser is blocked

---

# ⭐ **PART 7 — Cache-Control Header from Application**

Application sets caching values:

```
Cache-Control: public, max-age=60
```

Meaning:

* CloudFront caches response for **60 seconds**
* Browser may also cache response

This works perfectly with CloudFront.

---

# ⭐ **PART 8 — Monitoring, Logging, Price Class**

### **Monitoring**

CloudFront → Monitoring
You see:

* Request count
* Error count
* Latency
* Cache hit ratio

### **Logging**

You can enable:

```
Standard Logging → S3 bucket
Real-time Logging → Kinesis
```

### **Price Class**

* Price Class 100 → Only US & EU locations (cheap)
* Price Class 200 → US, EU, Asia (medium)
* Price Class All → Worldwide (expensive but fastest)

---

# ⭐ **PART 9 — Continuous Deployment / Blue-Green with CloudFront**

CloudFront supports **split traffic between two origins**.

Example:

* Origin A → old version
* Origin B → new version

You can route:

* 90% traffic → old app
* 10% traffic → new app

If the new version misbehaves:
→ Instantly rollback to 100% old

Used in **zero-downtime deployments** with CI/CD.

---

# ⭐ **FINAL SUMMARY (Super Important)**

CloudFront API issues happen because:

✔ CloudFront cache key does NOT include query params by default
✔ CloudFront serves wrong cached responses

**Solution:**
Enable **query string forwarding & caching**.

**Security:**
Only allow CloudFront to access the backend using **custom headers**.

**Caching:**
Control TTL from origin or CloudFront cache policy.

**Monitoring:**
Use CloudWatch metrics & logs.

**Deployment:**
Use continuous deployment / split traffic features for safe releases.

---

# If you want, I can also provide:

✅ A **complete Flask API application** (with pagination, headers, TTL)
✅ A **CloudFront-ready version**
✅ Dockerfile for the Flask app
✅ Terraform for EC2 + CloudFront deployment
✅ Architecture diagrams

Just tell me: **“Give Flask app”** or **“Give full deployment setup”**.

