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