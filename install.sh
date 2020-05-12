#!/bin/bash
apt-get update
apt install hcxdumptool hcxtools
pip3 install configparser netifaces 
chmod +x pi_attack.py
echo "Installation is complete"

