```bash
EC2 → Security Groups → Create Security Group
```
* Security Groups Are Stateful
  * If you allow INBOUND HTTP, then the outbound response is automatically allowed.
  * You do not need to manually configure outbound rules for return traffic.

* Security Groups Do NOT Support DENY Rules
    * Security Groups support only ALLOW.
    * You cannot say:
      * Block IP 10.1.1.5
      * Deny access to Russia
      * Block attacker IP
    * To block malicious traffic, use:
      * Network ACL
      * WAF
      * Firewall Manager

* One Instance Can Have Multiple Security Groups
* One Security Group Can Be Attached to Multiple Instances
* Use different security group for diff port/protocols
    * Like use diff SG for SSH, now you can detach this SG when you does not need SSH.    