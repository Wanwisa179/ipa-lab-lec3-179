import paramiko
import os
from dotenv import load_dotenv
load_dotenv()
privatekey = os.getenv("PRIVATE_PATH")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
network='172.31.30.'
for i in range(1, 6):
    ssh.connect(hostname=network+str(i), 
                username='admin', 
                key_filename=privatekey,
                allow_agent=False,
                look_for_keys=False, 
                disabled_algorithms=dict(pubkeys=['rsa-sha2-512', 'rsa-sha2-256']))
    print("connected to "+network+str(i))
    if i == 1:
        stdin, stdout, stderr = ssh.exec_command("sh runn")
        with open('R0_running_config', 'w') as file:
            file.write(stdout.read().decode())
        print("Saved R0 running config file R0_running_config")
    ssh.close()