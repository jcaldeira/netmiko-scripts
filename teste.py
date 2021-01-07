from netmiko import ConnectHandler
from getpass import getpass

password = open("/mnt/c/Users/joao.caldeira.ext/Documents/GitHub/netmiko-learning/pwd_tacacs_ris.txt", "r").read()

device = {
    'device_type': 'cisco_xe',
    'host': '10.254.98.22',
    'username': 'jcaldeira',
    'password': password,
    'ssh_config_file': '~/.ssh/config',
}

net_connect = ConnectHandler(**device)
output = net_connect.send_command("show users")
print(output)
