import netmiko
import re
# import xdrlib

def main():
	hosts = {
		'host': str,
		'device_type': str,
		'username': str,
		'password': str
	}

	connection = netmiko.ConnectHandler(**hosts)





if __name__ == '__main__':
	main()
