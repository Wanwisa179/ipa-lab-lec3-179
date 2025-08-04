from textfsm_lab import R1Config, R2Config, S1Config
from netmiko import ConnectHandler
from dotenv import load_dotenv
import os


def createdevice(ip):
    load_dotenv()
    privatekey = os.getenv("PRIVATE_PATH")
    device = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': 'admin',
        'use_keys': True,
        'key_file': privatekey,
        "disabled_algorithms": dict(pubkeys=['rsa-sha2-512', 'rsa-sha2-256'])
    }
    return device

network = "172.31.30."
device = [
    createdevice(network + "3"),  # S1
    createdevice(network + "4"),  # R1
    createdevice(network + "5"),  # R2
]

def get_interface_info():
    info = []
    for dev in device:
        conn = ConnectHandler(**dev)
        result = conn.send_command("sh int des", use_textfsm=True)
        info.append(result)
        conn.disconnect()
    return info

def test_S1():
    S1Config()
    info = get_interface_info()
    g00, g01, g02 = "", "", ""
    for intf in info[0]:
        if intf["port"] == "Gi0/0":
            g00 = intf["description"]
        elif intf["port"] == "Gi0/1":
            g01 = intf["description"]
        elif intf["port"] == "Gi0/2":
            g02 = intf["description"]
    assert g00 == "Connect to Gig 0/3 of S0"
    assert g01 == "Connect to Gig 0/2 of R2"
    assert g02 == "Connect to PC"

def test_R1():
    R1Config()
    info = get_interface_info()
    g00, g01, g02 = "", "", ""
    for intf in info[1]:
        if intf["port"] == "Gi0/0":
            g00 = intf["description"]
        elif intf["port"] == "Gi0/1":
            g01 = intf["description"]
        elif intf["port"] == "Gi0/2":
            g02 = intf["description"]
    assert g00 == "Connect to Gig 0/1 of S0"
    assert g01 == "Connect to PC"
    assert g02 == "Connect to Gig 0/1 of R2"

def test_R2():
    R2Config()
    info = get_interface_info()
    g00, g01, g02, g03 = "", "", "", ""
    for intf in info[2]:
        if intf["port"] == "Gi0/0":
            g00 = intf["description"]
        elif intf["port"] == "Gi0/1":
            g01 = intf["description"]
        elif intf["port"] == "Gi0/2":
            g02 = intf["description"]
        elif intf["port"] == "Gi0/3":
            g03 = intf["description"]
    assert g00 == "Connect to Gig 0/2 of S0"
    assert g01 == "Connect to Gig 0/2 of R1"
    assert g02 == "Connect to Gig 0/1 of S1"
    assert g03 == "Connect to WAN"
