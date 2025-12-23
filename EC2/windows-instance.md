
• **Launch Instance → Choose Windows AMI → Choose instance type → Launch.**

• Wait until **Instance State = Running** and **Status Checks = 2/2 passed**.

• Select the instance → Click **Connect** → Choose **RDP Client**.

• Click **Download Remote Desktop File (.rdp)**.

• Click **Get Password** → Upload your **.pem key** → Click **Decrypt Password**.

• Copy the **Administrator password**.

• Double-click the **.rdp file** → Paste the password → **Connect**.

• Windows Server desktop will open.

---

* **Access Windows EC2 Instance from Linux (Using Remmina)**
  * Install Remmina (RDP Client) on Linux
    ```bash
    sudo apt-get update
    sudo apt-get install remmina -y
    ```
  * Get Windows EC2 Password
    * Go to AWS Console → EC2 → Instances
    * Select your Windows instance → Click Connect
    * Choose RDP Client
    * Click Get Password
    * Upload your .pem key
    * Click Decrypt Password
    * Copy the Administrator password
  * Open Remmina in Linux
    * Search Remmina in your Linux applications
    * Open it
  * Create RDP Connection
    * Inside Remmina:
      * Click + (New Connection)
      * Protocol → RDP – Remote Desktop Protocol
      * Server → Windows EC2 Public IP
    * Enter: Username and Password
  * Accept Certificate
    * If Remmina shows “Unknown certificate” → Click Yes / Accept.
  * 