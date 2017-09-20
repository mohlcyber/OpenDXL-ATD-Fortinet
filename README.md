# OpenDXL-ATD-Fortinet
This integration is focusing on the automated threat response with McAfee ATD, OpenDXL and Fortinet Firewalls.
McAfee Advanced Threat Defense (ATD) will produce local threat intelligence that will be pushed via DXL. An OpenDXL wrapper will subscribe and parse IP indicators ATD produced and will automatically update Firewall rules.

<img width="887" alt="screen shot 2017-09-20 at 13 59 15" src="https://user-images.githubusercontent.com/25227268/30642635-eddc3ad6-9e0b-11e7-8303-5ebadb16ffbb.png">

## Component Description

**McAfee Advanced Threat Defense (ATD)** is a malware analytics solution combining signatures and behavioral analysis techniques to rapidly 
identify malicious content and provides local threat intelligence. ATD exports IOC data in STIX format in several ways including the DXL.
https://www.mcafee.com/in/products/advanced-threat-defense.aspx

**Fortinet Firewalls** provide high performance network security protection platform. 
https://www.fortinet.com/products/next-generation-firewall.html

## Prerequisites
McAfee ATD solution (tested with ATD 4.0.4)

Download the [Latest Release](Link)
* Extract the release .zip file

OpenDXL Python installation
1. Python SDK Installation ([Link](https://opendxl.github.io/opendxl-client-python/pydoc/installation.html))
    Install the required dependencies with the requirements.txt file:
    ```sh
    $ pip install -r requirements.txt
    ```
    This will install the dxlclient, and requests modules.    
2. Certificate Files Creation ([Link](https://opendxl.github.io/opendxl-client-python/pydoc/certcreation.html))
3. ePO Certificate Authority (CA) Import ([Link](https://opendxl.github.io/opendxl-client-python/pydoc/epocaimport.html))
4. ePO Broker Certificates Export ([Link](https://opendxl.github.io/opendxl-client-python/pydoc/epobrokercertsexport.html))

Fortinet Firewall (tested with FortiGate 5.6.2)

## Configuration
McAfee ATD receives files from multiple sensors like Endpoints, Web Gateways, Network IPS or via Rest API. 
ATD will perform malware analytics and produce local threat intelligence. After an analysis every indicator of comprise will be published via the Data Exchange Layer (topic: /mcafee/event/atd/file/report). 

### atd_subscriber.py
The atd_subscriber.py receives DXL messages from ATD, filters out discovered IP's and loads forti_push.py.

Change the CONFIG_FILE path in the atd_subscriber.py file.

`CONFIG_FILE = "/path/to/config/file"`

### Fortinet

Before Fortinet Firewalls can be updated via API it is neccessary to create a user that has access to the API.

### forti_push.py
The forti_push.py receives the discovered malicious IP's and will use API's to update Firewall rules / groups.

Change the username and password as well as the IP address. The IP address should point to the Fortinet Firewall.

<img width="243" alt="screen shot 2017-09-20 at 13 48 33" src="https://user-images.githubusercontent.com/25227268/30642288-81e724e0-9e0a-11e7-91a9-a783e8d7e649.png">

The script will:

1. create a new api session 
2. login
3. check if the host exist already and create it if it doesn't
4. check if the group exist already and create it if it doesn't
5. get members of a group and add the new created / discovered address
6. logout

Don't forget to create a new Firewall rule related to the BadIPList.

![screen shot 2017-09-20 at 13 52 14](https://user-images.githubusercontent.com/25227268/30642385-f976ad28-9e0a-11e7-8300-6601c01614b4.png)

## Run the OpenDXL wrapper
> python atd_subscriber.py

or

> nohup python atd_subscriber.py &

## Summary
With this use case, ATD produces local intelligence that is immediatly updating policy enforcement points like the 
Fortinet Next Generation Firewalls with malicious IP's.

