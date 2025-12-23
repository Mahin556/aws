* Terraform: Private S3 + CloudFront (OAC) + Bucket Policy
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
* Terraform aws_cloudfront_origin_access_control resource creates OAC which signs requests with SigV4.
* The bucket policy uses AWS:SourceArn to restrict to that CloudFront distribution only.
* If you use a custom domain, add viewer_certificate with ACM cert (in us-east-1 for CloudFront).
* After apply, upload files to the S3 bucket (private). Access via CloudFront domain, not S3 URL.
* If CloudFront returns AccessDenied, check the bucket policy SourceArn vs distribution ARN and that the distribution is deployed.

* **Sample Terraform snippet for WAFv2 (basic)**
```hcl
