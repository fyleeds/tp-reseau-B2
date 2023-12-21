import os
import sys

def lookup(command):
    current_directory = os.getcwd()
    filePath = current_directory + "/lookup.py"
    os.system(f"python3 {filePath} {command}")
def ping(command):
    current_directory = os.getcwd()
    filePath = current_directory + "/is_up.py"
    os.system(f"python3 {filePath} {command}")
def get_wifi_ip():
    current_directory = os.getcwd()
    filePath = current_directory + "/get_ip.py"
    os.system(f"python3 {filePath} ")

if (len(sys.argv) >= 2):
    option = sys.argv[1]

    if (len(sys.argv) >= 3):
        option2 = sys.argv[2]
        if(option == "lookup"):
            lookup(option2)
        elif(option == "ping"):
            ping(option2)
        else:
            print(f"{option} is not an available command. Déso.")
    else :
        if(option == "ip"):
            get_wifi_ip()
        else:
            print(f"{option} is not an available command. Déso.")

elif (len(sys.argv) >2):
    print("Too many arguments. Déso.")
else:
    pass


