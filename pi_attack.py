import netifaces 
import configparser
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
  interface=config["net_interface"]["Net_interface"]
  startup=config["startup"]["Run on startup"]
  check_daemon(startup) 
  enable_monitor_mode(interface)
 else:
  print_info("Config.ini wasn't found.Creating config...")
  interface=input("\nInterfaces:{}\nPlease enter your wifi interface:".format(netifaces.interfaces()))
  if interface in netifaces.interfaces():
   print_good("Setting {} as wifi interface".format(interface))	
   auto_load=input("Do you want to start this script on startup?(Y/n):")
   if auto_load.lower != "y" and auto_load.lower !='n':
    print_error("Invalid choice.Setting script on startup as default")
    auto_load='Y'
   print_info("Writing settings to config file")
   write_config(config,interface,auto_load.upper())
   check_daemon(auto_load.upper())
   print_info("Please restart script to apply changes from config file")
   exit()
  else:
   print_error("Invalid interface");exit() 
def write_config(config,interface,auto_load): 
 config["net_interface"]={'Net_interface':interface}
 config["startup"]={'Run on startup':auto_load}
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
main()

