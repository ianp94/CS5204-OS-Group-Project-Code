import random

test_length = 100
test_division = 5

test_action_list = []


with open('action_list.txt', 'r') as reader:
	actions = reader.readlines()

for action in actions:
	for i in range(test_length/test_division):
		test_action_list.append(action)

random.shuffle(test_action_list)

with open('test_action_list.txt', 'w') as writer:
	for test_action in test_action_list:
		writer.write(test_action)	


