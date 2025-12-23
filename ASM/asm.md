### Secret Management
* Secrets management is a critical topic for DevOps engineers and is very commonly asked in interviews, regardless of whether the platform is AWS, Azure, GCP, or on-premises.

* Secrets refer to sensitive information such as:

  * Database usernames and passwords
  * API keys and tokens
  * Docker registry credentials
  * Cloud provider credentials used by tools like Terraform and Ansible

* If secrets are leaked:

  * Unauthorized users can access databases
  * Docker images can be deleted or replaced
  * Infrastructure can be compromised
  * The security of the entire organization can be impacted

* Managing secrets securely is one of the core responsibilities of a DevOps engineer.

* On AWS, the most commonly used solutions for secrets management are:

  * AWS Systems Manager (Parameter Store)
  * AWS Secrets Manager
  * HashiCorp Vault (not an AWS-managed service)

* AWS Systems Manager (Parameter Store):

  * Used to store configuration values and secrets
  * Supports String, SecureString, and StringList
  * Easy to integrate with AWS services using IAM roles
  * Widely used in CI/CD pipelines such as CodePipeline and CodeBuild
  * Cost-effective compared to Secrets Manager
  * Best suited for moderately sensitive data

* Typical use cases for Parameter Store:

  * Docker username
  * Docker registry URL
  * Non-critical or less sensitive configuration values

* AWS Secrets Manager was introduced to handle highly sensitive data that requires extra security.

* AWS Secrets Manager provides:

  * Automatic secret rotation
  * Native integration with databases
  * Integration with AWS Lambda for custom rotation logic
  * Strong security controls
  * Higher cost compared to Parameter Store

* Secret rotation example:

  * Database passwords rotated every 90 days
  * Certificates rotated every 180, 270, or 360 days
  * Even if a secret is leaked, frequent rotation reduces the security risk window

* AWS Secrets Manager should be used for:

  * Database passwords
  * API tokens
  * Highly sensitive credentials

* Best practice on AWS is to use a combination of:

  * Systems Manager Parameter Store
  * AWS Secrets Manager
  * This balances security and cost optimization

* CI/CD example:

  * Container registry username → Systems Manager Parameter Store
  * Container registry URL → Systems Manager Parameter Store
  * Container registry password → AWS Secrets Manager

* Using everything in Secrets Manager increases cost, especially in large organizations where the number of secrets grows rapidly.

* HashiCorp Vault:

  * Not managed by AWS
  * Must be installed, configured, and maintained by the organization
  * Cloud-agnostic solution
  * Works across AWS, Azure, GCP, and on-premises environments

* Reasons organizations use HashiCorp Vault:

  * Multi-cloud or hybrid cloud strategies
  * Avoiding vendor lock-in
  * Centralized secrets management across platforms
  * Strong community support
  * Advanced encryption and security features

* Interview-ready explanation:

  * Use Systems Manager for less sensitive configuration data
  * Use Secrets Manager for highly sensitive data requiring rotation
  * Use HashiCorp Vault for multi-cloud or non-AWS environments

* Key takeaway for interviews:

  * There is no one-size-fits-all solution
  * The choice depends on security requirements, rotation needs, cost, and cloud strategy

---

### ASM

* Store secret in key value pair.
* Store DB password in ASM and application fetch credential from ASM and use them to connect to Db.
* Storing DB credential into the application make DB vulnerable so ASM prevent hardcoding credential into the application inself.
* Instead of storing secrets in the code:
    * Store them securely in Secrets Manager
    * Fetch them dynamically at runtime
* Fully managed AWS service helps you to securely store, manage and retrieve easly.
* These secrets can include:
    * Database passwords
    * API keys
    * Authentication tokens
    * Any sensitive configuration data(key/value pair)
* When the application is deployed on AWS:
    * It can access Secrets Manager
    * Retrieve secrets securely
    * Use them to connect to databases or APIs
* This ensures that:
    * Secrets are not exposed in source code
    * Security is improved
* It provides automatic features such as:
    * Encryption
    * Key rotation
    * Fine-grained access control using IAM
* It integrates seamlessly with AWS services.
