# **💡 What is BurstBalance (in EBS)?**

BurstBalance shows **how much burst credit your EBS gp2 volume has left**.

Burst credits = temporary performance boost.

If BurstBalance falls to **0%**, your volume becomes **VERY SLOW**.

---

# **📌 Why do EBS volumes need burst credits?**

Small gp2 volumes cannot always give high IOPS.

So AWS gives them a **bucket of I/O credits**, allowing short-term high performance.

Example:

| **Volume Size (gp2)** | **Baseline IOPS** | **Maximum Burst IOPS** |
| --------------------- | ----------------- | ---------------------- |
| 1 GB                  | 3 IOPS            | up to 3000 IOPS        |
| 100 GB                | 300 IOPS          | up to 3000 IOPS        |

When you burst to 3000 IOPS, you **consume burst credits**.

---

# **📉 Why BurstBalance drops**

BurstBalance decreases when:

* You continuously do more IOPS than baseline
* Long-running write/read workload
* Snapshot restore (heavy I/O)
* Large data copy/backup jobs

If you **consume credits faster than you earn**, BurstBalance reaches **0%**, and performance drops.

---

# **📌 What happens at 0% BurstBalance?**

Your volume becomes **limited to baseline speed only**.

Example:

A 20 GB gp2 volume has baseline = **60 IOPS**.

If BurstBalance hits 0%:

👉 your volume becomes **60 IOPS only**
👉 extremely slow performance
👉 applications crash
👉 database timeouts

---

# **📈 How to view BurstBalance?**

CloudWatch Metric:

**`VolumeBurstBalance`**

Value:

* **100% = full credits available**
* **0% = no credits left**

---

# **💡 How to prevent BurstBalance from going low**

* Switch gp2 → **gp3** (recommended)
* Or switch to **io1/io2**
* Use RAID0 with multiple volumes
* Increase EBS size (gp2 baseline increases with size)
* Reduce workload
* Pre-warm snapshot (for restore operations)

---

# **🧠 Simple Example**

You have a gp2 volume:

* Size = 50 GB
* Baseline IOPS = 150
* Burst IOPS = 3000

If your workload is 2000 IOPS:

* You are using **2000 − 150 = 1850 burst IOPS**
* Credits will drain fast
* After some minutes/hours → BurstBalance = 0%
* Volume slows to 150 IOPS

---

# **🟢 In One Line:**

**BurstBalance tells you how much “speed boost” your EBS volume has left.
If it hits 0%, your EBS becomes very slow.**

