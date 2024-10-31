# APReboot
Script to automate Meraki AP reboots on a schedule using an automation tool like CRON that can do multiple networks supplied in a networks.json file. The script expects the JSON configuration file path as the last command-line argument.

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
- Meraki Network ID 
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
    ├── sample.json
    └── AutoAPReboot.py  
```
4. Edit the ```sample_config.env``` file and rename to ```.env``` file, add the following variable:
```environment
#.env
---
apiKey = "Your_API_Key"
```
5. Edit the ```sample.json``` file or the ```networks.json``` file and add your network info:
```
[
    {
        "networkId": "L_networkId",
        "organizationId": "organizationId1",
        "orgName": "Name_of_Org_Houseing_APs_to_be_Rebooted",
        "tags": ["<tag-name>"]
    },
    {
        "networkId": "L_networkId2",
        "organizationId": "organizationId2",
        "orgName": "Name_of_Org_Houseing_APs_to_be_Rebooted",
        "tags": ["<tag-name>"]
    },
    {
        "networkId": "L_networkId3",
        "organizationId": "organizationId3",
        "orgName": "Name_of_Org_Houseing_APs_to_be_Rebooted",
        "tags": ["<tag-name>"]
    }
]
```

6. If no JSON file is provided, or if it fails to load, an error is printed, and the script exits. Now you can run the code by using the following command:
```console
python3 AutoAPReboot.py -ALL config.json
or 
python AutoAPReboot.py networks.json
```
## Output
If you have added Tags to your AccessPoints then this will find them and report them in the inital output.
Suggested format <orgName-AP>, where orgName is the name of the organization of the AP's you want to reboot.
The output should be as followed:
```
$ python AutoAPReboot.py networks.json

Processing network '<orgName>' (Network ID: <networkId>)...


```
## Author and Contributors
This script was written/copied by Dean Warren from DBMandrake. ChatGPT was used to make modifications but the original script was DBMandrake's. 

