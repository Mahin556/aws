* Create s3 bucket
    ```bash
    aws s3api create-bucket --bucket mahinraza-demo --region ap-south-1
    ```
* List s3 buckets
    ```bash
    aws s3 ls
    ```
* List objects in s3 bucket
    ```bash
    aws s3 ls s3://mahinraza-1
    ```
* Copy file to buckets
    ```bash
    aws s3 cp file1 s3://<bucket>
    ```
* Copy file from bucket
    ```bash
    aws s3 cp s3://<bucket> file1
    ```
* If your region is NOT us-east-1, you must add a location constraint:
    ```bash
    aws s3api create-bucket \
    --bucket mahinraza-2 \
    --region ap-south-1 \
    --create-bucket-configuration LocationConstraint=ap-south-1
    ```
* Block All Public Access
    ```bash
    aws s3api put-public-access-block \
    --bucket mahinraza-demo \
    --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
    ```
* Enable Versioning
    ```bash
    aws s3api put-bucket-versioning \
    --bucket mahinraza-demo \
    --versioning-configuration Status=Enabled
    ```
* Enable Default Encryption (SSE-S3)
    ```bash
    aws s3api put-bucket-encryption \
    --bucket mahinraza-demo \
    --server-side-encryption-configuration '{
        "Rules": [{
        "ApplyServerSideEncryptionByDefault": {
            "SSEAlgorithm": "AES256"
        }
        }]
    }'
    ```
* Enable Bucket for Static Website Hosting
    ```bash
    aws s3 website s3://mahinraza-demo/ \
    --index-document index.html \
    --error-document error.html
    ```
* Enable Transfer Acceleration
    ```bash
    aws s3api put-bucket-accelerate-configuration \
    --bucket mahinraza-demo \
    --accelerate-configuration Status=Enabled
    ```


