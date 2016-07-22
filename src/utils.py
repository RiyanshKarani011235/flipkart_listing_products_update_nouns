import os

def run_command_and_get_output(command, temp_file) : 
	# clearing output file
	with open(temp_file, 'w') as f : 
		f.write('')
	os.system(command + ' >> ' + temp_file)
	return_value = ''
	with open(temp_file, 'r') as f : 
		return_value = f.read()
	with open(temp_file, 'w') as f : 
		f.write('')
	return return_value

def write_to_output(string, output_file) : 
	with open(output_file, 'w') as f : 
		f.write(string)