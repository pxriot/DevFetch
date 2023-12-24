import scapy.all as scapy
import socket
from colorama import Fore, Style

def get_device_name(ip):
    try:
        name = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        name = "Unknown"
    return name

def scan_network():
    arp_request = scapy.ARP(pdst="192.168.1.1/24")
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    devices = []
    for element in answered_list:
        device = {"Name": "", "IP Address": "", "MAC Address": ""}
        device["IP Address"] = element[1].psrc
        device["MAC Address"] = element[1].hwsrc
        device["Name"] = get_device_name(device["IP Address"])
        devices.append(device)

    return devices

devices = scan_network()
print(f"{Fore.RED}Devices Connected to Your Network:{Style.RESET_ALL}")
for device in devices:
    print(f"{Fore.MAGENTA}Hostname: {device['Name']}")
    print(f"{Fore.GREEN}IP Address: {device['IP Address']}")
    print(f"{Fore.GREEN}MAC Address: {device['MAC Address']}\n")
    print(f"{Fore.RED}---------------------------------------------")