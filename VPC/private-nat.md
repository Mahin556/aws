### References:-
- https://youtu.be/L7TuaILbwOE?si=WJsZv86KuNZIlOQU
- https://youtu.be/fIcKD8jASyQ?si=aTkAlUilq48oSW7k
---

#### Public NAT
Traffic from private subnet ---> nat(based on route in route table) ---> IGW of the public subnet in which NAT present ---> Internat

#### Private NAT
* Allow traffic exchange between two VPCs that have same CIDR range.