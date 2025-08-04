from netmiko import ConnectHandler
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
import os

load_dotenv()
privatekey = os.getenv("PRIVATE_PATH")

def createdevice(ip):
    return {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': 'admin',
        'use_keys': True,
        'key_file': privatekey,
        "disabled_algorithms": dict(pubkeys=['rsa-sha2-512', 'rsa-sha2-256'])
    }

env = Environment(loader=FileSystemLoader("config"))

network = "172.31.30."
devices = {
    "S1": {
        "ip": network + "3",
        "template": "switch.j2",
        "data": {
            "vlan": {
                "id": 101,
                "name": "control-data",
                "interfaces": ["g0/1", "g0/2"]
            },
            "access_list": ["172.31.30.0 0.0.0.15", "193.168.82.0 0.0.0.255"]
        }
    },
    "R1": {
        "ip": network + "4",
        "template": "router.j2",
        "data": {
            "ospf": {
                "process_id": 69,
                "vrf": "control-data",
                "networks": [
                    {"ip": "172.31.30.32", "wildcard": "0.0.0.255", "area": 0},
                    {"ip": "172.31.30.16", "wildcard": "0.0.0.255", "area": 0}
                ],
                "default_originate": False
            },
            "access_list": ["172.31.30.0 0.0.0.15", "193.168.82.0 0.0.0.255"]
        }
    },
    "R2": {
        "ip": network + "5",
        "template": "router.j2",
        "data": {
            "ospf": {
                "process_id": 69,
                "vrf": "control-data",
                "networks": [
                    {"ip": "172.31.30.16", "wildcard": "0.0.0.255", "area": 0},
                    {"ip": "172.31.30.48", "wildcard": "0.0.0.255", "area": 0}
                ],
                "default_originate": True
            },
            "access_list": ["172.31.30.0 0.0.0.15", "193.168.82.0 0.0.0.255"], 
            "loopback": {
                "name": "Loopback0",
                "ip": "127.0.0.2",
                "mask": "255.255.255.255"
            }
        }
    }
}

for name, info in devices.items():
    template = env.get_template(info["template"])
    config_commands = template.render(**info["data"]).splitlines()

    connection = ConnectHandler(**createdevice(info["ip"]))
    output = connection.send_config_set(config_commands)
    print(output)
    connection.disconnect()