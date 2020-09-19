import sys, subprocess#, re, datetime, os
import logging#, threading
import paramiko, netmiko
# import xlwt, openpyxl, xlrd, xlutils

# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ Error Handeling ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import AuthenticationException
from paramiko.ssh_exception import SSHException


# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ Logging ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

logger = logging.getLogger(__name__) # criar um logger específico deste módulo
logger.setLevel(logging.DEBUG) # definir o nível de verbosidade do logger

file_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s') # criar o formato dos logs a aplicar no file_formatter
steam_formatter = logging.Formatter('%(name)s:%(message)s') # criar o formato dos logs a aplicar no stream_handler

file_handler = logging.FileHandler('netmiko-intro.log') # criar ficheiro de logs
file_handler.setLevel(logging.DEBUG) # definir o nível de verbosidade do file_handler
file_handler.setFormatter(file_formatter) # aplicar o formato de log anteriormente criado

stream_handler = logging.StreamHandler() # criar stream_handler que serve para mostrar logs noutros canais
stream_handler.setLevel(logging.DEBUG) # definir o nível de verbosidade do stream_handler
stream_handler.setFormatter(steam_formatter) # aplicar o formato de log anteriormente criado

logger.addHandler(file_handler) # aplicar file_handler ao logger
logger.addHandler(stream_handler) # aplicar stream_handler ao logger

# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ End Logging ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬


def cls():
	if sys.platform in ('linux', 'darwin'):
		subprocess.run(['clear'])
	elif sys.platform == 'win32':
		subprocess.run(['cls'], shell=True)


def main():

	# hostname =
	management_ip = '10.254.104.174'
	username = 'jcaldeira'
	password = 'CLD@caldeira0'



	equipment = {
		'device_type': 'cisco_xr',
		# 'host': hostname,
		'ip': management_ip,
		'username': username,
		'password': password,
	}

	# logger.debug(f'equipment = {equipment}')

	try:
		with netmiko.ConnectHandler(**equipment) as connection:
			# prompt = connection.find_prompt() # este passo é feito automáticamente pelo método 'send_command'
			# output = connection.send_command('sh ip int b')
			output = connection.find_prompt()
			logger.debug(output)
		output = connection.find_prompt()

	except NetMikoTimeoutException:
		logger.exception('Timeout exception')

	except AuthenticationException:
		logger.exception('Authentication failed')

	except SSHException:
		logger.exception('Error reading SSH protocol banner')






if __name__ == '__main__':
	cls()
	main()
	print()
