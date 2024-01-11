# On importe la lib argparse
import argparse
import sys
import logging
import time
import psutil
# Création d'un objet ArgumentParser
# parser = argparse.ArgumentParser()

# # On ajoute la gestion de l'option -n ou --name
# # "store" ça veut dire qu'on attend un argument à -n

# # on va stocker l'argument dans une variable
# parser.add_argument( help="Usage: python bs_server.py [OPTION]..."
#                     "Run a server"
#                     "Mandatory arguments to long options are mandatory for short options too."
#                     "-h, --help                  Help of the command"
# )

# # Permet de mettre à jour notre objet ArgumentParser avec les nouvelles options
# # 
# if (parser.parse_args()):
#     args = parser.parse_args()
# else : 
#     pass
# print(args.port)

# if (args.port < 0 or args.port> 65535):
#     print("ERROR Le port spécifié n'est pas un port possible (de 0 à 65535).")
#     sys.exit(1)
# elif (args.port >= 0 and args.port<= 1024):
#     print("ERROR Le port spécifié est un port privilégié. Spécifiez un port au dessus de 1024.")
#     sys.exit(2)

class CustomFormatter(logging.Formatter):

    yellow = "\x1b[33;20m"
    reset = "\x1b[0m"

    FORMATS = {
        logging.WARNING: yellow + "%(levelname)s %(asctime)s %(message)s" + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


try:
    # Create a custom logger
    logger = logging.getLogger("monit_logger")
    logger.setLevel(logging.DEBUG)  # This needs to be DEBUG to capture all levels of logs

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('./var/log/monit_log')
    c_handler.setLevel(logging.DEBUG)  # Set to DEBUG to ensure all levels are logged to console
    f_handler.setLevel(logging.DEBUG)  # Set to DEBUG to ensure all levels are logged to file

    # Create formatters and add it to handlers
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    c_handler.setFormatter(CustomFormatter())
    f_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
except Exception as e:
    print(f"Failed to configure logging: {e}")
    sys.exit(1)



logger.info("Le programme tourne")


def getCpuTimes():
    cpu_times = psutil.cpu_times()
    return cpu_times

def getCpusPercent():
    cpus_percent = psutil.cpu_percent(interval=1, percpu=True)
    return cpus_percent

def getCpuTimeUser():  
    cpu_time_user = round(getCpuTimes().user,2)
    logger.info("user time spend : %s",cpu_time_user)
    return cpu_time_user

def getCpuTimeSystem():  
    cpu_time_system = round(getCpuTimes().system,2)
    logger.info("system time spend : %s",cpu_time_system)
    return cpu_time_system

def getCpuTimeIdle():  
    cpu_time_idle = round(getCpuTimes().idle,2)
    logger.info("idle time spend: %s",cpu_time_idle)
    return cpu_time_idle

def getCpusPercentFormatted():
    cpus_percent =  getCpusPercent() 
    i=1
    cpus_percent_list = []
    logger.info("cpu list %s ",cpus_percent)
    for cpu_percent in cpus_percent:
        if cpu_percent != 0.0 :
            cpus_percent_list.append("cpu" + str(i) + " utilization: " + str(cpu_percent) +" % ")
            logger.info("cpu %s utilization: %s", i, cpu_percent)
            i = i + 1
    # cpu_time_idle = round(getCpuTimes().idle,2)
    return cpus_percent_list


def main():
    getCpuTimeUser()
    getCpuTimeSystem()
    getCpuTimeIdle()
    getCpusPercentFormatted()

if __name__ == "__main__":
    main()