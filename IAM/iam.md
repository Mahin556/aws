### References:
- [AWS IAM Identity](https://youtu.be/MDM8AraFgUE?si=GxfxxsoeinM5SLRs)
- [AWS Identity and Access Management (IAM) Basics](https://youtu.be/iF9fs8Rw4Uo?si=s-EKxDSRELOcBcnz)

---

* Help to securly control access to aws resources.
* Allow to manage user,roles,group and permission to define who can access and who can not what within your aws environment.
* **Free and global(every region) service**
* Root account create by default, not use root account instead create a IAM account and use it with.

* Users

* Groups ---> 
    * Collective permission
    * user inherit
    * policy

* Policy--> 
    * Permission
    * json doc
    * built-in 
    * custom(visual,JSON --> create,attach,fine-grain-control)
    * grant access to user,group,role
    * policies attach to IAM identity
    * Full admin access
    * services admin access

* IAM Permission --->
    * API action that can or can't be performed
    * represented in IAM policy.

* AWS IAM Policy Limits Summary
    * **IAM Group Policy Limit:**
    Each **IAM group** can have up to **10 managed policies** attached.

    * **IAM User Policy Limit:**
    Each **IAM user** can have up to **20 managed policies** attached directly.

    * **Group Membership:**
    A user can belong to **up to 10 groups**.
    → If each group has 10 managed policies, the user can **inherit permissions from up to 100 managed policies** (10 groups × 10 policies).

    * **Inline Policies:**

    * Groups can also have **inline policies** (custom JSON policy documents attached directly to the group).
    * Inline policies do **not count** toward the 10 managed policy limit.
    * However, they **do count toward the group’s total policy document size limit** (which is 5120 characters).

    | Entity Type | Max Managed Policies | Inline Policy Limit              | Notes                                               |
    | ----------- | -------------------- | -------------------------------- | --------------------------------------------------- |
    | IAM User    | 20                   | 1 per user (size limit applies)  | User also inherits from groups                      |
    | IAM Group   | 10                   | 1 per group (size limit applies) | Users can be in 10 groups                           |
    | IAM Role    | 10                   | 1 per role (size limit applies)  | Often used for AWS services or cross-account access |

* IAM account ---> 
    * name
    * permission(group,copy,policy)
    * password
    * password_change
    * create group
    * attach policy to group then add user to group

* Tags ---> 
    * grouping
    * identification
    * selection

* console sign-in link ---> 12 digit number--->autofil
* console login ---> username,password,console-sign-in-link
* Roles ---> temp access, to user,service accross diff aws resources, have policy attach to it.
* MFA --> security extra layer, User need to enter a security code(form mobile device) with the password.
* MFA Devices ---> authenticator app, passkey or security key, Hardware TOTP Token.
* AUthenticato app ---> duo mobile, google authenticator, authy app
* 2 codes  from authenticator app.


* IAM Identity
    * IAM USERS-> Log in to aws or interact with AWS resource programmatically or by clicking the UI console.
    * IAM GROUPS-> group users, users share permissions, eg:-Administrators, Developers, Auditors.
    * IAM ROLES-> Allow aws resource/service to perform specific API actions, policy attached, assigne to user,resource/service


* Console access to user can be given while creating a user account or after creating a user account

`AWSRevokeOldSessions`
* when we change a password we can assign this policy to the user
* The temporary inline policy is automatically attached to the IAM user when they click "Revoke active sessions" in the AWS Management Console.
* This ensures that all current console sessions (logged-in sessions) are terminated immediately, and the user must re-authenticate.
* Inline policy, not a managed one.
* Automatically attached to the IAM user by AWS (you cannot manually attach it).
* Forces revocation of active sessions by denying all AWS actions until the user signs in again.
* This invalidates the current session token and forces re-login for the affected user.
* The policy AWSRevokeOldSessions is temporary and system-managed.
* The policy disappears automatically after the user logs back in.
* It applies only to console sessions, not permanent access keys or API sessions.