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
logger = logging.getLogger(__name__) # criar um logger específico deste módulo
logger.setLevel(logging.DEBUG) # definir o nível de verbosidade do logger

file_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s') # criar o formato dos logs a aplicar no file_formatter
steam_formatter = logging.Formatter('%(message)s') # criar o formato dos logs a aplicar no stream_handler

file_handler = logging.FileHandler('netmiko-intro.log') # criar ficheiro de logs
file_handler.setLevel(logging.DEBUG) # definir o nível de verbosidade do file_handler
file_handler.setFormatter(file_formatter) # aplicar o formato de log anteriormente criado

stream_handler = logging.StreamHandler() # criar stream_handler que serve para mostrar logs noutros canais
stream_handler.setLevel(logging.INFO) # definir o nível de verbosidade do stream_handler
stream_handler.setFormatter(steam_formatter) # aplicar o formato de log anteriormente criado

logger.addHandler(file_handler) # aplicar file_handler ao logger
logger.addHandler(stream_handler) # aplicar stream_handler ao logger
# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ End Logging ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬


def cls():
	if sys.platform in ('linux', 'darwin'):
		subprocess.run(['clear'])
	elif sys.platform == 'win32':
		subprocess.run(['cls'], shell=True)



def env_exec():
	source_xl = xlrd.open_workbook('D:\\jcaldeira\\PycharmProjects\\netmiko-intro\\Cadastro.xlsm')
	source_sheet_xl = source_xl.sheet_by_name('Cadastro')

	username = 'jcaldeira'
	password = open('pwd_tacacs_ris.txt','r').read()

	device_list = []
	# xl_row = 1 # counter not in use

	# for row in range(1, source_sheet_xl.nrows):
	# 	if source_sheet_xl.cell_value(row, 5) == "Migrado":
	# 		site_id = source_sheet_xl.cell_value(row, 0)
	# 		management_ip = source_sheet_xl.cell_value(row, 8)
	# 		# nome = source_sheet_xl.cell_value(row, 2)
	# 		# hostname = source_sheet_xl.cell_value(row, 7)
	# 		# cc = source_sheet_xl.cell_value(row, 6)

	# 		# xl_row += 1

	# 		equipment = {
	# 			'device_type': 'cisco_xr',
	# 			'ip': management_ip,
	# 			'username': username,
	# 			'password': password,
	# 			'secret': site_id
	# 		}

	# 		device_list.append(equipment)

	equipment = {
	'device_type': 'cisco_xr',
	'ip': '10.254.103.81',
	'username': username,
	'password': password,
	'secret': '1433'
}

	device_list.append(equipment)


	logger.debug(f'device_list: {device_list}')


	# with concurrent.futures.ThreadPoolExecutor(max_workers = 75) as executor:
	# 	executor.map(connect_and_commands, device_list)

	return len(device_list)




def connect_and_commands(equipment):
	logger.info(f"Accessing: {equipment['secret']} ({equipment['ip']})")
	try:
		with netmiko.ConnectHandler(**equipment) as connection:
			command_string = 'sh ip access-list standart Gestao_PT'
			output = connection.send_command(command_string = command_string)

		pattern_to_search = r'\t05 '

		re_result_1 = re.findall(pattern_to_search, output)

		logger.debug(f're_result_1: {re_result_1}')

		if re_result_1 != None:
			for i in range(0, len(re_result_1)):
				with open('with_05.txt', 'a') as f:
					logger.debug(f"with_05{equipment['secret']} ({equipment['ip']}): {re_result_1[i]}")
					f.write(f"{equipment['secret']} ({equipment['ip']}): {re_result_1[i]}\n")
		else:
			with open('without_05.txt', 'a') as f:
					logger.debug(f"without_05: {equipment['secret']} ({equipment['ip']}): {re_result_1[i]}")
					f.write(f"{equipment['secret']} ({equipment['ip']}): {re_result_1[i]}\n")


	except NetMikoTimeoutException:
		logger.info(f"Timeout exception on {equipment['secret']} ({equipment['ip']})")

	except AuthenticationException:
		logger.info(f"Authentication failed on {equipment['secret']} ({equipment['ip']})")

	except SSHException:
		logger.info(f"Error reading SSH protocol banner on {equipment['secret']} ({equipment['ip']})")

	except:
		logger.exception(f"An error has occurred on {equipment['secret']} ({equipment['ip']})")




if __name__ == '__main__':
	cls()
	time_start = datetime.datetime.now()
	perf_counter_start = time.perf_counter()

	num_equips = env_exec()

	perf_counter_stop = time.perf_counter()
	time_stop = datetime.datetime.now()

	logger.info(f'Number of equipments: {num_equips}')
	logger.info(f'Finished in {round(perf_counter_stop - perf_counter_start, 3)} second(s)')
	logger.info(f'Started at {time_start} and finished at {time_stop}\n')
