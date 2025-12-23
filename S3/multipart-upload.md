- https://youtu.be/dfxXEQxJPzI?si=eUdVpMq34ebztfbN
- https://youtu.be/YKSzLVk4CMI?si=pyaipNZFpcW7dOl6

# 🧠 **1️⃣ What is S3 Multipart Upload?**

* **Multipart upload** allows you to **upload a single large object as a set of parts (chunks)** instead of one big file.
* Each part is uploaded **independently and in parallel**, which improves performance and reliability.
* After all parts are uploaded, S3 **assembles them into one complete object**.

---

# 💡 **2️⃣ Why Multipart Upload?**

| Benefit                | Explanation                                             |
| ---------------------- | ------------------------------------------------------- |
| **Speed**              | Upload parts in parallel for faster performance         |
| **Resumable uploads**  | If upload fails midway, you can retry only failed parts |
| **Handle large files** | Required for files **> 5 GB** (max single PUT = 5 GB)   |
| **Efficiency**         | Reduces timeouts and retries for large data transfers   |
| **Flexibility**        | You can pause/resume uploads easily                     |

---

# 📏 **3️⃣ Multipart Upload Size Rules**

| Parameter               | Limit                       |
| ----------------------- | --------------------------- |
| Minimum part size       | **5 MB** (except last part) |
| Maximum number of parts | **10,000**                  |
| Maximum object size     | **5 TB**                    |
| Each part numbered      | **1 to 10,000**             |

---

# 🧩 **4️⃣ Multipart Upload Lifecycle (Step-by-Step)**

---

### **Step 1️⃣ — Initiate Multipart Upload**

* You tell S3 you’re going to upload a file in parts.
* S3 returns an **UploadId**, which uniquely identifies this upload.

```bash
aws s3api create-multipart-upload --bucket mybucket --key bigfile.zip
```

✅ Output:

```json
{
    "Bucket": "mybucket",
    "Key": "bigfile.zip",
    "UploadId": "VXBsb2FkIElE..."
}
```

Save the **UploadId** — you’ll need it for subsequent parts.

---

### **Step 2️⃣ — Upload Each Part**

Each part is uploaded separately using its **part number (1–10,000)** and the **UploadId**.

Example:

```bash
aws s3api upload-part \
  --bucket mybucket \
  --key bigfile.zip \
  --part-number 1 \
  --body part1.zip \
  --upload-id VXBsb2FkIElE...
```

✅ You get an **ETag** for each part:

```json
{
    "ETag": "\"abc123ef45gh678\""
}
```

Upload all parts:

```bash
aws s3api upload-part --bucket mybucket --key bigfile.zip --part-number 2 --body part2.zip --upload-id VXBsb2FkIElE...
aws s3api upload-part --bucket mybucket --key bigfile.zip --part-number 3 --body part3.zip --upload-id VXBsb2FkIElE...
```

---

### **Step 3️⃣ — Complete Multipart Upload**

After uploading all parts, you tell S3 to **assemble them**.

You need to pass the list of all **part numbers and ETags** in a JSON file.

Example JSON (save as `parts.json`):

```json
{
  "Parts": [
    { "ETag": "\"abc123ef45gh678\"", "PartNumber": 1 },
    { "ETag": "\"def456ij78kl901\"", "PartNumber": 2 },
    { "ETag": "\"ghi789mn12op345\"", "PartNumber": 3 }
  ]
}
```

Now complete the upload:

```bash
aws s3api complete-multipart-upload \
  --multipart-upload file://parts.json \
  --bucket mybucket \
  --key bigfile.zip \
  --upload-id VXBsb2FkIElE...
```

✅ S3 merges all parts and finalizes your file.

Output:

```json
{
    "Location": "https://mybucket.s3.amazonaws.com/bigfile.zip",
    "Bucket": "mybucket",
    "Key": "bigfile.zip",
    "ETag": "\"abcd1234ef56789012345\""
}
```

---

### **Step 4️⃣ — (Optional) Abort Multipart Upload**

If something goes wrong, or you want to cancel an incomplete upload:

```bash
aws s3api abort-multipart-upload \
  --bucket mybucket \
  --key bigfile.zip \
  --upload-id VXBsb2FkIElE...
```

✅ This deletes all uploaded parts (not billed for storage).

---

# ⚙️ **5️⃣ Simplified CLI Upload (Automatic Handling)**

If you don’t want to handle parts manually, the AWS CLI can **auto-manage multipart uploads**:

```bash
aws s3 cp largefile.zip s3://mybucket/
```

✅ The CLI automatically:

* Splits the file into parts (default: 8–64 MB chunks)
* Uploads in parallel
* Retries failed parts
* Completes the upload automatically

You can tune this with:

```bash
--expected-size
--part-size
--storage-class
```

Example:

```bash
aws s3 cp largefile.zip s3://mybucket/ --storage-class STANDARD_IA --part-size 20MB
```

---

# 🔍 **6️⃣ List Multipart Uploads**

To see all ongoing multipart uploads:

```bash
aws s3api list-multipart-uploads --bucket mybucket
```

✅ Output:

```json
{
    "Uploads": [
        {
            "UploadId": "VXBsb2FkIElE...",
            "Key": "bigfile.zip",
            "Initiated": "2025-11-12T12:00:00Z"
        }
    ]
}
```

---

# 🧹 **7️⃣ Lifecycle Rule to Clean Up Incomplete Uploads**

To automatically clean up incomplete uploads (to avoid charges):

Example lifecycle rule:

```json
{
  "Rules": [
    {
      "ID": "AbortIncompleteMultipartUploads",
      "Status": "Enabled",
      "AbortIncompleteMultipartUpload": {
        "DaysAfterInitiation": 7
      }
    }
  ]
}
```

Apply it:

```bash
aws s3api put-bucket-lifecycle-configuration \
  --bucket mybucket \
  --lifecycle-configuration file://lifecycle.json
```

✅ Any incomplete multipart upload older than 7 days will be deleted.

---

# 💡 **8️⃣ Multipart Upload Summary Table**

| Step | Action              | Command                               |
| ---- | ------------------- | ------------------------------------- |
| 1    | Initiate upload     | `aws s3api create-multipart-upload`   |
| 2    | Upload each part    | `aws s3api upload-part`               |
| 3    | Complete upload     | `aws s3api complete-multipart-upload` |
| 4    | Abort upload        | `aws s3api abort-multipart-upload`    |
| 5    | List active uploads | `aws s3api list-multipart-uploads`    |

---

# 🧠 **9️⃣ Best Practices**

* Use multipart upload for **files > 100 MB** (required for > 5 GB).
* Always **complete or abort** to avoid storage costs.
* Enable **lifecycle cleanup** for incomplete parts.
* Upload parts **in parallel** to maximize performance.
* Use **encryption** (`--sse AES256` or `--sse aws:kms`) if needed.

---

# ✅ **10️⃣ In Simple Words**

> **S3 Multipart Upload** lets you upload large files in smaller parts, in parallel, to improve speed, reliability, and efficiency.
> AWS CLI can manage it automatically — or you can do it manually with API-style commands for full control.

---

Would you like me to show a **real working multipart upload demo** using `aws s3api` with example part files (`part1`, `part2`, etc.)?
