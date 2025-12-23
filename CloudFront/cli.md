```bash
#On deploy (CI pipeline), after uploading new assets to S3, run a CloudFront invalidation for changed paths or use versioned filenames to avoid invalidation. Invalidation can be automated via AWS CLI:
# invalidate everything (counts as 1 path)
aws cloudfront create-invalidation --distribution-id E123ABCD --paths "/*"

# invalidate specific file(s)
aws cloudfront create-invalidation --distribution-id E123ABCD --paths "/index.html" "/css/app.css"
```
```bash
$ curl -I https://d2urliw7w249fc.cloudfront.net/
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 568
Connection: keep-alive
Date: Mon, 17 Nov 2025 11:03:00 GMT
Last-Modified: Mon, 17 Nov 2025 10:15:01 GMT
ETag: "7a66126aaf1fc26d2b28f397881ead64"
x-amz-server-side-encryption: AES256
Accept-Ranges: bytes
Server: AmazonS3
X-Cache: Hit from cloudfront
Via: 1.1 3ad26026132de6a25b805c11f37e777c.cloudfront.net (CloudFront)
X-Amz-Cf-Pop: DEL51-P6
X-Amz-Cf-Id: wMxEhdKjvonj0OzIWE2AMdSxUJtod8vpiSuWWKlm3EEguxgihLrvJA==
Age: 18
```