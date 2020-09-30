import sys, subprocess, re, time, datetime
import logging, concurrent.futures
import paramiko, netmiko
import xlrd

# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ Error Handeling Imports ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import AuthenticationException
from paramiko.ssh_exception import SSHException
# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ End Error Handeling Imports ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬


# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ Logging ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
# logger = logging.getLogger(__name__) # criar um logger específico deste módulo
# logger.setLevel(logging.DEBUG) # definir o nível de verbosidade do logger

# file_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s') # criar o formato dos logs a aplicar no file_formatter
# steam_formatter = logging.Formatter('%(message)s') # criar o formato dos logs a aplicar no stream_handler

# file_handler = logging.FileHandler('change_ip_helper_address_single.log') # criar ficheiro de logs
# file_handler.setLevel(logging.DEBUG) # definir o nível de verbosidade do file_handler
# file_handler.setFormatter(file_formatter) # aplicar o formato de log anteriormente criado

# stream_handler = logging.StreamHandler() # criar stream_handler que serve para mostrar logs noutros canais
# stream_handler.setLevel(logging.INFO) # definir o nível de verbosidade do stream_handler
# stream_handler.setFormatter(steam_formatter) # aplicar o formato de log anteriormente criado

# logger.addHandler(file_handler) # aplicar file_handler ao logger
# logger.addHandler(stream_handler) # aplicar stream_handler ao logger

logging.basicConfig(filename='netmiko.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")
# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ End Logging ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬


def cls():
	if sys.platform in ('linux', 'darwin'):
		subprocess.run(['clear'])
	elif sys.platform == 'win32':
		subprocess.run(['cls'], shell=True)



def env_exec():
	# source_xl = xlrd.open_workbook('D:\\jcaldeira\\Python Projects\\netmiko-intro\\Cadastro.xlsm')
	# source_sheet_xl = source_xl.sheet_by_name('Cadastro')

	username = 'jcaldeira'
	password = open('pwd_tacacs_ris.txt','r').read()

	equipment = {
	'device_type': 'cisco_xe',
	'ip': '10.254.98.217',
	'username': username,
	'password': password,
	'secret': '1183'
}

	# logger.debug(f'device_list: {equipment}')

	connect_and_commands(equipment)




def connect_and_commands(equipment):
	# logger.info(f"Accessing: {equipment['secret']} ({equipment['ip']})")
	print(f"Accessing: {equipment['secret']} ({equipment['ip']})")
	try:
		with netmiko.ConnectHandler(**equipment) as connection:
			# prompt = connection.find_prompt()
			config_commands = [
				'ip access-list standard teste',
				'ip access-list standard teste2',
				]
			outputs = connection.send_config_set(config_commands = config_commands)

		# pattern_to_search = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'

		# re_result_1 = re.findall(pattern_to_search, output)

		# logger.info(f'outputs: {outputs}')
		print(outputs)

		# if re_result_1 is not None:
		# 	for i in range(0, len(re_result_1)):
		# 		with open('change_ip_helper_address_single.txt', 'a') as f:
		# 			logger.debug(f"{equipment['secret']} ({equipment['ip']}): {re_result_1[i]}")
		# 			f.write(f"{equipment['secret']} ({equipment['ip']}): {re_result_1[i]}\n")


	except NetMikoTimeoutException:
		print(f"Timeout exception on {equipment['secret']} ({equipment['ip']})")

	except AuthenticationException:
		print(f"Authentication failed on {equipment['secret']} ({equipment['ip']})")

	except SSHException:
		print(f"Error reading SSH protocol banner on {equipment['secret']} ({equipment['ip']})")

	except:
		print(f"An error has occurred on {equipment['secret']} ({equipment['ip']})")




if __name__ == '__main__':
	cls()
	time_start = datetime.datetime.now()
	perf_counter_start = time.perf_counter()

	env_exec()

	perf_counter_stop = time.perf_counter()
	time_stop = datetime.datetime.now()

	print(f'Finished in {round(perf_counter_stop - perf_counter_start, 3)} second(s)')
	print(f'Started at {time_start} and finished at {time_stop}\n')
	# logger.info(f'Finished in {round(perf_counter_stop - perf_counter_start, 3)} second(s)')
	# logger.info(f'Started at {time_start} and finished at {time_stop}\n')
