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

file_handler = logging.FileHandler('change_ip_helper_address_single.log') # criar ficheiro de logs
file_handler.setLevel(logging.DEBUG) # definir o nível de verbosidade do file_handler
file_handler.setFormatter(file_formatter) # aplicar o formato de log anteriormente criado

stream_handler = logging.StreamHandler() # criar stream_handler que serve para mostrar logs noutros canais
stream_handler.setLevel(logging.INFO) # definir o nível de verbosidade do stream_handler
stream_handler.setFormatter(steam_formatter) # aplicar o formato de log anteriormente criado

main_logger.addHandler(file_handler) # aplicar file_handler ao logger
main_logger.addHandler(stream_handler) # aplicar stream_handler ao logger

logging.basicConfig(filename='Logs\\netmiko.log', level=logging.DEBUG)
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

	equipment = {
	'device_type': 'cisco_xe',
	'ip': '10.254.102.141',
	'username': username,
	'password': password,
	'secret': '2640'
}

	main_logger.debug(f'device_list: {equipment}')

	connect_and_commands(equipment)




def connect_and_commands(equipment):
	main_logger.info(f"Accessing: {equipment['secret']} ({equipment['ip']})")
	try:
		with netmiko.ConnectHandler(**equipment) as connection:
			config_commands = [
				'',
				''
				]
			connection.config_mode(pattern = '(config)')
			connection.send_config_set(config_commands = config_commands, exit_config_mode = False, enter_config_mode = False)
			connection.exit_config_mode(pattern = 'SITE')
			connection.send_command('wr')



	except NetMikoTimeoutException:
		main_logger.info(f"Timeout exception on {equipment['secret']} ({equipment['ip']})")

	except AuthenticationException:
		main_logger.info(f"Authentication failed on {equipment['secret']} ({equipment['ip']})")

	except SSHException:
		main_logger.info(f"Error reading SSH protocol banner on {equipment['secret']} ({equipment['ip']})")

	except:
		main_logger.info(f"An error has occurred on {equipment['secret']} ({equipment['ip']})")




if __name__ == '__main__':
	cls()
	time_start = datetime.datetime.now()
	perf_counter_start = time.perf_counter()

	env_exec()

	perf_counter_stop = time.perf_counter()
	time_stop = datetime.datetime.now()

	main_logger.info(f'Finished in {round(perf_counter_stop - perf_counter_start, 3)} second(s)')
	main_logger.info(f'Started at {time_start} and finished at {time_stop}\n')
