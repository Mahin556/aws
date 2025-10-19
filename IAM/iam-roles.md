* Generic Role ---> Policy ---> Standalone user assume
* Role is just like a cap
* Creating role
    * When creating a role we need to select the trusted entity type(service, account etc)
    * To create role for service user service type or for account use account type(selete which account you want to assume this role)
    * name
    * trust policy
    * permission policy
    * tag

* assign user a role
    * go to user --> permission --> create a inline policy --> json --> 

    * **IAM Role**: A set of permissions that can be assumed by users, applications, or services.
    * **AssumeRole**: AWS API action that allows a user or service to assume a role and obtain temporary security credentials.
    * **Trust Policy**: Defines **who** can assume the role.
    * **Permission Policy**: Defines **what** actions the role can perform once assumed.

    To allow a **user to assume a role**, you need:
    1. A **role** with a **trust policy** that trusts the user.
    2. A **user** with a **policy that allows `sts:AssumeRole`** for that role.

    ## 2️⃣ Example: Role Trust Policy
    Suppose you have a role named `DevOpsRole` and a user `MahinRaza`. The role trust policy looks like this:

    ```json
    {
    "Version": "2012-10-17",
    "Statement": [
        {
        "Effect": "Allow",
        "Principal": {
            "AWS": "arn:aws:iam::123456789012:user/MahinRaza"
        },
        "Action": "sts:AssumeRole"
        }
    ]
    }
    ```
    * `"Principal"` → Who is allowed to assume this role.
    * `"Action"` → Must be `sts:AssumeRole`.
    * `"Effect"` → Allow or Deny.

    ## 3️⃣ Example: User Policy to Assume Role
    Now attach a policy to the IAM user (MahinRaza) that allows assuming the role:

    ```json
    {
    "Version": "2012-10-17",
    "Statement": [
        {
        "Effect": "Allow",
        "Action": "sts:AssumeRole",
        "Resource": "arn:aws:iam::123456789012:role/DevOpsRole"
        }
    ]
    }
    ```

    * `"Action"` → `sts:AssumeRole` allows calling the AssumeRole API.
    * `"Resource"` → The ARN of the role the user can assume.
    * now the user is allow to assume the role

    ## 4️⃣ How it Works
    1. User `MahinRaza` calls `sts:AssumeRole` for `DevOpsRole`.
    2. AWS checks the **role’s trust policy** to see if this user is allowed.
    3. If allowed, AWS returns **temporary security credentials**.
    4. The user can now perform actions allowed by the **role’s permission policy**.

    ## 5️⃣ Notes / Best Practices
    * Keep **trust policies minimal**; only allow specific users or services to assume roles.
    * Use **role chaining carefully**: A role assumed by a user can assume another role if allowed.
    * Temporary credentials have a **limited duration** (default 1 hour, max 12 hours for most roles).
    * For automation / DevOps pipelines, roles are preferred over permanent user credentials.

    * To the the url to switch the role go to roles->your role->summary->link to switch role in console->copy url
    * we can login through that role and account color change and you get the permission assign to the role and you lost you previous permissions.
    * to switch back to previous permissions you can go the top left and hit switch back button