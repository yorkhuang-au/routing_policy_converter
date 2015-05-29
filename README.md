# routing_policy_converter
This converts the ASA firewall routing policies to SR4 rules.

The program uses Python3.

Python Packages:
1. ipaddress
2. pysubnettree


All rights reserved by York Huang, 2015.



## Michael's exmaple
### Convert intermediate results to finals
Good original=access-list internet_inbound extended permit tcp host FF_Internet_Router object-group Getronics_Management_Subnet eq tacacs


Good original=access-list internet_inbound extended permit udp host FF_Internet_Router object-group Getronics_Management_Subnet eq tacacs
    policy: internet_inbound protocol:udp action:permit source:outside dest:inside port=tacacs.



set  security policies from-zone outside to-zone inside policy internet_inbound_1 match source-address FF_Internet_Router
set  security policies from-zone outside to-zone inside policy internet_inbound_1 match destination-address Getronics_Management_Subnet
set  security policies from-zone outside to-zone inside policy internet_inbound_1 match application tacacs
set  security policies from-zone outside to-zone inside policy internet_inbound_1 then permit
set  security policies from-zone outside to-zone inside policy internet_inbound_1 then log session-init


Good original=access-list internet_inbound extended permit tcp 
Good original=access-list internet_inbound extended permit tcp object-group First_Data object-group RTA_EFTPOS eq ftp
    policy: internet_inbound protocol:tcp action:permit source:outside dest:inside port=ftp.


set  security policies from-zone outside to-zone inside policy internet_inbound_2 match  First_Data
set  security policies from-zone outside to-zone inside policy internet_inbound_2 match  RTA_EFTPOS
set  security policies from-zone outside to-zone inside policy internet_inbound_2 match application ftp
set  security policies from-zone outside to-zone inside policy internet_inbound_2 then permit
set  security policies from-zone outside to-zone inside policy internet_inbound_2 then log session-init


Good original=access-list internet_inbound extended permit tcp object-group Test_SFTG_Access host SFTGTEST eq 
    policy: internet_inbound protocol:tcp action:permit source:outside dest:inside port=2222.


set  security policies from-zone outside to-zone inside policy internet_inbound_3 match Test_SFTG_Access 
set  security policies from-zone outside to-zone inside policy internet_inbound_3 match SFTGTEST 
set  security policies from-zone outside to-zone inside policy internet_inbound_3 match application TCP_2222
set  security policies from-zone outside to-zone inside policy internet_inbound_3 then permit
set  security policies from-zone outside to-zone inside policy internet_inbound_3 then log session-init

