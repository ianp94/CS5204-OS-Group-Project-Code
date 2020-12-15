import subprocess
import json
import re

activations_string = subprocess.check_output(['wsk','activation','list','/whisk.system','--full','--since','0'])

parts = re.split(r"""("[^"]*"|'[^']*')""", activations_string)
parts[::2] = map(lambda s: "".join(s.split()), parts[::2]) # outside quotes
activations_string = "".join(parts)
#print(activations_string[11:])
with open('activations.json','w') as writer:
	writer.write("[")
	count = 0
	for i in range(11,len(activations_string)):
		writer.write(activations_string[i])
		if activations_string[i] == "{":
			count = count + 1
			#print(count)
		elif activations_string[i] == "}":
			count = count - 1
		#print(activations_string[i])
		if count == 0 and i < len(activations_string)-1:
			#print("This is the end")
			writer.write(",")
	
	writer.write("]")

with open('activations.json','r') as reader:
	activations_json = reader.read()
	#print(activations_json)
activations = json.loads(activations_json)
function_names = []
cold_starts = []
init_times = []

for i in range(0,len(activations)):
	cold_start = False
	init_time = 0
	function_names.append(activations[i]["namespace"] + "_" + activations[i]["name"])
	for j in range(0,len(activations[i]["annotations"])):
		if activations[i]["annotations"][j]["key"] == "initTime":
			cold_start = True
			init_time = activations[i]["annotations"][j]["value"]
			#print activations[i]["annotations"][j]["value"]
	cold_starts.append(cold_start)
	init_times.append(init_time)

for i in range(0,len(function_names)):
	if init_times[i] == 0:
		print(str(i+1) + ". " + function_names[i] + ": " + str(cold_starts[i]))
	else:
		print(str(i+1) + ". " + function_names[i] + ": " + str(cold_starts[i]) + "-" + str(init_times[i]))

