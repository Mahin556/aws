```bash
EC2 → Network & Security → Elastic IPs
```
* This IP is now reserved for your account until you release it.

* Attach Elastic IP to Your EC2 Instance
```bash
Elastic IP → Actions → Associate Elastic IP
```
Now:
```bash
Elastic IP  → mapped to  → Instance ID
Public IP → now changed to Elastic IP
```
* EC2 Instance Connect using Elastic IP.

* **Use Cases**
* For websites → domain always needs the same IP
    * If IP changes → website stops working
    * SEO ranking drops → traffic lost
    * So never use dynamic public IP for websites

* For databases → servers whitelist fixed IPs only
    * If your app server’s IP changes → DB connection fails
    * Static IP keeps connections stable

* For VPNs & Firewalls → require trusted fixed IPs
    * Payment gateways check source IP before allowing requests
    * Static IP ensures secure and consistent access

---

* **Delete (Release) an Elastic IP**
  * You cannot release an Elastic IP if it is still attached to an EC2 instance
  * First step → Disassociate the Elastic IP from the instance
  * Go to Elastic IPs → Actions → Disassociate Elastic IP
  * After disassociation → the instance gets a new dynamic public IP
  * Now the Elastic IP becomes free / unattached
  * Go to Actions → Release Elastic IP address
  * Confirm → Release
  * AWS will stop charging since the IP is no longer reserved
  * After that, if needed → Terminate the EC2 instance

