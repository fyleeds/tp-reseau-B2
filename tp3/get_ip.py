import psutil
import sys
import os

# Get information about network interfaces
network_info = psutil.net_if_addrs()

# Iterate through network interfaces
for interface, addresses in network_info.items():
    for address in addresses:
        test=address.address.split('.')
        if test[0] == '10':
            result =address.address
        elif test[0] == '192':
            result = address.address
        else:
            pass
print(result)  
