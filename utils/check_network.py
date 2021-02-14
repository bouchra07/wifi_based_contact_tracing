#!/usr/bin/env python3
import subprocess
import re
from datetime import datetime
import pandas as pd

now = datetime.now()
curdate = now.strftime("%d/%m/%Y %H:%M:%S")

# curdate = datetime.date.today()
# curdate = str(curdate)

subprocess.run(['./commands/get_ip.sh'])

with open('./data/ip_address.txt') as file:
    for line in file:
        result = re.search(r"[0-9\.]*",line)


with open('./data/ip_address.txt','w') as file:
    file.write(result[0])

ip = result[0]
ip = ip.split('.') 
ip[len(ip)-1] = '1'
ip = '.'.join(ip) 
print(ip)

subprocess.run(['./commands/get_mac.sh',ip])
subprocess.run(['./commands/get_own_mac.sh',ip])

df = pd.read_csv('./data/device_log.txt', sep=' ', header=None)
df = df[:-1]
devices = df[4].values
i=0

with open('./data/mac_log.txt') as file:
    for line in file:
        result = re.search(r"..\:..\:..\:..\:..\:..",line)
        with open('./data/mac_addresses.txt','a') as f:
                f.write(result[0]+','+ devices[i] +','+ curdate +'\n')
        i=i+1

filepath ='./data/current_user.txt'

with open(filepath,'r') as inp:
    y = inp.read().upper()
with open(filepath,'w') as out:
    out.write(y)


with open(filepath, 'r') as f:
    data = f.read()
    with open(filepath, 'w') as w:
        w.write(data[:-1])



    



