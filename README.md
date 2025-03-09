# Net_Scanner
This Python-based Network Scanner is designed to detect active devices on a local network using ICMP ping, ARP requests, and MAC address lookups. It provides insights into connected devices, including their IP addresses, hostnames, MAC addresses, and manufacturers
Features

Ping-Based Device Detection: Asynchronously pings devices to check if they are online.

ARP-Based Discovery: Uses ARP requests to detect MAC addresses in the subnet.

MAC Address Manufacturer Lookup: Fetches manufacturer details using an external API.

Fast and Efficient Scanning: Uses asyncio for non-blocking execution.

Requirements

Ensure you have the following dependencies installed:
pip install scapy requests

Installation

Clone the repository and navigate to the project directory:
git clone https://github.com/yourusername/NetScanner.git
cd NetScanner

Usage

Run the script and provide a network range when prompted (e.g., 192.168.1.0/24).
python Net_Scanner.py

Example Output:
Enter the network address (e.g., 192.168.1.0/24): 192.168.1.0/24

Scanning network...

--- Alive Devices (from ping) ---
Device Name: MyLaptop, IP: 192.168.1.10
Device Name: Printer, IP: 192.168.1.15

--- Devices (from ARP) ---
Device IP: 192.168.1.10, MAC Address: 00:1A:2B:3C:4D:5E, Manufacturer: Dell Inc.
Device IP: 192.168.1.15, MAC Address: 11:22:33:44:55:66, Manufacturer: HP Inc.

Notes

Administrator privileges may be required to run ARP scans on some systems.

The script queries https://api.macvendors.com/ for manufacturer details.

License

This project is licensed under the MIT License.

Contributing

Pull requests are welcome! If you find any issues, feel free to open an issue or contribute.

Author

Kaushik petkar
