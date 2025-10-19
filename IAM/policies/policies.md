* define permission in form of JSON doc.
* assigned to user,group,role and give permission to perform specified API actions.
* 3 types --> aws Managed,customer managed,customer inline policy
    * AWS managed ---> manage by aws, you can't edit,labeled with orange box.
    * Customer managed ---> created by customer/you, editable, no symbol beside them.
    * inline policy ---> directly assign to the user.
* AWS interpretate the policy and show you the what user can do.
* when you add user to group you can see the in the user permission section that user inherit permission from the group.

---

* This policy allows full access to S3 — but only if the user has signed in using MFA
```json
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "DenyAllS3IfNoMFA",
			"Effect": "Deny",
			"Action": "s3:*",
			"Resource": "*",
			"Condition": {
				"BoolIfExists": {
					"aws:MultiFactorAuthPresent": "true"
				}
			}
		}
	]
}
```
---
* Denies all actions on all services if the user is not logged in with MFA.
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "DenyAllWithoutMFA",
            "Effect": "Deny",
            "Action": "*",
            "Resource": "*",
            "Condition": {
                "BoolIfExists": {
                    "aws:MultiFactorAuthPresent": "false"
                }
            }
        }
    ]
}
```
---

* Allow EC2 actions only when coming from a specific IP range
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowEC2FromOfficeIP",
            "Effect": "Allow",
            "Action": "ec2:*",
            "Resource": "*",
            "Condition": {
                "IpAddress": {
                    "aws:SourceIp": "203.0.113.0/24"
                }
            }
        }
    ]
}
```
* Allows EC2 operations only if requests originate from the given IP range (for example, your office network).
---

* Allow console access only with MFA
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowConsoleOnlyWithMFA",
            "Effect": "Deny",
            "Action": "aws-portal:*",
            "Resource": "*",
            "Condition": {
                "Bool": {
                    "aws:MultiFactorAuthPresent": "false"
                }
            }
        }
    ]
}
```
* Denies access to AWS Management Console billing and account settings unless MFA is used.

---

* Allow S3 read-only access to a specific bucket
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowS3ReadOnly",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::my-example-bucket",
                "arn:aws:s3:::my-example-bucket/*"
            ]
        }
    ]
}
```
* Grants read-only access to a single bucket and its contents.

---
* Require MFA for deleting S3 objects
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowS3ReadWrite",
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": "*"
        },
        {
            "Sid": "DenyDeleteWithoutMFA",
            "Effect": "Deny",
            "Action": [
                "s3:DeleteObject",
                "s3:DeleteBucket"
            ],
            "Resource": "*",
            "Condition": {
                "Bool": {
                    "aws:MultiFactorAuthPresent": "false"
                }
            }
        }
    ]
}
```
* Users can perform all S3 operations, but cannot delete buckets or objects without MFA.

---

* Allow EC2 Start/Stop only with MFA
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowStartStopWithMFA",
            "Effect": "Allow",
            "Action": [
                "ec2:StartInstances",
                "ec2:StopInstances"
            ],
            "Resource": "*",
            "Condition": {
                "Bool": {
                    "aws:MultiFactorAuthPresent": "true"
                }
            }
        }
    ]
}
```
* Users can only start or stop EC2 instances if they’ve logged in with MFA.
---
* Allow IAM actions only to view (not modify) users and roles
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "ViewOnlyIAM",
            "Effect": "Allow",
            "Action": [
                "iam:List*",
                "iam:Get*",
                "iam:GenerateServiceLastAccessedDetails"
            ],
            "Resource": "*"
        }
    ]
}
```
* Grants read-only access to IAM — allows viewing users, roles, and permissions but not editing them.

---
* Allow CloudWatch read-only access
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "CloudWatchReadOnly",
            "Effect": "Allow",
            "Action": [
                "cloudwatch:Describe*",
                "cloudwatch:Get*",
                "cloudwatch:List*"
            ],
            "Resource": "*"
        }
    ]
}
```
* Provides monitoring visibility without granting modification rights.