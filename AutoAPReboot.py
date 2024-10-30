#!/usr/bin/env python3

import json
import requests
import os
import time
import sys
import datetime
from dotenv import load_dotenv
import meraki

def display_help():
    help_text = """
    Usage: AutoAPReboot.py [OPTIONS]

    Options:
      --all           Reboot all devices in the specified network.
      [tag]           Reboot only devices with the specified tag.
      --help          Display this help message.

    Description:
      This script reboots access points in a Meraki network based on provided
      tags or for all devices. To use the script, ensure the following environment
      variables are defined in a .env file:
      
      - apiKey: Meraki API key
      - networkId: Meraki network ID
      - organizationId: Meraki organization ID

    Examples:
      Reboot all devices in the network:
        python AutoAPReboot.py --all

      Reboot only devices with a specific tag:
        python AutoAPReboot.py <tag>
    """
    print(help_text)

# Load environment variables
load_dotenv()

# Fetch credentials and network IDs
apikey = os.getenv("apiKey")
orgName = os.getenv("orgName")
network_id = os.getenv("networkId")
organization_id = os.getenv("organizationId")

# Display help if environment variables are missing
if not apikey or not network_id or not organization_id:
    print("Error: Missing required environment variables. Please check your .env file.")
    display_help()
    sys.exit(1)
else:
    print("This reboot will apply to Organization Name: ", orgName)

def reboot_ap(apikey, network_id, serial, suppress_print=False):
    """Reboot an access point (AP) using Meraki API."""
    base_url = 'https://api.meraki.com/api/v1'
    post_url = f'{base_url}/networks/{network_id}/devices/{serial}/reboot'
    headers = {
        'x-cisco-meraki-api-key': apikey,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(post_url, headers=headers)
        if response.status_code == 202:
            print(f"Reboot successful for device {serial}.")
        else:
            print(f"Error: Failed to reboot device {serial}. Status code: {response.status_code}, Response: {response.text}")
    except requests.RequestException as e:
        print(f"Error: Failed to reboot device {serial}. Exception: {e}")

def main():
    reboot_all = False
    cmdline = False

    # Parse command-line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--help':
            display_help()
            sys.exit(0)
        
        cmdline = True
        if sys.argv[1] == '--all':
            reboot_tag = None
            reboot_all = True
        else:
            reboot_tag = sys.argv[1]
    else:
        reboot_tag = None

    # Initialize Meraki dashboard API
    dashboard = meraki.DashboardAPI(apikey, suppress_logging=True)

    # Fetch list of devices from the network
    try:
        device_list = dashboard.networks.getNetworkDevices(network_id)
    except Exception as e:
        print(f"Error: Failed to retrieve devices. Exception: {e}")
        sys.exit(1)

    # Build a list of unique tags
    tag_list = set()
    for device in device_list:
        tags = device.get('tags', [])
        tag_list.update(tags)

    # Display the available tags
    print(datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y"))
    print('Available Tags:\n')
    for tag in tag_list:
        print(tag)

    # Prompt user to specify a tag, if not provided via command line
    if not cmdline:
        reboot_tag = input("\nEnter Tag of APs to reboot or press Enter for all APs: ")
        if not reboot_tag:
            reboot_all = True

    print('\nRebooting Devices:\n')
    for device in device_list:
        # Check if the device has the specified tag or if rebooting all
        if reboot_all or (reboot_tag in device.get('tags', [])):
            name = device.get('name', 'unknown')
            print(f"{name} {device['serial']} {device.get('lanIp', 'N/A')} {device.get('tags', [])} - ", end='')
            reboot_ap(apikey, network_id, device['serial'])
            time.sleep(0.5)

if __name__ == "__main__":
    main()
