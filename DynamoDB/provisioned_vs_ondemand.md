* **Provisioned Mode**
  * You **predefine capacity**
  * You set:
    * Read Capacity Units (RCU)
    * Write Capacity Units (WCU)
  * Best for **predictable traffic**
  * **Cheaper** than On-Demand for steady workloads
  * Can enable **Auto Scaling**
  * You must plan capacity
  * Risk of **throttling** if capacity is exceeded
  * Billing based on **provisioned RCU/WCU**, even if unused

* **On-Demand Mode**
  * **No capacity planning required**
  * DynamoDB automatically scales
  * Best for **unpredictable or spiky traffic**
  * **No throttling** due to capacity limits (soft limits still apply)
  * More **expensive per request**
  * Billing based on **actual read/write requests**
  * Very easy to start

* **Capacity Planning**
  * Provisioned → You think in **RCU/WCU**
  * On-Demand → You think in **requests**

* **Performance**
  * Both give **single-digit millisecond latency**
  * Difference is only in **cost model & scaling**

* **Cost Comparison**
  * Provisioned → Lower cost for constant usage
  * On-Demand → Higher cost but zero waste

* **Scaling Behavior**
  * Provisioned → Manual or Auto Scaling
  * On-Demand → Fully automatic

* **Throttling**
  * Provisioned → Possible if limits exceeded
  * On-Demand → Rare (handled automatically)

* **When to Use What**
  * Provisioned Mode
    * Stable workloads
    * Known access patterns
    * Long-running production systems
  * On-Demand Mode
    * New applications
    * Startups
    * Sudden traffic spikes
    * Uncertain usage patterns

* **Interview One-Liner**
  * Provisioned = **Prepaid & planned**
  * On-Demand = **Pay as you go**

* **Provisioned Mode**
  * Jitni **RCU/WCU aap provision karte ho**, **utni ka hi pay** karna hota hai (use ho ya na ho)
  * **Auto Scaling available hoti hai**, but:
    * Sudden spike me **immediate scale nahi hota**
    * Workload dekh ke **few minutes lag sakte hain**
  * Agar traffic achanak badh jaye → **throttling ho sakti hai**
  * **Best jab traffic predictable & consistent ho**
    * Example: enterprise apps, steady backend services
  * Cost generally **On-Demand se sasta** hota hai long-term steady load me
  * Capacity planning ki responsibility **aapki hoti hai**

* **On-Demand Mode**
  * **RCU/WCU define karne ki zarurat nahi**
  * DynamoDB automatically scale karta hai
  * **Pay sirf actual Read/Write requests ka**
  * Sudden traffic spikes ko **smoothly handle** karta hai
  * **New applications** ke liye best
  * Jab:
    * Traffic unpredictable ho
    * Inconsistent usage ho
  * Per-request cost **Provisioned se zyada** hoti hai
  * Throttling ka risk **bahut kam**

* **RCU / WCU clarification (important)**
  * 1 RCU = **4 KB strongly consistent read**
  * 1 WCU = **1 KB write**
  * Item size badhne par:
    * RCUs / WCUs **automatically zyada consume** hote hain
  * Ye rule **dono modes me same** rehta hai

* **Pricing statement correction**
  * “$0.25 per million RCUs” → conceptually correct idea hai
  * Actual pricing **region-based hoti hai** (exact numbers region ke hisaab se change ho sakte hain)
  * Interview me bolna safe hai:
    * “On-Demand me per request pricing hoti hai”

* **Simple interview-ready one-liners**
  * Provisioned Mode → *Pay for allocated capacity, good for predictable traffic*
  * On-Demand Mode → *Pay per request, best for unpredictable traffic*