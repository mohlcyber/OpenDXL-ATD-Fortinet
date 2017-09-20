# OpenDXL-ATD-Fortinet
This integration is focusing on the automated threat response with McAfee ATD, OpenDXL and Fortinet Firewalls.
McAfee Advanced Threat Defense (ATD) will produce local threat intelligence that will be pushed via DXL. An OpenDXL wrapper will subscribe and parse IP indicators ATD produced and will automatically update Firewall rules.

## Component Description

**McAfee Advanced Threat Defense (ATD)** is a malware analytics solution combining signatures and behavioral analysis techniques to rapidly 
identify malicious content and provides local threat intelligence. ATD exports IOC data in STIX format in several ways including the DXL.
https://www.mcafee.com/in/products/advanced-threat-defense.aspx

**Fortinet Firewalls** provide high performance network security protection platform. 
https://www.fortinet.com/products/next-generation-firewall.html
