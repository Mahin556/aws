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


---
* Give basic S3 access
```json
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "Statement1",
			"Effect": "Allow",
			"Action": [
				"s3:ListAllMyBuckets",
				"s3:ListBucket",
				"s3:ListBucketVersions",
				"s3:GetBucketAcl",
				"s3:GetBucketCORS",
				"s3:GetBucketPolicy",
				"s3:GetObject",
				"s3:GetObjectAcl",
				"s3:CreateBucket",
				"s3:DeleteBucket",
				"s3:DeleteObject"
			],
			"Resource": [
				"*"
			]
		}
	]
}
```
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::my-bucket",
                "arn:aws:s3:::my-bucket/*"
            ]
        }
    ]
}
```
* Full S3 access
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::my-bucket",
                "arn:aws:s3:::my-bucket/*"
            ]
        }
    ]
}
```
---
* **CloudWatch Logs policy**
* Useful if your EC2 instance (like an app or agent) needs to send logs to CloudWatch:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
```
---
* **EC2 Describe-only policy**
* Allows the instance to query AWS about EC2 resources, but not modify anything:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances",
                "ec2:DescribeVolumes",
                "ec2:DescribeTags"
            ],
            "Resource": "*"
        }
    ]
}
```
---
* Read/write to a specific S3 bucket
* Send logs to CloudWatch
* Describe EC2 instances
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:*"
            ],
            "Resource": [
                "arn:aws:s3:::my-app-bucket",
                "arn:aws:s3:::my-app-bucket/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances"
            ],
            "Resource": "*"
        }
    ]
}
```
* Allow EC2 Instance Creation in Specific Regions Only
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowEC2ActionsInSpecificRegions",
            "Effect": "Allow",
            "Action": [
                "ec2:RunInstances",
                "ec2:DescribeInstances",
                "ec2:DescribeImages",
                "ec2:DescribeInstanceTypes",
                "ec2:CreateTags"
            ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "aws:RequestedRegion": [
                        "us-east-1",
                        "ap-south-1"
                    ]
                }
            }
        },
        {
            "Sid": "DenyEC2ActionsInOtherRegions",
            "Effect": "Deny",
            "Action": "ec2:RunInstances",
            "Resource": "*",
            "Condition": {
                "StringNotEquals": {
                    "aws:RequestedRegion": [
                        "us-east-1",
                        "ap-south-1"
                    ]
                }
            }
        }
    ]
}
```
* Tag based access control
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowDescribeForVisibility",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances",
                "ec2:DescribeTags"
            ],
            "Resource": "*"
        },
        {
            "Sid": "AllowModifyOnlyTaggedInstances",
            "Effect": "Allow",
            "Action": [
                "ec2:StartInstances",
                "ec2:StopInstances",
                "ec2:RebootInstances",
                "ec2:TerminateInstances",
                "ec2:ModifyInstanceAttribute"
            ],
            "Resource": "arn:aws:ec2:*:*:instance/*",
            "Condition": {
                "StringEquals": {
                    "ec2:ResourceTag/Environment": "Dev"
                }
            }
        }
    ]
}
```