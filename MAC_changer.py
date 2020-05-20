#!/usr/bin/env python

import subprocess
import optparse
import re

# A simple script for changing an interface Mac Address

# Usage :  $ python MAC_changer.py -i <interface> -m <mac address>
# Use --help for help

# Get User Input function
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest='interface', help='Interface to change its MAC address')
    parser.add_option('-m', '--mac', dest='new_mac', help='New MAC Address')
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error('[-] Please specify an interface. Use --help for more info.')
    elif not options.new_mac:
       parser.error('[-] Please specify a new mac address. Use --help for more info.')
    return options

# Change Mac Address function
def change_mac(interface, new_mac):
    print('[+] Changing MAC address for ' + interface + 'to ' + new_mac)
    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['ifconfig', interface, 'up'])

# Get current Mac address Function
def get_current_mac(interface):
    # Check and Print ifconfig
    ifconfig_result = subprocess.check_output(['ifconfig', interface])

    # Regex code to search ifconfig for mac address only
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read mac address.")

# Code Execution
options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Current MAC Address:" + str(current_mac))
change_mac(options.interface, options.new_mac)

# Check if current Mac is same as user-requested Mac
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC Address was successfully changed to " + current_mac)
else:
    print("[-] MAC Address did not get changed.")


