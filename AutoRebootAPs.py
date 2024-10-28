#!/usr/bin/env python3
# Please note this script is based on decommishioned version of Meraki API V0. 
# This script probably won't work but was the basis for comparision of the working script.
import json
import requests
import time
import meraki
import sys
import datetime
from dotenv import load_dotenv

load_dotenv()

# Pull credentials/NetworkId from.env file
cisco_meraki_api_Key = os.getenv("apiKey")
dashboard = meraki.DashboardAPI(API_KEY)
network_id = os.getenv("networkId")
organizationId = os.getenv("organizationId")


baseUrl = 'https://dashboard.meraki.com/api/v0/'
inventory_api_url = "organizations/{}/inventory".format(organizationId)


headers = {
    'X-Cisco-Meraki-API-Key': cisco_meraki_api_Key,
    'Content-Type': 'application/json'
    }

get_inventory = requests.get(baseUrl+inventory_api_url,
                            headers=headers,
                            )

# Parse the get_inventory into json
inventory_json = get_inventory.json()



networkID = ""
serial = ""

# Opens or create a file name results
f = open('results.txt', "w+")

# loop over all the dictionaries inside inventory_json,
# if API is inside the dictionary it will get the NetworkID and the serial and then write it to the string above

for ap in inventory_json:
    try:
        if 'API' in ap['name']:
            networkID = ap['networkId']
            serial = ap['serial']
            ap_name = ap['name']
            reboot_api_call = requests.post(
                baseUrl+'/networks/{}/devices/{}/reboot'.format(networkID, serial ),
                headers=headers)
            if reboot_api_call.status_code == 200:
                print('Rebooting --->', ap_name, '---> Successful' , file=f)
                print("---------------------------------------------------",file=f)
            if reboot_api_call.status_code == 400:
                print ('Rebooting --->', ap_name, '---> Bad Request' , file=f)
                print("---------------------------------------------------",file=f)
            if reboot_api_call.status_code == 403:
                print ('Rebooting --->', ap_name, '---> Forbidden' , file=f)
                print("---------------------------------------------------",file=f)
            if reboot_api_call.status_code == 404:
                print ('Rebooting --->', ap_name, '---> Not Found' , file=f)
                print("---------------------------------------------------",file=f)
            if reboot_api_call.status_code == 429:
                print ('Rebooting --->', ap_name, '---> Too Many Requests' , file=f)
                print("---------------------------------------------------",file=f)
            time.sleep(2)
    except:
        continue

# closes the file
f.close()


# Setting up the SMTP Server
sender = 'meraki_api@company.local'
receiver = 'yourteam@company.com'

smtp_server = smtplib.SMTP(host='X.X.X.X', port=25)

f = open('results.txt', "r")

# reads the information inside the file results
script_result = f.read()

message = """From: <meraki_api@company.local>
To: <yourteam@company.com>
Subject: Meraki AP Reboot

API CODE: 200 = Successful
API CODE: 400 = Bad Request
API CODE: 403 = Forbidden
API CODE: 404 = Not Found
API CODE: 429 = Too Many Requests

{}
""".format(script_result)

# Email execution
try:
    smtp_server.sendmail(sender, receiver, message)
    print('Successfully sent email')
except:
    print('Error: Unable to send email')

# closes the file.
f.close()
