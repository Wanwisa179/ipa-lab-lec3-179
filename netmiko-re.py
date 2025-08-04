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
router = []
router.append(createdevice(network+"4"))
router.append(createdevice(network+"5"))

for i in range(2):
    router_connection = ConnectHandler(**router[i])
    int_br = router_connection.send_command("sh ip int br")
    acitve_interfaces = re.findall("(\\w*\\d\\/\\d)(?:.*up.*)", int_br)
    print("R"+str(i+1)+" active interfaces :\n", *acitve_interfaces)
    version = router_connection.send_command("sh version")
    print(" "+re.search("uptime is \\d* hours, \\d* minutes", version).group(0))
    router_connection.disconnect()