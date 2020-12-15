import subprocess
import time

with open('action_create.txt','r') as reader:
	actions = reader.readlines()

for action in actions:
	split_action = action.split()
	subprocess.Popen(split_action)

time.sleep(3)

with open('test_action_list.txt', 'r') as reader:
	actions = reader.readlines()

for action in actions:
	split_action = action.split()
	subprocess.Popen(split_action)

