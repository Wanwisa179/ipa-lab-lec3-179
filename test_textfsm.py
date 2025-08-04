from textfsm_lab import R1Config
from textfsm_lab import R2Config
from textfsm_lab import S1Config
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
        'key_file': privatekey,
        "disabled_algorithms":dict(pubkeys=['rsa-sha2-512', 'rsa-sha2-256'])
    }
    return device

network = "172.31.30."
device = []
device.append(createdevice(network+"3"))
device.append(createdevice(network+"4"))
device.append(createdevice(network+"5"))
info = []
for i in range(3):
    router_connection = ConnectHandler(**device[i])
    info.append(router_connection.send_command("sh int des", use_textfsm=True))
    router_connection.disconnect()

def test_S1():
    S1Config()
    g00, g01, g02 = "", "", ""
    for i in range(len(info[0])):
        if info[0][i]["port"] == "Gi0/0":
            g00 = info[0][i]["description"]
        elif info[0][i]["port"] == "Gi0/1":
            g01 = info[0][i]["description"]
        elif info[0][i]["port"] == "Gi0/2":
            g02 = info[0][i]["description"]
    assert g00 == "Connect to Gig 0/3 of S0"
    assert g01 == "Connect to Gig 0/2 of R2"
    assert g02 == "Connect to PC"

def test_R1():
    R1Config()
    g00, g01, g02 = "", "", ""
    for i in range(len(info[1])):
        if info[1][i]["port"] == "Gi0/0":
            g00 = info[1][i]["description"]
        elif info[1][i]["port"] == "Gi0/1":
            g01 = info[1][i]["description"]
        elif info[1][i]["port"] == "Gi0/2":
            g02 = info[1][i]["description"]
    assert g00 == "Connect to Gig 0/1 of S0"
    assert g01 == "Connect to PC"
    assert g02 == "Connect to Gig 0/1 of R2"

def test_R2():
    R2Config()
    g00, g01, g02, g03 = "", "", "", ""
    for i in range(len(info[2])):
        if info[2][i]["port"] == "Gi0/0":
            g00 = info[2][i]["description"]
        elif info[2][i]["port"] == "Gi0/1":
            g01 = info[2][i]["description"]
        elif info[2][i]["port"] == "Gi0/2":
            g02 = info[2][i]["description"]
        elif info[2][i]["port"] == "Gi0/3":
            g03 = info[2][i]["description"]
    assert g00 == "Connect to Gig 0/2 of S0"
    assert g01 == "Connect to Gig 0/2 of R1"
    assert g02 == "Connect to Gig 0/1 of S1"
    assert g03 == "Connect to WAN"