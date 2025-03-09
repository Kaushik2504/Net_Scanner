import asyncio
import subprocess
import platform
import socket
import ipaddress
import requests
from scapy.all import ARP, Ether, srp

# Function to check if the device is alive by pinging the IP asynchronously
async def ping_device(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        # Use asyncio.create_subprocess_exec for non-blocking ping
        process = await asyncio.create_subprocess_exec(
            "ping", param, "1", str(ip), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            # If the device is alive, attempt to get the device name (hostname)
            hostname = await get_device_name(str(ip))
            return ip, hostname
        else:
            return None
    except Exception as e:
        return None

# Function to get the device name (hostname) from the IP address
async def get_device_name(ip):
    try:
        # Attempt reverse DNS lookup to get the hostname
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        # Return the IP if hostname could not be resolved
        return ip

# Function to perform ARP discovery and find MAC addresses
def discover_devices_arp(network):
    # Create an ARP request packet to get MAC addresses of devices in the network
    arp_request = ARP(pdst=network)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    
    # Send the packet and capture the response
    answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    
    devices = []
    for element in answered_list:
        devices.append((element[1].psrc, element[1].hwsrc))  # IP, MAC Address
    
    return devices

# Function to lookup the manufacturer based on MAC address
def get_manufacturer(mac):
    # You can use an external API like macvendors.co or macaddress.io for this
    url = f"https://api.macvendors.com/{mac}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text  # Returns the manufacturer name (like TP-Link, Apple)
        else:
            return "Unknown Manufacturer"
    except requests.exceptions.RequestException:
        return "Error in lookup"

# Function to find alive devices in a network
async def find_alive_devices(network):
    ip_network = ipaddress.IPv4Network(network, strict=False)
    
    tasks = [ping_device(ip) for ip in ip_network.hosts()]
    
    # Wait for all tasks to finish
    alive_devices = await asyncio.gather(*tasks)
    
    # Return only the devices that responded to the ping
    return [result for result in alive_devices if result is not None]

# Main function to run the network scanner
async def net_scanner():
    # Input network (e.g., '192.168.1.0/24')
    network_input = input("Enter the network address (e.g., 192.168.1.0/24): ")

    print("\nScanning network...")
    alive_devices = await find_alive_devices(network_input)

    print("\nDiscovering devices using ARP...")
    arp_devices = discover_devices_arp(network_input)

    print("\n--- Alive Devices (from ping) ---")
    if alive_devices:
        for ip, hostname in alive_devices:
            print(f"Device Name: {hostname}, IP: {ip}")
    else:
        print("No devices found from ping.")

    print("\n--- Devices (from ARP) ---")
    if arp_devices:
        for ip, mac in arp_devices:
            manufacturer = get_manufacturer(mac)
            print(f"Device IP: {ip}, MAC Address: {mac}, Manufacturer: {manufacturer}")
    else:
        print("No devices found from ARP.")

if __name__ == "__main__":
    asyncio.run(net_scanner())
