from netmiko import ConnectHandler
from dotenv import load_dotenv

import os
#import logging
#logging.basicConfig(filename="ssh_log", level=logging.DEBUG) Just for loggin authen dont worry
def createdevice(ip):#Create template for all device
    load_dotenv()
    privatekey = os.getenv("PRIVATE_PATH")
    device = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': 'admin',
        'use_keys': True,
        'key_file': privatekey, #Dont worry only ai i use in this lab is just gimini in google search
        "disabled_algorithms":dict(pubkeys=['rsa-sha2-512', 'rsa-sha2-256'])
    }
    return device

network = "172.31.30."
R1 = createdevice(network+"4")
R2 = createdevice(network+"5")
S1 = createdevice(network+"3")

S1_config_commands = ["vlan 101", "name control-data", "exit",  
                    "int g0/1", "switchport mode access", "switchport access vlan 101", "exit",  
                    "int g0/2", "switchport mode access", "switchport access vlan 101", "no access-list 2", 
                    "access-list 2 permit 172.31.30.0 0.0.0.15",
                    "access-list 2 permit 193.168.82.0 0.0.0.255",
                    "line vty 0 4", "access-class 2 in vrf-also"]
R1_config_commands = ["router ospf 69 vrf control-data", 
                    "network 172.31.30.32 255.255.255.0 area 0", 
                    "network 172.31.30.16 255.255.255.0 area 0", "exit", "no access-list 2", 
                    "access-list 2 permit 172.31.30.0 0.0.0.15",
                    "access-list 2 permit 193.168.82.0 0.0.0.255",
                    "line vty 0 4", "access-class 2 in vrf-also"]
R2_config_commands = ["int lo0", "ip add 127.0.0.2 255.255.255.255", "exit", 
                    "router ospf 69 vrf control-data", 
                    "network 172.31.30.16 255.255.255.0 area 0", 
                    "network 172.31.30.48 255.255.255.0 area 0", 
                    "default-information originate", "exit",  "no access-list 2", 
                    "access-list 2 permit 172.31.30.0 0.0.0.15",
                    "access-list 2 permit 193.168.82.0 0.0.0.255",
                    "line vty 0 4", "access-class 2 in vrf-also"]
S1_connnect = ConnectHandler(**S1)
output = S1_connnect.send_config_set(S1_config_commands)
print(output)
S1_connnect.disconnect()
R1_connnect = ConnectHandler(**R1)
output = R1_connnect.send_config_set(R1_config_commands)
print(output)
R1_connnect.disconnect()
R2_connnect = ConnectHandler(**R2)
output = R2_connnect.send_config_set(R2_config_commands)
print(output)
R2_connnect.disconnect()