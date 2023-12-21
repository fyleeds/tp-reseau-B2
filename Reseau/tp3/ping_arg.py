import os
import sys

option1 = sys.argv[1]
command = f"ping {option1}"
# print(command)
result = os.system(command)
