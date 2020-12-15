import subprocess
import json
import re

#activations_string = subprocess.check_output(['wsk','activation','list','/whisk.system','--full'])

activations_string = subprocess.check_output(['curl', 'localhost:5984/whisk_local_activations/_all_docs?include_docs=true'])

parts = re.split(r"""("[^"]*"|'[^']*')""", activations_string)
parts[::2] = map(lambda s: "".join(s.split()), parts[::2]) # outside quotes
activations_string = "".join(parts)
#print(activations_string[11:])
with open('activations_couch.json','w') as writer:
	writer.write(activations_string)
#	writer.write("[")
#	count = 0
#	for i in range(11,len(activations_string)):
#		writer.write(activations_string[i])
#		if activations_string[i] == "{":
#			count = count + 1
#			#print(count)
#		elif activations_string[i] == "}":
#			count = count - 1
#		#print(activations_string[i])
#		if count == 0 and i < len(activations_string)-1:
#			#print("This is the end")
#			writer.write(",")
	
#	writer.write("]")

#with open('activations.json','r') as reader:
#	activations_json = reader.read()
	#print(activations_json)
#activations = json.loads(activations_json)
activations = json.loads(activations_string)
#print(activations)
function_names = [] # name of the function
durations = []      # total time it took the function to run, includes setup 
cold_starts = []    # Yes/no the function was cold started
init_times = []     # Cold start time, time it takes to initialize the function
wait_times = []     # Time between OpenWhisk receiving request and granting container
start_times = []    # Unix Time of start of activation
rows = activations["rows"]

with open('activations_only.json','w') as writer:
        writer.write("rows:[")

	for i in range(len(rows)-1,-1,-1):
	#for i in range(0,len(rows)):
        	if "_design" in rows[i]["id"]:
                	continue
		writer.write(str(rows[i]).encode('ascii','ignore'))
		if i == 5:
			writer.write("\n")
		else:
			writer.write(",\n")
	writer.write("]")

#print(rows)
for i in range(len(rows)-1,-1,-1):
#for i in range(0,len(rows)):
	cold_start = False
	init_time = 0
	wait_time = 0
	start_time = 0
	if "_design" in rows[i]["id"]:
		continue
	function_names.append(rows[i]["doc"]["name"])
	for j in range(0,len(rows[i]["doc"]["annotations"])):
		if rows[i]["doc"]["annotations"][j]["key"] == "initTime":
			cold_start = True
			init_time = rows[i]["doc"]["annotations"][j]["value"]
			#print activations[i]["annotations"][j]["value"]
		if rows[i]["doc"]["annotations"][j]["key"] == "waitTime":
			wait_time = rows[i]["doc"]["annotations"][j]["value"]
		start_time = rows[i]["doc"]["start"]
	durations.append(rows[i]["doc"]["duration"])
	cold_starts.append(cold_start)
	init_times.append(init_time)
	wait_times.append(wait_time)
	start_times.append(start_time)

tupled_runs = zip(start_times, function_names, durations, init_times, wait_times)
tupled_runs.sort()

with open('sorted_activations.csv','w') as writer:
	writer.write("name,start,duration,init_time,wait_time\n")
	for i in range(0,len(tupled_runs)):
		writer.write(tupled_runs[i][1]+","+str(tupled_runs[i][0])+","+str(tupled_runs[i][2])+","+str(tupled_runs[i][3])+","+str(tupled_runs[i][4])+"\n")

#for i in range(0,len(function_names)):
#	if init_times[i] == 0:
#		print(str(i+1) + ". " + function_names[i] + ": warmstart")
#	else:
#		print(str(i+1) + ". " + function_names[i] + ": coldstart, " + str(init_times[i]))

unique_function_names = set(function_names)
all_runs_init_times = {}
all_runs_wait_times = {}
all_runs_durations = {}
for name in unique_function_names:
	named_runs_init_times = []
	named_runs_wait_times = []
	named_runs_durations = []
	for i in range(0,len(tupled_runs)):
		if name == tupled_runs[i][1]: #function_names[i]:
			named_runs_init_times.append(tupled_runs[i][3]) #init_times[i])
			named_runs_wait_times.append(tupled_runs[i][4])
			named_runs_durations.append(tupled_runs[i][2])
	all_runs_init_times[name] = named_runs_init_times
	all_runs_wait_times[name] = named_runs_wait_times
	all_runs_durations[name] = named_runs_durations

for name in unique_function_names:
	print (name + "\t" +"  Duration\t"+" Cold Time\t"+"Wait Time") #str(all_runs_durations[name]))
	for i in range(len(all_runs_durations[name])):
		print("\t\t\t" + str(all_runs_durations[name][i]) + "\t\t" + str(all_runs_init_times[name][i]) + "\t\t" + str(all_runs_wait_times[name][i]))
	print
total_coldstart_time = sum(init_times)
print("Total coldstart time: " + str(total_coldstart_time))

