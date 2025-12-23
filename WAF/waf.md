### References:-
* https://youtu.be/sLnXHOkaNTk?si=d08q-bi07tPy6aSs

---

* Web Application Firewall (WAF) protects web applications by filtering, monitoring, and blocking HTTP/HTTPS traffic

* It protects against common attacks like SQL Injection, Cross-Site Scripting (XSS), DDoS, and malicious bots

* It reduces the attack surface of an application

* It helps protect against zero-day vulnerabilities even before vendor patches are available

* It works at the application layer (Layer 7)

* AWS WAF is a fully managed Web Application Firewall service provided by AWS

* It has no infrastructure or operational overhead

* It works without any change in application code

* It inspects incoming web requests using rules

* AWS WAF can be integrated with Application Load Balancer

* It can be integrated with API Gateway

* It can be used with Amazon CloudFront to protect AWS and on-premise workloads

* It also supports AppSync, Cognito, App Runner, and Verified Access

* AWS WAF provides multi-layer security controls

* It supports IP-based filtering

* It supports rate-based rules to limit request floods

* It provides bot protection

* It supports AWS-managed rule groups

* It supports third-party managed rule groups from AWS Marketplace

* It supports fully custom rules

* Web ACL (Web Access Control List) is the main configuration component

* Web ACL is attached to resources like ALB, API Gateway, or CloudFront

* Web ACL defines how traffic should be inspected and handled

* Rules define inspection conditions (statements)

* Rules define actions to take when a request matches conditions

* Rule Groups are reusable collections of rules

* Rule Groups can be AWS managed

* Rule Groups can be third-party managed

* Rule Groups can be custom created by users

* Web ACLs and Rule Groups are AWS resources

* Individual rules do not exist independently

* Rules only exist inside Web ACLs or Rule Groups

* Possible rule actions include Allow

* Possible rule actions include Block

* Possible rule actions include Count (monitor only)

* Possible rule actions include CAPTCHA

* Possible rule actions include Challenge

* AWS WAF protects applications before traffic reaches the backend

* It improves availability and performance

* It adds security without changing application code

* It is critical for production workloads

* AWS WAF evaluates rules inside a Web ACL or a Rule Group whenever a web request arrives

* Rule evaluation always starts with the **lowest numeric priority value**

* Rules are evaluated one by one in ascending priority order

* Evaluation stops as soon as a rule matches **and** the action is terminating

* If no rule matches, AWS WAF applies the **default action** of the Web ACL

* Priority decides execution order, not rule creation order

* Lower number means higher priority

* Rule Groups also have priorities, and rules inside a Rule Group have their own internal priorities

* Example priorities in a Web ACL
  * Rule1 with priority 0
  * RuleGroupA with priority 100
    * RuleA1 with priority 10000
    * RuleA2 with priority 20000
  * Rule2 with priority 200
  * RuleGroupB with priority 300
    * RuleB1 with priority 0
    * RuleB2 with priority 1

* Evaluation order in this example
  * Rule1
  * RuleGroupA RuleA1
  * RuleGroupA RuleA2
  * Rule2
  * RuleGroupB RuleB1
  * RuleGroupB RuleB2

* If Rule1 matches, no other rules are evaluated

* If Rule1 does not match, evaluation continues to RuleGroupA

* Rules inside a Rule Group are evaluated based on their internal priority

* If no match is found, AWS WAF continues until all rules are exhausted

* Every rule has two parts
  * Condition (statement)
  * Action

* Rule actions are divided into terminating and non-terminating actions

* Terminating actions
  * Allow
  * Block

* When a terminating action matches
  * Rule evaluation stops immediately
  * No further rules are processed

* Non-terminating actions
  * Count
  * CAPTCHA
  * Challenge

* Count action
  * Request is counted for monitoring
  * Evaluation continues to the next rule

* CAPTCHA and Challenge actions
  * AWS WAF checks token status
  * If token is valid, request behaves like Count and evaluation continues
  * If token is invalid or missing, evaluation stops
  * Client is asked to solve CAPTCHA or background challenge

* If no rule produces a terminating action
  * AWS WAF applies the Web ACL default action (Allow or Block)

