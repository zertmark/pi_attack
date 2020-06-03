#!/bin/python3 
from pyroute2 import IPRoute
import urllib
from scapy import *
from scapy.all import *
import shutil
import socket 
from socket import *
import netifaces 
import scapy
from os import system
import configparser
import threading
import os
from os import system
def print_error(text):
 print("[-] {}".format(text))
def print_info(text):
 print("[*] {}".format(text))
def print_good(text):
 print("[+] {}".format(text))
def parse_config():
 config=configparser.ConfigParser()
 if os.path.exists("config.ini"):
  print_good("Using wifi interface from config.ini file")
  config.read('config.ini')
  interface=config["net_interface"]["net_interface"]
  startup=config["startup"]["run on startup"]
  self_dis=config['system_distraction']["add system-destroyer script if something goes wrong"]
  snif=config["auto_scan"]["Enable auto-scan script"]
  check_script(self_dis)
  check_daemon(startup) 
  scan_network(interface)
  #enable_monitor_mode(interface)
 else:
  print_info("Config.ini wasn't found.Creating config...")
  interface=input("\nInterfaces:{}\nPlease enter your wifi interface:".format(netifaces.interfaces()))
  if interface in netifaces.interfaces():
    print_good("Setting {} as wifi interface".format(interface)) 
    auto_load=input("Do you want to start this script on startup?(Y/n):")
    selfdis=input("Do you want to add script which destroys system?(if something goes wrong)(y/N):")
    scan=input("Do you want scan all network?(if your device will be connected to Internet. After scan you can check file map.html to view results)(Y/n):") 
    if auto_load.lower()!= "y" and auto_load.lower()!="n":
     print_error("Invalid choice.Setting script on startup as default")
     auto_load='Y'
    if selfdis.lower()!="y" and selfdis.lower()!="n":
     print_error("Invalid choice. Setting system-distroyer script off by default")
     selfdis='N'
    if scan.lower()!="y" and scan.lower()!="n":
     print_error("Invalid choice. Setting auto-scannig on by default")
     scan='Y'
    print_info("Writing settings to config file")
    write_config(config,interface,auto_load.upper(),selfdis.upper(),scan)
    check_daemon(auto_load.upper())
    print_info("Please restart script to apply changes from config file")
    exit() 
  else:
   print_error("Invalid interface")
   exit() 
def check_script(self_dis):
 if self_dis.lower() == 'y':
  if os.path.exists("/bin/destroyer"):
   print_good("System-destroyer script is ready to use")
  else:
   print_info("System-destroyer script wasn't found.Creating script...")
   shutil.copy2("destroyer","/bin/destroyer"); system("chmod +x /bin/destroyer") 
   print_good("System-destroyer script was created and ready to use(/bin/destroyer)(just type destroyer)")
 else:
  pass
def write_config(config,interface,auto_load,selfdis,scan): 
 config["net_interface"]={'Net_interface':interface}
 config["startup"]={'Run on startup':auto_load}
 config["system_distraction"]={'Add system-destroyer script if something goes wrong':selfdis}
 config["auto_scan"]={"Enable auto-scan script":scan}
 with open("config.ini",'w') as config_file:
  config.write(config_file)
 print_good("Config was created")
def main():
 print_info("Starting...")
 parse_config()
def check_daemon(load_on_startup):
 if os.path.exists('/lib/systemd/system/pi_attack.service'):
  print_good("Daemon was found.Checking configuration...")
  if load_on_startup=="N":
   print_good("Changing daemon...")
   system("systemctl disable pi_attack.service")
  else:
   system("systemctl enable pi_attack.service") 
 else:
  print_error("Daemon wasn't found")
  create_daemon()
def create_daemon():
 print_info("Creating daemon...")
 with open("/lib/systemd/system/pi_attack.service",'w') as file:
  with open("daemon_text",'r') as daemon:
   file.write(daemon.read().format(os.path.join(os.getcwd(),__file__)))
   system("chmod 644 /lib/systemd/system/pi_attack.service && systemctl daemon-reload")   
 print_good("Daemon was created")
def start_capture(interface):
 try:
  print_good("Starting capturing PKMID's")
  system("hcxdumptool -i {} -o capture.pcapng --enable_status=15".format(interface))
 except KeyboardInterrupt:
  print_info("Stopping...")
  exit()
def enable_monitor_mode(interface):
 print_info("Starting monitor mode...")
 if interface in netifaces.interfaces():
  try:
   system("airmon-ng check kill && airmon-ng start {}".format(interface))
  except:
   print_error("Error while starting monitor mode")
   exit() 
  start_capture(interface+'mon')
 else:
  print_error("Interface from config file wasn't found")    
  exit()
#def sniff(snif,interface,filter):
# if snif.lower() != 'n':
#  if check_internet_connection != False:
#   print_good("Starting sniffer...")
#   sniffer=AsyncSniffer(iface=interface,filter=filter)
#   sniffer.start()
#   time.sleep(1)
#   while len(sniffer.results)<3000:
#    print(hashdump(sniffer.results)) 
#   if len(sniffer.results) == 3000:
#    sniffer.stop()
#    wrpcap("{}.cap".format(generate_name()),pkts)
#    print_good("Packets were saved. Restarting...")
#    sniff(snif,interface,filter)
#  else:
#   print_error("There is no internet connection. Waiting 5 minutes to next try")
#   time.sleep(300)
#   sniff(snif,interface,filter)
# else:
#  pass
def scan_network(interface):
 if check_internet_connection != False:
  if os.path.exists("nmap/"):
   print_info("Starting to scan network")
   system('cd nmap/ && ./nmapscan.pl')
  else:
   print_error("Directory nmap isn't found")
   exit()
 else:
  print_error("Internet connection isn't establish")
  exit() 
#def mask(interface):
# import socket
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.connect(("8.8.8.8", 80))
# print(s.getsockname()[0])
# ip = IPRoute()
# info = [{'iface': x['index'],
#         'addr': x.get_attr('IFA_ADDRESS'),
#         'mask': x['prefixlen']} for x in ip.get_addr()]
# print(info)
# ip.close()
def check_internet_connection():
 try:
  urllib.open("http://google.com")
  return True
 except IOError:
  return False
if __name__=="__main__":
 main()
