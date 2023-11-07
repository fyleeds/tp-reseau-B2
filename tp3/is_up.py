import os
import sys

option1 = sys.argv[1]
command2 = f"ping -c1 {option1}"
result = os.system(command2)

print("\n")

if result == 0:
    print("UP!")
else:
    print("DOWN!")

