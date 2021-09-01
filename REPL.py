from netmiko import ConnectHandler
import re

device = {
    'device_type': 'cisco_ios',
    'host': '',
    'username': 'jcaldeira',
    'password': 'CoN9m2%wVn^G',
    # 'ssh_config_file': '~/.ssh/config',
}
device = {
    'device_type': 'cisco_xe',
    'host': '10.254.111.91',
    'username': 'jcaldeira',
    'password': 'CLD@caldeira0',
    'ssh_config_file': '~/.ssh/config',
}

# net_connect = ConnectHandler(**device, conn_timeout=100)
net_connect = ConnectHandler(**device, conn_timeout=60)

net_connect.config_mode(pattern='(config)')
net_connect.find_prompt()
net_connect.exit_config_mode(pattern='-SW')

config_commands = ['sh run int vlan258']

output = net_connect.send_config_set(
    config_commands=config_commands,
    exit_config_mode=False,
    enter_config_mode=False
)

cfg_file = 'Config files/REPL.ios'

output = net_connect.send_config_from_file(
    config_file=cfg_file,
    exit_config_mode=False,
    enter_config_mode=False
)
print(output)

# net_connect.save_config()
net_connect.disconnect()

output_str = 'sh run | i ip prefix-list BGP-OUT seq\nip prefix-list BGP-OUT seq 5 permit 10.254.112.91/32\nip prefix-list BGP-OUT seq 10 permit 172.17.180.0/24\nip prefix-list BGP-OUT seq 15 permit 10.255.0.36/30\nip prefix-list BGP-OUT seq 20 permit 10.251.131.0/25\nSITE2913-RIS-B#  '

pattern_to_search = r"(10.255.\d{1,3}.\d{1,3}/30)"
compiled_pattern_to_search = re.compile(pattern_to_search)

re_result_1 = re.findall(pattern_to_search, output_str)
print(re_result_1)


re_result_2 = list(filter(compiled_pattern_to_search.search, output_str.split('\n')))
print(f'no {str(re_result_2)}')
