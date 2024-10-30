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
      --all           Reboot all devices in the specified networks.
      --help          Display this help message.

    Description:
      This script reboots access points in multiple Meraki networks based on
      tags provided in a JSON configuration file. To use the script, ensure the
      following environment variable is defined in a .env file:
      
      - apiKey: Meraki API key

      The JSON configuration file should contain:
      - networkId: Meraki network ID
      - organizationId: Meraki organization ID
      - orgName: Organization name (for logging)
      - tags: List of tags to filter devices (leave empty to reboot all)

    Examples:
      Reboot all devices in all networks:
        python AutoAPReboot.py --all
    """
    print(help_text)

def write_log(message):
    """Log message to a file."""
    with open("reboot_log.txt", "a") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{timestamp} - {message}\n")

# Load environment variables
load_dotenv()
apikey = os.getenv("apiKey")

# Display help if API key is missing
if not apikey:
    print("Error: Missing required environment variable `apiKey`. Please check your .env file.")
    display_help()
    sys.exit(1)

def reboot_ap(apikey, network_id, serial):
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
            write_log(f"Reboot successful for device {serial}.")
            print(f"Reboot successful for device {serial}.")
        else:
            error_msg = f"Failed to reboot device {serial}. Status code: {response.status_code}, Response: {response.text}"
            write_log(error_msg)
            print(f"Error: {error_msg}")
    except requests.RequestException as e:
        error_msg = f"Failed to reboot device {serial}. Exception: {e}"
        write_log(error_msg)
        print(f"Error: {error_msg}")

def reboot_devices_in_network(dashboard, network_id, tags, reboot_all):
    """Reboot devices in the specified network based on tags or all devices."""
    try:
        device_list = dashboard.networks.getNetworkDevices(network_id)
    except Exception as e:
        error_msg = f"Failed to retrieve devices for network {network_id}. Exception: {e}"
        write_log(error_msg)
        print(f"Error: {error_msg}")
        return

    for device in device_list:
        if reboot_all or any(tag in device.get('tags', []) for tag in tags):
            name = device.get('name', 'unknown')
            print(f"Rebooting {name} ({device['serial']}) with tags {device.get('tags', [])}...")
            reboot_ap(apikey, network_id, device['serial'])
            time.sleep(0.5)

def main():
    if '--help' in sys.argv:
        display_help()
        sys.exit(0)
    
    reboot_all = '--all' in sys.argv

    # Load networks from a JSON file
    try:
        with open('networks.json', 'r') as f:
            networks = json.load(f)
    except Exception as e:
        error_msg = f"Failed to load network configurations from 'networks.json'. Exception: {e}"
        write_log(error_msg)
        print(f"Error: {error_msg}")
        sys.exit(1)

    # Initialize Meraki dashboard API
    dashboard = meraki.DashboardAPI(apikey, suppress_logging=True)

    # Iterate over each network in the JSON file and reboot devices
    for network in networks:
        network_id = network.get('networkId')
        tags = network.get('tags', [])
        org_name = network.get('orgName', 'Unknown Organization')

        if not network_id:
            error_msg = f"Skipping network due to missing networkId for organization '{org_name}'."
            write_log(error_msg)
            print(f"Error: {error_msg}")
            continue

        print(f"\nProcessing network '{org_name}' (Network ID: {network_id})...")
        write_log(f"Processing network '{org_name}' (Network ID: {network_id}).")

        reboot_devices_in_network(dashboard, network_id, tags, reboot_all)

if __name__ == "__main__":
    main()
