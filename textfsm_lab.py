from netmiko import ConnectHandler
from dotenv import load_dotenv
import re
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

def config_gen(cdpnei):
    config = []
    for i in range(len(cdpnei)):
        local_interface = cdpnei[i]['local_interface'].replace(" ", "")
        remote_interface = cdpnei[i]['platform']+" "+cdpnei[i]['neighbor_interface']
        neighbor = re.sub(r'\..*', '', cdpnei[i]['neighbor_name'])
        config.append('int '+local_interface)
        config.append('no description')
        config.append('des Connect to {} of {}'.format(remote_interface, neighbor))
        config.append('exit')
    return config

def R1Config():
    R1 = createdevice("172.31.30.4")
    R1_connnect = ConnectHandler(**R1)
    output = R1_connnect.send_command("show cdp neighbors", use_textfsm=True)
    config = config_gen(output)
    config.extend(['int Gig0/1', 'des Connect to PC'])
    R1_connnect.send_config_set(config)
    R1_connnect.disconnect()

def R2Config():
    R2 = createdevice("172.31.30.5")
    R2_connnect = ConnectHandler(**R2)
    output = R2_connnect.send_command("show cdp neighbors", use_textfsm=True)
    config = config_gen(output)
    config.extend(['int Gig0/3', 'des Connect to WAN'])
    R2_connnect.send_config_set(config)
    R2_connnect.disconnect()

def S1Config():
    S1 = createdevice("172.31.30.3")
    S1_connnect = ConnectHandler(**S1)
    output = S1_connnect.send_command("show cdp neighbors", use_textfsm=True)
    config = config_gen(output)
    config.extend(['int Gig0/2', 'des Connect to PC'])
    S1_connnect.send_config_set(config)
    S1_connnect.disconnect()