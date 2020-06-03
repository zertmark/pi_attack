#!/bin/bash
apt-get update
apt install hcxdumptool hcxtools nmap traceroute iproute perl git wget  
pip3 install configparser netifaces 
chmod +x pi_attack.py
echo "Installation is complete"

