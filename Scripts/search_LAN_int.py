import sys, subprocess, re, time, datetime
import logging, concurrent.futures
import paramiko, netmiko

# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ Error Handeling Imports ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import AuthenticationException
from paramiko.ssh_exception import SSHException
# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ End Error Handeling Imports ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬


# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ Logging ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
main_logger = logging.getLogger(__name__) # criar um logger específico deste módulo
main_logger.setLevel(logging.DEBUG) # definir o nível de verbosidade do logger

file_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s') # criar o formato dos logs a aplicar no file_formatter
steam_formatter = logging.Formatter('%(message)s') # criar o formato dos logs a aplicar no stream_handler

file_handler = logging.FileHandler('netmiko-intro.log') # criar ficheiro de logs
file_handler.setLevel(logging.DEBUG) # definir o nível de verbosidade do file_handler
file_handler.setFormatter(file_formatter) # aplicar o formato de log anteriormente criado

stream_handler = logging.StreamHandler() # criar stream_handler que serve para mostrar logs noutros canais
stream_handler.setLevel(logging.INFO) # definir o nível de verbosidade do stream_handler
stream_handler.setFormatter(steam_formatter) # aplicar o formato de log anteriormente criado

main_logger.addHandler(file_handler) # aplicar file_handler ao logger
main_logger.addHandler(stream_handler) # aplicar stream_handler ao logger

logging.basicConfig(filename='netmiko.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")
# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ End Logging ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬


def cls():
	if sys.platform in ('linux', 'darwin'):
		subprocess.run(['clear'])
	elif sys.platform == 'win32':
		subprocess.run(['cls'], shell=True)



def env_exec():

	username = 'jcaldeira'
	password = open('pwd_tacacs_ris.txt','r').read()

	device_list = []

	equipment = {
	'device_type': 'cisco_xe',
	'ip': '10.254.98.22',
	'username': username,
	'password': password,
	'secret': '0931'
}

	device_list.append(equipment)


	main_logger.debug(f'device_list: {device_list}')


	return len(device_list)




def connect_and_commands(equipment):
	main_logger.info(f"Accessing: {equipment['secret']} ({equipment['ip']})")
	try:
		with netmiko.ConnectHandler(**equipment) as connection:
			command_string = 'show ip interfade brief'
			output = connection.send_command(command_string = command_string)

		pattern_to_search = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.'


		re_result_1 = re.search(pattern_to_search, ip_lan).group()

		main_logger.debug(f're_result_1: {re_result_1}')

		if re_result_1 != None:
			for i in range(0, len(re_result_1)):
				with open('with_05.txt', 'a') as f:
					main_logger.debug(f"with_05{equipment['secret']} ({equipment['ip']}): {re_result_1[i]}")
					f.write(f"{equipment['secret']} ({equipment['ip']}): {re_result_1[i]}\n")
		else:
			with open('without_05.txt', 'a') as f:
					main_logger.debug(f"without_05: {equipment['secret']} ({equipment['ip']}): {re_result_1[i]}")
					f.write(f"{equipment['secret']} ({equipment['ip']}): {re_result_1[i]}\n")


	except NetMikoTimeoutException:
		main_logger.info(f"Timeout exception on {equipment['secret']} ({equipment['ip']})")

	except AuthenticationException:
		main_logger.info(f"Authentication failed on {equipment['secret']} ({equipment['ip']})")

	except SSHException:
		main_logger.info(f"Error reading SSH protocol banner on {equipment['secret']} ({equipment['ip']})")

	except:
		main_logger.exception(f"An error has occurred on {equipment['secret']} ({equipment['ip']})")




if __name__ == '__main__':
	cls()
	time_start = datetime.datetime.now()
	perf_counter_start = time.perf_counter()

	num_equips = env_exec()

	perf_counter_stop = time.perf_counter()
	time_stop = datetime.datetime.now()

	main_logger.info(f'Number of equipments: {num_equips}')
	main_logger.info(f'Finished in {round(perf_counter_stop - perf_counter_start, 3)} second(s)')
	main_logger.info(f'Started at {time_start} and finished at {time_stop}\n')
