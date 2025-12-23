# **CloudFront Signed URLs & Signed Cookies (For Premium / Protected Content)**

CloudFront provides two powerful mechanisms to protect paid or private content:

* **Signed URLs**
* **Signed Cookies**

Both ensure that only authorized users can access premium resources.

---

# **1. CloudFront Signed URLs**

Signed URLs are used when you want to grant **temporary, restricted access** to a **single file**.

### **Use Cases**

* Paid online courses (example: Gaurav sir videos)
* Premium video streaming
* PDFs, eBooks, downloadable assets
* User-specific or time-limited access

---

## **How Signed URLs Work**

CloudFront generates a special URL that contains **authorization parameters**:

* Expiry time
* Signature
* Key Pair ID

### **Example Signed URL**

```
https://d123.cloudfront.net/video1.mp4
    ?Expires=1700000000
    &Signature=abcxyz123
    &Key-Pair-Id=K12345
```

### **What You Can Control**

* **TTL / Expiry Time** (URL valid for X minutes/hours)
* **IP Address Restriction**
* **Allowed Paths**
* **User-specific URLs**

### **What It Guarantees**

✔ Only authorized user can access the file
✔ URL stops working after expiry
✔ Direct S3 access is still blocked
✔ Great for pay-per-video or per-file protection

---

# **2. CloudFront Signed Cookies**

Signed cookies are used when a user needs access to **multiple protected files**, not just one.

### **Use Cases**

* Complete premium sections of a website
* Membership sites
* Multiple videos per user
* Large folder-based access control

### **How It Works**

CloudFront sends three cookies to the browser:

* `CloudFront-Expires`
* `CloudFront-Signature`
* `CloudFront-Key-Pair-Id`

Once set, the user can access:

```
/videos/*
/premium/*
/downloads/*
```

without generating individual signed URLs for each file.

### **Why Use Signed Cookies?**

| Scenario            | Use            |
| ------------------- | -------------- |
| Secure *one file*   | Signed URL     |
| Secure *many files* | Signed Cookies |

---

# **3. Full Security Architecture (S3 + CloudFront)**

Use all layers together for maximum protection.

| Layer               | Protection                                      |
| ------------------- | ----------------------------------------------- |
| **S3**              | Private bucket, accessible *only* to CloudFront |
| **CloudFront**      | OAC (Origin Access Control) + HTTPS             |
| **Application**     | Signed URLs or Signed Cookies                   |
| **WAF (Optional)**  | Block bots, IP ranges, countries                |
| **Security Groups** | Not needed for S3; S3 is not in VPC             |

This ensures:

* No direct S3 access
* All traffic goes through CloudFront
* Only authorized, signed requests succeed
* Extra security filters from WAF

---

# **Summary**

| Feature          | Signed URLs        | Signed Cookies       |
| ---------------- | ------------------ | -------------------- |
| Best for         | Single file        | Many files           |
| Use case         | Premium video, PDF | Entire folder access |
| User session     | Not required       | Required             |
| Cookie supported | Not needed         | Required             |
| Complexity       | Easy               | Medium               |
