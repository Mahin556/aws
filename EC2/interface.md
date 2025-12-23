* ENI (Elastic Network Interface) — multiple network cards on one EC2.
* Virtual network card attached to an EC2 instance.
* EC2 can have multiple ENIs like multiple LAN ports.
* Each ENI has:
  * Its own subnet
  * Its own private IP
  * Its own security group
* Connect EC2 to multiple subnets.
* Apply different security groups per interface.