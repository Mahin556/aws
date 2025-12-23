• Application Layer = Layer where **real applications run** (browser, curl, ssh, ftp, dns client, mail client).
• It does **not** manage routing or packets; it **formats & interfaces** data so end-user apps can send over the network.
• It defines **protocols**: HTTP, HTTPS, DNS, FTP, SSH, SMTP, POP3, IMAP, DHCP, NTP, SNMP, LDAP.

---

### **🔥 PRACTICAL PART 1 — Observe Application Layer in action (HTTP)**

• Install curl (if not installed):
`sudo yum install curl -y`
or
`sudo apt install curl -y`

• Send an HTTP request manually:
`curl -v http://example.com`

• What you will see:

* `GET / HTTP/1.1` → Application layer request
* `Host: example.com` → Application layer header
* `HTTP/1.1 200 OK` → Server response
* HTML content → Application layer data sent to your browser

• Change request method to POST:
`curl -v -X POST -d "name=mahin" https://httpbin.org/post`

• Add custom header:
`curl -v -H "X-Test: Hello" https://httpbin.org/headers`

• Application Layer lesson here:

* You generated real HTTP messages
* You saw how headers/requests look
* You tested methods (GET / POST)

---

### **🔥 PRACTICAL PART 2 — DNS Lookup (Application Layer Protocol)**

• DNS resolves domain → IP.
• Check DNS request using dig:
`dig google.com`

• Check only IP answer:
`dig +short google.com`

• Query specific record types:
`dig TXT google.com`
`dig MX gmail.com`

• Query using specific DNS server (Google DNS):
`dig @8.8.8.8 openai.com`

• Application Layer lesson:

* DNS runs entirely at the application layer
* Query, response, TTL fields appear
* No transport layer needed to understand the response

---

### **🔥 PRACTICAL PART 3 — SSH Authentication (Application Layer)**

• SSH is an Application Layer protocol (even though it uses port 22/TCP).

• Test SSH handshake:
`ssh -vvv user@server_ip`

• This shows:

* application layer negotiation
* key exchange
* cipher agreement
* username/password or key authentication

• Copy SSH public key using application layer protocol (SCP):
`scp file.txt user@server:/tmp`

• Application Layer lesson:

* SSH negotiates keys at layer 7
* File transfer (scp/sftp) also application layer

---

### **🔥 PRACTICAL PART 4 — FTP & SFTP Hands-On**

• Install FTP client:
`sudo yum install ftp -y`
or
`sudo apt install ftp -y`

• Connect to an FTP server:
`ftp speedtest.tele2.net`

• List files:
`ls`
`get 1MB.zip`
`bye`

• SFTP (secure):
`sftp user@server_ip`
`put file`
`get file`
`exit`

• Application Layer lesson:

* FTP is clear-text application protocol
* SFTP runs over SSH at application layer

---

### **🔥 PRACTICAL PART 5 — SMTP (Email sending by command)**

• Install netcat (nc):
`sudo yum install nc -y`
or
`sudo apt install netcat -y`

• Connect to mail server (Gmail blocks telnet, so use mailtrap/testing servers):
`nc smtp.mailtrap.io 2525`

• Manually send an email (Application layer commands):

```
HELO mahin.com
MAIL FROM:<test@mahin.com>
RCPT TO:<someone@example.com>
DATA
Subject: Test Email
This is a test email.
.
QUIT
```

• Application Layer lesson:

* HELO / MAIL FROM / RCPT are application layer commands
* Done via raw TCP connection

---

### **🔥 PRACTICAL PART 6 — DHCP Discovery (Real Packet Capture)**

• Install tcpdump:
`sudo yum install tcpdump -y`

• Capture DHCP packets:
`sudo tcpdump -i enp0s3 port 67 or port 68 -vv`

• Renew IP so DHCP generates traffic:
`sudo dhclient -r`
`sudo dhclient`

• Application Layer lesson:

* DHCP messages (Discover, Offer, Request, ACK)
* All visible in capture
* This is pure application layer message exchange

---

### **🔥 PRACTICAL PART 7 — NTP Time Sync (Application Layer)**

• Query NTP server:
`ntpdate -q time.google.com`

• You will see:

* offset
* delay
* polling

• Application Layer lesson:

* NTP is pure application layer protocol for clock sync

---

### **🔥 PRACTICAL PART 8 — Identify Application Layer Using Ports**

• Check active application layer connections:
`ss -tulnp`

• You will see:

* 80 → HTTP
* 443 → HTTPS
* 22 → SSH
* 53 → DNS
* 25 → SMTP
* 110 → POP3
* 143 → IMAP
* 3306 → MySQL
* 5432 → PostgreSQL

• Application Layer lesson:

* Every port has a service name defined at layer 7

---

### **🔥 PRACTICAL PART 9 — Packet Capture & Decode Application Layer**

• Sniff HTTP traffic:
`sudo tcpdump -i enp0s3 tcp port 80 -A`

• Sniff DNS traffic:
`sudo tcpdump -i enp0s3 udp port 53 -vvv`

• Sniff SSH negotiation:
`sudo tcpdump -i enp0s3 port 22`

• Application Layer lesson:

* packet begins with transport layer header but contains application protocol data
* tcpdump shows clear text for HTTP, DNS
* encrypted for HTTPS/SSH

---

### **🔥 PRACTICAL PART 10 — Build Your Own Application Layer Server (Python)**

• Install Python:
`sudo yum install python3 -y`

• Create a simple HTTP server:
`python3 -m http.server 8080`

• Access it from browser:
`http://<your_server_ip>:8080`

• What you observe:

* Browser sends GET request
* Python server responds with directory listing or file
* All communication at application layer

• Create a simple custom protocol server:

```
nc -lvp 9000
```

Open another terminal:
`nc <server_ip> 9000`
Type anything → the server receives it.

• Application Layer lesson:

* You built your own layer-7 protocol
* Anything over TCP/UDP can be a new application layer protocol

---

### **🔥 PRACTICAL PART 11 — LDAP, SNMP, REST API Testing (Bonus)**

• LDAP query example (if server exists):
`ldapsearch -x -H ldap://server -b dc=example,dc=com`

• SNMP walk:
`snmpwalk -v2c -c public server_ip`

• REST API test:
`curl -X GET https://api.github.com/users/mahin`

• Gigantic lesson:

* All modern microservices = Application layer
* All REST APIs = Application Layer JSON over HTTP

---

### **🔥 PRACTICAL SUMMARY (What you learned hands-on)**

• How Application Layer works in real life
• How browsers send/receive HTTP
• How DNS resolves domain names
• How SSH authenticates and negotiates keys
• How FTP, SMTP, NTP, DHCP use Layer 7
• How to inspect traffic using tcpdump
• How to start an HTTP server and analyze requests
• How to build your own protocol

---

