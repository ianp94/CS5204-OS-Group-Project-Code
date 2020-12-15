import json
import subprocess

#open the conf, since it is json you can use the json library
with open('auto_runtimes.conf') as f:
    data = json.load(f)

# Get actions from wsk action list including runtimes
actions = subprocess.check_output(['wsk', 'action', 'list'])

#get the number of actions of each type
njs10 = actions.count('nodejs:10')
njs14 = actions.count('nodejs:14')
njs10b = njs10
njs10s = njs10
njs14b = njs14
njs14s = njs14
p3 = actions.count('python:3')
p3b = p3
p3s = p3
MEMORY_AMOUNT_BIG = 2 # gigabytes !!!! SHOULD CHANGE TO SYSTEM CALL TO GET SYSTEM AMOUNT OF MEMORY
MEMORY_AMOUNT_SMALL = 2 # gigabytes !!!! SHOULD CHANGE TO SYSTEM CALL TO GET SYSTEM AMOUNT OF MEMORY
BIG_CONTAINER_MEMORY_SIZE = 256 # megabytes !!!! SHOULD NOT BE CONSTANT, BIGGER ACTIONS MAY NEED MORE
SMALL_CONTAINER_MEMORY_SIZE = 128 # megabytes !!!! SHOULD NOT BE CONSTANT, BIGGER ACTIONS MAY NEED MORE

# of containers available
NUM_OF_BIG_CONTAINERS = int((MEMORY_AMOUNT_BIG * 1024) / BIG_CONTAINER_MEMORY_SIZE)
NUM_OF_SMALL_CONTAINERS = int((MEMORY_AMOUNT_SMALL * 1024) / SMALL_CONTAINER_MEMORY_SIZE)

# CRUDE ALLOCATION SHOULD USE POPULARITY/SIJIAS PREDICTION
while ((njs10b + njs14b + p3b) > NUM_OF_BIG_CONTAINERS):
    if (p3b > (njs10b + njs14b)):
        p3b = p3b - 1
    elif (njs10b > njs14b):
        njs10b = njs10b - 1
    else:
        njs14b = njs14b - 1

while ((njs10s + njs14s + p3s) > NUM_OF_SMALL_CONTAINERS):
    if (p3s > (njs10s + njs14s)):
        p3s = p3s - 1
    elif (njs10s > njs14s):
        njs10s = njs10s - 1
    else:
        njs14s = njs14s - 1

#Look for node instances, could be more abstract AND ADAPT TO MULTIPLE CONTAINER SIZES
nodes = data["runtimes"]["node"]
for n in nodes:
    if (n['kind'] == 'nodejs:10'):
        n['stemCells'][0]['count'] = njs10b
        n['stemCells'][0]['memory'] = str(BIG_CONTAINER_MEMORY_SIZE) + ' MB'
        n['stemCells'][1]['count'] = njs10s
        n['stemCells'][1]['memory'] = str(SMALL_CONTAINER_MEMORY_SIZE) + ' MB'
    if (n['kind'] == 'nodejs:14'):
        n['stemCells'][0]['count'] = njs14b
        n['stemCells'][0]['memory'] = str(BIG_CONTAINER_MEMORY_SIZE) + ' MB'
        n['stemCells'][1]['count'] = njs14s
        n['stemCells'][1]['memory'] = str(SMALL_CONTAINER_MEMORY_SIZE) + ' MB'


#Look for python instances, could be more abstract, AND ADAPT TO MULTIPLE CONTAINER SIZES
nodes = data["runtimes"]["python"]
for n in nodes:
    if (n['kind'] == 'python:3'):
        n['stemCells'][0]['count'] = p3b
        n['stemCells'][0]['memory'] = str(BIG_CONTAINER_MEMORY_SIZE) + ' MB'
        n['stemCells'][1]['count'] = p3s
        n['stemCells'][1]['memory'] = str(SMALL_CONTAINER_MEMORY_SIZE) + ' MB'

#Write the changes back to the conf file
with open('auto_runtimes.conf', 'w') as json_file:
  json.dump(data, json_file)