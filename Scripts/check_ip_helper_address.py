import sys, subprocess, re, time, datetime, os
import logging, concurrent.futures
import paramiko, netmiko
import xlrd
# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ Error Handeling Imports ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import AuthenticationException
from paramiko.ssh_exception import SSHException
# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ End Error Handeling Imports ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬


# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ Logging ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
script_name = os.path.splitext(__file__)
script_name = os.path.basename(script_name[0])

if __name__ == "__main__":
	main_logger = logging.getLogger(script_name)  # criar um logger específico deste módulo se for invocado diretamente
else:
	main_logger = logging.getLogger(__name__)  # criar um logger específico deste módulo se for importado de outro módulo

main_logger.setLevel(logging.DEBUG)  # definir o nível de verbosidade do logger

file_formatter = logging.Formatter(
    "%(asctime)s |%(levelname)s |%(name)s |%(message)s"
)  # criar o formato dos logs a aplicar no file_formatter
stream_formatter = logging.Formatter(
    "%(message)s"
)  # criar o formato dos logs a aplicar no stream_handler

file_handler = logging.FileHandler(
    f"Logs\\{script_name}.log"
)  # criar ficheiro de logs
file_handler.setLevel(logging.DEBUG)  # definir o nível de verbosidade do file_handler
file_handler.setFormatter(
    file_formatter
)  # aplicar o formato de log anteriormente criado

stream_handler = (
    logging.StreamHandler()
)  # criar stream_handler que serve para mostrar logs noutros canais
stream_handler.setLevel(
    logging.INFO
)  # definir o nível de verbosidade do stream_handler
stream_handler.setFormatter(
    stream_formatter
)  # aplicar o formato de log anteriormente criado

main_logger.addHandler(file_handler)  # aplicar file_handler ao logger
main_logger.addHandler(stream_handler)  # aplicar stream_handler ao logger

logging.basicConfig(filename="Logs\\netmiko.log", level=logging.DEBUG)
logger = logging.getLogger("netmiko")
# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ End Logging ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬


def cls():
    if sys.platform in ("linux", "darwin"):
        subprocess.run(["clear"])
    elif sys.platform == "win32":
        subprocess.run(["cls"], shell=True)


def env_exec():
    source_xl = xlrd.open_workbook(
        "D:\\jcaldeira\\Python Projects\\netmiko-intro\\Cadastro.xlsm"
    )
    source_sheet_xl = source_xl.sheet_by_name("Cadastro")

    username = "jcaldeira"
    password = open("pwd_tacacs_ris.txt", "r").read()

    device_list = []
    # xl_row = 1 # counter not in use

    for row in range(1, source_sheet_xl.nrows):
        if (
            source_sheet_xl.cell_value(row, 5) == "Migrado"
            and source_sheet_xl.cell_value(row, 16) == "Sim"
        ):
            site_id = source_sheet_xl.cell_value(row, 0)
            management_ip = source_sheet_xl.cell_value(row, 8)
            # nome = source_sheet_xl.cell_value(row, 2)
            # hostname = source_sheet_xl.cell_value(row, 7)
            # cc = source_sheet_xl.cell_value(row, 6)

            # xl_row += 1

            equipment = {
                "device_type": "cisco_xe",
                "ip": management_ip,
                "username": username,
                "password": password,
                "secret": site_id,
            }

            device_list.append(equipment)

    main_logger.debug(f"device_list: {device_list}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(connect_and_commands, device_list)

    return len(device_list)


def connect_and_commands(equipment):
    main_logger.info(f"Accessing: {equipment['secret']} ({equipment['ip']})")
    regexes = {
        "10.30.2.151",
        "10.30.2.152",
    }

    with open("Logs\\check_ip_helper_address__ERRO.log", "a") as f_log:
        with open("Logs\\check_ip_helper_address.txt", "a") as f_txt:
            try:
                with netmiko.ConnectHandler(**equipment) as connection:
                    commands = "show run | i ip helper-address"
                    output = connection.send_command(command_string=commands)

                    pattern_to_search = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
                    re_result = set(re.findall(pattern_to_search, output))

                    list_compare = regexes.intersection(re_result)

                if regexes == list_compare:
                    f_txt.write(f"{equipment['secret']} ({equipment['ip']}): OK\n")

                elif regexes != list_compare:
                    diff_str = ""
                    for item in regexes.difference(re_result):
                        diff_str = f"{diff_str} {item} "
                    f_txt.write(
                        f"{equipment['secret']} ({equipment['ip']}): NOK: {diff_str}\n"
                    )

            except NetMikoTimeoutException as exep:
                # main_logger.exception(f"Timeout exception on {equipment['secret']} ({equipment['ip']})")
                main_logger.info(f" {exep}: {equipment['secret']} ({equipment['ip']})")
                # with open("Logs\\check_ip_helper_address__ERRO.log", "a") as f:
                f_log.write(f"{equipment['secret']} ({equipment['ip']}): {exep}\n")

            except AuthenticationException as exep:
                # main_logger.exception(f"Authentication failed on {equipment['secret']} ({equipment['ip']})")
                main_logger.info(f" {exep}: {equipment['secret']} ({equipment['ip']})")
                # with open("Logs\\check_ip_helper_address__ERRO.log", "a") as f:
                f_log.write(f"{equipment['secret']} ({equipment['ip']}): {exep}\n")

            except SSHException as exep:
                # main_logger.exception(f"Error reading SSH protocol banner on {equipment['secret']} ({equipment['ip']})")
                main_logger.info(f" {exep}: {equipment['secret']} ({equipment['ip']})")
                # with open("Logs\\check_ip_helper_address__ERRO.log", "a") as f:
                f_log.write(f"{equipment['secret']} ({equipment['ip']}): {exep}\n")

            except:
                # main_logger.info(f"An error has occurred on {equipment['secret']} ({equipment['ip']})")
                main_logger.exception(f"{equipment['secret']} ({equipment['ip']})")


if __name__ == "__main__":
    cls()
    time_start = datetime.datetime.now()
    perf_counter_start = time.perf_counter()

    num_equips = env_exec()

    perf_counter_stop = time.perf_counter()
    time_stop = datetime.datetime.now()

    main_logger.info(f"Number of equipments: {num_equips}")
    main_logger.info(
        f"Finished in {round(perf_counter_stop - perf_counter_start, 3)} second(s)"
    )
    main_logger.info(f"Started at {time_start} and finished at {time_stop}\n")
