- Vertualization --> Technology used to create VMs
- Virtual machine ---> 
    - Logical Seperation of H/W, 
    - Work like Physical Machine,
    - All vms work in isolated environement(secure)---> One VM can not create a impact on other VMs

- Hypervisor ---> Software use to achive virtualization
    - Can be install on any OS and enable Virtualization
    - Create a abstraction layer on top of it VMs run
    - Enable resource sharing
    - Can run different OS on different VMs
    - Logically seperate a H/W in VMs and then We can install a GuestOS on top of it.
    - Take the resources from the Host
    
- Type of hypervisors
    - Type1 ---> Directly install no bare metal(H/W),have basic OS, save resources, used by Cloud providers and Enterprise server. --> VMware ESXi, Microsoft Hyper-V, and Xen. 
    - Type2 ---> Install ontop of OS --> Oracle VM VirtualBox, VMware Workstation, and Parallels Desktop. 

- 

Use case
- Testing a application on different OS(Linux, Windows, macOS).


Benefits:
- Save cost
- Use single host and install multiple VM on top of it instead of using a seperate Machine.
- Secure
- Easy backup using Snapshots
- Easy recovery
- Save energy



