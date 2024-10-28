#!/usr/bin/env python3

import json
import requests
import os
import time
import meraki
import sys
import datetime
from dotenv import load_dotenv

load_dotenv()

# Pull credentials/NetworkId from.env file
apikey = os.getenv("apiKey")
network_id = os.getenv("networkId")
organizationId = os.getenv("organizationId")

def reboot_ap(apikey, networkid, serial, suppressprint=False):
    base_url = 'https://api.meraki.com/api/v1'
    calltype = 'Device'
    posturl = '{0}/networks/{1}/devices/{2}/reboot'.format(
        str(base_url), str(networkid), str(serial))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    postdata = {
        'serial': format(str(serial))
    }
    dashboard = requests.post(posturl, data=json.dumps(postdata),
                              headers=headers)
    print(dashboard.status_code, dashboard.text, calltype)
    return

# apikey = 'api_key_here'
# network_id = 'network_id_here'

reboot_all = False
cmdline = False

if len(sys.argv) > 1:
    cmdline = True
    if sys.argv[1] == '--all':
        reboot_tag = None
        reboot_all = True
    else:
        reboot_tag = sys.argv[1]

dashboard = meraki.DashboardAPI(apikey, suppress_logging=True)

deviceList = dashboard.networks.getNetworkDevices(network_id)

tag_list = []

for device in deviceList:
    new_tags = device['tags']
    for tag in new_tags:
        if not tag in tag_list:
            tag_list.append(tag)

now = datetime.datetime.now()
print(now.strftime("%H:%M:%S %d-%m-%Y"))

print('Available Tags:\n')

for tag in tag_list:
    print(tag)

if cmdline is False:
    reboot_tag = input("\nEnter Tag of APs to reboot or press enter for all APs: ")
    if not reboot_tag:
        reboot_all = True

print('\nRebooting Devices:\n')
for device in deviceList:
    if reboot_tag in device['tags'] or reboot_all:
        try:
            name = device['name']
        except:
            name = 'unknown'
        print(name, device['serial'], device['lanIp'], device['tags'], '- ',end='')
        reboot_ap(apikey, network_id, device['serial'])
        time.sleep(0.5)
print()