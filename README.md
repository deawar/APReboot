# APReboot
Script to automate Meraki AP reboots on a schedule using an automation tool like CRON.

## Script Forked from:
This script is based off the Meraki API documentation and the Script of DBMandrake on the MerakiTech Forums.

## What is it?
DBMandrake wrote a stand alone python script to do bulk AP reboots based on device tags, 
so that we can reboot either all AP's in the network, or AP's with a specific tag.
It works with the current V1 API and current Meraki python module.

## Source API
All the api calls were created using the Meraki API V1 Index at https://developer.cisco.com/meraki/api-v1/api-index/

## Prerequisites
- Meraki Dashboard access
- Meraki API key
- Meraki Network ID - this is not explicitly needed
- Meraki Organization ID

## Get started
1. Clone or download this repo
```console
https://github.com/deawar/APReboot.git
```
2. Install required packages
```console
python3 -m pip install -r requirements.txt
```
3. Rename sample_config.env and edit ```.env``` file as follow:
```diff
└── APReboot/
+   ├── .env
    ├── requirements.txt
    └── AutoAPReboot.py  
```
4. In the ```.env``` file, add the following variables:
```environment
#.env
---
apiKey = "Your_API_Key"

orgName = "Name_of_Org_Houseing_APs_to_be_Rebooted"
networkId = "L_networkId"
organizationId = "orgId"
```

5. Now you can run the code by using the following command:
```console
python3 AutoAPReboot.py
or 
python AutoAPReboot.py
```
## Output
If you have added Tags to your AccessPoints then this will find them and report them in the inital output.
Suggested format <orgName-AP>, where orgName is the name of the organization of the AP's you want to reboot.
The output should be as followed:
```
$ python AutoAPReboot.py
11:56:06 29-10-2024
Available Tags:

recently-added
<OrganizationName>-AP

Enter Tag of APs to reboot or press enter for all APs: Traceback (most recent call last): *-AP


```
## Author and Contributors
This script was written/copied by Dean Warren from DBMandrake.

